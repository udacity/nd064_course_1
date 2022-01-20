# Go Hello World

This is a simple Go web application that prints a "Hello World" message.

### Step 0. [Optional] Run the application locally
You should have [Go installed](https://go.dev/doc/install) in your local machine if you want to run the applicatiion locally. This application listens on port `6111`. To run the application, use the following command:
```
go run main.go 
```

Access the application on: http://127.0.0.1:6111/

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
# Access the application on: http://127.0.0.1:6111/ or http://localhost:6111/ or http://0.0.0.0:6111/

# tag the image
docker tag go-helloworld pixelpotato/go-helloworld:v1.0.0

# login into DockerHub
docker login

# push the image
docker push pixelpotato/go-helloworld:v1.0.0
```

### Step 3. Deploy to Kubernetes:
```
# Shortcut method to run the application with headless pods
kubectl run test --image pixelpotato/go-helloworld:v1.0.0
# Another way to deploy the application
kubectl create deploy go-helloworld --image=pixelpotato/go-helloworld:v1.0.0
# Display the pod name
kubectl get pods
# Copy the pod name from the output above
# Access the application on the local host
kubectl port-forward pod/go-helloworld-fcd468f98-rsj7p 6111:6111
```
Access the application in the local machine on http://192.168.50.4:6111/ or http://127.0.0.1:6111/ 
