import re
def task_filter(x): 
	para = re.findall("\?([^?]*)?",x)
	#switch (keyWord)
	sp = para[0].split('=')
	keyWord = sp[0]
	numBer  = sp[1]

	w2l = {
		'pinpai':'b',
		'region':'c',
		'catid':'f'
	}
	return {"url": 'http://www.lingshi.com/list/' + w2l[keyWord] + numBer +'.htm'} 
