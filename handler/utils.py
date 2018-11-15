import random
import json
import os
import urllib3
import json
from config import BASE_DIR

user_agent = [
	"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 "
	"Safari/534.50",
	"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
	"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
	"Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; "
	".NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
	"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
	"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
	"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
	"Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
	"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
	"Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 "
	"Safari/535.11",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR "
	"2.0.50727; SE 2.X MetaSr 1.0)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
	"Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) "
	"Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
	"Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) "
	"Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
	"Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 "
	"Mobile/8J2 Safari/6533.18.5",
	"Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) "
	"Version/4.0 Mobile Safari/533.1",
	"MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 ("
	"KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
	"Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
	"Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 "
	"Safari/534.13",
	"Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile "
	"Safari/534.1+",
	"Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 "
	"Safari/534.6 TouchPad/1.0",
	"Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) "
	"AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
	"Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
	"UCWEB7.0.2.37/28/999",
	"NOKIA5700/ UCWEB7.0.2.37/28/999",
	"Openwave/ UCWEB7.0.2.37/28/999",
	"Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
	# iPhone 6：
	"Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 "
	"Mobile/10A5376e Safari/8536.25",

]
agent = random.choice(user_agent)


def cut_string(contents):
	if contents:
		content_list = contents.split('  ')
		string_list = []
		for content in content_list:
			new_content = content.strip(' ')
			if new_content:
				string_list.append(new_content)
		return string_list
	else:
		return []


def set_user_code(code):
	ret = {'status': 1}
	try:
		with open(os.path.join(BASE_DIR, 'db', "settings.json"), "r") as f:
			dict1 = json.load(f)
	except Exception:
		ret['status'] = 0
		ret['msg'] = '读取数据错误'
		return ret
	dict1['user_code'] = code
	
	try:
		with open(os.path.join(BASE_DIR, 'db', "settings.json"), "w") as f:
			json.dump(dict1, f)
	
	except Exception:
		ret['status'] = 0
		ret['msg'] = '设置数据错误'
	return ret


def set_interval(interval):
	ret = {'status': 1}
	try:
		with open(os.path.join(BASE_DIR, 'db', "settings.json"), "r") as f:
			dict1 = json.load(f)
	except Exception:
		ret['status'] = 0
		ret['msg'] = '读取数据错误'
		return ret
	dict1['interval'] = interval
	try:
		with open(os.path.join(BASE_DIR, 'db', "settings.json"), "w") as f:
			json.dump(dict1, f)
	except Exception:
		ret['status'] = 0
		
		ret['msg'] = '设置数据错误'
	return ret


def set_visible():
	ret = {'status': 1}
	try:
		with open(os.path.join(BASE_DIR, 'db', "settings.json"), "r") as f:
			dict1 = json.load(f)
	except Exception:
		ret['status'] = 0
		ret['msg'] = '读取数据错误'
		return ret
	if dict1['visible']:
		dict1['visible'] = False
		ret['data'] = False
	else:
		dict1['visible'] = True
		ret['data'] = True
	try:
		with open(os.path.join(BASE_DIR, 'db', "settings.json"), "w") as f:
			json.dump(dict1, f)
	except Exception:
		ret['status'] = 0
		ret['msg'] = '设置数据错误'
	return ret


def get_visible():
	visible = False
	try:
		with open(os.path.join(BASE_DIR, 'db', "settings.json"), "r") as f:
			dict1 = json.load(f)
		visible = dict1['visible']
	except Exception:
		pass
	return visible


def get_interval():
	interval = 2
	try:
		with open(os.path.join(BASE_DIR, 'db', "settings.json"), "r") as f:
			dict1 = json.load(f)
		interval = dict1['interval']
	except Exception:
		pass
	return interval


def get_user_code():
	code = ''
	try:
		with open(os.path.join(BASE_DIR, 'db', "settings.json"), "r") as f:
			dict1 = json.load(f)
		code = dict1['user_code']
	except Exception as e:
		pass
	return code


def get_settings(para):
	ret = True
	try:
		with open(os.path.join(BASE_DIR, 'db', "settings.json"), "r") as f:
			dict1 = json.load(f)
		ret = dict1[para]
	except Exception as e:
		pass
	return ret


