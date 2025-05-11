package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
)

// HealthCheckResponse represents the /status JSON structure
type HealthCheckResponse struct {
    Result string `json:"result"`
}

// MetricsData holds metric details
type MetricsData struct {
    UserCount      int `json:"UserCount"`
    UserCountActive int `json:"UserCountActive"`
}

// MetricsResponse represents the /metrics JSON structure
type MetricsResponse struct {
    Status string      `json:"status"`
    Code   int         `json:"code"`
    Data   MetricsData `json:"data"`
}

func helloHandler(w http.ResponseWriter, r *http.Request) {
    log.Println("Main request successful")
    fmt.Fprintln(w, "Go - Hello World")
}

func statusHandler(w http.ResponseWriter, r *http.Request) {
    log.Println("Status request successful")
    response := HealthCheckResponse{Result: "OK - healthy"}
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

func metricsHandler(w http.ResponseWriter, r *http.Request) {
    log.Println("Metrics request successful")
    response := MetricsResponse{
        Status: "success",
        Code:   0,
        Data: MetricsData{
            UserCount:      140,
            UserCountActive: 23,
        },
    }
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

func main() {
    http.HandleFunc("/", helloHandler)
    http.HandleFunc("/status", statusHandler)
    http.HandleFunc("/metrics", metricsHandler)

    log.Println("Starting server on port 6111...")
    if err := http.ListenAndServe(":6111", nil); err != nil {
        log.Fatalf("Could not start server: %s\n", err)
    }
}
