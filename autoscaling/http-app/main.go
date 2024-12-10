package main

import (
	"fmt"
	"net/http"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

var (
	// Counter for total HTTP requests
	requestsTotal = prometheus.NewCounter(prometheus.CounterOpts{
		Name: "http_requests_total",
		Help: "Total number of HTTP requests received",
	})

	// Histogram for HTTP request durations
	requestDuration = prometheus.NewHistogram(prometheus.HistogramOpts{
		Name:    "http_request_duration_seconds",
		Help:    "Histogram of HTTP request durations in seconds",
		Buckets: prometheus.DefBuckets, // Default buckets: 0.005, 0.01, ..., 10 seconds
	})
)

func init() {
	// Register Prometheus metrics
	prometheus.MustRegister(requestsTotal)
	prometheus.MustRegister(requestDuration)
}

func handler(w http.ResponseWriter, r *http.Request) {
	// Increment the counter for total requests
	requestsTotal.Inc()

	// Measure the duration of the handler execution
	timer := prometheus.NewTimer(requestDuration)
	defer timer.ObserveDuration()

	fmt.Fprintln(w, "Hello, Kubernetes Autoscaling!")
}

func main() {
	// HTTP handlers
	http.Handle("/metrics", promhttp.Handler()) // Prometheus metrics endpoint
	http.HandleFunc("/", handler)               // Default application endpoint

	// Start the HTTP server
	fmt.Println("Starting server on :8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		fmt.Printf("Error starting server: %v\n", err)
	}
}
