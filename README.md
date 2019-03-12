# cse310_assignment2
CSE 310 Assignment 2 - Computer Networks; DNS Resolver

INSTRUCTIONS FOR mydig.py 
Tested for Python 3.6
  python3 mydig.py <domainname>
If you want to pipe to output, use
  python3 mydig.py | mydig_output.txt
If you want to output how the address was resolved, set showWork = True

INSTRUCTIONS FOR digTester.py
Works on Python 3.7
  Test all 25 websites
    python3.7 digTester.py
  Test top x websites where x <= 25
    python3.7 digTester.py x
