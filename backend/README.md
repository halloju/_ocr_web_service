# 目錄結構
```
.
├── Dockerfile(API service image)
├── app(主程式目錄)
│   ├── exceptions.py(自訂義 exceptions)
│   ├── main.py(API entrypoint)
│   ├── models(ORM models)
│   │   ├── login_hist.py
│   │   ├── register.py
│   ├── routers(API routing)
│   │   ├── db.py
│   │   ├── docs.py
│   │   ├── login.py
│   │   ├── register.py
│   ├── schema(資料格式封裝)
│   │   ├── common.py
│   │   └── users.py
│   ├── services(DB 資料存取，可以自行新增)
│   └── static(靜態檔案)
│       ├── css
│       │   └── swagger-ui.css
│       ├── images
│       │   └── esun.png
│       └── js
│           ├── redoc.standalone.js
│           └── swagger-ui-bundle.js
└── requirements.txt
└── requirements-text.txt
```

# 本機起服務
```
1. docker-compose up - d
2. 在瀏覽器網址輸入 localhost: 5000/docs 開啟 API 文件
```

# Components
* 查看各個服務元件
```
docker ps - a
```
* nginx(web server)
* if_cdp_backend(API server)
* redis(API cache server)
* postgres(Database)

# 連進 DB 查看方式
```
1. docker exec - it postgres / bin/sh
2. psql - U postgres
```

# 單元測試
* pip install requirements-test.txt
```
python3 - m pytest - -cov = . / --cov-report = html
```
打開 htmlcov 資料夾，可參考下列 test case coverage

# kafka
```sh
kafka-topics - -bootstrap-server broker: 9092 \
             - -create \
             - -topic if_gp_ocr.gp_callback
```

# reid
```sh
redis-cli - -scan | head - 10
```
