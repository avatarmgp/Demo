package mservice

import (
	"fmt"
	"os"
	"os/signal"
	"testing"
)

// 获取所有的数据中心
func TestServe(t *testing.T) {
	ln, _, _ := listen("mservice", 14881)

	gs := &GrpcServer{}
	go gs.Serve(ln)

	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt, os.Kill)
	sig := <-c
	fmt.Println("get signal:", sig)
}
