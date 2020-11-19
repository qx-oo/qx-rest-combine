import time
import requests


if __name__ == "__main__":
    req_data = {
        "request_list": [
            {
                "path": "/api/category/",
                "method": "post",
                "data": {
                    "name": "123"
                }
            },
            {
                "path": "/api/category/?page=2",
                "method": "get"
            },
            {
                "path": "/api/category/?page=1",
                "method": "get"
            },
            {
                "path": "/api/category/?page=2",
                "method": "get"
            },
        ]
    }
    start = time.time()
    resp = requests.post(
        'http://127.0.0.1:9000/api/resource/?test=10', json=req_data)
    secs = round(time.time() - start, 3)
    ret = resp.json()
    print("request 1, {}:".format(secs))
    print(ret)
    req_data = {
        "request_list": [
            {
                "path": "/api/category/{}/".format(ret['data'][0]['id']),
                "method": "get"
            },
        ]
    }
    start = time.time()
    resp = requests.post('http://127.0.0.1:9000/api/resource/', json=req_data)
    secs = round(time.time() - start, 3)
    ret = resp.json()
    print()
    print("request 2, {}:".format(secs))
    print(ret)

    start = time.time()
    resp = requests.get('http://127.0.0.1:9000/api/category/test/')
    secs = round(time.time() - start, 3)
    ret = resp.json()
    print()
    print("request 3, {}:".format(secs))
    print(ret)
