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
    print('querying', server, 'for domain', domainStr)
    
    r = queryServer(domainStr, 'A', server)
    rStr = r.__str__()
    #print(rStr)    enable for debugging; prints entire response to each request
    
    if len(r.answer) > 0:
        #print('answer section has len:', len(r.answer[0]))
        answerStr = (r.answer[0]).to_text()
        pattern = domainStr + r'\.* \d+ IN A (\d+\.\d+\.\d+\.\d+)'
        match = re.search(pattern, answerStr)
        if match:
            print('\n\n----ANSWER MATCH FOUND----:', match.group(1), '\n')
            print('time is', str(time.time()-startTime), 'seconds')
            print('LAST RESPONSE SHOWN BELOW\n')
            print(rStr)
            exit()
        else:
            pattern = domainStr + r'\.* \d+ IN CNAME (.*)'
            matchC = re.search(pattern, answerStr)
            if matchC:
                print('\nCNAME MATCH FOUND:', matchC.group(1))
                print('resolving CNAME...\n')
                main(matchC.group(1))
            else:
                print('No match in non-empty answer section?')
                print(rStr)
                exit()

    pattern = r'(\d+\.\d+\.\d+\.\d+)'
    match = re.search(pattern, rStr)
    if match:
        recursiveNSResolver(domainStr, match.group(1))
    else:
        print('\n\n----NO IP FOUND----\n')
        print('last result shown below')
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
        startTime = time.time()
        main(sys.argv[1])
