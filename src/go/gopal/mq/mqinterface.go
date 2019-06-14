package mq

type QMsg struct {
	QueueName string // 队列名
	JobID     string // 消息id
	Message   string // 消息内容
}

type MqInterface interface {
	Push(name string, data string) error                  // 推送一条消息
	AddConsumeListener(name string, listener func(*QMsg)) // 注册消费者函数
}
