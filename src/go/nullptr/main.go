// 空指针传递

package main

func main() {
	var p *int
	modify(&p)
	print(*p)

	modify(nil)
}

func modify(ip **int) {
	if ip != nil {
		i := 1
		*ip = &i
	}
}
