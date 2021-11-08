# What is gRPC?

## 1. RPC (Remote Procedure Call)

### 1-1. RPC 는 무엇인가?

- software communication protocol
    - network 의 상세 정보를 몰라도, 한 프로그램이 다른 컴퓨터에 있는 프로그램의 서비스에 request 를 할 수 있다.
- 외부 process 가 다른 process 를 호출하기 위해서 사용된다.
- **Procedure call:** function call or subroutine call
    - 함수 호출과 같은 순차적인 호출
- client - server 모델을 사용한다.
    - request 를 하는 프로그램이 client
    - service 를 제공하는 프로그램이 server
    - RPC 는 일반적인 함수 호출과 동작이 비슷하다.
        - server 에서 결과를 리턴 할 때까지 정지하는 synchronous(동기식) 동작이다.
    - 그러나, 같은 주소 공간을 공유하는 lightweight(가벼운) process 나 thread 을 사용하면 multiple RPCs 가 동시에 동작 할 수 있다.
- **IDL(Interface Definition Language):** 소프트웨어 컴포넌트의 API(Application Programming Interface) 를 설명하는 특정 언어
    - RPC software 에서 일반적으로 사용된다.
    - IDL 은 다른 OS 와 컴퓨터 언어를 사용하는 연결된 양 끝 노드의 연결 다리를 제공한다.

### 1-2. RPC 는 무엇을 할까?

- RPC 가 호출되면, 호출한 client 의 프로그램은 정지하고, parameters 가 네트워크를 통해서 동작이 실행 될 수 있는 server 환경으로 전달되고, 해당 동작이 server 환경에서 실행 된다.
- 동작이 끝이나면, server 는 결과를 다시 RPC 를 호출한 환경으로 전달하고, client 다음 절차를 재개한다.
- RPC 수행 절차
    1. client 가 client stub 을 호출(일반적인 방법으로 stack 에 푸시된 파라미터와 함께 local procedure call) 한다.
    2. client stub 은 procedure parameter 를 message 로 묶고, message 를 보내기 위해서 system call 을 준비한다. 메세지는 **marshalling** 을 호출 한다.
    3. local OS 에 있는 client 는 remote server machine 으로 메세지를 보낸다.
    4. server OS 는 들어온 packet 을 server stub 으로 전달한다.
    5. server stub 은 **unmarshalling** 을 호출하여 메세지에 들어있는 파라미터를 unpack 한다.
    6. server procedure 가 끝이나면, server stub 으로 결과를 보내고, server stub 은 return value 를 message 로 marshal 한다. server stub 은 메세지를 transport layer 로 보낸다.
    7. transport layer 는 결과 메세제를 client의 transport layer 로 보낸다.
    8. client stub 은 결과 메세지를 unmarshall 하고, 함수 콜에 대한 리턴을 한다.

### 1-3. RPC 의 타입

- 몇 가지 RPC 모델과 분산 컴퓨팅 implementation 이 존재한다. 인기있는 모델과 implementation 은 OSF(Open Software Foundation) 의 DCE(Distributed Computing Environment) 다.
- IEEE 는 RPC 를 **"ISO Remote Procedure Call Specification, ISO/IEC CD 11578 N6561, ISO/IEC, November 1991."** 로 정의한다.
- RPC 구성 예제
    - client 가 호출하고, server 가 응답을 리턴 할 때 까지 진행하지 않는 일반적인 method 이다.
    - 서버가 응답하지 않아도 client 는 호출하고 동시에 자신만의 처리를 진행한다.
    - 여러 client nonblocking 호출을 한 묶음으로 보내는 역할을 한다.
    - RPC client 는 메세제를 여러 서버에 보내고 모든 결과를 응답받는 broadcast 기능이 있다.
    - client 는 nonblocking client/server call 을 한다. server 는 client 와 연결된 procedure 가 호출 완료되었다는 시그널을 보낸다.
- RPC 는 네트워크 communication 의 OSI(Open Systems Interconnection) 모델의 transport layer 와 application layer 에 걸쳐있다.
- RPC 는 network 를 사용하는 분산된 여러 프로그램을 포함하는 application 을 쉽게 배포 할 수 있도록 만들어 준다.
- client-server 커뮤니케이션의 대체 방안으로는 message queueing 과 IBM 의 APPC(Advanced Program-to-Program Communication) 이 있다.

