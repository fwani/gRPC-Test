package main

import (
	"context"
	"log"
	"time"

	"google.golang.org/grpc"

	pb "github.com/fwani/gRPC-Test/server-script/aggfuncs"
)

func main() {
	conn, err := grpc.Dial("127.0.0.1:4321", grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		log.Fatalf("did not connect: %v\n", err)
	}
	defer conn.Close()
	client := pb.NewGRPCRouteFuncsClient(conn)

	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	var x int32
	var y int32
	x = 5
	y = 3
	res, err := client.Sum(ctx, &pb.InputArgsOfBinaryFunc{Value1: x, Value2: y})
	if err != nil {
		log.Fatalf("could not request: %v\n", err)
	}

	log.Printf("sum: %d + %d = %v\n", x, y, res)

	res, err = client.Multiply(ctx, &pb.InputArgsOfBinaryFunc{Value1: x, Value2: y})
	if err != nil {
		log.Fatalf("could not request: %v\n", err)
	}

	log.Printf("multiply: %d * %d = %v\n", x, y, res)
}