def set_settings(para):
	ret = {'status': 1}
	try:
		with open(os.path.join(BASE_DIR, 'db', "settings.json"), "r") as f:
			dict1 = json.load(f)
	except Exception:
		ret['status'] = 0
		ret['msg'] = '读取数据错误'
		return ret
	if dict1[para]:
		dict1[para] = False
		ret['data'] = False
	else:
		dict1[para] = True
		ret['data'] = True
	try:
		with open(os.path.join(BASE_DIR, 'db', "settings.json"), "w") as f:
			json.dump(dict1, f)
	except Exception:
		ret['status'] = 0
		ret['msg'] = '设置数据错误'
	return ret


def verify(code):
	
	ret = {'status': 1}
	url = 'http://www.girlsfootprint.com/verify'
	http = urllib3.PoolManager()
	try:
		ret = http.request('GET', url, fields={'code': code})
		print(ret.status)
		ret = json.loads(ret.data.decode('utf-8'))
	except Exception:
		ret['status'] = 0
		ret['msg'] = '验证错误'
	return ret


def get_votes(name):
	
	ret = {'status': 1}
	url = 'http://www.girlsfootprint.com/vote'
	http = urllib3.PoolManager()
	try:
		ret1 = http.request('GET', url, fields={'name': name})
		ret = json.loads(ret1.data.decode('utf-8'))
	except Exception:
		ret['status'] = 0
		ret['msg'] = '获取错误'
		ret['data'] =None
	return ret


def set_votes(name, url,desc):
	import urllib3
	import json
	ret = {'status': 1}
	address = 'http://www.girlsfootprint.com/vote'
	http = urllib3.PoolManager()
	try:
		ret1 = http.request('POST', address, fields={'name': name, 'url': url,'desc':desc})
		ret = json.loads(ret1.data)
	except Exception:
		ret['status'] = 0
		ret['msg'] = '设置错误'
	return ret

 
def get_artists():
	artists = []
	try:
		with open(os.path.join(BASE_DIR, 'db', "settings.json"), "r") as f:
			dict1 = json.load(f)
		artists = dict1['artists']
	except Exception:
		pass
	return artists


def add_artists(a):
	ret = {'status': 1}
	try:
		with open(os.path.join(BASE_DIR, 'db', "settings.json"), "r") as f:
			dict1 = json.load(f)
		if a in dict1['artists']:
			ret['status'] = 2
		else:
			dict1['artists'].append(a)
	
	except Exception:
		ret['status'] = 0
		ret['msg'] = '读取数据错误'
	try:
		with open(os.path.join(BASE_DIR, 'db', "settings.json"), "w") as f:
			json.dump(dict1, f)
	except Exception:
		ret['status'] = 0
		ret['msg'] = '设置数据错误'
	return ret


def del_artists(a):
	ret = {'status': 1}
	try:
		with open(os.path.join(BASE_DIR, 'db', "settings.json"), "r") as f:
			dict1 = json.load(f)
		dict1['artists'].remove(a)
	except Exception:
		ret['status'] = 0
		ret['msg'] = '读取数据错误'
	try:
		with open(os.path.join(BASE_DIR, 'db', "settings.json"), "w") as f:
			json.dump(dict1, f)
	except Exception:
		ret['status'] = 0
		ret['msg'] = '设置数据错误'
	return ret

def get_grade(code):
	url = 'http://www.girlsfootprint.com/get_account'
	http = urllib3.PoolManager()
	ret = {}
	try:
		ret1 = http.request('GET', url, fields={'code':code })
		ret = json.loads(ret1.data.decode('utf-8'))
	except Exception:
		ret['status'] = 0
		ret['msg'] = '获取错误'
	return ret
 
def get_poster():
	ret = {'status': 1}
	url = 'http://www.girlsfootprint.com/get_post'
	http = urllib3.PoolManager()
	try:
		ret1 = http.request('GET', url)
		ret = json.loads(ret1.data.decode('utf-8'))
	except Exception:
		ret['status'] = 0
	return ret
 
