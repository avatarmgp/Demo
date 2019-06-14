package b

import (
	"fmt"
	"go/cycledep/i"
)

type B struct {
}

func (b B) PrintB() {
	fmt.Println(b)
}

func NewB() *B {
	b := new(B)
	return b
}

func RequireA(ap i.Aprinter) {
	o := ap
	o.PrintA()
}
