FROM python:alpine3.12

RUN addgroup -S pywebapp && adduser -S app-user -G pywebapp
RUN apk add python3
RUN apk add --update py3-pip

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps
 
USER app-user
COPY . /home/app-user/pythonapp
WORKDIR /home/app-user/pythonapp

ENTRYPOINT [ "python3" ]
CMD [ "webapp.py" ]
