FROM python:3.4

LABEL maintainer="test@test.denice"

RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi
RUN pip install Flask==0.10.1 uWSGI requests redis==2.10.3
WORKDIR /app
COPY app /app

EXPOSE 9090 9191
USER uwsgi

COPY cmd.sh /

CMD ["/cmd.sh"]
