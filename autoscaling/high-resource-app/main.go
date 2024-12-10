package main

import (
	"log"
	"math"
	"os"
	"os/signal"
	"sync"
	"syscall"
	"time"
)

// High CPU simulation
func busyLoop(wg *sync.WaitGroup) {
	defer wg.Done()
	log.Println("Starting CPU-intensive task")
	for {
		for i := 0; i < 1e7; i++ {
			_ = math.Sqrt(float64(i)) // Perform some CPU-intensive computation
		}
		time.Sleep(100 * time.Millisecond) // Short sleep to simulate periodic CPU spikes
	}
}

// High memory simulation
func memoryConsumer(wg *sync.WaitGroup) {
	defer wg.Done()
	log.Println("Starting memory-intensive task")
	var data [][]byte
	for {
		chunk := make([]byte, 10*1024*1024) // Allocate 10 MB chunks
		data = append(data, chunk)
		time.Sleep(500 * time.Millisecond) // Delay to simulate gradual memory growth
	}
}

func main() {
	var wg sync.WaitGroup

	// Trap interrupt signals to allow graceful shutdown
	stop := make(chan os.Signal, 1)
	signal.Notify(stop, syscall.SIGINT, syscall.SIGTERM)

	// Start CPU and memory simulations
	wg.Add(2)
	go busyLoop(&wg)
	go memoryConsumer(&wg)

	// Wait for interrupt signal
	<-stop
	log.Println("Shutting down gracefully...")

	// Clean up goroutines (optional, since the app will terminate)
	wg.Wait()
	log.Println("All tasks stopped. Exiting.")
}
