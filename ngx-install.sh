#!/bin/bash

# Set environment variables
APPNAME=uwsgi_server       # Name of the uWSGI Custom Application
APPPORT=14071              # Assigned port for the uWSGI Custom Application
PYTHON=python2.7           # Django python version
DJANGOAPP=baiadospiratas_test           # Django application name
DJANGOPROJECT=baia_dos_piratas    # Django project name

mkdir -p $HOME/webapps/$APPNAME/{bin,nginx,src,tmp}

cd $HOME/webapps/$APPNAME/src
wget 'https://github.com/pagespeed/ngx_pagespeed/archive/release-1.5.27.3-beta.zip'
mv release-1.5.27.3-beta release-1.5.27.3-beta.zip
unzip release-1.5.27.3-beta.zip
cd ngx_pagespeed-release-1.5.27.3-beta
wget 'https://dl.google.com/dl/page-speed/psol/1.5.27.3.tar.gz'
tar -xzf 1.5.27.3.tar.gz


###########################################################
# nginx 1.5.2
# original: http://nginx.org/download/nginx-1.5.2.tar.gz
###########################################################
cd $HOME/webapps/$APPNAME/src
wget 'http://nginx.org/download/nginx-1.5.2.tar.gz'
tar -xzf nginx-1.5.2.tar.gz
cd nginx-1.5.2
./configure \
  --add-module=$HOME/webapps/$APPNAME/src/ngx_pagespeed-release-1.5.27.3-beta \
  --prefix=$HOME/webapps/$APPNAME/nginx \
  --sbin-path=$HOME/webapps/$APPNAME/nginx/sbin/nginx \
  --conf-path=$HOME/webapps/$APPNAME/nginx/nginx.conf \
  --error-log-path=$HOME/webapps/$APPNAME/nginx/log/nginx/error.log \
  --pid-path=$HOME/webapps/$APPNAME/nginx/run/nginx/nginx.pid  \
  --lock-path=$HOME/webapps/$APPNAME/nginx/lock/nginx.lock \
  --with-http_flv_module \
  --with-http_gzip_static_module \
  --http-log-path=$HOME/webapps/$APPNAME/nginx/log/nginx/access.log \
  --http-client-body-temp-path=$HOME/webapps/$APPNAME/nginx/tmp/nginx/client/ \
  --http-proxy-temp-path=$HOME/webapps/$APPNAME/nginx/tmp/nginx/proxy/ \
  --http-fastcgi-temp-path=$HOME/webapps/$APPNAME/nginx/tmp/nginx/fcgi/
make && make install

###########################################################
# uwsgi 1.9.13
# original: http://projects.unbit.it/downloads/uwsgi-1.9.13.tar.gz
###########################################################
cd $HOME/webapps/$APPNAME/src
wget 'http://projects.unbit.it/downloads/uwsgi-1.9.13.tar.gz'
tar -xzf uwsgi-1.9.13.tar.gz
cd uwsgi-1.9.13
$PYTHON uwsgiconfig.py --build
mv ./uwsgi $HOME/webapps/$APPNAME/bin
ln -s $HOME/webapps/$APPNAME/nginx/sbin/nginx $HOME/webapps/$APPNAME/bin

mkdir -p $HOME/webapps/$APPNAME/nginx/tmp/nginx/client

cat << EOF > $HOME/webapps/$APPNAME/nginx/nginx.conf
worker_processes  1;

events {
    worker_connections  1024;
}

http {
    access_log  ${HOME}/logs/user/access_${APPNAME}.log combined;
    error_log   ${HOME}/logs/user/error_${APPNAME}.log  crit;

    include mime.types;
    sendfile on;

    pagespeed on;
    pagespeed FileCachePath ${HOME}/tmp/ngx_pagespeed_cache;

    pagespeed RewriteLevel PassThrough;
    pagespeed EnableFilters add_head,combine_css,convert_jpeg_to_progressive,convert_meta_tags,flatten_css_imports;
    pagespeed EnableFilters inline_css,inline_import_to_link;
    pagespeed EnableFilters rewrite_css,rewrite_images,rewrite_style_attributes_with_url;
    pagespeed EnableFilters insert_image_dimensions,remove_comments,collapse_whitespace;
    pagespeed EnableFilters remove_quotes,insert_dns_prefetch,trim_urls;
    pagespeed CustomFetchHeader Accept-Encoding gzip;

    gzip on;
    gzip_static on;
    gzip_http_version 1.1;
    gzip_vary on;
    gzip_comp_level 6;
    gzip_proxied any;
    gzip_types text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript;
    gzip_buffers 16 8k;
    gzip_disable "MSIE [1-6]\.(?!.*SV1)";

    server {
        listen 127.0.0.1:${APPPORT};

        location / {

            include uwsgi_params;
            uwsgi_pass unix://${HOME}/webapps/${APPNAME}/uwsgi.sock;

            location ~ "\.pagespeed\.([a-z]\.)?[a-z]{2}\.[^.]{10}\.[^.]+" { add_header "" ""; }
            location ~ "^/ngx_pagespeed_static/" { }
            location ~ "^/ngx_pagespeed_beacon$" { }
            location /ngx_pagespeed_statistics { allow 127.0.0.1; deny all; }
            location /ngx_pagespeed_message { allow 127.0.0.1; deny all; }

        }
    }
}
EOF

cat << EOF > $HOME/webapps/$APPNAME/wsgi.py
import sys, os

sys.path = ['${HOME}/webapps/${DJANGOAPP}/${DJANGOPROJECT}/${DJANGOPROJECT}',
            '${HOME}/webapps/${DJANGOAPP}/${DJANGOPROJECT}',
            '${HOME}/webapps/${DJANGOAPP}/lib/${PYTHON}',
           ] + sys.path

os.environ['DJANGO_SETTINGS_MODULE'] = '${DJANGOPROJECT}.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
EOF

# make the start, stop, and restart scripts
cat << EOF > $HOME/webapps/$APPNAME/bin/start
#!/bin/bash

APPNAME=${APPNAME}

# Start uwsgi
\${HOME}/webapps/\${APPNAME}/bin/uwsgi \\
  --uwsgi-socket "\${HOME}/webapps/\${APPNAME}/uwsgi.sock" \\
  --master \\
  --workers 1 \\
  --max-requests 10000 \\
  --harakiri 60 \\
  --daemonize \${HOME}/webapps/\${APPNAME}/uwsgi.log \\
  --pidfile \${HOME}/webapps/\${APPNAME}/uwsgi.pid \\
  --vacuum \\
  --python-path \${HOME}/webapps/\${APPNAME} \\
  --wsgi wsgi

# Start nginx
\${HOME}/webapps/\${APPNAME}/bin/nginx
EOF

cat << EOF > $HOME/webapps/$APPNAME/bin/stop
#!/bin/bash

APPNAME=${APPNAME}

# stop uwsgi
\${HOME}/webapps/\${APPNAME}/bin/uwsgi --stop \${HOME}/webapps/\${APPNAME}/uwsgi.pid

# stop nginx
kill \$(cat \${HOME}/webapps/\${APPNAME}/nginx/run/nginx/nginx.pid)
EOF

cat << EOF > $HOME/webapps/$APPNAME/bin/restart
#!/bin/bash

APPNAME=${APPNAME}

\${HOME}/webapps/\${APPNAME}/bin/stop
sleep 5
\${HOME}/webapps/\${APPNAME}/bin/start
EOF

chmod 755 $HOME/webapps/$APPNAME/bin/{start,stop,restart}