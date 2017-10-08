# -*- coding: utf-8 -*-

import os
from pathlib import Path
import vk_api
import argparse
import photos
import groups
import wall

BACKUP_DIR = '%s/%s' % (os.path.dirname(os.path.abspath(__file__)), '/backup')

parser = argparse.ArgumentParser(description='Great Description To Be Here')
parser.add_argument('-l', '--login', dest='login', help='VK password')
parser.add_argument('-p', '--password', dest='password', help='VK password')
parser.add_argument('-a', '--appid', dest='app_id', help='VK App ID')
parser.add_argument('-d', '--dir', dest='backup_dir', help='Directory for backup files')
args = parser.parse_args();

def create_backup_dir(path= BACKUP_DIR):
    path = Path(path)
    if args.backup_dir:
        path = Path(args.backup_dir)
    if not os.path.exists(path):
        path.mkdir(parents=True)
    return path


def auth():
    vk_session = vk_api.VkApi(args.login,
                              args.password,
                              app_id=args.app_id,
                              scope='photos,audio,wall,messages,offline,groups')

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    return vk_session

def main():
    vk_session = auth()
    dir_path = create_backup_dir()
    #photos.backup_all_photo(vk_session, backup_dir=dir_path)
    #groups.get_user_groups(vk_session, backup_dir=dir_path)
    wall.get_wall(vk_session, backup_dir=dir_path)

if __name__ == '__main__':
    main()