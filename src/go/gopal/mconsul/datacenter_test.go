package mconsul

import (
	"fmt"
	"testing"
)

// 获取所有的数据中心
func TestDataCenter(t *testing.T) {
	dc := NewDatacenter("dc1")
	if dc != nil {
		resp, err := dc.GetDatacenters()
		fmt.Printf("resp:%v,err:%v", resp, err)
	}
}

// 获取默认数据中心
func TestDefaultDataCenter(t *testing.T) {
	resp, err := DefaultDatacenter.GetDatacenters()
	fmt.Printf("resp:%v,err:%v", resp, err)
}
