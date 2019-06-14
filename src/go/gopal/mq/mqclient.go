/*
业务层接口
*/

package mq

// 异步消息
type AsyncMsg struct {
	name string // 消息名称
	data string // 消息数据
}

// 定义chan数组，max为1024个
var asyncMsgChan = make(chan *AsyncMsg, 1024)

// 结束chan
var stopChan = make(chan bool, 1)

// 写入消息队列
func HandleWriteMq() {
	for {
		select {
		case <-stopChan:
			return
		case w := <-asyncMsgChan:
			// 发送消息
			print(w)
		}
	}
}

// 开启消息队列
func StartMq() {
	go HandleWriteMq()
}

// 停止消息队列
func StopMq() {
	stopChan <- true
}

// 推送消息
func PushMsg(name string, data string) error {
	asyncMsgChan <- &AsyncMsg{
		name: name,
		data: data,
	}
	return nil
}