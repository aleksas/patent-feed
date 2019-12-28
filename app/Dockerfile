FROM python:3.6

EXPOSE 5000

WORKDIR /app

#COPY requirements.txt /app
ADD . /app
RUN pip install -r requirements.txt

#COPY app.py /app
#COPY channels.py /app
#COPY templates /app/templates
CMD python app.py
