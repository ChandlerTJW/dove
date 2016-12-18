from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import Blueprint
from flask import abort
from flask import session

from models.user import User

import time


def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        return u


def current_time():
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime()
    dt = time.strftime(format, value)
    return dt


def log(*args, **kwargs):
    dt = current_time()
    with open('log.txt', 'a', encoding="utf-8") as f:
        print(dt, *args, file=f, **kwargs)
