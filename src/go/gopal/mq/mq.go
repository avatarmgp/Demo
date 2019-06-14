/*
和disque交互层
*/
package mq

import (
	"context"
	"time"

	"github.com/zencoder/disque-go/disque"
)

type mq struct {
	p            *disque.Pool   // 连接池
	listenerWait time.Duration  //等待时间
	c            *disque.Disque // 连接
}

// 获取disque连接接口
func NewDisqueClient() (*mq, error) {
	hosts := []string{"127.0.0.1:7711"}
	p := disque.NewPool(hosts, 1, 1, 1, time.Duration(1))
	c, _ := p.Get(context.Background())
	return &mq{p: p, c: c}, nil
}

// 发送消息
func (this *mq) Push(name string, data string, t time.Duration) error {
	this.c.Push(name, data, t)
	return nil
}

// 注册消费者函数
func (this *mq) AddConsumeListener(name string, listener func(*QMsg)) error {
	println("AddConsumeListener")
	if this.p.IsClosed() {
		return nil
	}
	c, e := this.p.Get(context.Background())
	job, e := c.Fetch(name, 0)
	go this.AddConsumeListener(name, listener)
	if job == nil {
		return nil
	}
	if e != nil {
		return e
	}
	e = this.c.Ack(job.JobID)
	if e != nil {
		return e
	}

	qmsg := &QMsg{
		QueueName: job.QueueName,
		Message:   job.Message,
	}
	listener(qmsg)
	return nil
}
