"""import request"""
import requests

from papercli.save import projects_list, version_groups_list, versions_list, builds_list


def api_requests(url):
    """Get request_json"""
    request_resp = requests.get(url)
    request_json = request_resp.json()
    return request_json


def projects():
    """Get projects_list"""
    project_json = api_requests('https://papermc.io/api/v2/projects')
    for item in project_json:
        for data_items in project_json[item]:
            projects_list.append(data_items)
    return projects_list


def version_groups(selected_project):
    """Get version_groups_list"""
    project_info_json = api_requests('https://papermc.io/api/v2/projects/' + projects_list[selected_project])
    for item in project_info_json['version_groups']:
        version_groups_list.append(item)
    return version_groups_list


def version_group_builds(selected_project, groop):
    """get build_infos_version_group_json"""
    build_infos_version_group_json = api_requests(
        'https://papermc.io/api/v2/projects/' + projects_list[selected_project] + '/version_group/' +
        version_groups_list[groop] + '/builds')
    return build_infos_version_group_json['builds'][-15:]


def versions(selected_project):
    """get versions_list"""
    version_json = api_requests('https://papermc.io/api/v2/projects/' + projects_list[selected_project])
    for item in version_json['versions']:
        versions_list.append(item)
    return versions_list


def builds(selected_project, mc_version):
    """Get builds_list"""
    builds_json = api_requests('https://papermc.io/api/v2/projects/' + projects_list[selected_project] + '/versions/' +
                               versions_list[mc_version])
    for item in builds_json['builds']:
        builds_list.append(item)
    return builds_list


def build_info(selected_project, mc_version, build):
    """get build_info_json"""
    build_info_json = api_requests(
        'https://papermc.io/api/v2/projects/' + projects_list[selected_project] + '/versions/' +
        versions_list[mc_version] + '/builds/' + str(build))
    return build_info_json
