from api import *


def project_list():
    counter = 0
    for item in projects():
        print('(' + str(counter) + ') ' + item)
        counter += 1


def version_group_list(project_number):
    counter = 0
    for item in version_groups(project_number):
        print('(' + str(counter) + ') ' + item)
        counter += 1


def build_list(project_number, mc_version):
    counter = 0
    returnvalue = version_group_builds(project_number, mc_version)
    for item in returnvalue:
        print('(' + str(counter) + ') ' + 'Build: ' + str(item['build']) + 'for version' + str(item['version']))
        print(item)
        print(item['build'])
        counter += 1