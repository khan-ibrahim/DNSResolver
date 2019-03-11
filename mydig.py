import sys
import dns.query
import dns.message
import re
import time

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
    startTime = time.time()

    print('querying', server, 'for domain', domainStr)
    r = queryServer(domainStr, 'A', server)
    rStr = r.__str__()
    #print(rStr)    enable for debugging; prints entire response to each request
    if len(r.answer) > 0:

        print('answer section has len:', len(r.answer[0]))
        answerStr = (r.answer[0]).to_text()
        print('using first line', answerStr)
        pattern = domainStr + r'\.* \d+ IN A (\d+\.\d+\.\d+\.\d+)'
        print('using pattern', pattern)
        match = re.search(pattern, answerStr)
        if match:
            print('ANSWER MATCH FOUND:', match.group(1))
            print('LAST RESPONSE SHOWN BELOW')
            print(rStr)
            print('time is', str(time.time()-startTime))
            exit()
        else:
            pattern = domainStr + r'\.* \d+ IN CNAME (.*)'
            matchC = re.search(pattern, answerStr)
            if matchC:
                print('CNAME MATCH FOUND:', matchC.group(1))
                print('resolving CNAME...')
                main(matchC.group(1))
            else:
                print('No match in answer section?')
                print(rStr)
                exit()

    pattern = r'(\d+\.\d+\.\d+\.\d+)'
    match = re.search(pattern, rStr)
    if match:
        recursiveNSResolver(domainStr, match.group(1))
    else:
        print('No IP found -------')
        print(rStr)

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
