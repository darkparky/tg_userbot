FROM python:3.7.4-alpine3.9

ENV PATH="/app/bin:$PATH"
WORKDIR /app

RUN apk add git ffmpeg libpq git bash redis curl sudo neofetch neofetch libxml2 libwebp-dev libffi-dev openssl-dev musl-dev gcc libxslt-dev libxml2-dev zlib zlib-dev libjpeg libjpeg-turbo-dev linux-headers jq pv

COPY . ./
RUN pip install -r ./requirements.txt

CMD ["bash","./init/start.sh"]
