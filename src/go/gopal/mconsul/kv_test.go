package mconsul

import (
	"fmt"
	"testing"
)

// 获取所有的数据中心
func TestIsOpen(t *testing.T) {
	print(IsOpen())
}

// 设置默认数据中心
func TestSetValue(t *testing.T) {
	DefaultDatacenter.SetValue("test", []byte("test"))
}

// 获取默认数据中心
func TestGetValue(t *testing.T) {
	data, err := DefaultDatacenter.GetValue("test")
	fmt.Printf("data:%v,err:%v", string(data), err)
}
