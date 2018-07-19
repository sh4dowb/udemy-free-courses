import requests, re
data = requests.get("https://www.discudemy.com/language/english/0").text
datas = re.findall(r"<a class=\"cardHeader\" href=\"(.*?)\">", data)
for link in datas:
    details = requests.get(link.replace('/english/', '/go/')).text
    url = "https://www.udemy.com/" + details.split('<a  href="https://www.udemy.com/')[1].split('"')[0]
    if(len(url) > 75):
        continue
    f = open("udemy_free.txt", "a")
    f.write(url + "\n")
    f.close()
