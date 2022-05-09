from dns import resolver

res = resolver.query("www.baidu.com", 'A')
for i in res.response.answer:
    for j in i.items:
        print(j)