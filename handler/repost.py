from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

from handler.pre_driver import pre_cookies,init_driver_data


def forward(url, content, user, c,visible):
	"""
	:param url: 需要转发的地址
	:param content: 需要转发的内容
	:param user:使用的账号
	:param c:是否需要同时评论
	:return:
	"""
	ret = {
		'status': 1,
		'msg': 'ok'
	}
	if url.find('type') != -1:
		url = url.replace('comment', 'repost')
		url = url.replace('like','repost')
	else:
		if url.find('?') == -1:
			url += '?type=repost'
		else:
			url += '&type=repost'
	try:
		options = pre_cookies(user,visible)
		driver = webdriver.Chrome(chrome_options=options)
		driver.get(url)
	except Exception:
		ret['status'] = 0
		ret['msg'] = '浏览器启动错误'
		return ret
	
	wait = WebDriverWait(driver, 10)
	try:
		login = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#pl_common_top > div > div > div.gn_position > div.gn_login > ul > li:nth-child(3) > a')))
		if login.text == '登录':
			driver.quit()
			ret['status'] = 0
			ret['msg'] = '未登录'
			return ret
	except Exception:
		pass
	
	try:
		re_text = wait.until(EC.presence_of_element_located(
			(By.CSS_SELECTOR, 'div > div > div > div > div > div.p_input.p_textarea > textarea')))
	except Exception as e:
		ret['status'] = 0
		ret['msg'] = '元素定位不成功'
		driver.quit()
		return ret
	time.sleep(5)
	# print('here text',re_text.text())
	if re_text.text == 'undefined':
		re_text.clear()
	re_text.send_keys(content)
	if c:
		time.sleep(2)
		try:
			comment_btn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
			                                                           'div > div > div '
			                                                           '> div:nth-child(5) > div > div:nth-child(2) > '
			                                                           'div > div > div > div > div > '
			                                                           'div.p_opt.clearfix > div.opt.clearfix > ul > '
			                                                           'li > label')))
			 
			comment_btn.click()
		except Exception as e:
				print(e)
	try:
		re_btn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
		                                                      'div > div > div > div:nth-child(5) > div > '
		                                                      'div:nth-child(2) > div > div > div > div > div > '
		                                                      'div.p_opt.clearfix > div.btn.W_fr > a')))
		re_btn.click()
		time.sleep(5)
	except Exception as e:
		ret['status'] = 0
		ret['msg'] = '转发错误'
		driver.quit()
		return ret
	
	ret['status'] = 1
	ret['msg'] = '转发ok'
	driver.quit()
	return ret




def m_trans(url, content, user,visible):
	'''
	移动端转发
	:param url: 转发网址
	:param content: 转发内容
	:param user: 转发账号
	:return: 回复时候成功
	'''
	ret = {
		'status': 1,
		'msg': 'ok'
	}
	print(url, content)
	text = content
	base_url = 'https://m.weibo.cn/compose/repost?id=%s'
	url1 = base_url % (url.split('/')[-1],)
	try:
		options = pre_cookies(user,visible)
		driver = webdriver.Chrome(chrome_options=options)
		driver.get(url)
	except Exception:
		ret['status'] = 0
		ret['msg'] = '浏览器启动错误'
		return ret
	wait = WebDriverWait(driver, 20)
	try:
		click_first = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
		                                                         '#app > div.lite-page-wrap > div > '
		                                                         'div.lite-page-editor > div > '
		                                                         'div.box-right.m-box-center-a > '
		                                                         'i.lite-iconf.lite-iconf-report')))
		click_first.click()
		re_text = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
		                                                     '#app > div.m-wrapper.m-wbox > div > main > '
		                                                     'div.m-box-model.m-pos-r > div > span > '
		                                                     'textarea:nth-child(1)')))
		text1 = ''
		re_text.send_keys(text)
	except Exception as e:
		ret['status'] = 0
		ret['msg'] = '网页元素定位错误'
		driver.close()
		return ret
	while True:
		if driver.current_url != url1:
			driver.back()
			start = text.find('#') + 1
			text = text[start:]
			if text.count('#') <= 1:
				text1 = text
			else:
				index1 = text.find('#') + 1
				end = text.find('#', index1) + 1
				text1 = text[:end]
				text = text[end - 1:]
				time.sleep(3)
		re_text.send_keys(text1)
		if text.count('#') <= 1:
			if driver.current_url != url1:
				driver.back()
			break
	time.sleep(4)
	try:
		check_comment = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
		                                                           '#app > div.m-wrapper.m-wbox > div > footer > '
		                                                           'div.m-fcb-col.m-fd-row.m-box-model > label > '
		                                                           'input[type="checkbox"]')))
		time.sleep(3)
		check_comment.click()
		time.sleep(3)
		re_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
		                                                    '#app > div.m-wrapper.m-wbox > div > header > '
		                                                    'div.m-box.m-flex-grow1.m-box-model.m-fd-row.m-aln-center.m-justify-end.m-flex-base0 > a')))
		re_btn.click()
		ret['status'] = 1
		ret['msg'] = '成功发送'
		driver.close()
	except Exception as e:
		ret['status'] = 0
		ret['msg'] = '网页元素定位错误'
		driver.close()
	return ret

