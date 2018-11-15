import datetime
import sqlite3
from config import DB_PATH
class InitDB():
	db = None
	def __init__(self):
		if InitDB.db:
			return InitDB.db
		else:
			InitDB.db.conn = sqlite3.connect(DB_PATH)
			InitDB.db.c = InitDB.db.conn.cursor()
			return InitDB.db

class W_DB():
	db = None
	def __init__(self, ):
		self.ret = {
			'status': 0,
			'msg': 'ok'
		}
		if InitDB.db:
			self.conn = InitDB.conn
			self.c = InitDB.c
		else:
			self.conn = InitDB.conn = sqlite3.connect(DB_PATH)
			self.c = InitDB.c = self.conn.cursor()
	 
	
	def get_task(self):
		'''
		获取转发任务
		:return:
		'''
		sql = '''SELECT ID,url,content,status,account FROM forward WHERE status=0 or status BETWEEN 2 and 10'''
		task = None
		try:
			self.c.execute(sql)
			task = self.c.fetchone()
		except Exception:
			self.ret['status'] = 2
			self.ret['msg'] = '获取任务失败'
		if task:
			self.ret['data'] = task
			self.ret['status'] = 1
			return self.ret
		else:
			self.ret['status'] = 0
			self.ret['msg'] = '当前没有任务'
			return self.ret
	
	def set_task(self, url, content, status,account):
		'''
		设置转发任务
		:param url:转发微博地址
		:param content: 转发内容
		:param status: 状态
		:param account: 转发用的账号
		:return: 转发是否成功
		'''
		sql = '''INSERT INTO forward (url,content,status,account)
		VALUES ('{0}', '{1}',{2},"{3}");'''.format(url, content, status,account)
		try:
			self.c.execute(sql)
			self.conn.commit()
			self.ret['status'] = 1
		except Exception as e:
			self.ret['status'] = 0
			self.ret['msg'] = '任务提交失败'
		return self.ret
	def get_yes_tasks(self):
		today = datetime.datetime.now().date()
		date_count = datetime.timedelta(days=1)
		start_date = today - date_count
		sql = '''SELECT url,COUNT(ID),content FROM forward WHERE  excute_time="{0}" GROUP BY url ORDER BY count(ID)'''.format(start_date)
		try:
			self.c.execute(sql)
			task_list = self.c.fetchall()
			if len(task_list) >= 5:
				task_list = task_list[-5:]
			self.ret['data'] = task_list
			self.ret['status'] = 1
		except Exception as e:
			self.ret['status'] = 0
			self.ret['data'] = []
			self.ret['msg'] = '获取任务失败'
		return self.ret
	
	def update_task(self, id, status,date):
		'''
		更新转发任务
		:param id:转发任务id
		:param status: 转发任务状态
		:param date: 转发任务执行日期
		:return: 更新是否成功
		'''
		sql = '''UPDATE forward set status = {0},excute_time="{1}" where ID={2}
		'''.format(status,date,id)
		try:
			self.c.execute(sql)
			self.conn.commit()
			self.ret['status'] = 0
			self.ret['msg'] = '设置正确'
		except Exception as e:
			self.ret['status'] = 4
			self.ret['code'] = '设置状态失败'
		return self.ret
	
	def get_all_tasks_count(self,type,account):
		'''
		:param type:任务类型
		:param account:账号
		:return: 返回此账号完成此任务类型的总数
		'''
		sql = '''SELECT SUM("{0}") FROM record WHERE account="{1}"'''.format(type,account)
		sql_ret = None
		try:
			
			self.c.execute(sql)
			sql_ret = self.c.fetchone()
		except Exception as e:
			self.ret['status'] = 0
			self.ret['data'] = 0
			self.ret['msg'] = '获取任务数失败'
		if sql_ret:
			count = sql_ret[0]
			if count:
				self.ret['data'] = count
			else:
				self.ret['data'] = 0
			self.ret['status'] = 1
			
		return self.ret
	def get_error_tasks(self):
		'''
		获取尝试十次以上的转发任务
		:return:
		'''
		sql = '''
		SELECT account,url,content FROM forward WHERE status >10'''
		try:
			self.c.execute(sql)
			data = self.c.fetchall()
			self.ret['data'] = data
			self.ret['status'] = 1
		except Exception as e:
			self.ret['status'] = 0
			self.ret['msg'] = '获取错误'
			self.ret['data'] = []
		return self.ret
	
	
	def get_untask_count(self):
		'''
		获取还未执行或者正在尝试执行的转发任务
		:return:
		'''
		sql = '''SELECT COUNT(ID)
		FROM forward WHERE status=0 OR status BETWEEN 2 AND 10;
				'''
		sql_ret = None
		count = 0
		try:
			self.c.execute(sql)
			sql_ret = self.c.fetchone()
		except Exception:
			self.ret['status'] = 5
			self.ret['msg'] = '获取任务数失败'
		if sql_ret:
			count = sql_ret[0]
		self.ret['data'] = count
		return self.ret

	def check_date(self,account, sdate=None):
		'''
		检查record表里有没有当天执行的记录
		:param sdate:
		:return:
		'''
		now_date = datetime.datetime.now().date()
		if sdate:
			now_date = sdate
		sql = '''SELECT count(ID) FROM record WHERE  account = "{0}" AND date = "{1}"'''.format(account,now_date)
		count = 0
		try:
			self.c.execute(sql)
			count = self.c.fetchone()[0]
		except Exception:
			self.ret['status'] = 0
			return self.ret
		
		if count == 0:
			self.ret['status'] = 0
		else:
			self.ret['status'] = 1
		return self.ret
	
	def add_new_record(self, para,account,sdate=None):
		'''
		在record表里添加记录
		:param para: 任务类型：转发、评论、发微博
		:param account: 使用的账号
		:param sdate: 执行日期
		:return:
		'''
		now_date = datetime.datetime.now().date()
		if sdate:
			now_date = sdate
		
		sql = '''INSERT INTO record (date,{0},account) VALUES ("{1}",1,"{2}")'''.format(para,now_date,account)
		try:
			self.c.execute(sql)
			self.conn.commit()
			self.ret['status'] = 1
			return self.ret
		except Exception as e:
			self.ret['status'] = 0
			return self.ret
	
	def add_fo_record(self, para,account,sdate=None):
		'''
		添加执行记录
		:param para:
		:param account:
		:param sdate:
		:return:
		'''
		
		now_date = datetime.datetime.now().date()
		
		if sdate:
			now_date = sdate
		if self.check_date(account,sdate)['status'] == 0:
			ret = self.add_new_record(para,account,sdate)
			if ret['status'] == 0:
				self.ret['status'] = 1
				self.ret['msg'] = '添加新数据成功'
			else:
				self.ret['status'] = 0
				self.ret['msg'] = '添加新数据失败'
			
			return self.ret
		
		count = self.get_record_count(para,0,account)
		if count['status'] == 1:
			count = count['data']
		else:
			self.ret['status'] = 0
			return self.ret
		sql = '''UPDATE record SET {0}={1} WHERE date="{2}" AND account="{3}"'''.format(para, count + 1, now_date,account)
		try:
			self.c.execute(sql)
			self.conn.commit()
			self.ret['status'] = 1
		except Exception:
			self.ret['status'] = 0
			self.ret['msg'] = '更新数据失败'
		return self.ret
	
	def get_record_count(self, type,num,account):
		'''
		:param type:查询的操作类型
		:param num: 查询的具体日期距今天的数字
		:return: 某天执行某操作的记录
		'''
		today = datetime.date.today()
		oneday = datetime.timedelta(days=num)
		count_day = today - oneday
		sql = '''SELECT {0} FROM record WHERE date="{1}" AND account="{2}"'''.format(type, count_day,account)
		count = 0
		try:
			self.c.execute(sql)
			count = self.c.fetchone()[0]
		except Exception:
			self.ret['status'] = 0
			self.ret['data'] = 0
			return self.ret
		self.ret['status'] = 1
		if count:
			self.ret['data'] = count
		else:
			self.ret['data'] = 0
		return self.ret
	
	def get_comp(self, para, num=0):
		if num == 0:
			sql = '''
			SELECT  SUM({0})  FROM record'''.format(para)
		else:
			today = datetime.date.today()
			oneday = datetime.timedelta(days=num)
			count_day = today - oneday
			sql = """SELECT SUM({0})  FROM record WHERE date BETWEEN  '{1}' AND '{2}'""".format(para, count_day, today)
		
		count = 0
		try:
			self.c.execute(sql)
			count = self.c.fetchone()
			count = count[0]
		except Exception:
			self.ret['status'] = 0
			return self.ret
		self.ret['status'] = 1
		self.ret['data'] = count
		return self.ret
	def add_account(self,user,passwd):
		'''
		添加账号
		:param user:
		:param passwd:
		:return:
		'''
		sql = '''INSERT INTO account (user,passwd) VALUES ("{0}","{1}")'''.format(user,passwd)
		try:
			self.c.execute(sql)
			self.conn.commit()
			self.ret['status'] = 1
			self.ret['msg'] = '账户设置成功'
		except Exception as e:
			self.ret['status'] = 0
			self.ret['msg'] = '账户设置错误'
		return self.ret
	def del_account(self,user):
		'''
		删除账号
		:param user:
		:return:
		'''
		sql = '''DELETE FROM account WHERE user="{0}"'''.format(user)
		try:
			self.c.execute(sql)
			self.conn.commit()
			self.ret['status'] = 1
			self.ret['msg'] = '账户删除成功'
		except Exception as e:
			self.ret['status'] = 0
			self.ret['msg'] = '账户删除错误'
		return self.ret
	def get_accounts(self):
		'''
		获取所有账号列表
		:return:
		'''
		sql = '''
			SELECT user FROM account'''
		try:
			self.c.execute(sql)
			account_list = [x[0] for x in self.c.fetchall()]
			self.ret['status'] = 1
			self.ret['data'] = account_list
		 
		except Exception as e:
			self.ret['status'] = 0
			self.ret['data'] = []
			self.ret['msg'] = '获取账户失败'
	 
		return self.ret
	def del_forward_by_account(self,account):
		sql = '''DELETE FROM forward WHERE status != 1 AND account={0}'''.format(account)
		try:
			self.c.execute(sql)
			self.conn.commit()
			self.ret['status'] = 1
		except Exception:
			self.ret['status'] = 0
		return self.ret
	def get_sect_count(self,type,start,end,account):
		'''
		获取某期间某账号转发任务数量
		:param type:
		:param start:
		:param end:
		:param account:
		:return:
		'''
		today = datetime.datetime.now().date()
		date_count = datetime.timedelta(days=end)
		start_date = today - date_count
		date_count = datetime.timedelta(days=start)
		end_date = today - date_count
		sql = '''select sum("{0}") from record WHERE account="{1}" AND date BETWEEN "{2}" and "{3}"'''.format(type,account,start_date,end_date)
		try:
			self.c.execute(sql)
			count = self.c.fetchone()[0]
			self.ret['status'] = 1
		except Exception as e:
			self.ret['status'] = 0
			self.ret['data'] = 0
			self.ret['msg'] = '获取数据失败'
		if count:
			self.ret['data'] = count
		else:
			self.ret['data'] = 0
		return self.ret
	def del_task(self):
		'''
		删除尝试10次以上的转发任务
		:return:
		'''
		sql = '''DELETE FROM forward WHERE status>10'''
		try:
			self.c.execute(sql)
			self.conn.commit()
			self.ret['status'] = 1
			self.ret['msg'] = '删除成功'
		except Exception as e :
			self.ret['status'] = 0
			self.ret['msg'] = '删除错误'
		return self.ret
	def show_tasks_info(self):
		'''
		获取记录信息
		:return:
		'''
		pass
	def delete_all_tasks(self):
		'''
		删除三天以前的转发记录
		:return:
		'''
		today = datetime.datetime.now().date()
		date_count = datetime.timedelta(days=3)
		start_date = today - date_count
		sql = '''DELETE FROM forward WHERE status = 1 AND excute_time<"{0}"'''.format(start_date)
		try:
	
			self.c.execute(sql)
			self.conn.commit()
			self.ret['status'] = 1
			self.ret['msg'] = '删除成功'
		except Exception :
			self.ret['status'] = 0
			self.ret['msg'] = '删除错误'
		return self.ret
	def add_keyword(self,keyword,expect):
		'''
		添加关键词
		:param keyword:关键词
		:param expect: 希望执行次数
		:return: 添加结果
		'''
		sql_check = '''SELECT ID from search WHERE keyword="{0}"'''.format(keyword)
		
		exist = None
		try:
			self.c.execute(sql_check)
			exist = self.c.fetchone()[0]
		except Exception as e:
			self.ret['status'] = 0
			self.ret['msg'] = '增加关键词失败'
		if exist:
			sql_expect = '''SELECT expect FROM search WHERE keyword="{0}"'''.format(keyword)
			try:
				self.c.execute(sql_expect)
				e_expect = self.c.fetchone()[0]
			 
			except Exception as e:
				self.ret['status'] = 0
				self.ret['msg'] = '设置关键词失败'
			
			sql_update = '''UPDATE search SET expect={0} WHERE keyword="{1}"'''.format(expect+e_expect,keyword)
			try:
				self.c.execute(sql_update)
				self.conn.commit()
				self.ret['status'] = 2
				self.ret['data'] = expect+e_expect
				self.ret['id'] = exist
			except Exception as e:
				self.ret['status'] = 0
				self.ret['msg'] = '关键词设置失败'
			return self.ret
		else:
			sql = '''
			INSERT INTO search (keyword,expect) VALUES ("{0}",{1})'''.format(keyword,expect)
			sql_id = '''select last_insert_rowid()'''
			try:
				self.c.execute(sql)
				self.conn.commit()
				self.ret['status'] = 1
				self.ret['msg'] = '关键词增加成功'
				self.c.execute(sql_id)
				self.ret['id'] = self.c.fetchone()[0]
				self.ret['data'] = expect
			except Exception as e:
				self.ret['status'] = 0
				self.ret['msg'] = '关键词增加失败'
			return self.ret
	def get_keywords(self):
		'''
		获取关键词信息
		:return:
		'''
		sql = '''SELECT ID,keyword,times,expect FROM search'''
		try:
			self.c.execute(sql)
			self.ret['data'] = self.c.fetchall()
			self.ret['status'] = 1
		except Exception as e:
			self.ret['status'] = 0
			self.ret['msg'] = '关键词获取失败'
			self.ret['data'] = []
		return self.ret
	def delete_keyword(self,id):
		'''
		删除关键词
		:param id:
		:return:
		'''
		sql = '''DELETE FROM search WHERE ID={0}'''.format(id)
		try:
			self.c.execute(sql)
			self.conn.commit()
			self.ret['status'] = 1
	
		except Exception as e:
			self.ret['status'] = 0
			self.ret['msg'] = '删除错误'
		return self.ret
	def get_search_task(self):
		'''
		获取需要搜索的关键词信息
		:return:
		'''
		sql = '''SELECT ID,keyword,times,expect FROM search WHERE expect>0'''
		try:
			self.c.execute(sql)
			self.ret['data'] = self.c.fetchone()
			self.ret['status'] = 1
		except Exception as e:
			self.ret['status'] = 0
			self.ret['msg'] = '获取关键词错误'
		return self.ret
	def update_search(self,id,expect,times):
		'''
		:param id: 需要更改的次数的id
		:param expect: 需要更改的次数
		:return:
		'''
		sql = '''UPDATE search SET  expect={0},times={1} WHERE ID={2}'''.format(expect,times,id)
		try:
		
			self.c.execute(sql)
			self.conn.commit()
			self.ret['status'] = 1
		except Exception :
			self.ret['status'] = 0
			self.ret['msg'] = '设置执行次数出错'
		return self.ret
	def change_status(self,id,status):
		'''
		更改关键词执行状态，1是没有在执行，2是正在执行
		:param id:需要更改的关键词的id
		:return:
		'''
		sql = '''UPDATE search SET status={0} WHERE id={1}'''.format(status,id)
		try:
			self.c.execute(sql)
			self.conn.commit()
			self.ret['status'] = 1
		except Exception :
			self.ret['status'] = 0
			self.ret['msg'] = '设置状态失败'
		return self.ret
	def get_searching(self):
		'''
		获取正在执行搜索的关键词的信息
		:return:
		'''
		sql = '''SELECT keyword,expect,ID,times FROM search WHERE status = 2'''
		try:
			self.c.execute(sql)
			self.ret['data'] = self.c.fetchone()
			if not self.ret['data']:
				self.ret['data'] = []
			self.ret['status'] = 1
		except Exception:
			self.ret['status'] = 0
			self.ret['msg'] = '获取正在搜索数据失败'
		return self.ret
	def set_vote_tasks(self,name,desc,url,account):
		check_sql = '''SELECT url FROM vote WHERE account ="{0}"'''.format(account)
		urls = []
		try:
			self.c.execute(check_sql)
			urls = self.c.fetchall()
		except Exception as e:
			pass
		if urls:
			urls = [x[0] for x in urls]
		if url not in urls:
			sql = '''INSERT INTO vote (name,desc, url, status, account) VALUES ("{0}","{1}","{2}",0,"{3}")'''.format(name,desc,url,account)
			try:
				self.c.execute(sql)
				self.conn.commit()
				self.ret['status'] = 1
			except Exception as e:
				self.ret['status'] = 0
		return self.ret
	def get_vote_tasks(self,name):
		sql = '''
		SELECT ID,name,desc,url,account FROM vote WHERE name="{0}" AND status=0'''.format(name)
		try:
			self.c.execute(sql)
			url_list = self.c.fetchall()
			self.ret['status'] = 1
			self.ret['data'] = url_list
		except Exception as e:
			self.ret['status'] = 0
			self.ret['data'] = []
		return self.ret
	def del_vote_task(self,account,url):
		sql = '''
		UPDATE vote SET status = 3 WHERE account="{0}" AND url="{1}"'''.format(account,url)
		try:
			self.c.execute(sql)
			self.conn.commit()
			self.ret['status'] = 1
		except Exception :
			self.ret['status'] = 0
		return self.ret
	def get_vote_task(self):
		sql = '''SELECT ID,name,url,account FROM vote WHERE status=0'''
		try:
			self.c.execute(sql)
			data = self.c.fetchone()
			if data :
				self.ret['status'] = 1
				self.ret['data'] = data
			else:
				self.ret['status'] = 0
		except Exception:
			self.ret['status'] = 0
		return self.ret
	def get_vote_task_list(self,status):
		sql = '''SELECT desc,url,account FROM vote WHERE status={0}'''.format(status)
		data = []
		try:
			self.c.execute(sql)
			data = self.c.fetchall()
			
		except Exception :
			pass
		return data
	def check_vote_tasks(self,name,url):
		sql = '''SELECT COUNT(ID) FROM vote WHERE name="{0}" AND url="{1}"'''.format(name,url)
		try:
			self.c.execute(sql)
			data = self.c.fetchone()[0]
			self.ret['status'] = 1
			self.ret['data'] = data
		except Exception as e:
			self.ret['status'] = 0
			self.ret['data'] = 0
		return self.ret
	def  update_vote_task(self,id,status):
		sql = '''UPDATE vote SET status={0} WHERE id={1}'''.format(status,id)
		try:
			self.c.execute(sql)
			self.conn.commit()
			self.ret['status'] = 1
		except Exception :
			self.ret['status'] = 0
		return self.ret
	def del_e_votes(self):
		sql = '''UPDATE vote SET status=3 WHERE status=2'''
		try:
			self.c.execute(sql)
			self.conn.commit()
			self.ret['status'] = 1
		except Exception :
			self.ret['status'] = 0
		return self.ret
	def del_all_vote_task(self):
		today = datetime.datetime.now().date()
		date_count = datetime.timedelta(days=10)
		start_date = today - date_count
		sql = '''DELETE FROM vote WHERE status = 3 AND excute_time<"{0}"'''.format(start_date)
		try:
			self.c.execute(sql)
			self.conn.commit()
			self.ret['status'] = 1
		except Exception:
			self.ret['status'] = 0
		return self.ret
	
	def close(self):
		'''关闭连接'''
		try:
			self.c.close()
			self.conn.close()
		except Exception :
			pass

