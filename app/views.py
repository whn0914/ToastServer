# -*- coding: utf-8 -*-  
from flask import request, jsonify, render_template
from app import app, db
from models import Toast, ToastUser, ToastOperation, Scanner
from response import Response
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

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


ITEMS_PER_PAGE = 20

# 拉取吐槽列表
@app.route('/listToasts')
def list_toasts():
	page = int(request.args.get('page'))
	uid = int(request.args.get('uid'))
	paginate = Toast.query.order_by(Toast.creation_time.desc()).paginate(page, ITEMS_PER_PAGE, False)
	toast_list = paginate.items
	res = []
	for item in toast_list:
		item_res = {	
						"toast_id":item.id,
						"body":item.body, 
						"time":item.creation_time.strftime("%Y-%m-%d %H:%M:%S"), 
						"trumpet_count":item.trumpet_count,
						"shit_count":item.shit_count,
						"trumpet":0,
						"shit":0
					}

		toast_operation_list = ToastOperation.query.filter_by(uid=uid).filter_by(toast_id=item.id).all()
		for operation in toast_operation_list:
			if operation.type == 0:
				item_res['shit'] = 1
			if operation.type == 1:
				item_res['trumpet'] = 1

		res.append(item_res)
	return jsonify(Response.success(msg="拉取成功", data=res))

# 操作码注释
TRUMPET_OPERATION = 1
SHIT_OPERATION = 0

# 呐喊
@app.route('/trumpet')
def trumpet():
	toast_id = int(request.args.get('toastId'))
	uid = int(request.args.get('uid'))
	trumpet_operation = ToastOperation(uid, toast_id, TRUMPET_OPERATION, datetime.now())
	db.session.add(trumpet_operation)
	db.session.commit()
	# 让记录+1
	toast = Toast.query.get(toast_id)
	if toast is not None:
		toast.trumpet_count += 1
		db.session.commit()
	else:
		return jsonify(Response.fail(msg="找不到这条toast"))
	return jsonify(Response.success(msg="呐喊成功"))

# shit
@app.route('/shit')
def shit():
	toast_id = int(request.args.get('toastId'))
	uid = int(request.args.get('uid'))
	shit_operation = ToastOperation(uid, toast_id, SHIT_OPERATION, datetime.now())
	db.session.add(shit_operation)
	db.session.commit()
	# 让记录+1
	toast = Toast.query.get(toast_id)
	if toast is not None:
		toast.shit_count += 1
		db.session.commit()
	else:
		return jsonify(Response.fail(msg="找不到这条toast"))
	return jsonify(Response.success(msg="shit成功"))

# 根据 toast id 获取 toast
@app.route('/getToast')
def getToast():
	toast_id = int(request.args.get('toastId'))
	item = Toast.query.get(toast_id)
	if item is not None:
		res = {	
				"toast_id":item.id,
				"body":item.body, 
				"time":item.creation_time.strftime("%Y-%m-%d %H:%M:%S"), 
				"trumpet_count":item.trumpet_count,
				"shit_count":item.shit_count
			}
		return jsonify(Response.success(msg="拉取成功", data=res))
	else:
		return jsonify(Response.fail(msg="找不到这条toast"))


# 以下是二维码扫描器相关接口

# 将信息入库
@app.route('/scanner/insertInfo')
def insertInfo():
	name = request.args.get('name')
	phone = request.args.get('phone')
	position = request.args.get('position')
	if phone is None or len(phone.strip())<1 or not phone.isdigit():
		return jsonify(Response.fail(msg="信息有误"))
	items = Scanner.query.filter_by(phone=phone).all()
	if len(items)>0:
		return jsonify(Response.fail(msg="该手机号已录入，请更换手机号"))
	else:
		scanner = Scanner(name, phone, position)
		db.session.add(scanner)
		db.session.commit()
		return jsonify(Response.success(msg="插入成功", data=scanner.id))

# 验证二维码
@app.route('/scanner/verify')
def verify():
	info = request.args.get('info')
	if info is None or len(info.strip())<1:
		return jsonify(Response.fail(msg="信息有误，验证失败"))
	else:
		infoSegs = info.strip().split('-');
		if(len(infoSegs) == 2):
			item = Scanner.query.get(infoSegs[0])
			if item is None or cmp(item.phone, infoSegs[1])!=0:
				return jsonify(Response.fail(msg="信息有误，验证失败"))
			if item.valid == 0:
				return jsonify(Response.fail(msg="该二维码已被验证，不可重复验证"))
			item.valid = 0
			db.session.commit()
			res = {'name':item.name, 'phone':item.phone, 'position':item.position}
			return jsonify(Response.success(msg="验证通过", data=res))
		return jsonify(Response.fail(msg="信息有误，验证失败"))

