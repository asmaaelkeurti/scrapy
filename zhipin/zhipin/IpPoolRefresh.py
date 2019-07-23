import requests
import time


class Ip_Refresh:
    def __init__(self):
        pass

    def refresh(self):
        time.sleep(2)
        while True:
            response = requests.get(
                "http://http.tiqu.alicdns.com/getip3?num=1&type=1&pro=&city=0&yys=0&port=1&pack=58752&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions=&gm=4")
            with open("ip_pool", 'w') as f:
                if len(response.content.decode("utf-8")) < 25:
                    f.write(response.content.decode("utf-8"))
                    print('refresh')
                    return
                else:
                    time.sleep(2)

    def record_job_page(self, url):
        with open("job_page_url", 'w') as f:
            f.write(url)
        print('url_stored')

    def read_job_page(self):
        with open("job_page_url", 'r') as f:
            url = f.read()
        return url


if __name__ == '__main__':
    Ip_Refresh().refresh()


