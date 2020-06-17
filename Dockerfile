FROM python:3-alpine

RUN set -x && apk add --no-cache gcc musl-dev libxml2-dev libxslt-dev

WORKDIR /data

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "./wozzwo.py"]
CMD ["--help"]
