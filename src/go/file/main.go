package main

import (
	"io/ioutil"
	"log"
	"net/http"
	"os"
)

func handleGetFile(w http.ResponseWriter, r *http.Request) {
	r.ParseForm() //解析参数，默认是不会解析的
	log.Println("Recv:", r.RemoteAddr)
	pwd, _ := os.Getwd()
	des := pwd + string(os.PathSeparator) + r.URL.Path[1:len(r.URL.Path)]
	desStat, err := os.Stat(des)
	if err != nil {
		log.Println("File Not Exit", des)
		http.NotFoundHandler().ServeHTTP(w, r)
	} else if desStat.IsDir() {
		log.Println("File Is Dir", des)
		http.NotFoundHandler().ServeHTTP(w, r)
	} else {
		fileData, err := ioutil.ReadFile(des)
		if err != nil {
			log.Println("Read File Err:", err.Error())
		} else {
			log.Println("Send File:", des)
			w.Write(fileData)
		}
	}
}

func main() {
	http.HandleFunc("/", handleGetFile)
	err := http.ListenAndServe(":9090", nil)
	if err != nil {
		log.Fatalln("Get Dir Err", err.Error())
	}
}
