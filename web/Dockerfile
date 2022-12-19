FROM node:17-alpine
# 設置項目目錄
WORKDIR /app
# 安裝項目依賴
COPY package.json .
COPY package-lock.json .
RUN npm install
# 運行
CMD ["npm", "run", "dev"]
