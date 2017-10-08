# -*- coding: utf-8 -*-

from vk_api import VkTools
import json
import codecs
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_user_groups(session, backup_dir):
    path = backup_dir if backup_dir else ROOT_DIR
    tools = VkTools(session)
    groups = tools.get_all('groups.get', 1000, {'owner_id': session.token['user_id'], 'extended': 1})
    write_json(groups, path)

def get_groups_dir_path(path):
    return '%s/groups.json' % (path)

def write_json(groups, path):
    path_to_json = get_groups_dir_path(path)

    file = codecs.open(path_to_json, 'w', 'utf-8')
    file.write(json.dumps(groups, ensure_ascii=False))
    file.close()
    print('Saved groups list (%s)'%(groups['count']))