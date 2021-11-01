package main

import (
	"context"
	pb "github.com/fwani/gRPC-Test/server-script/aggfuncs"
	"log"
	"net"

	"google.golang.org/grpc"
)

type server struct {
	pb.UnimplementedGRPCRouteFuncsServer
}

func (s *server) Sum(_ context.Context, in *pb.InputArgsOfBinaryFunc) (*pb.ReturnValue, error) {
	result := in.Value1 + in.Value2
	log.Printf("%d + %d = %d", in.Value1, in.Value2, result)
	return &pb.ReturnValue{Value: result}, nil
}

func (s *server) Multiply(_ context.Context, in *pb.InputArgsOfBinaryFunc) (*pb.ReturnValue, error) {
	result := in.Value1 * in.Value2
	log.Printf("%d * %d = %d", in.Value1, in.Value2, result)
	return &pb.ReturnValue{Value: result}, nil
}

func main() {
	listen, err := net.Listen("tcp", "127.0.0.1:4321")
	if err != nil {
		log.Fatalf("failed to listen: %v\n", err)
	}

	s := grpc.NewServer()
	pb.RegisterGRPCRouteFuncsServer(s, &server{})
	if err := s.Serve(listen); err != nil {
		log.Fatalf("failed to serve: %v\n", err)
	}
}
