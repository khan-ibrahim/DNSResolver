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

def debugOutput(str):
    if debuggingEnabled:
        print(str)

def main(domainStr):
    debugOutput("starting query for ", domainStr)
    recursiveNSResolver(domainStr, rootServer)


def recursiveNSResolver(domainStr, server):
    debugOutput('querying', server, 'for domain', domainStr)
    r = queryServer(domainStr, 'A', server).__str__()

    if len(r.answer) > 0:

        answerStr = r.answer[0].to_Text
        pattern = domainStr + r'\. \d+ IN A (\d+\.\d+\.\d+\.\d+)'
        debugOutput('checking:', pattern)
        match = re.search(pattern, r)
        if match:
            debugOutput('answer match found', match.group(1))
            debugOutput(r)
            exit()
    else:
        debugOutput('answer not yet found')

    pattern = r'(\d+\.\d+\.\d+\.\d+)'
    match = re.search(pattern, r)
    if match:
        debugOutput('match found!', match.group(1))
        recursiveNSResolver(domainStr, match.group(1))
    else:
        debugOutput('No IP found -------')
        debugOutput(r)

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
