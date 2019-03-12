// 指针引用
/*
需求：一个函数，有指针参数，
多个地方调用，某些地方传递为空，某些地方传递不为空
怎么传递一个指针为引用，传递指向指针的指针
*/

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
