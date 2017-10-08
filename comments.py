# -*- coding: utf-8 -*-
#TODO: сделать сохранение комментариев и файлов из комментариев

from vk_api import VkTools
import os
from pathlib import Path
import json
import codecs


def get_comments_with_files(comments, path, session):
    create_comments_assets(path)

def create_comments_assets(path):
    path_to_dir = Path('%s/comments'%(path))
    if os.path.exists(path_to_dir):
        return path_to_dir
        path_to_dir.mkdir(parents=True)
    return path_to_dir

def write_json(json, path):
    file = codecs.open('%s/comments.json' % (path), 'w', 'utf-8')
    file.write(json.dumps(comments, ensure_ascii=False))
    file.close()