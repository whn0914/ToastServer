# -*- coding: utf-8 -*-  

from app import db

class Toast(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	uid = db.Column(db.Integer)
	body = db.Column(db.String(512))
	creation_time = db.Column(db.DateTime)
	trumpet_count = db.Column(db.Integer)
	shit_count = db.Column(db.Integer)

	def __init__(self, uid, body, creation_time, trumpet_count, shit_count):
		self.uid = uid
		self.body = body
		self.creation_time = creation_time
		self.trumpet_count = trumpet_count
		self.shit_count = shit_count

class ToastUser(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	creation_time = db.Column(db.DateTime)

	def __init__(self, creation_time):
		self.creation_time = creation_time

class ToastOperation(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	uid = db.Column(db.Integer)
	toast_id = db.Column(db.Integer)
	type = db.Column(db.Integer)
	creation_time = db.Column(db.DateTime)

	def __init__(self, uid, toast_id, type, creation_time):
		self.uid = uid
		self.toast_id = toast_id
		self.type = type
		self.creation_time = creation_time
		
class Scanner(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(256))
	phone = db.Column(db.String(20))
	position = db.Column(db.String(256))
	valid = db.Column(db.Integer)
	
	def __init__(self, name, phone, position):
		self.name = name
		self.phone = phone
		self.position = position
		self.valid = 1
		