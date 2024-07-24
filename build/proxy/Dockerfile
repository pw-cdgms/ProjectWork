FROM nginx:latest

RUN mkdir /etc/nginx/ssl && \
    apt-get update && apt-get install -y openssl && \
    openssl req -x509 -newkey rsa:4096 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt -days 365 -nodes -subj "/C=IT/ST=Emilia-Romagna/L=Bologna/O=Nginx/CN=localhost"

COPY nginx.conf /etc/nginx/conf.d/nginx.conf

EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]
