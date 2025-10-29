#!/usr/bin/env python3
"""Verify knowledge.json is not writable and provide advisory commands to lock it.

Exits with code 0 if file appears protected (not world-writable), 1 otherwise.
"""
import os
import stat
import sys

KNOW = os.path.join(os.path.dirname(__file__), '..', 'knowledge', 'knowledge.json')
KNOW = os.path.abspath(KNOW)

def is_writable(path):
    return os.access(path, os.W_OK)

def main():
    if not os.path.exists(KNOW):
        print('knowledge.json not found at', KNOW)
        sys.exit(1)
    writable = is_writable(KNOW)
    print('Checking', KNOW)
    st = os.stat(KNOW)
    mode = stat.filemode(st.st_mode)
    print('Permissions:', mode)
    if writable:
        print('WARNING: knowledge.json is writable. To lock it on Linux run:')
        print(f'  sudo chattr +i {KNOW}')
        print('On Windows, restrict write access to Administrators via icacls.')
        sys.exit(1)
    else:
        print('OK: knowledge.json is not writable by current user.')
        sys.exit(0)

if __name__ == '__main__':
    main()
