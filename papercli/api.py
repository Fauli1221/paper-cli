import requests

from papercli.save import *


def api_requests(url):
    request_resp = requests.get(url)
    request_json = request_resp.json()
    return request_json


def projects():
    project_json = api_requests('https://papermc.io/api/v2/projects')
    for item in project_json:
        for data_items in project_json[item]:
            projects_list.append(data_items)
    return projects_list


def version_groups(selected_project):
    project_info_json = api_requests('https://papermc.io/api/v2/projects/' + projects_list[selected_project])
    for item in project_info_json['version_groups']:
        version_groups_list.append(item)
    return version_groups_list


def version_group_builds(selected_project, groop):
    build_infos_version_group_json = api_requests(
        'https://papermc.io/api/v2/projects/' + projects_list[selected_project] + '/version_group/' +
        version_groups_list[groop] + '/builds')
    return build_infos_version_group_json['builds'][-15:]


def versions(selected_project):
    version_json = api_requests('https://papermc.io/api/v2/projects/' + projects_list[selected_project])
    for item in version_json['versions']:
        versions_list.append(item)
    return versions_list


def builds(selected_project, mc_version):
    builds_json = api_requests('https://papermc.io/api/v2/projects/' + projects_list[selected_project] + '/versions/' +
                               versions_list[mc_version])
    for item in builds_json['builds']:
        build_list.append(item)
    return build_list[-20:]


def build_info(selected_project, mc_version, build):
    build_info_json = api_requests(
        'https://papermc.io/api/v2/projects/' + projects_list[selected_project] + '/versions/' +
        versions_list[mc_version] + '/builds/' + str(build_list[build]))
    return build_info_json
