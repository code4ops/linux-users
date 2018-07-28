## Linux users and duplicates finder


#### Features:
* List users found in the /etc/passwd
* Search by username/s
* Find duplicate usernames
* Find duplicate UIDs

#### Prerequisites:
* Python version => 3

##### List all the options:
*Execute `--help` to display options*

```
shell#: python3 users.py --help
usage: users.py [-h] [-a] [-u USERS [USERS ...]] [-s SORT_BY]
                [--dup-usernames] [--dup-uids]

Lists users from /etc/passwd and allows to find duplicate usernames or uids

optional arguments:
  -h, --help            show this help message and exit
  -a, --all             List all users and search for duplicates
  -u USERS [USERS ...], --users USERS [USERS ...]
                        Search for one or more space/comma delimited users.
                        Allows Regex
  -s SORT_BY, --sort-by SORT_BY
                        Provide field number to sort results by (i.e: 1, 2, 3,
                        4). Default is 1 (USERNAME)
  --dup-usernames       Check for duplicate usernames. Default is Disabled
  --dup-uids            Check for duplicate uids. Default is Disabled

```
