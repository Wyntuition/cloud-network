package main

import (
	"bufio"
	"fmt"
	"net/http"
	"os"
	"strconv"
	"strings"
	"time"
)

// Cached state to track previous metrics
var previousRequestCount float64

// Fetch metrics from the /metrics endpoint
func fetchMetrics(url string) (string, error) {
	resp, err := http.Get(url)
	if err != nil {
		return "", fmt.Errorf("error fetching metrics: %w", err)
	}
	defer resp.Body.Close()

	// Read response body
	var metricsBuilder strings.Builder
	scanner := bufio.NewScanner(resp.Body)
	for scanner.Scan() {
		metricsBuilder.WriteString(scanner.Text() + "\n")
	}

	if err := scanner.Err(); err != nil {
		return "", fmt.Errorf("error reading response: %w", err)
	}

	return metricsBuilder.String(), nil
}

// Parse HTTP requests per second using `http_requests_total`
func calculateMessagesPerSecond(metrics string) float64 {
	lines := strings.Split(metrics, "\n")
	var currentRequests float64

	for _, line := range lines {
		if strings.HasPrefix(line, "http_requests_total") {
			// Extract the last number from the http_requests_total line
			parts := strings.Fields(line)
			if len(parts) < 2 {
				continue
			}
			requestCount, err := strconv.ParseFloat(parts[1], 64)
			if err != nil {
				continue
			}

			currentRequests = requestCount
			break
		}
	}

	// Calculate rate per second over a sliding window
	rate := (currentRequests - previousRequestCount) / 5.0 // 5-second sliding window
	previousRequestCount = currentRequests                 // Update the cache with the new value
	return rate
}

// Parse pod resource usage (CPU & Memory) metrics
func parsePodResourceUsage(metrics string) {
	lines := strings.Split(metrics, "\n")
	fmt.Println("\n(v1) Parsing pod resource usage metrics:")

	for _, line := range lines {
		if strings.HasPrefix(line, "container_cpu_usage_seconds_total") {
			// Extract CPU usage per container
			parts := strings.Fields(line)
			if len(parts) < 2 {
				continue
			}
			fmt.Println("Container CPU usage:", parts)
		}
		if strings.HasPrefix(line, "container_memory_usage_bytes") {
			// Extract memory usage per container
			parts := strings.Fields(line)
			if len(parts) < 2 {
				continue
			}
			fmt.Println("Container Memory usage:", parts)
		}
	}
}

// Parse node-level resource usage (CPU/Memory)
func parseNodeResourceUsage(metrics string) {
	lines := strings.Split(metrics, "\n")
	fmt.Println("\nParsing node-level resource usage metrics:")

	for _, line := range lines {
		if strings.HasPrefix(line, "node_cpu_seconds_total") {
			// Extract CPU usage information from node metrics
			parts := strings.Fields(line)
			if len(parts) < 2 {
				continue
			}
			fmt.Println("Node CPU usage:", parts)
		}

		if strings.HasPrefix(line, "node_memory_Active_bytes") {
			// Extract memory usage from node metrics
			parts := strings.Fields(line)
			if len(parts) < 2 {
				continue
			}
			fmt.Println("Node Memory usage:", parts)
		}

		// New parsing for process_cpu_seconds_total
		if strings.HasPrefix(line, "process_cpu_seconds_total") {
			parts := strings.Fields(line)
			if len(parts) < 2 {
				continue
			}
			cpuSeconds, err := strconv.ParseFloat(parts[1], 64)
			if err != nil {
				fmt.Println("Error parsing process_cpu_seconds_total:", err)
				continue
			}
			fmt.Printf("Process Total CPU Seconds: %.2f\n", cpuSeconds)
		}
	}
}

func main() {
	metricsURL := os.Getenv("METRICS_URL")
	if metricsURL == "" {
		metricsURL = "http://http-app:8080/metrics"
	}

	for {
		fmt.Println("\nFetching metrics from:", metricsURL)

		// Fetch metrics
		metricsResponse, err := fetchMetrics(metricsURL)
		if err != nil {
			fmt.Println("Error fetching metrics:", err)
		} else {
			// Calculate HTTP requests per second
			rate := calculateMessagesPerSecond(metricsResponse)
			fmt.Printf("\nRequests per second: %.2f\n", rate)

			// Extract pod CPU/Memory usage
			parsePodResourceUsage(metricsResponse)

			// Extract node-level resource usage
			parseNodeResourceUsage(metricsResponse)
		}

		// Wait for 5 seconds before polling metrics again
		time.Sleep(2 * time.Second)
	}
}
