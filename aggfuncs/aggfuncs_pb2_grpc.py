# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import aggfuncs_pb2 as aggfuncs__pb2


class gRPCRouteFuncsStub(object):
    """함수 리스트
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.sum = channel.unary_unary(
                '/proto.gRPCRouteFuncs/sum',
                request_serializer=aggfuncs__pb2.InputArgsOfBinaryFunc.SerializeToString,
                response_deserializer=aggfuncs__pb2.ReturnValue.FromString,
                )
        self.multiply = channel.unary_unary(
                '/proto.gRPCRouteFuncs/multiply',
                request_serializer=aggfuncs__pb2.InputArgsOfBinaryFunc.SerializeToString,
                response_deserializer=aggfuncs__pb2.ReturnValue.FromString,
                )


class gRPCRouteFuncsServicer(object):
    """함수 리스트
    """

    def sum(self, request, context):
        """rpc protocol 정의, sum 함수 정의
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def multiply(self, request, context):
        """rpc protocol 정의, multiply 함수 정의
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_gRPCRouteFuncsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'sum': grpc.unary_unary_rpc_method_handler(
                    servicer.sum,
                    request_deserializer=aggfuncs__pb2.InputArgsOfBinaryFunc.FromString,
                    response_serializer=aggfuncs__pb2.ReturnValue.SerializeToString,
            ),
            'multiply': grpc.unary_unary_rpc_method_handler(
                    servicer.multiply,
                    request_deserializer=aggfuncs__pb2.InputArgsOfBinaryFunc.FromString,
                    response_serializer=aggfuncs__pb2.ReturnValue.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'proto.gRPCRouteFuncs', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class gRPCRouteFuncs(object):
    """함수 리스트
    """

    @staticmethod
    def sum(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.gRPCRouteFuncs/sum',
            aggfuncs__pb2.InputArgsOfBinaryFunc.SerializeToString,
            aggfuncs__pb2.ReturnValue.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def multiply(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.gRPCRouteFuncs/multiply',
            aggfuncs__pb2.InputArgsOfBinaryFunc.SerializeToString,
            aggfuncs__pb2.ReturnValue.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)