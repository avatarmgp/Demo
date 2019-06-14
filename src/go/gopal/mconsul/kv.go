/*
获取key-value
*/
package mconsul

import (
	"github.com/hashicorp/consul/api"
)

func IsOpen() bool {
	_, err := DefaultDatacenter.getConsul().Agent().NodeName()
	if err != nil {
		return false
	}
	return true
}

func GetValue(key string) ([]byte, error) {
	return DefaultDatacenter.GetValue(key)
}

func (dc *Datacenter) ValueListStr(prefix string) (map[string]string, error) {
	pairs, _, err := dc.getConsul().KV().List(prefix, dc.getQueryOption())
	if err != nil {
		return nil, err
	}
	ret := make(map[string]string, len(pairs))
	for _, item := range pairs {
		ret[item.Key] = string(item.Value)
	}
	return ret, nil
}

type Pairs struct {
	Key   string
	Value []byte
}

func (dc *Datacenter) GetList(key string) ([]Pairs, error) {
	pairs, _, err := dc.getConsul().KV().List(key, dc.getQueryOption())
	if err != nil {
		return nil, err
	}
	ret := make([]Pairs, len(pairs))
	for idx := range pairs {
		ret[idx] = Pairs{pairs[idx].Key, pairs[idx].Value}
	}
	return ret, nil
}

func (dc *Datacenter) GetValue(key string) ([]byte, error) {
	kvp, _, err := dc.getConsul().KV().Get(key, dc.getQueryOption())
	if err != nil {
		return nil, err
	}
	if kvp == nil {
		return nil, nil
	}
	return kvp.Value, nil
}

func SetValue(key string, val []byte) error {
	return DefaultDatacenter.SetValue(key, val)
}

func (dc *Datacenter) SetValue(key string, val []byte) error {
	_, err := dc.getConsul().KV().Put(&api.KVPair{
		Key:   key,
		Value: val,
	}, dc.getWriteOption())
	return err
}

func CAS(key string, val []byte, modifyIndex uint64) (bool, error) {
	return DefaultDatacenter.CAS(key, val, modifyIndex)
}

func (dc *Datacenter) CAS(key string, val []byte, modifyIndex uint64) (bool, error) {
	r, _, err := dc.getConsul().KV().CAS(&api.KVPair{
		Key:         key,
		Value:       val,
		ModifyIndex: modifyIndex,
	}, dc.getWriteOption())
	return r, err
}

func GetValueAndModifyIndex(key string) ([]byte, uint64, error) {
	return DefaultDatacenter.GetValueAndModifyIndex(key)
}

func (dc *Datacenter) GetValueAndModifyIndex(key string) ([]byte, uint64, error) {
	kvp, _, err := dc.getConsul().KV().Get(key, dc.getQueryOption())
	if err != nil {
		return nil, 0, err
	}
	if kvp == nil {
		return nil, 0, nil
	}
	return kvp.Value, kvp.ModifyIndex, nil
}
