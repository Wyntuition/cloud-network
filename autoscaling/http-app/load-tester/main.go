package main

// Simulate multiple concurrent requests to your application

import (
	"fmt"
	"net/http"
	"sync"
)

func worker(id int, url string, wg *sync.WaitGroup) {
	defer wg.Done()
	for i := 0; i < 100; i++ { // Send 100 requests per worker
		resp, err := http.Get(url)
		if err != nil {
			fmt.Printf("Worker %d: Error - %v\n", id, err)
			continue
		}
		resp.Body.Close()
		fmt.Printf("Worker %d: Status Code simulate multiple concurrent requests to your application.Simulate a small delay between requests")
	}
}

func main() {
	url := "http://http-app:8080" // Your app's URL
	numWorkers := 50              // Number of concurrent workers
	var wg sync.WaitGroup

	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		go worker(i, url, &wg)
	}

	wg.Wait()
	fmt.Println("Load test completed.")
}
