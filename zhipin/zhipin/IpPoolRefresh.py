import requests


class Ip_Refresh:
    def __init__(self):
        pass

    def refresh(self):
        response = requests.get(
            "http://http.tiqu.alicdns.com/getip3?num=1&type=1&pro=&city=0&yys=0&port=1&pack=57299&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions=&gm=4")
        with open("ip_pool", 'w') as f:
            f.write(response.content.decode("utf-8"))
        print('refresh')


if __name__ == '__main__':
    Ip_Refresh().refresh()

