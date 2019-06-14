package main

import "sync"

func main(){
	//设定map
	/*m := make(map[int]int, 100)
	m[0] = 0
	print(len(m))*/

	/*pa := new([]int)
	*pa = append(*pa, 0)
	print(len(*pa))*/

	c := make(chan int, 4)
	var wg sync.WaitGroup
	wg.Add(4)
	go func(){
		for true{
			select{
			case data := <- c:
				println(data)
				wg.Done()
			default:
				println("default")
			}
		}
	}()
	c <- 100
	c <- 100
	c <- 100
	c <- 100

	wg.Wait()
}