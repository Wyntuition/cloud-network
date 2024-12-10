# Use an official Golang runtime as a parent image
FROM golang:1.23 AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy the Go module files
COPY go.mod go.sum ./

# Download dependencies (ensures go.mod and go.sum are up-to-date)
RUN go mod download

# Copy the source code
COPY *.go ./

# Build the Go app
RUN CGO_ENABLED=0 GOOS=linux go build -o http-app

# Use a lightweight image for runtime
FROM alpine:3.18
WORKDIR /app
COPY --from=builder /app/http-app .
EXPOSE 8080
CMD ["./http-app"]
