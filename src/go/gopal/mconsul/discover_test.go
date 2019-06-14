package mconsul

import (
	"fmt"
	"testing"
)

func TestWatchServices(t *testing.T) {
	sl, err := WatchServices()
	data := <-sl
	fmt.Printf("sl:%v,err:%v", data, err)
}
