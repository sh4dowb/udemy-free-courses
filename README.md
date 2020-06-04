# udemy-free-courses

discudemy.com scraper & a list of free Udemy courses.<br>
Many thanks to discudemy.com.<br>


usage:
```
python3 discudemy-fetch.py discudemy-url [writeid] [quick]

# discudemy-url: example: https://www.discudemy.com/language/english/
# writeid: write id|coupon instead of URLs to use with autobuy script
# quick: faster scrape from discudemy
```


example:
```
python3 discudemy-fetch.py https://www.discudemy.com/language/english/ 0 1
# writes urls to udemy_free.txt
```

```
python3 discudemy-fetch.py https://www.discudemy.com/language/english/ 1 1
# writes id|coupon to udemy_free.txt
```
then edit JS file with the contents of udemy_free.txt, go to udemy.com and run the script on js console (F12)
