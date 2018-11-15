from . import vote_blue
from flask import Flask, render_template, request, json, redirect
from handler import utils
from handler import db_op


@vote_blue.route('/add_artist')
def add_artist():
	ret = {'status': 1}
	name = request.args.get('name')
	ret = utils.add_artists(name)
	return json.jsonify(ret)


@vote_blue.route('/del_artist')
def del_artist():
	ret = {'status': 1}
	name = request.args.get('name')
	ret = utils.del_artists(name)
	return json.jsonify(ret)


@vote_blue.route('/', methods=['GET', 'POST'])
def vote():
	'''
	返回首页
	:return:
	'''
	visible = utils.get_settings('v_visible')
	user_code = utils.get_user_code()
	grade = int(utils.get_grade(user_code)['data'])
	artists = utils.get_artists()
	vote_list = []
	op = db_op.W_DB()
	account_list = op.get_accounts()['data']
	error_tasks = op.get_vote_task_list(2)
	f_tasks = op.get_vote_task_list(1)
	poster = None
	for artist in artists:
		a_list = op.get_vote_tasks(artist)['data']
		vote_list.append((artist, a_list))
	poster_result = utils.get_poster()
	if poster_result['status'] == 1:
		if poster_result['data']:
			poster = poster_result['data']
	op.close()
	

	return render_template('vote.html', user_code=user_code, vote_list=vote_list,visible=visible,
	                       account_list=account_list,error_tasks=error_tasks,f_tasks=f_tasks,
	                       grade=grade,poster=poster)


@vote_blue.route('/add', methods=['POST'])
def add():
	
	try:
		name = request.form.get('name')
		url = request.form.get('url').split('?')[0]
		desc = request.form.get('desc')
	except Exception :
		ret = {'status': 4, 'msg': '提交数据错误'}
		return json.jsonify(ret)
	
	user_code = utils.get_user_code()
	account_check = utils.get_grade(user_code)
	if account_check['status'] == 0:
		return json.jsonify(account_check)
	else:
		
		if account_check['data'] == '1':
			ret = {'status': 0,'msg':'等级不够添加'}
		else:
			op = db_op.W_DB()
			check_task = op.check_vote_tasks(name, url)
			if check_task['data'] == 0:
				ret = utils.set_votes(name, url, desc)
			else:
				ret = {'status':3,'msg':'此条投票已存在'}
			op.close()
		return json.jsonify(ret)

@vote_blue.route('/set_visible', methods=['GET'])
def set_visible():
	ret = utils.set_settings('v_visible')
	return  json.jsonify(ret)
@vote_blue.route('/update', methods=['GET', 'POST'])
def update():
	'''
	更新未投票的
	:return:
	'''
	ret = {'status': 1}
	artists = utils.get_artists()
	account_list = utils.cut_string(request.args.get('accounts', ''))
	op = db_op.W_DB()
	for account in account_list:
		for artist in artists:
			ret = utils.get_votes(artist)
			url_list = ret['data']
			if url_list:
				for url in url_list:
					ret = op.set_vote_tasks(url[0], url[1],url[2],account)
	op.close()
	return json.jsonify(ret)
@vote_blue.route('/del_task', methods=['GET', 'POST'])
def del_task():
	ret = {'status':1}
	account = request.form.get('account')
	url = request.form.get('url')
	op = db_op.W_DB()
	ret = op.del_vote_task(account,url)
	op.close()
	return json.jsonify(ret)

@vote_blue.route('/del_e_task', methods=[ 'POST'])
def del_e_task():
	op = db_op.W_DB()
	ret = op.del_e_votes()
	op.close()
	return json.jsonify(ret)