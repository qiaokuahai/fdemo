#include "socket_lib h"
#include <unistd.h>
#include <assert.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/epoll.h>

#define MAX_CLIENT 10000
#define MIN_RSIZE 124
#define BACKLOG 128
#define EVENT_NUM 64

// 缓存结点
struct twbuffer {
    struct twbuffer *next;      // 下一个缓存
    void *buffer;        // 缓存
    char *ptr;           // 当前未发送的缓存，buffer != ptr表示只发送了一部分
    int size;            // 当前未发送的缓存大小
};

// 缓存列表
struct twblist {
    struct twbuffer *head;
    struct twbuffer *tail;
};

// 客户端连接信息
struct tclient {
    int fd;             // 客户端fd
    int rsize;          // 当前读的缓存区大小
    int wbsize;         // 还未写完的缓存大小
    struct twblist wblist;  // 写缓存链表
};

// 服务器信息
struct tserver {
    int listenfd;       // 监听fd
    int epollfd;        // epollfd
    struct tclient clients[MAX_CLIENT];     // 客户端结构数组
};

// epoll增加读事件
void epoll_add(int efd, int fd, void *ud) {
    struct epoll_event ev;
    ev.events = EPOLLIN;
    ev.data.ptr = ud;
    epoll_ctl(efd, EPOLL_CTL_ADD, fd, &ev);
}

// epoll修改写事件
void epoll_write(int efd, int fd, void *ud, int enabled) {
    struct epoll_event ev;
    ev.events = EPOLLIN | (enabled ? EPOLLOUT : 0);
    ev.data.ptr = ud;
    epoll_ctl(efd, EPOLL_CTL_MOD, fd, &ev);
}

// epoll删除fd
void epoll_del(int efd, int fd) {
    epoll_ctl(efd, EPOLL_CTL_DEL, fd, NULL);
}

// 设置socket为非阻塞
void set_nonblocking(int fd) {
    int flag = fcntl(fd, F_GETFL, 0);
    if (flag >= 0) {
        fcntl(fd, F_SETFL, flag | O_NONBLOCK);
    }
}

// 增加写缓存
void add_wbuffer(struct twblist *list, void *buffer, int sz) {
    struct twbuffer *wb = malloc(sizeof(*wb));
    wb->buffer = buffer;
    wb->ptr = buffer;
    wb->size = sz;
    wb->next = NULL;
    if (!list->head) {
        list->head = list->tail = wb;
    } else {
        list->tail->next = wb;
        list->tail = wb;
    }
}

// 释放写缓存
void free_wblist(struct twblist *list) {
    struct twbuffer *wb = list->head;
    while (wb) {
        struct twbuffer *tmp = wb;
        wb = wb->next;
        free(tmp);
    }
    list->head = NULL;
    list->tail = NULL;
}

// 创建客户端信息
struct tclient* create_client(struct tserver *server, int fd) {
    int i;
    struct tclient *client = NULL;
    for (i = 0; i < MAX_CLIENT; ++i) {
        if (server->clients[i].fd < 0) {
            client = &server->clients[i];
            break;
        }
    }
    if (client) {
        client->fd = fd;
        client->rsize = MIN_RSIZE;
        set_nonblocking(fd);        // 设为非阻塞模式
        epoll_add(server->epollfd, fd, client);     // 增加读事件
        return client;
    } else {
        fprintf(stderr, "too many client: %d\n", fd);
        close(fd);
        return NULL;
    }
}

// 关闭客户端
void close_client(struct tserver *server, struct tclient *client) {
    assert(client->fd >= 0);
    epoll_del(server->epollfd, client->fd);
    if (close(client->fd) < 0) perror("close: ");
    client->fd = -1;
    client->wbsize = 0;
    free_wblist(&client->wblist);
}

// 初始化服务信息
struct tserver* create_server(const char *host, const char *port) {
    struct tserver *server = malloc(sizeof(*server));
    memset(server, 0, sizeof(*server));
    for (int i = 0; i < MAX_CLIENT; ++i) {
        server->clients[i].fd = -1;
    }
    server->epollfd = epoll_create(MAX_CLIENT);
    server->listenfd = tcpListen(host, port, BACKLOG);
    epoll_add(server->epollfd, server->listenfd, NULL);
    return server;
}

