#!/usr/bin/env python3

import sys
import argparse
import re
from collections import Counter


def check_python_version(v):
    v = str(v).split('.')
    try:
        if not 1 < int(v[0]) <= 3:
            raise ValueError('Error: You are requiring invalid Python version ' + v[0])
    except ValueError as e:
        print(e)
        sys.exit(1)
    if sys.version_info[0] != int(v[0]):
        print('This script requires Python version ' + v[0] + '+')
        print('You are using {0}.{1}.{2} {3}'.format(sys.version_info[0],
                                                     sys.version_info[1],
                                                     sys.version_info[2],
                                                     sys.version_info[3]))
        sys.exit(1)


def get_users(users=None, sort_by=0):
    try:
        with open('/etc/passwd', 'r') as fr:
            passwd = fr.readlines()
    except FileNotFoundError:
        print('Error: File /etc/passwd not found')
        sys.exit(1)

    usrs = []

    for usr in passwd:
        if not re.match(r'(^#)', usr):
            username = usr.split(':')[0]
            shell = usr.split(':')[-1]
            uid = int(usr.split(':')[2])
            name = usr.split(':')[4]
            if not users:
                usrs.append((username, uid, name, shell))
            else:
                for each in users:
                    if re.match(each, username):
                        usrs.append((username, uid, name, shell))

    try:
        if sort_by == 1:
            usrs.sort(key=lambda x: x[sort_by])
        else:
            usrs.sort(key=lambda x: x[sort_by].lower())

        if sort_by < 0 or sort_by > 4:
            raise IndexError()
    except IndexError:
        print('Error: Invalid field number. Use either 1, 2, 3 or 4\n')
        sys.exit(1)

    return usrs


def dup_usernames():
    usernames = []
    usr_dups = {}

    for item in get_users():
        usernames.append(item[0])

    dup_users_count = Counter(usernames)
    for each, count in dup_users_count.most_common():
        if count > 1:
            usr_dups[each] = count

    usr_dups = dict(sorted(zip(usr_dups.keys(), usr_dups.values()), key=lambda x: x[1]))

    return usr_dups


def dup_uids():
    uids = []
    uid_dups = {}

    for item in get_users():
        uids.append(item[1])

    dup_uids_count = Counter(uids)
    for each, count in dup_uids_count.most_common():
        if count > 1:
            uid_dups[each] = count

    uid_dups = dict(sorted(zip(uid_dups.keys(), uid_dups.values()), key=lambda x: x[1]))

    return uid_dups


def print_results(s_users, sort_field):
    if get_users(s_users, sort_by=sort_field):
        print('\n{usrname:{max_u}} {uid:4} {nme:{max_n}} {shll}'.format(usrname='USERNAME', uid='UID', nme='NAME',
                                                                        shll='SHELL',
                                                                        max_u=max_usrname,
                                                                        max_n=max_name))
        print('{0} {1} {2} {3}'.format('-' * max_usrname, '-' * 4, '-' * max_name, '-' * 15))
        for item in get_users(s_users, sort_by=sort_field):
            print('{0:{max_u}} {1:4} {2:{max_n}} {3}'.format(item[0], item[1], item[2], item[3], max_u=max_usrname,
                                                             max_n=max_name))
    else:
        print('no results found')


if __name__ == "__main__":
    check_python_version('3')

    parser = argparse.ArgumentParser(description='Lists users from /etc/passwd and allows to find duplicate usernames or uids')
    parser.add_argument('-a', '--all', action='store_true', help='List all users and search for duplicates', default=False)
    parser.add_argument('-u', '--users', nargs='+', help='Search for one or more space/comma delimited users. Allows Regex')
    parser.add_argument('-s', '--sort-by', type=int, help='Provide field number to sort results by (i.e: 1, 2, 3, 4). Default is 1 (USERNAME)', default=1)
    parser.add_argument('--dup-usernames', action='store_true',help='Check for duplicate usernames. Default is Disabled', default=False)
    parser.add_argument('--dup-uids', action='store_true',help='Check for duplicate uids. Default is Disabled', default=False)
    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()

    max_usrname = max(len(l[0]) for l in get_users())
    max_name = max(len(l[2]) for l in get_users())

    sort_field = args.sort_by - 1

    if not args.users:
        s_users = None
    else:
        seen = set()
        s_users = [x for x in str(' '.join(args.users)).replace(',', ' ').split() if not (x in seen or seen.add(x))]

    if args.users:
        print_results(s_users, sort_field)
    if args.all:
        print_results(s_users, sort_field)

    if args.dup_usernames or args.all:
        u_dups = []

        for u_name in dup_usernames():
            u_dups.append(u_name)
        if u_dups:
            print('Found',str(len(u_dups)), 'duplicate usernames')
            print_results(u_dups, sort_field)
        else:
            print('No duplicate usernames found\n')

    if args.dup_uids or args.all:
        uid_dups = []
        u_dups = get_users()
        s_dups = []

        for uid in dup_uids():
            uid_dups.append(uid)
        if uid_dups:
            print('Found',str(len(uid_dups)), 'duplicate UIDs')
            for each in u_dups:
                if each[1] in uid_dups:
                    s_dups.append(each[0])
            s_dups = list(set(s_dups))
            print_results(s_dups, sort_field)
        else:
            print('No duplicate UIDs found\n')
