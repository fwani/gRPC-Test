import grpc

from aggfuncs import aggfuncs_pb2_grpc as agg_pb_grpc, aggfuncs_pb2 as agg_pb


def run():
    channel = grpc.insecure_channel('127.0.0.1:4321')
    stub = agg_pb_grpc.gRPCRouteFuncsStub(channel)
    response = stub.sum(agg_pb.InputArgsOfBinaryFunc(value1=4, value2=5))
    print(f"Greeter client received: {response.value}")
    response = stub.multiply(agg_pb.InputArgsOfBinaryFunc(value1=4, value2=5))
    print(f"Greeter client received: {response.value}")


if __name__ == '__main__':
    run()
