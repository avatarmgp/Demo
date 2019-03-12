/*
工程模式
go实现多态
interface定义抽象接口
struct实现接口，工厂返回interface，实际由struct构建
*/

package main

import (
	"fmt"
	"reflect"
)

//抽象类
type Animal interface {
	Sleep()
	Age() int
	Type() string
}

//子类cat
type Cat struct {
	MaxAge int
}

func (this *Cat) Sleep() {
	print("Cat sleep")
}

func (this *Cat) Age() int {
	return this.MaxAge
}

func (this *Cat) Type() string {
	return "Cat"
}

//子类dog
type Dog struct {
	MaxAge int
}

func (this *Dog) Sleep() {
	print("Dog sleep")
}

func (this *Dog) Age() int {
	return this.MaxAge
}

func (this *Dog) Type() string {
	return "Dog"
}

func Factory(name string) Animal {
	switch name {
	case "cat":
		return &Cat{MaxAge: 10}
	case "dog":
		return &Dog{MaxAge: 20}
	default:
		panic("No such animal")
	}
}

func main() {
	animal := Factory("cat")
	animal.Sleep()
	fmt.Println("type", reflect.TypeOf(animal))
}
