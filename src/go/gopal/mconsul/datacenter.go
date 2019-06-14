/*
数据中心
*/
package mconsul

import (
	"sync"

	"github.com/hashicorp/consul/api"
)

var DefaultDatacenter = NewDatacenter("")

type Datacenter struct {
	Name string

	instance     *api.Client
	instanceOnce sync.Once
}

func NewDatacenter(name string) *Datacenter {
	return &Datacenter{
		Name: name,
	}
}

func (d *Datacenter) getConsul() *api.Client {
	d.instanceOnce.Do(func() {
		cli, err := api.NewClient(&api.Config{
			Address:    "",
			Datacenter: d.Name,
		})
		if err != nil {
			panic(err)
		}
		d.instance = cli
	})
	return d.instance
}

func (dc *Datacenter) GetDatacenters() ([]string, error) {
	return dc.getConsul().Catalog().Datacenters()
}

func (d *Datacenter) getWriteOption() *api.WriteOptions {
	return &api.WriteOptions{
		Token:      "",
		Datacenter: d.Name,
	}
}

func (d *Datacenter) getQueryOption() *api.QueryOptions {
	return &api.QueryOptions{
		Token:      "",
		Datacenter: d.Name,
	}
}
