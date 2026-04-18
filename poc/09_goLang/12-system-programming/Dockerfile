FROM golang:1.22-alpine

RUN apk add --no-cache strace gcc musl-dev

WORKDIR /app
COPY . .

# 의존성 다운로드
RUN go mod download

CMD ["sh"]
