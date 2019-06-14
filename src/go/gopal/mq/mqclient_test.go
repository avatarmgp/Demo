package mq

import (
	"testing"
	"time"
)

// 发送消息
func pushMsg(mq *mq) {
	for i := 0; i < 10; i++ {
		mq.Push("test", "test", 0)
	}
}

// 接受消息
func popMsg(mq *mq) {
	mq.AddConsumeListener("test", dealMsg)
}

// 处理消息
func dealMsg(qmsg *QMsg) {
	//println(qmsg.Message)
}

func TestPushMsg(t *testing.T) {
	mq, err := NewDisqueClient()
	if err != nil {
		return
	}

	pushMsg(mq)

	popMsg(mq)

	time.Sleep(time.Second * 100)
}
