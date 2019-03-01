/*组合模式*/

package main

type Animal struct{}

func (a *Animal) Eat() {
	print("eating")
}

type Fish struct {
	Animal
}

func (f *Fish) Eat() {
	println("fish eating")
}

func (f *Fish) Swim() {
	println("swimming")
}

func main() {
	fish := &Fish{}
	fish.Eat()
	fish.Swim()
}
