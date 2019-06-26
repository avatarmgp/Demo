package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"time"
)

var jsonData string

func index(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, jsonData)
}

func ReadData() {
	data, err := ioutil.ReadFile("version.json")
	if err != nil {
		log.Print(err)
		return
	}

	jsonData = string(data)
}

func main() {
	http.HandleFunc("/", index)

	ReadData()

	go func() {
		ticker := time.NewTicker(time.Second * 5)
		defer ticker.Stop()
		for {
			select {
			case <-ticker.C:
				ReadData()
			}
		}
	}()

	err := http.ListenAndServe(":9090", nil)
	if err != nil {
		log.Fatal("ListenAndServe:", err)
	}
}
