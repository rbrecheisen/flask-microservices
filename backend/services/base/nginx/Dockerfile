FROM ubuntu:14.04

MAINTAINER Ralph Brecheisen <ralph.brecheisen@gmail.com>

ENV NGINX_VERSION 1.10.1
ENV LD_LIBRARY_PATH /usr/local/lib

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y build-essential autoconf openssl libssl-dev \
    libpcre3 libpcre3-dev zlib1g zlib1g-dev wget git curl dnsutils \
    && mkdir -p /tmp/src \
	&& cd /tmp/src \
    && git clone http://luajit.org/git/luajit-2.0.git \
    && cd luajit-2.0 \
    && make \
    && make install \
    && cd .. \
    && wget http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz \
    && tar -zxf nginx-${NGINX_VERSION}.tar.gz \
    && rm nginx-${NGINX_VERSION}.tar.gz \
    && git clone https://github.com/simpl/ngx_devel_kit.git \
    && git clone https://github.com/openresty/lua-nginx-module.git \
    && wget https://github.com/openresty/set-misc-nginx-module/archive/v0.28.tar.gz -O set-misc-nginx-module.tar.gz \
    && mkdir set-misc-nginx-module \
    && tar -zxf set-misc-nginx-module.tar.gz -C set-misc-nginx-module --strip-components=1 \
    && cd nginx-${NGINX_VERSION} \
    && ./configure --prefix=/usr/local/nginx \
            --with-http_gzip_static_module \
            --with-http_ssl_module \
            --with-http_stub_status_module \
    		--with-http_auth_request_module \
            --http-log-path=/var/log/nginx/access.log \
            --error-log-path=/var/log/nginx/error.log \
            --sbin-path=/usr/local/sbin/nginx \
            --add-module=../ngx_devel_kit \
            --add-module=../lua-nginx-module \
            --add-module=../set-misc-nginx-module \
    && make \
    && make install \
    && cd .. \
    && mkdir -p /usr/local/nginx/modules \
	&& ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log \
	&& rm -rf /tmp/src

EXPOSE 80 443

CMD ["nginx"]