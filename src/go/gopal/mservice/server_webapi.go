package mservice

import (
	"net"
	"net/http"
	"net/http/pprof"

	"git.ezbuy.me/ezbuy/base/dist/mservice/mconsul"
	"git.ezbuy.me/ezbuy/base/misc/context"
)

type WebServer struct {
	mux        Mux
	options    Options
	methods    map[string][]string
	services   []*mconsul.Service
	middleware []Middleware
	thriftName string
}

func (s *WebServer) Serve(ctx context.T, ln net.Listener) error {
	s.initMux()
	s.mux.HandleFunc("/ping", s.Ping)
	s.mux.HandleFunc("/debug/pprof/", pprof.Index)
	s.mux.HandleFunc("/debug/pprof/cmdline", pprof.Cmdline)
	s.mux.HandleFunc("/debug/pprof/profile", pprof.Profile)
	s.mux.HandleFunc("/debug/pprof/symbol", pprof.Symbol)
	s.mux.HandleFunc("/debug/pprof/trace", pprof.Trace)
	for serviceName := range s.methods {
		s.mux.HandleFunc("/api/"+serviceName+"/ping", s.Ping)
	}
	svr := &http.Server{
		Handler: s.mux,
	}
	return svr.Serve(ln)
}
