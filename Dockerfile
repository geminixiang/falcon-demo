FROM python:3.10.2-alpine as base
FROM base as builder

RUN apk add libffi-dev gcc musl-dev make

COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install --user -r /requirements.txt

FROM base
COPY --from=builder /root/.local /root/.local

COPY . /workspace/
WORKDIR /workspace/

EXPOSE 8000
