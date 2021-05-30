# -----------------------------------------------------------
# handles all the data processing operations.
# author: Mohit
# -----------------------------------------------------------

import requests
import json
import yaml
import base64
import os

from processing_layer import constants as const
from db_layer import db
from processing_layer import repo_model as rm

ORG_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')


def get_organizations():
    """
    get list of all organizations from 'orgs.yaml'
    :param: none
    :return: none
    """

    with open(r'./org.yaml') as file:
        all_orgs = yaml.full_load(file)
        if 'orgs' in all_orgs:
            for org in all_orgs['orgs']['name']:
                repo_list = []
                repos_url = const.ORG_REPO_URL.format(org_name=org)
                headers = {
                    'Authorization': 'Bearer {}'.format(ORG_TOKEN)
                }
                repos_data = json.loads(requests.get(repos_url, headers=headers).text)
                for repo in repos_data:
                    repo_details = rm.Repo()
                    repo_details.name = repo['name']
                    repo_details.owner = repo['owner']['login']
                    repo_list.append(repo_details)

                for repo_owner_details in repo_list:
                    read_org_repo(repo_owner_details)
            print("org details added in db")

        else:
            print("Organization list is empty")


def read_org_repo(repo_details: object):
    """
    get the step details from config.yml for particular repo
    :param repo_details: Contains repo name and owner details
    :type repo_details:object
    :return: none
    """
    file_data, sha = get_config_file(repo_details.owner, repo_details.name)
    try:
        all_steps = []
        missing_steps = []
        for step in file_data['jobs']['build']['steps']:
            if 'run' in step:
                pass
            else:
                all_steps.append(step)
        print(all_steps)

        repo_details.steps = all_steps

        check = all(item in all_steps for item in const.CIRCLECI_MANDATORY_STEPS)

        if check:
            repo_details.status = const.REPO_COMPLAINT
            repo_details.req_steps = None
        else:
            repo_details.status = const.REPO_NON_COMPLAINT
            for step_req in const.CIRCLECI_MANDATORY_STEPS:
                if step_req not in all_steps:
                    missing_steps.append(step_req)

        repo_details.req_steps = missing_steps
        db.repo_insert(repo_details)
    except:
        print("no steps found")


def get_repo_steps(org, repo):
    """
    get the circleci steps available in repo
    :param org: organization name in which repo present
    :type org: str
    :param repo: repository name from which circleci steps needs to read
    :type repo: str
    :return result: all steps present in repo
    :rtype result: list
    """
    data = db.get_repo_details(org, repo)
    repo_steps = []
    result = {}
    if 'Item' in data:
        for step in data['Item']['steps']:
            repo_steps.append(step)
        result['steps'] = repo_steps
        return result
    else:
        result['msg'] = "details not found"
        return result


def add_repo_steps(org, repo, data):
    """
    add steps to existing config.yml file
    :param org: organization name
    :type org: str
    :param repo: repository name
    :type repo: str
    :param data: steps to be added
    :type data: dict
    :return response: returns the http response
    """
    config_file, sha_code = get_config_file(org, repo)
    new_steps = data['steps']
    for step in new_steps:
        config_file['jobs']['build']['steps'].append(step)
    response = git_commit(config_file, org, repo, sha_code, const.GIT_COMMIT_MESSAGE)
    return response


def remove_all_steps(org, repo):
    """
    delete all steps form config.yml
    :param org: organization name
    :type org: str
    :param repo: repository name
    :type repo: str
    :return response: returns the http response
    """
    config_file, sha_code = get_config_file(org, repo)
    config_file['jobs']['build']['steps'].clear()
    response = git_commit(config_file, org, repo, sha_code, const.GIT_DELETE_COMMIT_MESSAGE)
    return response


def get_config_file(org, repo):
    """
    get the content of file config.yml
    :param org: organization name
    :type org: str
    :param repo: repository name
    :type repo: str
    :return file_data: content of config.yml file
    :rtype file_data: dict
    :return file_sha: sha code associated with config.yml
    :rtype file_sha: str
    """
    repo_content_url = const.REPO_CONTENT_URL.format(owner=org, repo_name=repo)
    headers = {
        'Authorization': 'Bearer {}'.format(ORG_TOKEN)
    }
    config_data = json.loads(requests.get(repo_content_url, headers=headers).text)
    file_sha = config_data['sha']
    file_download_url = config_data['download_url']
    file = requests.get(file_download_url, headers=headers).text
    file_data = yaml.full_load(file)
    return file_data, file_sha


def git_commit(config_file, org, repo, sha_code, commit_message):
    """
    this method will commit the config.yml file to github
    :param config_file: content of config.yml file
    :type config_file: dict
    :param org: organization name
    :type org: str
    :param repo: repository name
    :type repo: str
    :param sha_code: SHA code associated with config.yml
    :type sha_code: str
    :param commit_message: message used for commit
    :type commit_message: str
    :return response: returns the http response
    """
    updated_file = yaml.dump(config_file)
    updated_file_byte = updated_file.encode("ascii")
    content = base64.b64encode(updated_file_byte)
    repo_content_url = const.REPO_CONTENT_URL.format(owner=org, repo_name=repo)
    headers = {
        'Authorization': 'Bearer {}'.format(ORG_TOKEN)
    }
    req_body = {
        "message": "{}".format(commit_message),
        "content": "{}".format(content.decode("utf-8")),
        "sha": "{}".format(sha_code)
    }

    response = requests.put(repo_content_url, data=json.dumps(req_body), headers=headers)
    return response


def get_repo_report(org_name):
    """
    creates the report containing repo, status, missing steps
    :param org_name: organization name
    :type org_name: str
    :return response: returns the compliant report of repo's
    :rtype response: list
    """
    response = db.query_org_repo(org_name)
    if response:
        for item in response:
            del item['steps']
        return response
    else:
        error = {'msg': 'Organization not found'}
        response.append(error)
        return response


