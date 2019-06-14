package main

import "time"

func routin() {
	println("enter routin")
	time.Sleep(time.Second * 1)
	go routin()
	println("exit routin")
}
func main() {
	go routin()

	time.Sleep(time.Second * 10)
}
