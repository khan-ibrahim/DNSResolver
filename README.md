# cse310_assignment2
CSE 310 Assignment 2 - Computer Networks; DNS Resolver
All Tested for Python 3.7 on Ubuntu

Must install dnspython
  Included in dnspython folder in zip
  sudo python3.7 setup.py install

INSTRUCTIONS FOR mydig.py
  python3.7 mydig.py <domainname>
If you want to pipe to output, use
  python3 mydig.py > mydig_output.txt
If you want to output how the address was resolved, set showWork = True
If it takes too long, interrupt using Ctl C, and try again.

INSTRUCTIONS FOR digTester.py
Default uses bash dig. set useMydig = True to test mydig.
  Test all 25 websites
    python3.7 digTester.py
  Test top (x+1) website where 0 < x < 25
    python3.7 digTester.py x
