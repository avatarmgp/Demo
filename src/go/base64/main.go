package main

import "encoding/hex"

func test(src string) string {
	return string(hex.EncodeToString([]byte(src)))
}

func main() {
	print(test("5cd90f2a38d92a000990862c"))
}
