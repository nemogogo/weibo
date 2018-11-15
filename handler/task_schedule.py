import datetime
import schedule
import threading
import time
from handler.db_op import W_DB
from handler import repost
from handler.pre_driver import init_driver_data
from handler.utils import get_interval,get_visible,get_settings
from handler.utils import set_settings


def trans():
	'''
	执行转发任务
	:return:
	'''
	op = W_DB()
	ret = op.get_task()
	op.close()
	if ret['status'] == 1:
		task_status = int(ret['data'][3])
		task_id = ret['data'][0]
		task_url = ret['data'][1]
		task_content = ret['data'][2]
		task_account = ret['data'][4]
		now_day = datetime.datetime.now().date()
		c = get_settings('comment')
		visible = get_settings('t_visible')
		if task_url.find('m.weibo') == -1:
			result = repost.forward(task_url,task_content,task_account,c,visible)
		else:
			result = repost.m_trans(task_url,task_content,task_account,visible)
		op = W_DB()
		if result['status'] == 1:
			if op.update_task(task_id,1,now_day)['status'] == 4:
				op.update_task(task_id, 1, now_day)['status']
			op.add_fo_record('forward',task_account)
		else:
			if task_status == 0:
				op.update_task(task_id,task_status+2,now_day)
			else:
				op.update_task(task_id,task_status+1,now_day)
			init_ret = init_driver_data(user=task_account,visible=True)
			if init_ret['status'] == 0:
				set_settings('t_visible')
		op.close()
	vote()
	
	

def search():
	'''
	执行搜索任务
	:return:
	'''
	time.sleep(2)
	op = W_DB()
	try:
		ret = op.get_search_task()
		if ret['status']==1:
			task= ret['data']
			id = task[0]
			keyword = task[1]
			times = task[2]
			expect = task[3]
			op.change_status(id,2)
			op.close()
			headless = get_visible()
			ret = repost.search(keyword,headless) #执行搜索任务
			if ret['status'] == 1:
				op = W_DB()
				op.update_search(id,expect-1,times+1)
				if expect-1 == 0:
					op.change_status(id,1)
				op.close()
	except Exception as e:
		pass
	

		
		
def vote():
	op = W_DB()
	get_task = op.get_vote_task()
	op.close()
	if get_task['status'] == 0:
		return
	else:
		vote_task = get_task['data']
		vote_id = vote_task[0]
		vote_name = vote_task[1]
		vote_url = vote_task[2]
		vote_account = vote_task[3]
		visible = get_settings('v_visible')
		op = W_DB()
		ret = repost.vote(vote_name,vote_url,vote_account,visible)
		if ret['status'] == 1:
			op.update_vote_task(vote_id,1)
			op.close()
		else:
			op.update_vote_task(vote_id,2)
			op.close()

def job1_task():
	threading.Thread(target=trans).start()


def job2_task():
	threading.Thread(target=search).start()

def run():
	trans()
	interval = get_interval()
	op = W_DB()
	op.delete_all_tasks()
	op.del_all_vote_task()
	op.close()
	schedule.every(interval*60).seconds.do(job1_task)
	schedule.every(60*2).seconds.do(job2_task)
	
	while True:
		schedule.run_pending()
		time.sleep(1)
