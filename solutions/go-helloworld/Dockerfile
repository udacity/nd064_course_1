FROM golang:alpine

WORKDIR /go/src/app

ADD . .

# If this error comes: "go: go.mod file not found in current directory or any parent directory; see 'go help modules'", then uncomment the below line.
#RUN go mod init

RUN go build  -o helloworld

EXPOSE 6111

CMD ["./helloworld"]

