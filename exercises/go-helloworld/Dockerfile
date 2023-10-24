FROM golang:alpine

WORKDIR /go/src/app

ADD . .

RUN go mod init && go build -o helloworld

EXPOSE 6112

CMD ["./helloworld"]
