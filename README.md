# Messages_Server
>CLI apps to manage users and send messages between them

# Requirements
* Set up *DB_NAME* and *DB_URI* in models package
```
# Example
DB_NAME = 'msg_server_db'
DB_URI = 'postgresql://postgres@localhost'
```

* Models Contains several methods to set up database
```
nuke_db()
create_db()
create_table_users()
create_table_messages()
```

# Users
List of arguments
```
'-u', '--username',  help='user login'
'-p', '--password', help='user password'
'-l', '--list', action='store_true', help='lists all users'
'-n', '--new-pass', help='set new password'
'-e', '--edit', help='edit user login'
'-d', '--delete', action='store_true', help='delete user'
'-c', '--confirm', help='confirm password for new user\n'
                        'or confirm new password for existing user\n'
                        'or confirm new login\n'
                        'or confirm login for deleted user'
```

## Usage examples

* Create new user
```
python3 users.py --username USERNAME --password PASSWORD --confirm PASSWORD
python3 users.py -u USERNAME -p PASSWORD -c PASSWORD
```

* Edit user login
```
python3 users.py --username USERNAME --password PASSWORD --edit NEW_USERNAME --confirm NEW_USERNAME
python3 users.py -u USERNAME -p PASSWORD -e NEW_USERNAME -c NEW_USERNAME
```

* New user password
```
python3 users.py --username USERNAME --password PASSWORD --new-pass NEW_PASSWORD --confirm NEW_PASSWORD
python3 users.py -u USERNAME -p PASSWORD -n NEW_PASSWORD -c NEW_PASSWORD
```

* Delete user
```
python3 users.py --username USERNAME --password PASSWORD --delete --confirm USERNAME
python3 users.py -u USERNAME -p PASSWORD -d -c USERNAME
```

* List all users
```
python3 users.py --username USERNAME --password PASSWORD --list
python3 users.py -u USERNAME -p PASSWORD -l
```


# Messages
List of arguments
```
'-u', '--username', help='user login'
'-p', '--password', help='user password'
'-l', '--list', action='store_true',help='lists all messages or list all messages with specific user'
'-s', '--send', help='new message to send'
'-t', '--to', help='recipient username or username for messages with specific user'
```

## Usage examples


* Send message to user
```
python3 messages.py --username USERNAME --password PASSWORD --to RECIPIENt_USERNAME --send "TEXT MESSAGE"
python3 messages.py -u USERNAME -p PASSWORD -t RECIPIENT_USERNAME -s "TEXT MESSAGE"
```

* List all messages
```
python3 messages.py --username USERNAME --password PASSWORD --list
python3 messages.py -u USERNAME -p PASSWORD -l
```

* List all messages with specific user
```
python3 messages.py --username USERNAME --password PASSWORD --list --to OTHER_USERNAME
python3 messages.py -u USERNAME -p PASSWORD -l -t OTHER_USERNAME
```

