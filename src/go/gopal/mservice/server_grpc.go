/*
grpc服务
*/

package mservice

import (
	"fmt"
	"net"
	"sync"
	"time"

	"google.golang.org/grpc"
)

// grpc服务注册接口
type GrpcRegister interface {
	GetServer() *grpc.Server
	RegisterService(name string, methods []string)
}

// grpc服务信息
type grpcServiceInfo struct {
	name   string   // 名称
	method []string // 方法
}

// grpc服务结构体
type GrpcServer struct {
	methodInfo map[string]methodInfo // 方法

	services []grpcServiceInfo // 服务信息,比如cartpublic,cartservice，名字-方法配对
	repoName string
	grpc     *grpc.Server // 当前的gprc服务
	//options  Options

	unaryInterceptor []grpc.UnaryServerInterceptor // 拦截器
	traceOnce        sync.Once
}

// 查看是否有服务
func (s *GrpcServer) isGrpcEnable() bool {
	return len(s.services) > 0
}

// 添加拦截器
func (s *GrpcServer) GrpcAddInterceptor(i grpc.UnaryServerInterceptor) {
	s.unaryInterceptor = append(s.unaryInterceptor, i)
}

// 注册服务
func (s *GrpcServer) RegisterService(name string, method []string) {
	s.services = append(s.services, grpcServiceInfo{name, method})
}

// 获取到服务
func (s *GrpcServer) Serve(ln net.Listener) {
	s.GetServer().Serve(ln)
}

type methodInfo struct {
	timeout time.Duration
}

/*func (s *GrpcServer) getMethodInfo() map[string]methodInfo {
	data := make(map[string]methodInfo)
	if s.options == nil {
		return nil
	}
	for _, item := range s.options.GetAllServiceDesc() {
		for _, method := range item.Methods {
			key := fmt.Sprintf("/%v/%v", item.Name, method.Name)
			data[key] = methodInfo{
				timeout: method.Timeout.Duration(),
			}
		}
	}
	return data
}*/

// 获取到当前的gpc服务
func (s *GrpcServer) GetServer() *grpc.Server {
	if s.grpc == nil {
		s.methodInfo = nil
		s.grpc = grpc.NewServer(grpc.UnaryInterceptor(nil))
	}
	return s.grpc
}

func (s *GrpcServer) Close() error {
	return nil
}

func listen(name string, port int) (ln net.Listener, isDynamic bool, err error) {
	isDynamic = port == 0
	ln, err = net.Listen("tcp", fmt.Sprintf(":%v", port))
	if err != nil {
		return nil, isDynamic, err
	}
	port = ln.Addr().(*net.TCPAddr).Port
	return ln, isDynamic, nil
}
