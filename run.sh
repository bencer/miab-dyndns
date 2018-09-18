docker kill miab-dyndns
docker rm miab-dyndns
docker kill haproxy
docker rm haproxy
docker build -t miab-dyndns:latest .
docker run -d --restart always -v $(pwd)/config.py:/app/config.py:ro --name miab-dyndns miab-dyndns
docker run -d --restart always -p 5443:5443 -v $(pwd)/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro -v /home/user-data/ssl/combined.pem:/combined.pem:ro --link miab-dyndns:dyndns --name haproxy haproxy:1.8
