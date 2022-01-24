FROM golang:alpine

WORKDIR /go/src/app

ADD . .

# import dependencies and build the app
RUN  go mod init && go build -o helloworld

EXPOSE 6111

CMD ["./helloworld"]

