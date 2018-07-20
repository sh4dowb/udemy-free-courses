import requests, threading, time, traceback
from multiprocessing import Queue
q = Queue()

cookies = """..."""
csrftoken = "" # can be found in cookies
def buy(queue):
	global bearer
	global cookies
	i = 1
	checkoutdata = '{"shopping_cart":{"items":['
	while not queue.empty():
		data = queue.get().split('|')
		if data[1] != "":
			if i % 11 == 0:
				headers = {
					'Accept': 'application/json, text/plain, */*',
					'Referer': 'https://www.udemy.com/cart/checkout/',
					'Origin': 'https://www.udemy.com',
					'X-Requested-With': 'XMLHttpRequest',
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
					'X-CSRFToken': csrftoken,
					'Content-Type': 'application/json;charset=UTF-8',
					'cookie': cookies
				}

				print(requests.post('https://www.udemy.com/payment/shopping-cart-submit/', headers=headers, data=checkoutdata[:-1]+']}}').text)
			else:
				checkoutdata += '{"discountInfo":{"code":"'+data[1]+'"},"purchasePrice":{"amount":0,"currency":"TRY","price_string":"Free","currency_symbol":"\\u20ba"},"buyableType":"course","buyableId":'+data[0]+',"buyableContext":{}},'
			i += 1
		else:
			continue
			headers = {
				'Accept': 'application/json, text/plain, */*',
				'Referer': 'https://www.udemy.com/cart/checkout/',
				'Origin': 'https://www.udemy.com',
				'X-Requested-With': 'XMLHttpRequest',
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
				'Content-Type': 'application/json;charset=UTF-8',
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
