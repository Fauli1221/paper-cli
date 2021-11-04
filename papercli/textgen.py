"""Import re rich api and saved data"""
import re

from rich import print

from papercli.api import version_groups, version_group_builds
from papercli.save import selected_builds, selected_mc_version, build_name, projects_list


def project_list():
    """List Project's"""
    counter = 0
    for item in projects_list:
        print('(' + str(counter) + ') ' + item)
        counter += 1


def version_group_list(project_number):
    """List Versions"""
    counter = 0
    for item in version_groups(project_number):
        print('(' + str(counter) + ') ' + item)
        counter += 1


def build_list(project_number, mc_version):
    """List Builds"""
    counter = 0
    returnvalue = version_group_builds(project_number, mc_version)
    sorted_val = sorted(returnvalue, key=lambda k: k['build'], reverse=True)
    project = projects_list[project_number]
    for item in sorted_val:
        try:
            print(
                '(' + str(counter) + ') ' + 'Build: ' + str(item['build']) + ' for MC version ' + str(item['version']))
            link = '[link=https://github.com/PaperMC/{poje}/commit/{commit_number}]'.format(
                commit_number=str(item['changes'][0]['commit']), poje=project)
            unformated_summary = str(item['changes'][0]['summary']).format()
            matches = re.search(r"#(\d*)", unformated_summary)
            if matches:
                issueurl = '[link=https://github.com/PaperMC/{poje}/issues/{group}]{urltext}[/link]'.format(
                    group=matches.group(1), urltext=matches.group(), poje=project)
                summery_without_url = re.sub(r"#(\d*)", "", unformated_summary, 1)
                formated_summary = summery_without_url[:matches.start()] + issueurl + summery_without_url[
                                                                                      matches.start():]
            else:
                formated_summary = unformated_summary

            print('     [{commitlink}{commitshort}[/link]] {summary}'.format(commitlink=link,
                                                                             commitshort=str(
                                                                                 item['changes'][0]['commit'])[
                                                                                         :7], summary=formated_summary))
            counter = infosave(counter, item)
        except IndexError:
            print('      there was no info found about ' + str(item['build']))
            counter = infosave(counter, item)


def infosave(counter, item):
    """save info"""
    build_name.append(counter)
    build_name.append(item['downloads']['application']['name'])
    selected_builds.append(counter)
    selected_builds.append(item['build'])
    selected_mc_version.append(counter)
    selected_mc_version.append(item['version'])
    counter += 1
    return counter
