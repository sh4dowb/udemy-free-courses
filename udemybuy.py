import requests, threading, time, traceback
from multiprocessing import Queue
q = Queue()

bearer = ".."
cookies = """..."""
def buy(queue):
	global bearer
	global cookies
	while not queue.empty():
		data = queue.get().split('|')
		if data[1] != "":
			#Temporarily disabled, because Udemy will request captcha if this is requested too frequently.
			#Adding to cart, then mass buying it won't work also, because Udemy requires you to visit course page first for CSRF thing. (https://www.udemy.com/courseidhere)
			continue
			courseid = data[0]
			coupon = data[1]
			print(courseid)
			s = requests.session()
			headers = {
				'authorization': 'Bearer '+bearer,
				'accept-encoding': 'gzip, deflate, br',
				'accept-language': 'en-US,en;q=0.9',
				'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
				'x-udemy-authorization': 'Bearer '+bearer,
				'accept': 'application/json, text/plain, */*',
				'authority': 'www.udemy.com',
				'x-requested-with': 'XMLHttpRequest',
			}
			try:
				print(s.get('https://www.udemy.com/api-2.0/course-landing-components/'+courseid+'/me/?couponCode='+coupon+'&components=redeem_coupon', headers=headers).text)
			except:
				traceback.print_exc()
				exit()
			
			#headers = {
			#	'accept': 'application/json, text/plain, */*',
			#	'accept-encoding': 'gzip, deflate, br',
			#	'accept-language': 'en-US,en;q=0.9',
			#	'authority': 'www.udemy.com',
			#	'authorization': 'Bearer *****',
			#	'cache-control': 'max-age=0',
			#	'content-type': 'application/json;charset=UTF-8',
			#	'origin': 'https://www.udemy.com',
			#	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
			#	'x-requested-with': 'XMLHttpRequest',
			#	'x-udemy-authorization': 'Bearer ***',
			#}

			#data = '{"buyables":[{"buyable_object_type":"course","id":'+courseid+',"buyable_context":{}}]}'

			#print(s.post('https://www.udemy.com/api-2.0/shopping-carts/me/cart/', headers=headers, data=data).text)
			data = '{"shopping_cart":{"items":[{"discountInfo":{"code":"'+coupon+'"},"buyableType":"course","buyableId":'+courseid+',"purchasePrice":{"price_string":"Free","currency_symbol":"\\u20ba","currency":"TRY","amount":0}}]}}'
			print(requests.post('https://www.udemy.com/payment/shopping-cart-submit/', headers=headers, data=data).text)
		else:
			headers = {
				'authority': 'www.udemy.com',
				'upgrade-insecure-requests': '1',
				'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
				'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
				'referer': 'https://www.udemy.com/katalon-studio-step-by-step-for-beginners/',
				'accept-encoding': 'gzip, deflate, br',
				'accept-language': 'en-US,en;q=0.9',
				'cookie': cookies
			}
			resp = requests.get('https://www.udemy.com/course/subscribe/?courseId='+data[0], headers=headers).text
			if "automation tools" in resp:
				print("Captcha required! " + str(data[0]))
				exit()

datalist = requests.get("https://cagriari.com/udemy_free.txt?nocache").text.split("\n")
for data in datalist:
	q.put(data)

for i in range(0, 10):
	worker = threading.Thread(target=buy, args=(q,))
	worker.setDaemon(True)
	worker.start()