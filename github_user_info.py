#!bin/env python

"""
A python program/script to get user info (ie languages used) from a specific
user.
"""

import sys
import requests
import argparse
import github_config as gh_config

def get_github_user_api(username, user_info):
    """function to get the correct path to the github user's API"""
    if user_info:
        user_resp = requests.get(
            'https://api.github.com/users/' + username, auth=gh_config.auth
        )
        if user_resp.status_code == '200':
            print user_resp
            # print_user_info(user_resp)
        else:
            print "Error getting user info." + str(user_resp)
    repos_resp = requests.get(
        'https://api.github.com/users/' + username + '/repos',
        auth=gh_config.auth
    )

def main(argv):
    """Main part of the program"""

    # Parsing with argparse for the github username
    parser = argparse.ArgumentParser(
        description="Output info on a github user."
    )
    parser.add_argument(
        '--user_name', '-u', dest='username', metavar='USER', type=str,
        required=True,
        help=("The user from whom to get the info from.")
    )
    parser.add_argument(
        '--user_info', dest='user_info', action='store_true',
        help=("More info on the user")
    )
    parser.set_defaults(user_info=False)
    args = parser.parse_args(argv[1:])
    user = args.username
    user_info = args.user_info

    get_github_user_api(user, user_info)



if __name__ == "__main__":
    main(sys.argv)