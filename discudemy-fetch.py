import requests, re, sys
if len(sys.argv) != 3:
	print("Usage: python udemy.py <url/id> <pagebypage/atonce>\n")
	print("url = output format is URL with coupon parameter - better for sharing")
	print("id = output format: id|coupon - probably better for using with bots\n")
	print("pagebypage = fetch from discudemy.com slower, page by page.")
	print("atonce = fetch from discudemy.com quicker, but sometimes it won't work")
	exit()
	
geturl = sys.argv[1] == "url"
def processpage(num):
	data = requests.get("https://www.discudemy.com/language/english/"+str(num)).text
	contents = re.findall(re.compile('<section class="card">((.|\n)*?)<div class="extra content">', re.MULTILINE), data)
	for content in contents:
		content = content[0]
		courseid = content.split('https://udemy-images.udemy.com/course/')[1].split('"')[0].split('/')[-1].split('_')[0]
		coupon = ""
		if geturl or 'line-through' in content:
			link = content.split('"card-header" href="')[1].split('"')[0]
			details = requests.get(link.replace('/English/', '/go/')).text
			url = "https://www.udemy.com/" + details.split('<a  href="https://www.udemy.com/')[1].split('" target="_blank">')[0]
			if("\n" in url or len(url) > 200):
				continue
			if "couponCode" in url:
				coupon = url.split('couponCode=')[1].split('&')[0]
		
		f = open("udemy_free.txt", "a")
		if geturl:
			f.write(url + "\n")
		else:
			f.write(courseid + "|" + coupon + "\n")
		f.close()
	return 999
#	return re.sub(r"\s+", '', data).split('">»</a></li></div>')[0].split('</a></li><li><ahref="https://www.discudemy.com/all/')[0].split('>')[1]

if sys.argv[2] == "atonce":
	processpage(0)
else:
	lastpage = processpage(1)
	for i in range(1, lastpage + 1):
		processpage(i)
