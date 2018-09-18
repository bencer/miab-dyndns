# miab-dyndns
A damn simple DynDNS for Mail-in-a-Box.

Since I didn't want to put my Mail-in-a-Box administrator password across a few boxes that require DynDNS, I had my dog to write this damn simple DynDNS proxy, with no defensive code whatsoever, using Flask and HAproxy.

The DynDNS service will receive requests from any box to update a DNS record given in the URL with the client public IP address. Clients can do this using `curl` (in your crontab for example):

```
*/15 * * * * curl -X POST -n https://casi.cauterized.net:5443/update/cauterized.net/home
```

while storing credentials on a `.netrc` file:

```
machine your-miab-dyndns-server
  login your-user-for-this-host
  password your-password
```

You can create different authentication credentials for different DNS records in `config.py`:

```
URL = 'https://box.domain.tld/admin/'
USER = ''
PASSWD = ';
AUTH = { 'test.domain.tld': {'username':'admin', 'password':'secret'}}
```

As you might guess, the `URL`, `USER` and `PASSWD` are your Mail-in-a-Box endpoint and administrator credentials.

To run the service, you just need Docker installed:

```
docker build -t miab-dyndns:latest .
docker run -d --restart always -v $(pwd)/config.py:/app/config.py:ro --name miab-dyndns miab-dyndns
docker run -d --restart always -p 5443:5443 -v $(pwd)/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro -v /home/user-data/ssl/combined.pem:/combined.pem:ro --link miab-dyndns:dyndns --name haproxy haproxy:1.8
```

