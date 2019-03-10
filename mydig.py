import sys
import dns.query
import dns.message

__author__ = "Ibrahim Khan"


rootServers['198.41.0.4', '199.9.14.201', '192.33.4.12', '199.7.91.13', \
    '192.203.230.10', '192.5.5.241', '192.112.36.4', '198.97.190.53', \
    '192.36.148.17', '192.58.128.30', '193.0.14.129', '202.12.27.33']

rootServer = rootServers[6] #DOD NIC

def main(domainStr):
    print("starting query for ", domainStr)
    print(queryServer(domainStr, 'NS', rootServer))
    print(queryServer(domainStr, 'A', rootServer))

def queryServer(qname, rdtype, serverAddr):
    q = dns.message.make_query(qname, rdtype)
    r = dns.query.udp(q, serverAddr)
    return r

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("too few arguments. usage: python3 mydig.py <domainName>")
        exit()
    else:
        main(sys.argv[1])
