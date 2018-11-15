from selenium import webdriver
from config import BASE_DIR
import os
import time
from handler.db_op import W_DB as DB
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
options = webdriver.ChromeOptions()


def add_account(user, passwd):
	'''
	添加微博账号
	:param user:
	:param passwd:
	:return:
	'''
	db = DB()
	sql = '''
	INSERT INTO account(user,passwd)
VALUES ({0},{1});'''.format(user, passwd)
	db.c.execute(sql)
	db.conn.commit()
	db.close()


def get_account(user):
	'''
	获取账号信息
	:param user:
	:return:
	'''
	db = DB()
	ret = {'status': 1}
	sql = '''SELECT user,passwd FROM account WHERE user="{0}"'''.format(user)
	try:
		db.c.execute(sql)
		data = db.c.fetchone()
		db.conn.commit()
		db.close()
		ret['data'] = data
	except Exception:
		ret['data'] = None
		ret['status'] = 0
	return ret


def get_dir(user):
	'''
	获取用户的cookies文件夹
	:param user:
	:return:
	'''
	user_dir = os.path.join(BASE_DIR, 'cookies', user)
	if not os.path.exists(user_dir):
		os.mkdir(user_dir)
	return user_dir

def pre_cookies(user, visible=True):
	'''
	获取用户的cookies
	:param user:用户名
	:param visible:是否可见
	:return:
	'''
	user_dir = get_dir(user)
	options = webdriver.ChromeOptions()
	prefs = {
		'profile.default_content_setting_values':
			{
				'notifications': 2
			}
	}
	options.add_experimental_option('prefs', prefs)
	options.add_argument("user-data-dir=" + user_dir)
	if not visible:
		options.add_argument('--headless')
	return options


def login(options, user, passwd):
	'''
	登录微博
	:param options:用户的cookies文件夹
	:param user: 用户名
	:param passwd: 密码
	:return:
	'''
	ret = {'status': 1, 'msg': '登陆成功'}
	try:
		driver = webdriver.Chrome(chrome_options=options)
		driver.get('https://weibo.com/')
	except Exception as e:
		ret['status'] = 0
		ret['msg'] = '浏览器启动失败'
		driver.quit()
		return ret
	
	wait = WebDriverWait(driver, 10)
	try:
		login_name = wait.until(EC.visibility_of_element_located((By.ID, 'loginname')))
		login_name.send_keys(user)
	except Exception as e:
		ret['status'] = 0
		driver.quit()
		return ret
	try:
		password = wait.until(EC.visibility_of_element_located(
			(By.CSS_SELECTOR, '#pl_login_form > div > div:nth-child(3) > div.info_list.password > div > input')))
		password.send_keys(passwd)
	except Exception as e:
		ret['status'] = 0
		ret['data'] = '元素定位不成功'
		driver.quit()
		return ret
	time.sleep(1)
	try:
		btn = wait.until(EC.element_to_be_clickable(
			(By.CSS_SELECTOR, '#pl_login_form > div > div:nth-child(3) > div.info_list.login_btn > a')))
		btn.click()
		time.sleep(20)
	except Exception as e:
		ret['status'] = 0
		ret['data'] = '元素定位不成功'
		driver.quit()
		return ret

	driver.close()
	driver.quit()
	return ret

def init_driver_data(user, visible=True):
	'''
	初始化用户
	:param user:用户名
	:param visible:是否可见
	:return:
	'''
	options = pre_cookies(user,visible)
	account = get_account(user)
	if account['data']:
		account = account['data']
		ret = login(options, *account)
	else:
		ret = {'status':0}
	return ret

