// autoscaling/http-app/main.go
package main

import (
	"fmt"
	"net/http"
<<<<<<< HEAD
	"strconv"
	"sync"
=======

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
>>>>>>> 9e1c5f3443bf2670bf9dd853a428fb42fda5e4e5
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

func stressCPU(w http.ResponseWriter, r *http.Request) {
	// Parse query parameter for number of goroutines
	threadsStr := r.URL.Query().Get("threads")
	threads, err := strconv.Atoi(threadsStr)
	if err != nil || threads <= 0 {
		threads = 4 // default number of threads
	}

	var wg sync.WaitGroup
	for i := 0; i < threads; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			// Busy loop to consume CPU
			for {
			}
		}()
	}
	wg.Wait()
}

func stressMemory(w http.ResponseWriter, r *http.Request) {
	// Parse query parameter for memory usage in MB
	mbStr := r.URL.Query().Get("mb")
	mb, err := strconv.Atoi(mbStr)
	if err != nil || mb <= 0 {
		mb = 100 // default memory usage
	}

	// Allocate memory
	var mem [][]byte
	for i := 0; i < mb; i++ {
		mem = append(mem, make([]byte, 1024*1024)) // 1MB per iteration
	}
	fmt.Fprintf(w, "Allocated %d MB of memory\n", mb)
}

func main() {
<<<<<<< HEAD
	fmt.Println("Starting server on port 8080")
	http.HandleFunc("/", handler)
	http.HandleFunc("/stress/cpu", stressCPU)
	http.HandleFunc("/stress/memory", stressMemory)
	http.ListenAndServe(":8080", nil)
=======
	// HTTP handlers
	http.Handle("/metrics", promhttp.Handler()) // Prometheus metrics endpoint
	http.HandleFunc("/", handler)               // Default application endpoint

	// Start the HTTP server
	fmt.Println("Starting server on :8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		fmt.Printf("Error starting server: %v\n", err)
	}
>>>>>>> 9e1c5f3443bf2670bf9dd853a428fb42fda5e4e5
}
