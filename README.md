# 智能 OCR 系統

## Roles
| 角色 | 成員 |
| ------------- | ------------- |
| PM  | 李立晟 |
| PG (Frontend) | 何信賢、林莞筑 |
| PG (Backend) | 王逸庭、張晏誠 |
| Team Lead | 蔡根元、李杰恩 |
| Tech Lead | 劉軒彤 |

## 安裝 Docker Engine
[Link](https://www.docker.com/products/docker-desktop/)

## 本機起服務
```
1. docker-compose up -d
2. 在瀏覽器網址輸入 localhost:5000/docs 開啟 API 文件
3. 在瀏覽器網址輸入 localhost 可查看網頁
```
## Components
* 查看各個服務元件
```
docker ps -a
```

* 查看錯誤訊息
```
docker logs -f backend
```

* 停止服務
```
docker-compose stop
```

* 重啟 image (有更新到 image / db init setting)
```
docker-compose down
docker-compose build --no-cache
```

* nginx (web server)
* backend (API server)
* frontend (web)

## Frontend
![image]()

## Backend
![image]()

## Minio
URL:http://localhost:9001/

![image](https://user-images.githubusercontent.com/40282726/193745456-221492ef-7a20-4276-8697-39e7c284485a.png)

