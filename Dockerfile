FROM python:3.6-alpine
MAINTAINER Jorge Salamero <bencer@cauterized.net>
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
