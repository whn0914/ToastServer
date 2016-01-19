# -*- coding: utf-8 -*- 
class Response():

	@staticmethod
	def success(msg=None, data=None):
		return {
					"status":1,
					"code":1,
					"msg":msg,
					"data":data
				}

	@staticmethod
	def fail(status=-1, code=-1, msg="服务器出错"):
		return {
					"status":status,
					"code":code,
					"msg":msg,
				}