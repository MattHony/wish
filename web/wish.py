# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/8/2 21:08
# @Author : '红文'
# @File : wish.py
# @Software: PyCharm
from flask import flash, url_for, render_template
from werkzeug.utils import redirect

from app.models.base import db
from app.models.wish import Wish
from app.view_models.wish import MyWishes
from . import web
from flask_login import  current_user


@web.route('/my/wish')
def my_wish():
    uid = current_user.id
    wishes_of_mine = Wish.get_user_gifts(uid)
    isbn_list = [wish.isbn for wish in wishes_of_mine]
    gift_count_list = Wish.get_wishes_counts(isbn_list)
    view_model = MyWishes(wishes_of_mine,gift_count_list)
    return render_template('my_wishes.html', wishes=view_model.gifts)
    # return 'My Wish'


@web.route('/wish/book/<isbn>')
def save_to_wishes(isbn):
    if current_user.can_save_to_list(isbn):
        # 事务
        # rollback
        # try:
        with db.auto_commit():
            gift = Wish()
            gift.isbn = isbn
            gift.uid = current_user.id
            #############################
            # current_user.beans += 0.5
            # current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
            # db.session.commit()
        # except Exception as e:
        #     db.session.rollback()
        #     raise e
    else:
        flash('这本书已添加至你的赠送清单或者已存在你的心愿清单，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
def satisfy_wish(wid):


@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    pass
