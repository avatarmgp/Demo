package mconsul

import (
	"fmt"
	"testing"
)

// 获取所有的数据中心
func TestRegisterServiceAddr(t *testing.T) {
	resp, err := RegisterServiceAddr("cart", 14881, false)
	fmt.Printf("resp:%v,err:%v", resp, err)
}
