from dns import resolver

ans = resolver.query("www.baidu.com", "A")
print("qname:",ans.qname)
print ("reclass:",ans.rdclass)
print ("rdtype:",ans.rdtype)
print ("rrset:",ans.rrset)
print ("response:",ans.response)