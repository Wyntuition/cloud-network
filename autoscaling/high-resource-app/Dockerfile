# Use an official Golang runtime as a parent image
FROM golang:1.23 as builder

# Set the working directory inside the container
WORKDIR /app

# Copy the Go module files and download dependencies
COPY go.mod ./
RUN go mod download

# Copy the source code
COPY . .

# Build the Go app
RUN go build -o high-resource-app

# Use a minimal base image for the final container
FROM alpine:3.18

# Set the working directory inside the container
WORKDIR /app

# Copy the binary from the builder stage
COPY --from=builder /app/high-resource-app .

# Expose a port (optional, if the app needs to serve HTTP or metrics)
EXPOSE 8080

# Set the command to run the app
CMD ["./high-resource-app"]
