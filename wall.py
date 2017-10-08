# -*- coding: utf-8 -*-

from vk_api import VkTools
import json
import codecs
import os
from pathlib import Path

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_wall(session, backup_dir):
    path = backup_dir if backup_dir else ROOT_DIR
    create_backup_dir(path)
    tools = VkTools(session)
    wall = tools.get_all('wall.get', 100, {'owner_id': session.token['user_id']})
    print(wall)
    create_json(wall, path)

def create_backup_dir(backup_dir):
    path = Path('%s/wall/' % (backup_dir))
    if os.path.isdir(path):
        return path
    path.mkdir(parents=True)
    return path

def get_wall_dir_path(path):
    return '%s/wall/groups.json' % (path)

def create_json(wall, path):
    path_to_json = get_wall_dir_path(path)
    file = codecs.open(path_to_json, 'w', 'utf-8')
    file.write(json.dumps(wall, ensure_ascii=False))
    file.close()
    print('Saved wall posts (%s)' % (wall['count']))