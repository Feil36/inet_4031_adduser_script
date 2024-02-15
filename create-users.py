#!/usr/bin/env python3 

import os
import re
import sys

def main():
    for line in sys.stdin:
        # Use re.match to check if the line starts with a hashtag (#)
        match = re.match(r'^#', line)

        # Strips whitespace from the beginning and end of the line, then splits it into an array by ':'
        fields = line.strip().split(':')

        # Checks if there's a match (line starts with #) or if the line does not have exactly five fields
        if match or len(fields) != 5:
            continue  # Skips the rest of the loop for this iteration

        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3], fields[2])

        # Splits the last field into a list by commas, used to determine group memberships
        groups = fields[4].split(',')

        print("==> Creating account for {}...".format(username))
        cmd = "/usr/sbin/adduser --disabled-password --gecos '{}' {}".format(gecos, username)
       
        os.system(cmd)
        print("==> Setting the password for {}...".format(username))
        cmd = "/bin/echo -ne '{}\n{}' | /usr/bin/sudo /usr/bin/passwd {}".format(password, password, username)
       
        os.system(cmd)

        for group in groups:
            if group != '-':
                print("==> Assigning {} to the {} group...".format(username, group))
                cmd = "/usr/sbin/adduser {} {}".format(username, group)
                os.system(cmd)

if __name__ == '__main__':
    main()
