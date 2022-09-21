# production environment
FROM nginx:1.15-alpine

COPY nginx.conf /etc/nginx/conf.d

CMD ["nginx", "-g", "daemon off;"]