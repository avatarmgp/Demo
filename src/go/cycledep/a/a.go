package a

import (
	"fmt"
	"go/cycledep/i"
)

type A struct {
}

func (a A) PrintA() {
	fmt.Println(a)
}

func NewA() *A {
	a := new(A)
	return a
}

func RequireB(bp i.Bprinter) {
	o := bp
	o.PrintB()
}
