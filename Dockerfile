FROM python:alpine3.12

RUN addgroup -S sectools && adduser -S app-user -G sectools
RUN apk add python3
RUN apk add --update py3-pip

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt

USER app-user
COPY . /home/app-user/pythonapp
WORKDIR /home/app-user/pythonapp

ENTRYPOINT [ "python3" ]

CMD [ "webapp.py" ]