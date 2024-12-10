package main

import (
	"fmt"
	"net/http"
	"os"
	"strconv"
	"sync"
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
func worker(id int, url string, requestsPerWorker int, delay time.Duration, wg *sync.WaitGroup) {
	defer wg.Done()
	for i := 0; i < requestsPerWorker; i++ {
		start := time.Now()
		resp, err := http.Get(url)
		if err != nil {
			fmt.Printf("Worker %d: Error - %v\n", id, err)
			continue
		}
		resp.Body.Close()
		fmt.Printf("Worker %d: Request to %s completed with status %d\n", id, url, resp.StatusCode)

		// Sleep for the calculated delay to maintain the target rate
		elapsed := time.Since(start)
		if delay > elapsed {
			time.Sleep(delay - elapsed)
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
	requestsPerWorker := getEnv("REQUESTS_PER_WORKER", 1000)
	targetRPS := getEnv("TARGET_RPS", 1000) // Set desired requests per second

	// Calculate delay per request based on the target RPS
	delayPerRequest := time.Second / time.Duration(targetRPS)

	fmt.Printf("Starting load test:\n - Target URL: %s\n - Workers: %d\n - Requests per worker: %d\n - Target RPS: %d\n", url, workers, requestsPerWorker, targetRPS)
	fmt.Printf("Calculated delay per request to maintain target RPS: %s\n", delayPerRequest)

	var wg sync.WaitGroup
	for i := 0; i < workers; i++ {
		wg.Add(1)
		go worker(i, url, requestsPerWorker, delayPerRequest, &wg)
	}
	wg.Wait()
	fmt.Println("Load test completed.")
}
