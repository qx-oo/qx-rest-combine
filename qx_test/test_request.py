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
        ]
    }
    resp = requests.post(
        'http://127.0.0.1:9000/api/resource/?test=10', json=req_data)
    ret = resp.json()
    print("request 1:")
    print(ret)
    req_data = {
        "request_list": [
            {
                "path": "/api/category/{}/".format(ret['data'][0]['id']),
                "method": "get"
            },
        ]
    }
    resp = requests.post('http://127.0.0.1:9000/api/resource/', json=req_data)
    ret = resp.json()
    print()
    print("request 2:")
    print(ret)
