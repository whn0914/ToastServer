# -*- coding: utf-8 -*-  
from flask import request, jsonify
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

# 添加吐槽
@app.route('/toast')
def toast():
	uid = request.args.get('uid')
	body = request.args.get('body')
	toast = Toast(uid, body, datetime.now(), 0, 0)
	db.session.add(toast)
	db.session.commit()
	return jsonify(Response.success(msg="吐槽成功"))

