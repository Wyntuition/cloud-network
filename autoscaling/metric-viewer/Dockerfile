# Use an official Golang runtime as a parent image
FROM golang:1.23 AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy the Go module files
COPY go.mod ./

# Copy the source code
COPY *.go ./

# Build the Go app
RUN CGO_ENABLED=0 GOOS=linux go build -o metrics-viewer

FROM alpine:3.18
WORKDIR /app
COPY --from=builder /app/metrics-viewer .
EXPOSE 8080
CMD ["./metrics-viewer"]