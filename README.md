# if_gp_ocr_system
玉山 OCR 系統

## Roles
| 角色  | 成員 |
| ------------- | ------------- |
| PM  | 李立晟 |
| PG  |  何信賢、林莞筑、王逸庭 |
| TL  | 蔡根元 |

## 安裝 Docker Engine
[Link](https://www.docker.com/products/docker-desktop/)

## 本機起服務
```
1. docker-composer up -d
2. 在瀏覽器網址輸入 localhost:5000/docs 開啟 API 文件
3. 在瀏覽器網址輸入 localhost 可查看網頁
```
## Components
* 查看各個服務元件
```
docker ps -a
```
* nginx (web server)
* backend (API server)
* frontend (web)

## Frontend
![image](https://user-images.githubusercontent.com/40282726/189018870-bb41aea1-6385-474c-9900-a31a97611a1b.png)

## Backend
![image](https://user-images.githubusercontent.com/40282726/189018899-cec8398f-1762-4421-9de9-e39d564d0ac1.png)
