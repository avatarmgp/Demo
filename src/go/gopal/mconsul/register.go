/*
注册服务
*/

package mconsul

import (
	"fmt"
	"strings"

	"github.com/hashicorp/consul/api"
)

// 注册某个服务
func RegisterServiceAddr(name string, port int, deregister bool) (string, error) {
	client, err := api.NewClient(&api.Config{
		Address:    "",
		Datacenter: "dc1",
	})
	if err != nil {
		return "", err
	}
	sp := strings.Split(name, ".")
	nodeName, err := client.Agent().NodeName()
	if err != nil {
		return "", err
	}
	node, _, err := client.Catalog().Node(nodeName, nil)
	if err != nil {
		return "", err
	}
	if node == nil {
		return "", err
	}

	check := fmt.Sprintf("%v:%v", node.Node.Address, fmt.Sprint(port))
	deregisterDuration := ""
	if deregister {
		deregisterDuration = "1m"
	}
	id := fmt.Sprintf("%v:%v", name, check)
	err = client.Agent().ServiceRegister(&api.AgentServiceRegistration{
		ID:      id,
		Name:    name,
		Address: node.Node.Address,
		Port:    port,
		Tags:    []string{"service", sp[0]},
		Check: &api.AgentServiceCheck{
			Interval: "5s",
			TCP:      check,
			Timeout:  "10s",
			DeregisterCriticalServiceAfter: deregisterDuration,
		},
	})
	if err != nil {
		return "", err
	}
	return id, nil
}
