#Must use Python 3.7 on Unix
#tests dig for either all 25 top websites or specified number of top websites
#uses either dig or mydig

import sys
import subprocess
import re

topWebsites = ['google.com','youtube.com','facebook.com','baidu.com', \
        'wikipedia.org','qq.com', 'yahoo.com', 'taobao.com', 'tmall.com', \
        'amazon.com', 'twitter.com', 'Sohu.com', 'jd.com', 'live.com', \
        'vk.com', 'instagram.com', 'sina.com.cn', 'weibo.com', 'Yandex.ru', \
        'reddit.com', '360.cn', 'blogspot.com', 'login.tmall.com', \
        'netflix.com', 'linkedin.com']

def digResolveTime(websiteDomain):
    normal = subprocess.run(['dig', websiteDomain], stdout=subprocess.PIPE, \
            stderr=subprocess.PIPE, check=True, text='True')
    outputStr = str(normal.stdout)

    pattern = r'Query time: (\d+) ms'
    match = re.search(pattern, outputStr)
    if match:
        #print(outputStr)   enable for debugging
        time = int(match.group(1)) / 1000.0
        return time
    else:
        print('ERROR, TIME NOT FOUND?')
        print(outputStr)
        return 10   #large value if not found

def main():
    results = []
    for website in topWebsites:
        currentResults = []
        currentResults.append(website)
        for a in range(10):
            currentResults.append(digResolveTime(website))
        results.append(currentResults)
    #print(results)
    for websiteData in results:
        print(','.join(map(str, websiteData)))
    return results

def mydigResolveTime(websiteDomain):
    normal = subprocess.run(['python3', 'mydig.py',websiteDomain], stdout=subprocess.PIPE, \
            stderr=subprocess.PIPE, check=True, text='True')
    outputStr = str(normal.stdout)

    pattern = r'Query time: (\d+\.\d+) ms'
    match = re.search(pattern, outputStr)
    if match:
        #print(outputStr)   enable for debugging
        time = int(match.group(1)) / 1000.0
        return time
    else:
        print('ERROR, TIME NOT FOUND?')
        print(outputStr)
        return 10   #large value if not found

if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
        topWebsites = topWebsites[8:10]
    else:
        topWebsites = topWebsites[:int(sys.argv[1])]
        main()
