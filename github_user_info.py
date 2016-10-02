#!bin/env python

"""
A python program/script to get user info (ie languages used) from a specific
user.
"""

import sys
import requests
import argparse
import datetime
import github_config as gh_config

def convert_github_datetime(datetime_str):
    """function to convert the time format of Github to datetime format
    datetime_str: string - github datetime string format to convert
    """

    converted_datetime = datetime.datetime.strptime(
        datetime_str, "%Y-%m-%dT%H:%M:%SZ"
        )
    return converted_datetime

def print_user_info(user_resp):
    """function to format and print user information
    user_resp: response object - the response on user from github API
    """

    user_json = user_resp.json()
    print "login:\t" + str(user_json.get("login"))
    print "\tname:\t" + str(user_json.get("name"))
    print "\tcompany:\t" + str(user_json.get("company"))
    print "\twebsite:\t" + str(user_json.get("blog"))
    print "\tlocation:\t" + str(user_json.get("location"))
    print "\temail:\t\t" + str(user_json.get("email"))
    print "\tpublic repos:\t" + str(user_json.get("public_repos"))
    print "\tcreated:\t" + str(
        convert_github_datetime(user_json.get("created_at"))
        )
    print "\tupdated:\t" + str(
        convert_github_datetime(user_json.get("updated_at"))
        )
    # print a newline to separate from rest of program
    print

def print_repo_activity(repo):
    """function to print relevant information about the repository
    repo: json object - individual repository information to get
    information from.
    """
    print "\t\tfork:\t\t" + str(repo.get("fork"))
    print "\t\tmain language:\t" + str(repo.get("language"))
    print "\t\tcreated:\t" + str(
        convert_github_datetime(repo.get("created_at"))
        )
    print "\t\tupdated:\t" + str(
        convert_github_datetime(repo.get("updated_at"))
        )

def print_user_repos_info(repos_resp):
    """function to print basic repository information
    repos_resp: response object - the response on repository information from
    the github API
    """

    repos_json = repos_resp.json()
    print "Repositories:"
    for repo in repos_json:
        print "\t" + str(repo.get("name"))
        print_repo_activity(repo) # TODO
    # print repos_json

def get_github_user_api(username, user_info, number_repos):
    """function to get the correct path to the github user's API
    username: string - the Github username to get the information from the API
    user_info: boolean - tells the program wether or not to print user info
    """

    if user_info:
        user_resp = requests.get(
            'https://api.github.com/users/' + username, auth=gh_config.auth
        )
        if user_resp.status_code == 200:
            print_user_info(user_resp)
        else:
            print "Error getting user info." + str(user_resp)
    # if number_repos:
    repos_resp = requests.get(
        'https://api.github.com/users/' + username + '/repos',
        auth=gh_config.auth
    )
    print_user_repos_info(repos_resp)

def main(argv):
    """Main part of the program
    argv: array - all the arguments given to the program to be parsed
    """

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
        default=False,
        help=("More info on the user")
    )
    parser.add_argument(
        '--number_repos', dest='number_repos', metavar='N', type=int,
        default=None,
        help=("The N most committed repos.")
    )
    args = parser.parse_args(argv[1:])
    user = args.username
    user_info = args.user_info
    number_repos = args.number_repos

    get_github_user_api(user, user_info, number_repos)

if __name__ == "__main__":
    main(sys.argv)