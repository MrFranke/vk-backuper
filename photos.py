# -*- coding: utf-8 -*-

from vk_api import VkTools
import urllib
import os
import ssl
from pathlib import Path
import json
import codecs

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ssl._create_default_https_context = ssl._create_unverified_context

def backup_all_photo(session, backup_dir):
    get_all_album(session, 'wall', backup_dir)
    get_all_album(session, 'saved', backup_dir)
    get_all_album(session, 'profile', backup_dir)

    api = session.get_api()
    albums = api.photos.getAlbums(owner_id = session.token['user_id'])
    for album in albums['items']:
        get_all_album(session, album['id'], backup_dir, album['title'])
        get_albums_comments(session, album['id'], backup_dir, album['title'])

def get_all_album(session, id, backup_dir, title=None):
    if title is None:
        title = id
    tools = VkTools(session)
    photos = tools.get_all('photos.get', 1000,
                           {'owner_id': session.token['user_id'], 'album_id': id, 'photo_sizes': 1})
    extractes_photo = extract_photos_to_tmp(photos, title, backup_dir)
    print('Saved photos: %d, downloaded: %d' % (photos['count'], len(extractes_photo)))
    return extractes_photo

def get_album_dir_path(title, backup_dir):
    return Path('%s/photo/%s' % (backup_dir, title))

def create_backup_dir(title, backup_dir):
    path = get_album_dir_path(title, backup_dir)
    if os.path.isdir(path):
        return path
    path.mkdir(parents=True)
    return path

def extract_photos_to_tmp(photos, title, backup_dir):
    dir_path = get_album_dir_path(title, backup_dir)
    results = []
    create_backup_dir(title, backup_dir)
    for photo in photos['items']:
        path = '%s/%s%s' % (dir_path, photo['id'], '.jpg')
        if os.path.exists(path):
            continue
        urllib.request.urlretrieve(photo['sizes'][-1]['src'], path)
        results.append(path)
        print(path, '%s/%s' % (len(results), photos['count']))
    return results

def get_albums_comments(session, id, backup_dir, title=None):
    if title is None:
        title = id
    tools = VkTools(session)
    comments = tools.get_all('photos.getAllComments', 100, {'owner_id': session.token['user_id'],'album_id': id})
    path = get_album_dir_path(title, backup_dir)

    file = codecs.open('%s/comments.json'%(path), 'w', 'utf-8')
    file.write(json.dumps(comments, ensure_ascii=False))
    file.close()
    print('Save comments for: %s'%(title))