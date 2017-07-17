#!/usr/bin/env python
#
# PROVIDED AS IS WITH NO WARRANTY OR GUARANTEES
# Copyright (c) 2017 Evident.io, Inc., All Rights Reserved
#
# This script dumps a list of ESP users for an organization to a csv file called,
# "esp_users_report.csv" in the same directory that the script is executed in.
# Alternatively, you can simply list ESP users in json format to the screen.
#
# Requirements:
#
# * Python3 (Tested with version 3.6.1)
#   `python --version`
#
# * Install the ESP Python SDK
#   https://github.com/EvidentSecurity/esp-sdk-python2 
# 
# * Valid ESP credentials / API keys
#   https://esp.evident.io/settings/api_keys
#   export ESP_ACCESS_KEY_ID=<your_access_key>
#   export ESP_SECRET_ACCESS_KEY=<your_secret_access_key>
#

import esp_sdk
import csv
import os
import json
import sys
import argparse

def usage():
    print('usage:', sys.argv[0], '[-h] -o <output>')
    sys.exit(1)

def script_args():
    p = argparse.ArgumentParser(description='Output option.')
    p.add_argument ('-o', metavar = '<output>', type = str, help = 'csv or json', required = True)
    args = p.parse_args()

    return args


def create_user_report(users):
    """ Build a user report """

    report = []
    for u, user in enumerate(users):

        report_info = {
          'First Name'       : user.first_name,
          'Last Name'        : user.last_name,
          'Email'            : user.email,
          'Role'             : user.role.name,
          'Organization'     : user.organization.name,
          'Last Updated'     : user.updated_at.strftime("%b %d, %Y %I:%M:%S %p"),
          'MFA Enabled'      : user.mfa_enabled
        }

        report.append(report_info)

    return report


def create_csv_file(csv_file_name, report):
    """ Create csv formatted file """

    try:
        with open(csv_file_name, 'w') as f:
            head = [ 'First Name', 'Last Name', 'Email', 'Role', 'Organization', 'Last Updated', 'MFA Enabled' ]
            writer = csv.DictWriter(f, fieldnames=head)
            writer.writeheader()
            for row in report:
                writer.writerow(row)
    except:
        pass 

    if os.path.exists(csv_file_name) == True and os.stat(csv_file_name).st_size > 0:
        result = 'Success: Created ESP csv user report, ' + csv_file_name +'.'
    else:
        result = 'Error: Failed to create csv file, ' + csv_file_name +'.'

    return result


def main(csv_file_name):
    """ Run checks and do the work """

    args = script_args()
    if args.o != 'json' and args.o != 'csv':
        usage()

    try:
        users_api = esp_sdk.UsersApi()
        users = users_api.list(include='role,organization,sub_organizations,teams')
    except esp_sdk.rest.ApiException as e:
        if str(e.status) == '401':
            print('Error: Please check your ESP credentials / API keys.')
        else:
            print(e)
        sys.exit(1)

    if args.o == 'json':
        report = create_user_report(users)
        print(json.dumps(report, sort_keys=False, indent=4))
    elif os.path.exists(csv_file_name) == True:
        print('Error: The file ' + csv_file_name + ' already exists.')
        sys.exit(1)
    else:
        report = create_user_report(users)
        result = create_csv_file(csv_file_name, report)
        print(result)
        

if __name__ == "__main__":

  main(csv_file_name = 'esp_users_report.csv')
