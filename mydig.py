import sys
import dns.query
import dns.message
import re

__author__ = "Ibrahim Khan"
debuggingEnabled = True

rootServers = ['198.41.0.4', '199.9.14.201', '192.33.4.12', '199.7.91.13', \
    '192.203.230.10', '192.5.5.241', '192.112.36.4', '198.97.190.53', \
    '192.36.148.17', '192.58.128.30', '193.0.14.129', '202.12.27.33']

rootServer = rootServers[6] #DOD NIC

def main(domainStr):
    print("starting query for ", domainStr)
    recursiveNSResolver(domainStr, rootServer)

def recursiveNSResolver(domainStr, server):
    print('querying', server, 'for domain', domainStr)
    r = queryServer(domainStr, 'A', server).__str__()

    if len(r.answer) > 0:

        debugOutout('answer section has len:', len(r.answer))
        answerStr = r.answer[0].to_text()
        print('using first line', answerStr)
        pattern = domainStr + r'\. \d+ IN A (\d+\.\d+\.\d+\.\d+)'
        match = re.search(pattern, answerStr)
        if match:
            print(match.group(1))
            exit()
        else:
            print('No match in answer section?')
            print(r)
            exit()

    pattern = r'(\d+\.\d+\.\d+\.\d+)'
    match = re.search(pattern, r)
    if match:
        print('match found!', match.group(1))
        recursiveNSResolver(domainStr, match.group(1))
    else:
        print('No IP found -------')
        print(r)

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
