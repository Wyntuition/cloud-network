// autoscaling/http-app/main.go
package main

import (
	"fmt"
	"net/http"
	"strconv"
	"sync"
)

func handler(w http.ResponseWriter, r *http.Request) {
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
	fmt.Println("Starting server on port 8080")
	http.HandleFunc("/", handler)
	http.HandleFunc("/stress/cpu", stressCPU)
	http.HandleFunc("/stress/memory", stressMemory)
	http.ListenAndServe(":8080", nil)
}
