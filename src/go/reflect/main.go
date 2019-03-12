package main

import (
	"fmt"
	"reflect"
)

func fun(param interface{}) {
	t := reflect.TypeOf(param)
	if t == nil {
		print("invalid param")
		return
	}

	fmt.Println("type:", reflect.TypeOf(param))
	fmt.Println("value:", reflect.ValueOf(param))
}

func main() {
	fun(12)
	fun(1.2)

	type s struct {
		a int
	}

	ps := &s{
		a: 100,
	}

	fun(ps)

	fun(nil)
}