def search(text, headless=False):
	'''
	:param text: 搜索关键词
	:param headless: 是否有界面,true代表可见
	:return: 返回是否搜索成功
	'''
	options = webdriver.ChromeOptions()
	if not headless:
		options.add_argument('--headless')
	url = 'https://s.weibo.com/'
	ret = {'status': 1}
	try:
		driver = webdriver.Chrome(chrome_options=options)
		driver.get(url)
		wait = WebDriverWait(driver, 20)
	except Exception as e:
		ret['status'] = 0
		return ret
	try:
		text_input = wait.until(EC.presence_of_element_located(
			(By.CSS_SELECTOR, '#pl_homepage_search > div > div.searchbox > div > input[type="text"]')))
		text_input.send_keys(text)
	except Exception:
		ret['status'] = 0
		ret['msg'] = '元素定位错误'
		driver.quit()
		return ret
	try:
		search_btn = wait.until(EC.presence_of_element_located((
			By.CSS_SELECTOR,'#pl_homepage_search > div > div.searchbox > button'
		)))
		search_btn.click()
	except Exception as e:
		ret['status'] = 0
		ret['msg'] ='网页元素定位错误'
		driver.quit()
		
		return ret
	height = 10000
	p = 1
	while p<8:
		try:
			driver.execute_script("window.scrollTo(0,%s)" % height)
			next_page = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#pl_feedlist_index > div.m-page > div > a')))
			if p>1:
				next_page = wait.until(
					EC.presence_of_element_located((By.CSS_SELECTOR, '#pl_feedlist_index > div.m-page > div > a.next')))
			time.sleep(5)
			next_page.click()
			p += 1
		except Exception as e:
			if height < 50000:
				height += 2000
			else:
				driver.quit()
				ret['status'] = 0
				return ret
			time.sleep(5)
	driver.quit()
	return ret
	
def vote(name,url,account,visible=False):
	url = url.replace('com','cn')
	ret = {'status':1}
	try:
		options = pre_cookies(account, visible)
		driver = webdriver.Chrome(chrome_options=options)
		driver.get(url)
	except Exception:
		ret['status'] = 0
		ret['msg'] = '浏览器启动错误'
		return ret
	
	wait = WebDriverWait(driver, 20)
	time.sleep(3)
	try:
		submit = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.btnA')))
		if submit.text == '已结束':
			ret['status'] = 0
			driver.close()
			driver.quit()
			return ret
		if submit.text == '已投票':
			ret['status'] = 1
			driver.close()
			driver.quit()
			return ret
	except Exception as e:
		pass
	try:
		vote_text = driver.find_elements_by_css_selector('.mct-a')
		driver.execute_script("window.scrollTo(0,%s)" % 10000)
	except Exception as e:
		ret['status'] = 0
		return ret
	# print(dir(vote_text))
	flag = True
	for vote in vote_text:
		if vote.text == name:
			vote.click()
			flag = False       #判断选项中是否有要投票的名字
			time.sleep(2)
		
	try:
		submit = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.btnA')))
		submit.click()
	except Exception as e:
		ret['status']= 0
	if flag:
		ret['status'] = 0
	time.sleep(5)
	driver.quit()
	return ret

