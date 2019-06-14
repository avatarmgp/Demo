#启动consul
#-config-dir 配置文件路径
#-data-dir 数据路径
#-datacenter 数据中心名称
#-ui 启动内置的静态webui资源
#-bind 绑定本机网卡地址
#-server 服务器节点
#-client 客户端节点
#-join-wan 开启节点的时候加入到wan,可以指定多个


./consul agent -bind 10.10.10.235 -config-dir /Users/sh-ezbuy-007-009/Demo/src/go/gopal/config/consul.d -data-dir /Users/sh-ezbuy-007-009/Demo/src/go/gopal/config/consul_dev -datacenter gopal -ui -server -client 0.0.0.0 -join-wan 192.168.199.64 -advertise 127.0.0.1 -advertise-wan 10.10.10.235 -bootstrap > $EZHOME/config/Procfile

#-join-wan 192.168.199.64 -advertise 127.0.0.1 -advertise-wan $myip #-server -client 0.0.0.0 -bootstrap > $EZHOME/config/Procfile


./consul agent -config-dir $EZHOME/config/consul.d -data-dir $EZHOME/config/consul_dev -datacenter gopal -ui -join-wan 192.168.199.64 -advertise 127.0.0.1 -advertise-wan 10.10.10.235 -server -client 0.0.0.0 
#-bootstrap > $EZHOME/config/Procfile -bind 10.10.10.235

./consul agent -dev
./consul agent -server -bind 10.10.10.235 -data-dir /Users/sh-ezbuy-007-009/Demo/src/go/gopal/config/consul_dev