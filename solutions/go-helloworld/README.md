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
# change the Dockerhub username, as applicable to you, for e.g., sudkul/go-helloworld:v1.0.0
docker tag go-helloworld pixelpotato/go-helloworld:v1.0.0

# login into DockerHub
docker login

# push the image
docker push pixelpotato/go-helloworld:v1.0.0
```


### Step 3. Deploy to Kubernetes 
This step is relevant for the "Exercise: Deploy Your First Kubernetes Cluster". The commands below are supposed to be run *only* after you have run the commands above. 
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
