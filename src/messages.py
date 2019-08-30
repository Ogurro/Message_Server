import sys
import argparse
from models.User import User
from models.Message import Message
from operator import attrgetter
from datetime import datetime


def parse_arguments():
    parser = argparse.ArgumentParser(description='Manage messages')
    exclusive_group = parser.add_mutually_exclusive_group()
    parser.add_argument('--username', '-u', help='user login')
    parser.add_argument('--password', '-p', help='user password')
    exclusive_group.add_argument('--list', '-l', action='store_true',
                                 help='lists all messages or list all messages with specific user')
    exclusive_group.add_argument('--send', '-s', help='new message to send')
    parser.add_argument('--to', '-t', help='recipient username or username for messages with specific user')
    args = parser.parse_args()
    if not args.list and not args.send:
        parser.print_help()
        sys.exit()
    else:
        return args


def parse_user_and_password(args):
    if args.username and args.password:
        user = User.load_user_by_name(args.username)
        if user:
            if user.check_password(args.password, user.hashed_password):
                print(f'Correct password for user "{args.username}"')
                return user
            else:
                print('Wrong username or password!')
                sys.exit()
        else:
            print('Wrong username or password!')
            sys.exit()


def clean_messages(args, messages_list):
    rv_list = []
    user = User.load_user_by_name(args.to)
    if user:
        for m in messages_list:
            if m.to_id == user.id or m.from_id == user.id:
                rv_list.append(m)
        return rv_list
    else:
        print(f'User {args.to} not fount!')
        sys.exit()


if __name__ == '__main__':
    args = parse_arguments()
    user = parse_user_and_password(args)
    if user.username == args.to:
        print('Can not list or send messages to yourself')
    elif args.list:
        message_list = []
        messages_from = Message.load_all_messages_form_user(user.id)
        messages_to = Message.load_all_messages_to_user(user.id)
        for m in messages_from:
            message_list.append(m)
        for m in messages_to:
            message_list.append(m)
        if args.to:
            message_list = clean_messages(args, message_list)
        message_list.sort(key=attrgetter('creation_date'))
        for m in message_list:
            date = datetime.strftime(m.creation_date, '%d.%m.%Y %H:%M:%S')
            user_to = User.load_user_by_id(m.to_id)
            user_from = User.load_user_by_id(m.from_id)
            print(f'{date} To:{user_to.username} From:{user_from.username} | {m.text}')
    elif args.send:
        if args.to:
            user2 = User.load_user_by_name(args.to)
            message = Message()
            message.from_id = user.id
            message.to_id = user2.id
            message.text = args.send
            message.save_to_db()
            print(f'Message has been send to user "{user2.username}"')
        else:
            print('--to (-t) must be given along --send (-s) with recipient username')
    else:
        pass
