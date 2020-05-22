FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip3 install -r requirements.txt
COPY . /code/
RUN python manage.py collectstatic --noinput
CMD contact_trace.asgi:application --port $PORT --bind 0.0.0.0 -v2