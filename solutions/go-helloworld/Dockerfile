FROM golang:alpine

WORKDIR /go/src/app

ADD . .

# import dependencies and build the app
# RUN  go mod init && go build -o helloworld
# Another method:
RUN go env -w GO111MODULE=auto
RUN go build  -o helloworld

EXPOSE 6111

CMD ["./helloworld"]