### 1-4. RPC 의 장단점 (Pros and cons)

- 개발자와 application 매니저에게 제공하는 RPC 의 장점
    - client 가 server 와 통신을 하는데 high-level language 안에서 전통적인 절차지향 호출을 사용 할 수 있다.
    - 분산 환경에서 사용할 수 있다.
    - 내부 message-passing 매커니즘은 유저에게 감출 수 있다.
    - 코드를 rewrite and redevelop 하는데 쉽다.
    - 추출(abstraction) 을 제공한다.
    - 성능 향상을 위해 많은 protocol layer 를 생략한다.
- 단점
    - client 와 server 가 다른 실행 환경을 사용한다. resource 역시 더 복잡하다. RPC 시스템은 많은 양의 데이터를 전달할 때 적절하다.
    - RPC 는 다른 머신과 프로세스와의 communication system 을 포함하기 때문에 실패에 높게 노출(vulnerable) 되어있다.
    - RPC 의 standard 포멧이 없기 때문에 다양한 방법으로 동작된다.
    - RPC 는 상호 작용 기반이기 때문에 하드웨어 아키텍처의 유연성을 제공하지 않는다.

## 2. gRPC

### 2-1. gRPC 는 무엇인가?

- gRPC 와 protocol buffer

#### 2-1-1. gRPC

- google 에서 만든 오픈소스 RPC 프레임워크
- gRPC 는 IDL(Interface Definition Language) 와 기본적인 message 교환 포멧과 함께 protocol buffer 를 사용 할 수 있다.
- gRPC 에서, client 어플리케이션은 다른 머신에 있는 server 어플리케이션의 함수를 local object 처럼 직접 호출 할 수 있기 때문에 분산 어플리케이션과 서비스를 만드는데 쉽다.
- 다른 많은 RPC 시스템 처럼, gRPC 외부에서 파라이터와 함께 호출이 가능한 특정 메소드를 가진 서비스를 정의해야 한다.
- server 측에서는, 서버는 이 interface 를 구현하고, gRPC 서버를 실행하여 클라이언트 호출을 처리한다.
- client 측에서는, 서버와 동일한 메소드를 제공하는 stub 을 가지고 있다.

