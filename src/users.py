import sys
import argparse
from models.User import User


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', '-u', help='user login')
    parser.add_argument('--password', '-p', help='user password')
    exclusive_group = parser.add_mutually_exclusive_group()
    exclusive_group.add_argument('--list', '-l', action='store_true', help='lists all users')
    exclusive_group.add_argument('--new-pass', '-n', help='set new password')
    exclusive_group.add_argument('--edit', '-e', help='edit user login')
    exclusive_group.add_argument('--delete', '-d', action='store_true', help='delete user')
    parser.add_argument('--confirm', '-c', help='confirm password for new user\n'
                                                'or confirm new password for existing user\n'
                                                'or confirm new login\n'
                                                'or confirm login for deleted user')
    return parser.parse_args()


def parse_user_and_password(args):
    if args.username and args.password:
        user = User.load_user_by_name(args.username)
        if user:
            if user.check_password(args.password, user.hashed_password):
                print(f'Correct password for user "{args.username}"')
                return user
            else:
                print('Wrong username or password!')
        else:
            print(f'No user "{args.username}" has been found')
            if create_user(args):
                print(f'Created new user "{args.username}"')
                sys.exit()
    else:
        print('--user (-u) and --password (-p) must be given together')


def create_user(args):
    if not args.confirm:
        print('--confirm (-c) must be given with --password (-p) to create new user')
    elif not args.confirm == args.password or len(args.password) < 8:
        print('confirm password do not match password or password is shorter than 8 characters')
    else:
        new_user = User()
        new_user.username = args.username
        new_user.hashed_password = args.password
        return new_user.save_to_db()


def parse_list_users():
    print('Users list:')
    for user in User.load_all_users():
        print(f'\t{user.username}')
    sys.exit()


if __name__ == '__main__':
    args = parse_arguments()
    user = parse_user_and_password(args)
    if user:
        if args.list:
            parse_list_users()
        elif args.delete:
            if args.confirm == args.username:
                user.delete()
                print(f'Deleted user "{args.username}"')
            else:
                print(
                    '--confirm (-c) argument with repeated username argument must be given to delete specific user')
        elif args.edit:
            if args.confirm == args.edit:
                user.username = args.edit
                user.save_to_db()
                print(f'Changed username from "{args.username}" to "{args.edit}"')
            else:
                print(
                    '--confirm (-c) argument with repeated edit argument must be given to change specific username')
        elif args.new_pass:
            if args.confirm == args.new_pass:
                if len(args.new_pass) < 8:
                    print('Password too short, require at least 8 characters!')
                else:
                    user.hashed_password = args.new_pass
                    user.save_to_db()
                    print(f'Password changed!')
            else:
                print(
                    '--confirm (-c) argument with repeated password argument must be given to change password')
