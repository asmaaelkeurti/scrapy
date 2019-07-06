import time
import requests


while True:
    response = requests.get("http://http.tiqu.alicdns.com/getip3?num=2&type=1&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4")
    with open("ip_pool", 'w') as f:
        f.write(response.content.decode("utf-8"))
    time.sleep(200)
    print('refresh')
