FROM golang:alpine

WORKDIR /go/src/app

ADD . .

RUN go env -w GO111MODULE=auto
RUN go build  -o helloworld

EXPOSE 6111

CMD ["./helloworld"]

