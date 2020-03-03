#!/usr/bin/env python
# -*- encoding: utf-8
"""gitone.

Usage:
  ghclone <url>
  ghclone (-h | --help)
  ghclone (-v | --version)

Options:
  -h --help           Show this screen.
  -v --version        Show version.
"""
from docopt import docopt
import requests
import re
import os
import errno

TOKEN = None
__version__ = 1.0
USERAGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'
API_BASE_URL = 'https://api.github.com'
REPO_CONTENTS_ENDPOINT = API_BASE_URL + '/repos/{}/{}/contents'
BASE_NORMALIZE_REGEX = re.compile(r'.*github\.com\/')

req = requests.session()
req.headers.update({'User-Agent': USERAGENT})


def doexit(m='An error occured'):  # 方便退出时可以显示报错信息
    print(m)
    exit(1)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as err:  # Python >2.5
        if err.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def clone_file(download_url, file_path):
    r = req.get(download_url, stream=True)
    try:
        r.raise_for_status()
    except Exception as e:
        doexit('Failed to clone ' + download_url)

    with open(file_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)


def clone(base_url, rel_url=None, path=None, ref=None):
    req_url = base_url + '/' + rel_url if rel_url else base_url

    # Get path metadata
    r = req.get(req_url) if not ref else req.get(req_url, params={'ref': ref})
    try:
        r.raise_for_status()
    except Exception as e:
        doexit('Failed to fetch metadata for ' + path)
    repo_data = r.json()

    # Recursively clone content
    for item in repo_data:
        if item['type'] == 'dir':
            # Fetch dir recursively
            clone(base_url, item['path'], path, ref)
        else:
            # Fetch the file
            new_file_path = resolve_path(item['path'], path)
            new_path = os.path.dirname(new_file_path)
            # Create path locally
            mkdir_p(new_path)
            # Download the file
            clone_file(item['download_url'], new_file_path)
            # print('Cloned', item['path'])


def resolve_path(path, dir):
    index = path.find(dir)
    if index is -1:
        return os.path.abspath(os.path.join(dir, path))
    else:
        return os.path.abspath(path[index:])


def main():
    args = docopt(__doc__)
    if args['--version']:
        print(__version__)
        exit(0)

    x_url = args['<url>']
    normal_url = re.sub(BASE_NORMALIZE_REGEX, '', x_url)
    x_args = normal_url.replace('/tree', '').split('/')

    if len(x_args) < 2 or normal_url == x_url:
        doexit('Failed! Invalid GitHub URL')

    if TOKEN is None:
        doexit(
            "Error: No token! Get your token here: https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line")
    req.headers.update({'Authorization': 'token ' + TOKEN})

    # print(x_args)
    user, repo = x_args[:2]
    ref = None
    rel_url = None

    if len(x_args) >= 2:
        # Clone entire repo
        path = repo

    if len(x_args) >= 3:
        # Clone entire repo at the branch
        ref = x_args[2]

    if len(x_args) >= 4:
        # Clone subdirectory
        rel_url = os.path.join(*x_args[3:])
        path = x_args[-1]

    api_req_url = REPO_CONTENTS_ENDPOINT.format(user, repo)

    # print(api_req_url)

    print("Cloning into '%s'..." % path)
    clone(api_req_url, rel_url, path, ref)
    print("done.")


if __name__ == '__main__':
    main()
