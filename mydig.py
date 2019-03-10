import sys


__author__ = "Ibrahim Khan"


def main(domainStr):
    print("hello", domainStr)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("too few arguments. usage: python3 mydig.py <domainName>")
        exit()
    else:
        main(sys.argv[1])
