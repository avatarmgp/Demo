/*
服务发现
*/

package mconsul

import (
	"github.com/hashicorp/consul/watch"
)

type ServiceList map[string][]string

func (s ServiceList) Get(name string) ([]string, bool) {
	tags, ok := s[name]
	return tags, ok
}

func WatchServices() (<-chan ServiceList, error) {
	wp, err := watch.Parse(map[string]interface{}{
		"type": "services",
	})
	if err != nil {
		return nil, err
	}
	ret := make(chan ServiceList)
	wp.Handler = func(idx uint64, obj interface{}) {
		se, ok := obj.(map[string][]string)
		if !ok {
			return
		}
		ret <- se
	}
	go func() {
		wp.Run("127.0.0.1:8500")
	}()
	return ret, nil
}
