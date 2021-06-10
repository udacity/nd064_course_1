FROM golang:alpine

WORKDIR /go/src/app
ADD . .
RUN go mod init
RUN go build -o helloworld
RUN go mod tidy

EXPOSE 6111
CMD ["./helloworld"]