// 释放服务器
void release_server(struct tserver *server) {
    for (int i = 0; i < MAX_CLIENT; ++i) {
        struct tclient *client = &server->clients[i];
        if (client->fd >= 0) {
            close_client(server, client);
        }
    }
    epoll_del(server->epollfd, server->listenfd);
    close(server->listenfd);
    close(server->epollfd);
    free(server);
}

// 处理接受
void handle_accept(struct tserver *server) {
    struct sockaddr_storage claddr;
    socklen_t addrlen = sizeof(struct sockaddr_storage);
    for (;;) {
        int cfd = accept(server->listenfd, (struct sockaddr*)&claddr, &addrlen);
        if (cfd < 0) {
            int no = errno;
            if (no == EINTR)
                continue;
            perror("accept: ");
            exit(1);        // 出错
        } 
        char host[NI_MAXHOST];
        char service[NI_MAXSERV];
        if (getnameinfo((struct sockaddr *)&claddr, addrlen, host, NI_MAXHOST, service, NI_MAXSERV, 0) == 0)
            printf("client connect: fd=%d, (%s:%s)\n", cfd, host, service);
        else
            printf("client connect: fd=%d, (?UNKNOWN?)\n", cfd);

        create_client(server, cfd);
        break;
    }   
}

// 处理读
void handle_read(struct tserver *server, struct tclient *client) {
    int sz = client->rsize;
    char *buf = malloc(sz);
    ssize_t n = read(client->fd, buf, sz);
    if (n < 0) {        // error
        free(buf);
        int no = errno;
        if (no != EINTR && no != EAGAIN && no != EWOULDBLOCK) {
            perror("read: ");
            close_client(server, client);
        }
        return;
    }
    if (n == 0) {       // client close
        free(buf);
        printf("client close: %d\n", client->fd);
        close_client(server, client);
        return;
    }
    // 确定下一次读的大小
    if (n == sz)
        client->rsize >>= 1;
    else if (sz > MIN_RSIZE && n *2 < sz)
        client->rsize <<= 1;
    // 加入写缓存
    add_wbuffer(&client->wblist, buf, n);
    // 增加写事件
    epoll_write(server->epollfd, client->fd, client, 1);
}

// 处理写
void handle_write(struct tserver *server, struct tclient *client) {
    struct twblist *list = &client->wblist;
    while (list->head) {
        struct twbuffer *wb = list->head;
        for (;;) {
            ssize_t sz = write(client->fd, wb->ptr, wb->size);
            if (sz < 0) {
                int no = errno;
                if (no == EINTR)        // 信号中断，继续
                    continue;
                else if (no == EAGAIN || no == EWOULDBLOCK)   // 内核缓冲满了，下次再来
                    return;
                else {      // 其他错误 
                    perror("write: ");
                    close_client(server, client);
                    return;
                }
            }
            client->wbsize -= sz;
            if (sz != wb->size) {       // 未完全发送出去，下次再来
                wb->ptr += sz;
                wb->size -= sz;
                return;
            }
            break;
        }
        list->head = wb->next;
        free(wb);
    }
    list->tail = NULL;
    // 到这里写全部完成，关闭写事件
    epoll_write(server->epollfd, client->fd, client, 0);
}

// 先处理错误
void handle_error(struct tserver *server, struct tclient *client) {
    perror("client error: ");
    close_client(server, client);
}

int main() {
    signal(SIGPIPE, SIG_IGN);

    struct tserver *server = create_server("127.0.0.1", "3459");

    struct epoll_event events[EVENT_NUM];
    for (;;) {
        int nevent = epoll_wait(server->epollfd, events, EVENT_NUM, -1);
        if (nevent <= 0) {
            if (nevent < 0 && errno != EINTR) {
                perror("epoll_wait: ");
                return 1;
            }
            continue;
        }
        int i = 0;
        for (i = 0; i < nevent; ++i) {
            struct epoll_event ev = events[i];
            if (ev.data.ptr == NULL) {  // accept
                handle_accept(server);
            } else {
                if (ev.events & (EPOLLIN | EPOLLHUP)) {  // read
                    handle_read(server, ev.data.ptr);
                }
                if (ev.events & EPOLLOUT) {     // write
                    handle_write(server, ev.data.ptr);
                }
                if (ev.events & EPOLLERR) {     // error
                    handle_error(server, ev.data.ptr);
                }
            }
        }
    }

    release_server(server);
    return 0;
}