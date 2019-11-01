FROM python:3.7.4-alpine3.9

ENV PATH="/app/bin:$PATH"
ENV GRPC_PYTHON_VERSION 1.15.0

CMD ["bash","./init/start.sh"]

WORKDIR /app

RUN apk --no-cache add ffmpeg libpq bash redis curl sudo neofetch neofetch jq pv git libxml2 libwebp-dev libffi-dev openssl-dev musl-dev gcc g++ libxslt-dev libxml2-dev zlib zlib-dev libjpeg libjpeg-turbo-dev linux-headers
RUN python -m pip install --upgrade pip setuptools

COPY requirements.txt ./

RUN pip install -r ./requirements.txt

COPY . ./
