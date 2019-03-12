import sys
import dns.query
import dns.message
import re
import time
import datetime

__author__ = "Ibrahim Khan"


showWork = False    #set True to see how address was resolved
rootServers = ['198.41.0.4', '199.9.14.201', '192.33.4.12', '199.7.91.13', \
    '192.203.230.10', '192.5.5.241', '192.112.36.4', '198.97.190.53', \
    '192.36.148.17', '192.58.128.30', '193.0.14.129', '202.12.27.33']

rootServer = rootServers[6] #DOD NIC
mydigTime = 0.0
whenDateTime = datetime.datetime.now()
messageLength = 0
requestedDomain = ''

def main(domainStr):
    if showWork:
        print("starting query for ", domainStr)
    ip = recursiveNSResolver(domainStr, rootServer)
    if domainStr == requestedDomain:
        print('Query time:', str(mydigTime*1000), 'msec')
        print('WHEN:', str(whenDateTime))
        print('MSG SIZE recvd:', messageLength)
    return ip

def recursiveNSResolver(domainStr, server):
    if showWork:
        print('querying', server, 'for domain', domainStr)
    
    r = queryServer(domainStr, 'A', server)
    rStr = r.__str__()
    ##print(rStr)    enable for debugging; prints entire response to each request
    
    if len(r.answer) > 0:
        ##print('answer section has len:', len(r.answer[0]))
        answerStr = (r.answer[0]).to_text()
        pattern = domainStr + r'\.* \d+ IN A (\d+\.\d+\.\d+\.\d+)'
        match = re.search(pattern, answerStr)
        if match:
            ip = str(match.group(1))
            if domainStr == requestedDomain:
                global mydigTime
                mydigTime = time.time()- mydigTime
                whenDateTime = datetime.datetime.now()
                pattern = r''';(QUESTION\n.*\n;ANSWER\n.*\n);AUTHORITY'''
                match = re.search(pattern, rStr)
                if match:
                    print('\n' + match.group(1))
                    global messageLength
                    messageLength = len(match.group(1))
                else:
                    print('PARSE ERROR')
                    print(rStr, '\n')
            return ip
        else:
            pattern = domainStr + r'\.* \d+ IN CNAME (.*)'
            matchC = re.search(pattern, answerStr)
            if matchC:
                if showWork:
                    print('\nCNAME MATCH FOUND:', matchC.group(1))
                    print('resolving CNAME...\n')
                return main(matchC.group(1))
            else:
                print('No match in non-empty answer section?')
                print(rStr)
                exit()

    pattern = r'(\d+\.\d+\.\d+\.\d+)'
    match = re.search(pattern, rStr)
    if match:
        return recursiveNSResolver(domainStr, match.group(1))
    else:
        pattern = domainStr + r'\.* \d+ IN NS (.*)'
        match = re.search(pattern, rStr)
        if match:
            if showWork:
                print('\n--NS FOUND--:', match.group(1), '\n')
                print('resolving NS IP...')
            nsip = main(match.group(1))
            if showWork:
                print('\n--NS IP RESOLVED--', nsip, '\n')
            return recursiveNSResolver(domainStr, nsip)
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
        mydigTime = time.time()
        requestedDomain = sys.argv[1]
        main(requestedDomain)