![landing-2.svg](https://grpc.io/img/landing-2.svg)

- gRPC client 와 server 는 각자 다양한 환경과 gPRC 를 지원하는 어떤 언어로 작성되어 있어도 서로 실행하고 대화 할 수 있다.

#### 2-1-2. Protocol Buffer

- 기본적으로 gRPC 는 구조화된 데이터를 직렬화(serialize) 하기 위해서 구글의 성숙한 오픈소스 매커니즘인 Protocol Buffers 를 사용한다.

- 작동원리

    - protocol buffer 와 함께 동작하기 위한 첫 번째 단계는 데이터를 내가 원하는 대로 직렬화 하는 구조를 **proto file**(일반적인 text file 로 `.proto` 확장자로 정의된다.) 에  정의 하는 것이다.
    - protocol buffer data 는 메세지들로 구성되어 있다. 이 각 메세지는 name-value pair 로 이루어진 series 를 포함하는 작은 논리적 record 이다.

  ```protobuf
  message Person {
    string name = 1;
    int32 id = 2;
    bool has_ponycopter = 3;
  }
  ```

    - 그리고, protocol buffer compiler 인 `protoc`를 사용해서 proto 정의된 구조를 각 언어에서 접근이 가능한 class 로 변환 할 수 있다.
    - 전체 구조를 from/to raw bytes 로 serialize/parse 를 위해서 `name()`, `set_name()` 과 같은 메소드를 제공한다.
    - 일반 proto 파일에서 gRPC 서비스를 정의하면 RPC 메서드 매개 변수 및 반환 유형이 protocol buffer messages 로 지정됩니다.
    - gRPC 는 proto file 로 code 를 생성하는 특수 gRPC 플러그인인 `protoc` 를 사용한다. 즉, 생성된 gRPC client 와 server 코드 와 populating, serializing, retrieving message types 를 위한 일반적인 protocol buffer code 를 생성할 수 있다.

- 더 자세한 내용은 [protocol buffers documentation](https://developers.google.com/protocol-buffers/docs/overview) 참고

- version

    - 현재 기본 버전은 proto2 이다
    - proto3 가 배포되고 있는데 proto3 를 쓰는 것을 추천하고 있다.

### 2-2. gRPC 의 주요 컨셉과 lifecycle

#### 2-2-1. Service definition

- 다른 RPC 시스템과 마찬가지로, gRPC 또한 외부 환경의 특정 method 를 parameter 와 return type 을 이용해서 호출이 가능한 서비스를 정의하는데 기반을 둔다.
- gRPC 는 서비스 interface 와 payload message 의 구조를 정의하기 위해서 기본적으로 protocol buffer 를 사용한다. 다른것도 사용은 가능하다.

```protobuf
service HelloService {
  rpc SayHello (HelloRequest) returns (HelloResponse);
}

message HelloRequest {
  string greeting = 1;
}

message HelloResponse {
  string reply = 1;
}
```

- gRPC 를 사용해서 다음 4가지 종류의 서비스 method 를 만들 수 있다.

    - **Unary RPC:** client 가 server 로 single request 를 보내고, single repsonse 를 돌려받는 일반적인 function call 예제

  ```protobuf
  rpc SayHello(HelloRequest) returns (HelloResponse);
  ```

    - **Server Streaming RPC:** client 가 server 로 request 를 보내면 sequence of message 를 stream 형태로 돌려받는 것
        - client 는 return 된 stream 을 더 이상 올 메세지가 없을 때까지 읽는다.
        - gRPC 는 개별적인 RPC call 에 대한 메세지 순서를 보증한다.

  ```protobuf
  rpc LotsOfReplies(HelloRequest) returns (stream HelloResponse);
  ```

    - **Client Streaming RPC:** client 가 server 로 sequence of message 를 stream 형태로 보낸다.
        - client 가 message 를 다 보내고, server 가 다 읽을 때까지 기다리고, response 를 리턴한다.
        - gRPC 는 개별적인 RPC call 에 대한 메세지 순서를 보증한다.

  ```protobuf
  rpc LotsOfGreetings(stream HelloRequest) returns (HelloRepsponse);
  ```

    - **Bidirectional(양방향) Streaming RPC:** 양 사이드에서 메세지를 stream 형태로 읽고/쓴다.
        - 두 stream 은 독립적으로 동작한다. 그래서 client 나 server 는 원하는 순서로 읽고 쓰기가 가능하다.
        - 예를 들어, server 가 response 를 보내기전에 모든 client message 받기 위해 기다릴 수 있다. (메세지 하나받고 하나 처리하는 형식이 아니라 모든걸 받고 각각 처리해주는 형식)
        - 각 스트림의 메세지 순서는 보존된다.

  ```protobuf
  rpc BidiHello(stream HelloRequest) returns (stream HelloResponse);
  ```

    - 더 많은 종류의 RPC lifecyle 을 사용 할 수 있다.

#### 2-2-2. API 사용하기

- `.proto` 파일에 서비스 정의를 시작으로, gRPC 는 client/server side code 를 생성하는 protocol buffer compiler plugin 을 제공한다.
- gRPC 사용자는 server side 에서 동일한 API 를 실행하기 위해서 일반적으로 client side 에서 이 API 를 사용한다.
    - server side 에서, server 는 server 에 의해서 declared(선언된) method 를 실행하고 client 호출을 처리하기 위해서 gRPC server 를 실행한다. gRPC 요소는 들어오는 request 를 decode 하고, service method 를 실행하고, service response 를 encoding 한다.
    - clinet side 에서, client 는 service 의 같은 method 를 구현하는 stub 이라는 local object 를 가지고 있다. client 는 단순히 local object 에 있는 이 method 를 실행함으로, 적절한 protocol buffer message type 으로 파라미터를 래핑할 수 있다. gRPC 는 request 를 server 로 보내고 server 의 protocol buffer response 를 반환 받은 후에 찾는다.

#### 2-2-3. Synchronous vs. asynchronous

- **Synchronous RPC call:** server 로 부터 response 가 도착 할 때까지 block 된다. RPC 가 원하는 절차지향 호출에 가장 가까운 개념이다.
    - 반면에, 네트워크는 본질적으로 비동기이고, 많은 시나리오에서 현재 thread 를 block 하지 않고 RPC 를 시작할 수 있다.
- 대부분 언어에서 **gRPC programming API** 동기적/비동기적 형태 둘다 사용가능하다.

### 2-3. gRPC server/client 구현하기

#### 2-3-1. proto 파일 만들기


- `.proto` 만들기

    - [protocol buffer Language Guide](https://developers.google.com/protocol-buffers/docs/proto3) 참고

  ```protobuf
  // file name: aggfunc.proto
  
  // proto3 버전 사용
  syntax = "proto3";
  
  // ...?
  package proto;
  option go_package = "proto/agg";
  
  // 함수 리스트
  service gRPCRouteFuncs {
      rpc sum (InputArgsOfBinaryFunc) returns (ReturnValue);  // rpc protocol 정의, sum 함수 정의
      rpc multiply (InputArgsOfBinaryFunc) returns (ReturnValue);  // rpc protocol 정의, multiply 함수 정의
  }
  
  message InputArgsOfBinaryFunc {
      int32 value1 = 1;  // 숫자는 serialize 순서인듯
      int32 value2 = 2;
  }
  
  message ReturnValue {
      int32 value = 1;
  }
  ```

#### 2-3-2. gRPC server with Go

- protobuf compiler 설치

  ```bash
  # protoc 명령어 설치
  # Linux
  apt install -y protobuf-compiler
  # Mac
  brew install protobuf
  ```

- go grpc plugin 설치

  ```bash
  go get -u google.golang.org/grpc
  go get -u github.com/golang/protobuf/protoc-gen-go
  ```

- protoc 로 go 언어용 proto 파일 만들기

  ```bash
  protoc --go_out=. --go_opt=paths=source_relative
  	--go-grpc_out=. --go-grpc_opt=paths=source_relative
    <proto file 의 경로>/aggfuncs.proto
  ```

- `aggfuncs.pb.go`, `aggfuncs_grpc.pb.go` 파일이 생성됨

- `server.go` 파일에 sum, multiply 함수를 동작 할 수 있도록 코드 작성

    - https://github.com/fwani/gRPC-Test/blob/main/server-script/main.go

#### 2-3-3. gRPC client with Go

- `aggfuncs.pb.go`, `aggfuncs_grpc.pb.go` 파일을 이용
- `client.go` 파일 작성
    - https://github.com/fwani/gRPC-Test/blob/main/client-script/client.go

#### 2-3-4. gRPC client with Python

- requirements 설치

  ```bash
  pip install grpc grpc-tools
  ```

- 위에서 만든 `.proto` 파일을 이용해서 python 용 protoc 로 `aggfuncs_pb2.py`, `aggfuncs_pb2_grpc.py` 파일 생성

  ```bash
  python -m grpc_tools.protoc -I<proto file 의 경로> --python_out=<pb2 output 파일 경로> --grpc_python_out=<pb2_grpc output 파일 경로> aggfuncs.proto 
  ```

- `client.py` 파일 작성

    - https://github.com/fwani/gRPC-Test/blob/main/client-script/client.py

## References

- [Remote Procedure Call (RPC)](https://searchapparchitecture.techtarget.com/definition/Remote-Procedure-Call-RPC)
- [Introduction to gRPC](https://grpc.io/docs/what-is-grpc/introduction/)
- [Core concepts, architecture and lifecycle](https://grpc.io/docs/what-is-grpc/core-concepts/)
- [protocol buffer Language Guide](https://developers.google.com/protocol-buffers/docs/proto3)
- [gRPC with Go Quick start](https://grpc.io/docs/languages/go/quickstart/)
- [gRPC with Python Quick start](https://grpc.io/docs/languages/python/quickstart/)

