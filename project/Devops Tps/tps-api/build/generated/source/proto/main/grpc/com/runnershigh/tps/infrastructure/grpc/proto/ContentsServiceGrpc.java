package com.runnershigh.tps.infrastructure.grpc.proto;

import static io.grpc.MethodDescriptor.generateFullMethodName;

/**
 */
@javax.annotation.Generated(
    value = "by gRPC proto compiler (version 1.60.1)",
    comments = "Source: v1/contents.proto")
@io.grpc.stub.annotations.GrpcGenerated
public final class ContentsServiceGrpc {

  private ContentsServiceGrpc() {}

  public static final java.lang.String SERVICE_NAME = "gitprovider.v1.ContentsService";

  // Static method descriptors that strictly reflect the proto.
  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.GetTreeRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.GetTreeResponse> getGetTreeMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "GetTree",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.GetTreeRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.GetTreeResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.GetTreeRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.GetTreeResponse> getGetTreeMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.GetTreeRequest, com.runnershigh.tps.infrastructure.grpc.proto.GetTreeResponse> getGetTreeMethod;
    if ((getGetTreeMethod = ContentsServiceGrpc.getGetTreeMethod) == null) {
      synchronized (ContentsServiceGrpc.class) {
        if ((getGetTreeMethod = ContentsServiceGrpc.getGetTreeMethod) == null) {
          ContentsServiceGrpc.getGetTreeMethod = getGetTreeMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.GetTreeRequest, com.runnershigh.tps.infrastructure.grpc.proto.GetTreeResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetTree"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.GetTreeRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.GetTreeResponse.getDefaultInstance()))
              .setSchemaDescriptor(new ContentsServiceMethodDescriptorSupplier("GetTree"))
              .build();
        }
      }
    }
    return getGetTreeMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.GetContentsRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.GetContentsResponse> getGetContentsMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "GetContents",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.GetContentsRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.GetContentsResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.GetContentsRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.GetContentsResponse> getGetContentsMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.GetContentsRequest, com.runnershigh.tps.infrastructure.grpc.proto.GetContentsResponse> getGetContentsMethod;
    if ((getGetContentsMethod = ContentsServiceGrpc.getGetContentsMethod) == null) {
      synchronized (ContentsServiceGrpc.class) {
        if ((getGetContentsMethod = ContentsServiceGrpc.getGetContentsMethod) == null) {
          ContentsServiceGrpc.getGetContentsMethod = getGetContentsMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.GetContentsRequest, com.runnershigh.tps.infrastructure.grpc.proto.GetContentsResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetContents"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.GetContentsRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.GetContentsResponse.getDefaultInstance()))
              .setSchemaDescriptor(new ContentsServiceMethodDescriptorSupplier("GetContents"))
              .build();
        }
      }
    }
    return getGetContentsMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.GetReadmeRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.GetReadmeResponse> getGetReadmeMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "GetReadme",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.GetReadmeRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.GetReadmeResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.GetReadmeRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.GetReadmeResponse> getGetReadmeMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.GetReadmeRequest, com.runnershigh.tps.infrastructure.grpc.proto.GetReadmeResponse> getGetReadmeMethod;
    if ((getGetReadmeMethod = ContentsServiceGrpc.getGetReadmeMethod) == null) {
      synchronized (ContentsServiceGrpc.class) {
        if ((getGetReadmeMethod = ContentsServiceGrpc.getGetReadmeMethod) == null) {
          ContentsServiceGrpc.getGetReadmeMethod = getGetReadmeMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.GetReadmeRequest, com.runnershigh.tps.infrastructure.grpc.proto.GetReadmeResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetReadme"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.GetReadmeRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.GetReadmeResponse.getDefaultInstance()))
              .setSchemaDescriptor(new ContentsServiceMethodDescriptorSupplier("GetReadme"))
              .build();
        }
      }
    }
    return getGetReadmeMethod;
  }

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static ContentsServiceStub newStub(io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<ContentsServiceStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<ContentsServiceStub>() {
        @java.lang.Override
        public ContentsServiceStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new ContentsServiceStub(channel, callOptions);
        }
      };
    return ContentsServiceStub.newStub(factory, channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static ContentsServiceBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<ContentsServiceBlockingStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<ContentsServiceBlockingStub>() {
        @java.lang.Override
        public ContentsServiceBlockingStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new ContentsServiceBlockingStub(channel, callOptions);
        }
      };
    return ContentsServiceBlockingStub.newStub(factory, channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static ContentsServiceFutureStub newFutureStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<ContentsServiceFutureStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<ContentsServiceFutureStub>() {
        @java.lang.Override
        public ContentsServiceFutureStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new ContentsServiceFutureStub(channel, callOptions);
        }
      };
    return ContentsServiceFutureStub.newStub(factory, channel);
  }

  /**
   */
  public interface AsyncService {

    /**
     * <pre>
     * 저장소의 전체 파일 트리를 조회합니다.
     * </pre>
     */
    default void getTree(com.runnershigh.tps.infrastructure.grpc.proto.GetTreeRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.GetTreeResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetTreeMethod(), responseObserver);
    }

    /**
     * <pre>
     * 특정 경로의 파일/디렉토리 내용을 조회합니다.
     * </pre>
     */
    default void getContents(com.runnershigh.tps.infrastructure.grpc.proto.GetContentsRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.GetContentsResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetContentsMethod(), responseObserver);
    }

    /**
     * <pre>
     * README 파일을 조회합니다.
     * </pre>
     */
    default void getReadme(com.runnershigh.tps.infrastructure.grpc.proto.GetReadmeRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.GetReadmeResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetReadmeMethod(), responseObserver);
    }
  }

  /**
   * Base class for the server implementation of the service ContentsService.
   */
  public static abstract class ContentsServiceImplBase
      implements io.grpc.BindableService, AsyncService {

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return ContentsServiceGrpc.bindService(this);
    }
  }

  /**
   * A stub to allow clients to do asynchronous rpc calls to service ContentsService.
   */
  public static final class ContentsServiceStub
      extends io.grpc.stub.AbstractAsyncStub<ContentsServiceStub> {
    private ContentsServiceStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected ContentsServiceStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new ContentsServiceStub(channel, callOptions);
    }

    /**
     * <pre>
     * 저장소의 전체 파일 트리를 조회합니다.
     * </pre>
     */
    public void getTree(com.runnershigh.tps.infrastructure.grpc.proto.GetTreeRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.GetTreeResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getGetTreeMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * 특정 경로의 파일/디렉토리 내용을 조회합니다.
     * </pre>
     */
    public void getContents(com.runnershigh.tps.infrastructure.grpc.proto.GetContentsRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.GetContentsResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getGetContentsMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * README 파일을 조회합니다.
     * </pre>
     */
    public void getReadme(com.runnershigh.tps.infrastructure.grpc.proto.GetReadmeRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.GetReadmeResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getGetReadmeMethod(), getCallOptions()), request, responseObserver);
    }
  }

  /**
   * A stub to allow clients to do synchronous rpc calls to service ContentsService.
   */
  public static final class ContentsServiceBlockingStub
      extends io.grpc.stub.AbstractBlockingStub<ContentsServiceBlockingStub> {
    private ContentsServiceBlockingStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected ContentsServiceBlockingStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new ContentsServiceBlockingStub(channel, callOptions);
    }

    /**
     * <pre>
     * 저장소의 전체 파일 트리를 조회합니다.
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.GetTreeResponse getTree(com.runnershigh.tps.infrastructure.grpc.proto.GetTreeRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getGetTreeMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * 특정 경로의 파일/디렉토리 내용을 조회합니다.
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.GetContentsResponse getContents(com.runnershigh.tps.infrastructure.grpc.proto.GetContentsRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getGetContentsMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * README 파일을 조회합니다.
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.GetReadmeResponse getReadme(com.runnershigh.tps.infrastructure.grpc.proto.GetReadmeRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getGetReadmeMethod(), getCallOptions(), request);
    }
  }

  /**
   * A stub to allow clients to do ListenableFuture-style rpc calls to service ContentsService.
   */
  public static final class ContentsServiceFutureStub
      extends io.grpc.stub.AbstractFutureStub<ContentsServiceFutureStub> {
    private ContentsServiceFutureStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected ContentsServiceFutureStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new ContentsServiceFutureStub(channel, callOptions);
    }

    /**
     * <pre>
     * 저장소의 전체 파일 트리를 조회합니다.
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.GetTreeResponse> getTree(
        com.runnershigh.tps.infrastructure.grpc.proto.GetTreeRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getGetTreeMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * 특정 경로의 파일/디렉토리 내용을 조회합니다.
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.GetContentsResponse> getContents(
        com.runnershigh.tps.infrastructure.grpc.proto.GetContentsRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getGetContentsMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * README 파일을 조회합니다.
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.GetReadmeResponse> getReadme(
        com.runnershigh.tps.infrastructure.grpc.proto.GetReadmeRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getGetReadmeMethod(), getCallOptions()), request);
    }
  }

  private static final int METHODID_GET_TREE = 0;
  private static final int METHODID_GET_CONTENTS = 1;
  private static final int METHODID_GET_README = 2;

  private static final class MethodHandlers<Req, Resp> implements
      io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {
    private final AsyncService serviceImpl;
    private final int methodId;

    MethodHandlers(AsyncService serviceImpl, int methodId) {
      this.serviceImpl = serviceImpl;
      this.methodId = methodId;
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        case METHODID_GET_TREE:
          serviceImpl.getTree((com.runnershigh.tps.infrastructure.grpc.proto.GetTreeRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.GetTreeResponse>) responseObserver);
          break;
        case METHODID_GET_CONTENTS:
          serviceImpl.getContents((com.runnershigh.tps.infrastructure.grpc.proto.GetContentsRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.GetContentsResponse>) responseObserver);
          break;
        case METHODID_GET_README:
          serviceImpl.getReadme((com.runnershigh.tps.infrastructure.grpc.proto.GetReadmeRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.GetReadmeResponse>) responseObserver);
          break;
        default:
          throw new AssertionError();
      }
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public io.grpc.stub.StreamObserver<Req> invoke(
        io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        default:
          throw new AssertionError();
      }
    }
  }

  public static final io.grpc.ServerServiceDefinition bindService(AsyncService service) {
    return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor())
        .addMethod(
          getGetTreeMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.GetTreeRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.GetTreeResponse>(
                service, METHODID_GET_TREE)))
        .addMethod(
          getGetContentsMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.GetContentsRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.GetContentsResponse>(
                service, METHODID_GET_CONTENTS)))
        .addMethod(
          getGetReadmeMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.GetReadmeRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.GetReadmeResponse>(
                service, METHODID_GET_README)))
        .build();
  }

  private static abstract class ContentsServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    ContentsServiceBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return com.runnershigh.tps.infrastructure.grpc.proto.ContentsProto.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("ContentsService");
    }
  }

  private static final class ContentsServiceFileDescriptorSupplier
      extends ContentsServiceBaseDescriptorSupplier {
    ContentsServiceFileDescriptorSupplier() {}
  }

  private static final class ContentsServiceMethodDescriptorSupplier
      extends ContentsServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final java.lang.String methodName;

    ContentsServiceMethodDescriptorSupplier(java.lang.String methodName) {
      this.methodName = methodName;
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.MethodDescriptor getMethodDescriptor() {
      return getServiceDescriptor().findMethodByName(methodName);
    }
  }

  private static volatile io.grpc.ServiceDescriptor serviceDescriptor;

  public static io.grpc.ServiceDescriptor getServiceDescriptor() {
    io.grpc.ServiceDescriptor result = serviceDescriptor;
    if (result == null) {
      synchronized (ContentsServiceGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new ContentsServiceFileDescriptorSupplier())
              .addMethod(getGetTreeMethod())
              .addMethod(getGetContentsMethod())
              .addMethod(getGetReadmeMethod())
              .build();
        }
      }
    }
    return result;
  }
}
