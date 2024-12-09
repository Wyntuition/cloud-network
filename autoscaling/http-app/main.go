package main

import (
	"fmt"
	"net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "Hello, Kubernetes Autoscaling!")
}

func main() {
	print("Starting server on port 8080")
	http.HandleFunc("/", handler)
	http.ListenAndServe(":8080", nil)
}
