#tests dig for either all 25 top websites or specified number of top websites

import sys
import subprocess
import re


topWebsites = ['google.com','youtube.com','facebook.com','baidu.com', \
        'wikipedia.org','qq.com', 'yahoo.com', 'taobao.com', 'tmall.com', \
        'amazon.com', 'twitter.com', 'Sohu.com', 'jd.com', 'live.com', \
        'vk.com', 'instagram.com', 'sina.com.cn', 'weibo.com', 'Yandex.ru', \
        'reddit.com', '360.cn', 'blogspot.com', 'login.tmall.com', \
        'netflix.com', 'linkedin.com']

def testResolveTime(websiteDomain):
    normal = subprocess.run(['dig', 'google.com'], stdout=subprocess.PIPE, \
            stderr=subprocess.PIPE, check=True, text='True')
    
    outputStr = str(normal.stdout)
    pattern = r'Query time: (d+) ms'
    match = re.search(pattern, outputStr)
    if match:
        return int(match.group(1))
    else:
        print('ERROR, TIME NOT FOUND?')
        print(outputStr)

def main():
    for website in topWebsites:
        resolve(website)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    else:
        topWebsites = topWebsites[:int(sys.argv[1])]
        main()
