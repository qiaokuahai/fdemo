# -*- coding=utf-8 -*-
import dns
import dns.resolver


def to_dig():
    resolver = dns.resolver.Resolver()
    res1 = resolver.query("www.baidu.com", rdtype=dns.rdatatype.RdataType.A)
    print(res1.response.answer)


if __name__ == '__main__':
    to_dig()
