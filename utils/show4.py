import socket
import dns.resolver

domain = 'www.baidu.com'
name_server = '60.191.95.242'


# # Basic query
# res = dns.resolver.query(domain)
# for i in res.response.answer:
#     for j in i.items:
#         print(j)
 


# Set the DNS Server
resolver = dns.resolver.Resolver()
# resolver.nameservers=[socket.gethostbyname(name_server)]
resolver.nameservers=[name_server]
res1 = resolver.query(domain)
ans = res1.response.answer
details = ans[-1].items.keys()
ip_list = [str(x) for x in ans[-1].items.keys()]
q_res = ",".join(ip_list)
print(q_res)



# for d in details:
#     res = str(d)
#     print(res)
# for i in res1.response.answer:
#     ans = res1.response.answer
#     for j in i.items:
#         print(j)