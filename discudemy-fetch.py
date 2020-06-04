import requests, re, sys
# python3 udemy.py https://www.discudemy.com/language/English/ 0 0
if len(sys.argv) == 1:
        print("Usage: python udemy.py baseurl [saveid] [quick]\n")
        print("baseurl: discudemy URL without page number (example: https://www.discudemy.com/language/english/ )\n")
        print("saveid: 1 if you want to use with autobuy script")
        print("quick: 1 if you want to quick scrape all\n")
        print("")
        exit()


baseurl = sys.argv[1]
saveid = len(sys.argv) > 2 and sys.argv[2] == "1"
quick = len(sys.argv) > 3 and sys.argv[3] == "1"
# quick mode sets page to 0, and all courses are shown at the same page

if not baseurl.endswith("/"):
        baseurl += "/"

f = open("udemy_free.txt","a")

page = 0 if quick else 1
while True:
        resp = requests.get(baseurl + str(page)).text
        courses = resp.split('<section class="card">')[1:]

        for course in courses:
                if "adsbygoogle" in course:
                        continue
                url = course.split('href="')[1].split('"')[0]
                title = course.split('href="')[1].split('">')[1].split('</')[0]
                cid = course.split('responsive" src="')[1].split('">')[0].split('/')[-1].split('_')[0]

                gourl = url.split('/')
                gourl[-2] = "go"
                goresp = requests.get('/'.join(gourl)).text
                courseurl = goresp.split('Course Coupon:')[1].split('">')[1].split('</')[0]
                coupon = "N/A"
                try:
                        coupon = courseurl.split('?couponCode=')[1]
                except:
                        pass

                print("writing to udemy_free.txt : "+title)
                if saveid:
                        if coupon == "N/A":
                                continue
                        f.write("{}|{}\n".format(cid, coupon))
                else:
                        f.write(courseurl+"\n")

                f.flush()

        if "<li>" not in resp.split('pagination3')[1].split('</div>')[0].split(' class="active"')[1]:
                exit()

        if quick:
                break

        page += 1

f.close()
