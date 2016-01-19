# -*- coding: utf-8 -*-  
from flask import jsonify
from app import app, db
from models import Toast, ToastUser
from response import Response
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
	return "Hehe!"

# 插入新用户
@app.route('/addUser')
def add_user():
	user = ToastUser(datetime.now())
	db.session.add(user)
	db.session.commit()
	return jsonify(Response.success(msg="插入成功", data=user.id))


@app.route('/toasts/')
def list_toasts():
    toasts = Toast.query.all()
    dic= {}
    for t in toasts:  
       dic = {"uid":t.uid, "body":t.body, "time":t.creation_time.strftime("%Y-%m-%d %H:%M:%S")}
       print t.body
       print jsonify(dic)
    return jsonify(Response.success(msg="成功啦", data=dic))