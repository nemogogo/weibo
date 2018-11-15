from flask import Flask, render_template, request, json, redirect

app = Flask(__name__)
from handler import db_op
import config
from handler import utils
from handler.pre_driver import init_driver_data
import threading
from handler import task_schedule
from vote import vote_blue
app.config.from_object(config)  # 使用模块的名字
app.register_blueprint(vote_blue,url_prefix="/vote")



@app.route('/del_tasks', methods=['GET'])
def del_tasks():
	'''
	清除尝试转发10次以上不成功的转发数据
	:return:
	'''
	op = db_op.W_DB()
	ret = op.del_task()
	if ret['status'] == 1:
		return redirect('/')
	else:
		return '清除任务错误'


@app.route('/delete_keyword', methods=['GET'])
def delete_keyword():
	'''
	删除需要搜索的关键词
	:return:
	'''
	id = request.args.get('id')
	op = db_op.W_DB()
	ret = op.delete_keyword(id)
	op.close()
	return json.jsonify(ret)


@app.route('/set_comment', methods=['GET'])
def set_comment():
	'''
	设置是否评论
	:return:
	'''
	ret = utils.set_settings('comment')
	return json.jsonify(ret)


@app.route('/search', methods=['GET'])
def search():
	'''
	返回搜索页面
	:return:
	'''
	op = db_op.W_DB()
	keywords = op.get_keywords()['data']
	visible = utils.get_visible()
	user_code = utils.get_user_code()

	grade = int(utils.get_grade(user_code)['data'])

	op.close()
	return render_template('search.html', grade=grade,user_code=user_code,keywords=keywords, visible=visible)


@app.route('/add_keyword', methods=['GET'])
def add_keyword():
	'''
	添加关键词
	:return:
	'''
	content = request.args.get('content')
	expect = int(request.args.get('expect'))
	if content and expect:
		op = db_op.W_DB()
		ret = op.add_keyword(content, expect)
	else:
		ret = {'status': 0, 'msg': '没有数据'}
	
	return json.jsonify(ret)


@app.route('/get_searching', methods=['GET'])
def get_searching():
	'''
	获取正在搜索的关键词信息
	:return:
	'''
	op = db_op.W_DB()
	ret = op.get_searching()
	return json.jsonify(ret)


@app.route('/set_visible', methods=['GET'])
def set_visible():
	'''
	设置搜索是否可见
	:return:
	'''
	ret = utils.set_visible()
	return json.jsonify(ret)



 
	
@app.route('/', methods=['GET', 'POST'])
def index():
	'''
	返回首页
	:return:
	'''
	data = ''
	op = db_op.W_DB()
	user_code = utils.get_user_code()
	grade = int(utils.get_grade(user_code)['data'])
	interval = utils.get_interval()
	visible = utils.get_settings('t_visible')
	comment = utils.get_settings('comment')
	account_list = op.get_accounts()['data']
	yes_list = op.get_yes_tasks()['data']
	data_list = []
	total_count = 0
	for account in account_list:
		fo_today = op.get_record_count('forward', 0, account)['data']
		fo_yes = op.get_record_count('forward', 1, account)['data']
		fo_all = op.get_all_tasks_count('forward', account)['data']
		fo_week = op.get_sect_count('forward', 1, 7, account)['data']
		data_list.append((account, fo_yes, fo_week, fo_all, fo_today))
		total_count += fo_today
	task_count = op.get_untask_count()['data']
	error_tasks = op.get_error_tasks()['data']
	
	return render_template('index.html', address=request.form.get('weibo_info'), interval=interval, comment=comment,
	                       data_list=data_list, task_count=task_count, error_tasks=error_tasks, yes_list=yes_list,
	                       total_count=total_count > 5,grade=grade,
	                       account_list=account_list, back=data, visible=visible, user_code=user_code)


@app.route('/foward', methods=['POST'])
def forward():
	'''
	提交需要转发的url，content
	:return: 返回提交状态
	'''
	op = db_op.W_DB()
	url = request.form.get('fo_url').replace('comment', 'repost')
	contents = request.form.get('fo_content')
	accounts = request.form.get('accounts')
	forward_list = utils.cut_string(contents)
	account_list = utils.cut_string(accounts)
	content_list = set(forward_list)
	ret = {'status': 1, 'msg': '任务存储完毕'}
	if content_list and account_list and url:
		for content in content_list:
			if account_list:
				for account in account_list:
					if len(content) > 140:
						content = content[:139]
					ret = op.set_task(url, content, 0, account)
		ret['data'] = len(content_list)
	
	else:
		ret['status'] = 0
		ret['msg'] = '任务提交失败'
	return json.jsonify(ret)


@app.route('/login', methods=['GET'])
def login():
	'''
	验证用户码，返回是否验证成功
	:return:
	'''
	code = request.args.get('code')
	ret = utils.verify(code)
	if ret['status'] == 1:
		ret = utils.set_user_code(code)
	return json.jsonify(ret)


@app.route('/add_account', methods=['POST'])
def add_account():
	'''
	添加微博账号
	:return:
	'''
	op = db_op.W_DB()
	user = request.form.get('user')
	passwd = request.form.get('passwd')
	ret = op.add_account(user, passwd)
	if ret['status'] == 1:
		ret = init_driver_data(user)
		if ret['status'] == 0:
			op.del_account(user)
	
	return json.jsonify(ret)


@app.route('/set_interval', methods=['GET'])
def set_interval():
	'''
	设置微博转发频率，中间间隔分钟数
	:return:
	'''
	ret = {'status': 1}
	try:
		interval = int(request.args.get('interval'))
	except Exception:
		ret['status'] = 0
		ret['status'] = '参数错误'
	ret = utils.set_interval(interval)
	return json.jsonify(ret)


@app.route('/get_task_count', methods=['GET'])
def get_task_count():
	'''
	实时获取正在等待转发的微博数量
	:return:
	'''
	op = db_op.W_DB()
	task_count = op.get_untask_count()
	return json.jsonify(task_count)


@app.route('/del_account', methods=['GET'])
def del_account():
	'''
	删除账号
	:return:
	'''
	op = db_op.W_DB()
	user = request.args.get('user')
	ret = op.del_account(user)
	op.del_forward_by_account(user)
	op.close()
	return json.jsonify(ret)


@app.route('/set_t_visible', methods=['GET'])
def set_t_visible():
	'''设置转发模式
	:return:
	'''
	ret = utils.set_settings('t_visible')
	return json.jsonify(ret)




#threads = []
#threading.Thread(target=app.run, args=('run_with_reloader'))

if __name__ == '__main__':
	t = threading.Thread(target=app.run, )
	t.start()
	t2 = threading.Thread(target=task_schedule.run, )
	t2.start()
