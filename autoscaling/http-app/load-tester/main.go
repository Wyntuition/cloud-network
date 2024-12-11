package main

import (
	"fmt"
	"net/http"
	"os"
	"strconv"
	"sync"
	"sync/atomic"
	"time"
)

// Fetch environment variable or return the default value
func getEnv(key string, defaultValue int) int {
	if value, err := strconv.Atoi(os.Getenv(key)); err == nil && value > 0 {
		return value
	}
	return defaultValue
}

// Worker function with controlled delay to throttle the rate
func worker(id int, url string, requestsPerWorker int, delay time.Duration, wg *sync.WaitGroup, counter *uint64) {
	defer wg.Done()
	for i := 0; i < requestsPerWorker; i++ {
		start := time.Now()
		resp, err := http.Get(url)
		if err != nil {
			// Only log errors to avoid overwhelming the console
			fmt.Printf("Worker %d: Error - %v\n", id, err)
			continue
		}
		resp.Body.Close()

		// Increment the counter for successful requests
		atomic.AddUint64(counter, 1)

		// Log only every 100th request to reduce clutter
		if i%100 == 0 {
			fmt.Printf("Worker %d: Processed %d requests.\n", id, i)
		}

		// Sleep for the calculated delay to maintain the target rate
		elapsed := time.Since(start)
		if delay > elapsed {
			time.Sleep(delay - elapsed)
		}
	}
}

// Periodically calculate and print the RPS
func monitorRPS(counter *uint64, duration time.Duration, stopChan chan bool) {
	ticker := time.NewTicker(duration)
	defer ticker.Stop()
	var lastCount uint64
	for {
		select {
		case <-ticker.C:
			// Calculate the number of requests since the last check
			currentCount := atomic.LoadUint64(counter)
			rps := float64(currentCount-lastCount) / duration.Seconds()
			lastCount = currentCount

			// Print RPS prominently
			fmt.Printf("\n*** Current RPS: %.2f ***\n", rps)
		case <-stopChan:
			return
		}
	}
}

func main() {
	// Configurable parameters with defaults
	url := os.Getenv("TARGET_URL")
	if url == "" {
		url = "http://http-app:8080"
	}
	workers := getEnv("WORKER_COUNT", 100)
	requestsPerWorker := getEnv("REQUESTS_PER_WORKER", 2000)
	targetRPS := getEnv("TARGET_RPS", 1000) // Set desired requests per second

	// Calculate delay per request based on the target RPS
	delayPerRequest := time.Second / time.Duration(targetRPS)

	fmt.Printf("Starting load test:\n - Target URL: %s\n - Workers: %d\n - Requests per worker: %d\n - Target RPS: %d\n", url, workers, requestsPerWorker, targetRPS)
	fmt.Printf("Calculated delay per request to maintain target RPS: %s\n", delayPerRequest)

	var wg sync.WaitGroup
	var successfulRequests uint64
	stopChan := make(chan bool)

	// Start monitoring RPS
	go monitorRPS(&successfulRequests, 1*time.Second, stopChan)

	// Start workers
	for i := 0; i < workers; i++ {
		wg.Add(1)
		go worker(i, url, requestsPerWorker, delayPerRequest, &wg, &successfulRequests)
	}

	wg.Wait()

	// Stop RPS monitoring
	stopChan <- true

	fmt.Println("Load test completed.")
}
