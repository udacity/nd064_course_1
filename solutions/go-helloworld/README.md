### Step 1. Get the Dockerfile ready
```
# use the golang:alpine base image
FROM golang:alpine

# set the working directory to /go/src/app
WORKDIR /go/src/app

# copy all the files from the current directory to the container working directory
ADD . .

# import dependencies using `go mod init` and build the application using `go build -o helloworld` command
RUN  go mod init && go build -o helloworld

# expose the port 6111
EXPOSE 6111

# start the container
CMD ["./helloworld"]
```

### Step 2. Package the application
Steps to package the application using Docker commands:

``` 
# build the image
docker build -t go-helloworld .

# run the image
docker run -d -p 6111:6111 go-helloworld

# tag the image
docker tag go-helloworld pixelpotato/go-helloworld:v1.0.0

# push the image
docker push pixelpotato/go-helloworld:v1.0.0

# login into DockerHub
docker login
```

### Step 3. Deploy to Kubernetes:
```
# run the application
kubectl run test --image pixelpotato/go-helloworld:v1.0.0

# access the application on the local host
kubectl port-forward test-97856cf4-6fvjw 7111:6111
```
