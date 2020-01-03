FROM python:3.6-alpine

EXPOSE 5000

RUN pip install Flask mysql-connector feedgen
RUN apt install -y git
RUN git clone https://github.com/aleksas/patent-feed.git

WORKDIR /patent-feed/app

CMD python app.py
