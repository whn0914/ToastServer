# -*- coding: utf-8 -*-  

dbhost = '218.244.132.65:3306' 
dbuser = 'root'
dbpassword = '920704'  
dbname = 'toast_db'  
  
SQLALCHEMY_DATABASE_URI = 'mysql://' + dbuser + ':' + dbpassword + '@' + dbhost + '/' +dbname
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
