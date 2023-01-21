A small tool for sending files under 2 GB. You can take the necessary data (api_id, api_hash) from my.telegram.org. To set up the right packets:

```
$ pip3 install -r requirements.txt
```

To start:

```
$ python3 -m uvicorn main:app
```