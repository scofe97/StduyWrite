package com.runnershigh.tps.infrastructure.grpc.proto;

import static io.grpc.MethodDescriptor.generateFullMethodName;

/**
 */
@javax.annotation.Generated(
    value = "by gRPC proto compiler (version 1.60.1)",
    comments = "Source: v1/provider.proto")
@io.grpc.stub.annotations.GrpcGenerated
public final class ProviderServiceGrpc {

  private ProviderServiceGrpc() {}

  public static final java.lang.String SERVICE_NAME = "gitprovider.v1.ProviderService";

  // Static method descriptors that strictly reflect the proto.
  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.RegisterProviderRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.RegisterProviderResponse> getRegisterProviderMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "RegisterProvider",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.RegisterProviderRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.RegisterProviderResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.RegisterProviderRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.RegisterProviderResponse> getRegisterProviderMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.RegisterProviderRequest, com.runnershigh.tps.infrastructure.grpc.proto.RegisterProviderResponse> getRegisterProviderMethod;
    if ((getRegisterProviderMethod = ProviderServiceGrpc.getRegisterProviderMethod) == null) {
      synchronized (ProviderServiceGrpc.class) {
        if ((getRegisterProviderMethod = ProviderServiceGrpc.getRegisterProviderMethod) == null) {
          ProviderServiceGrpc.getRegisterProviderMethod = getRegisterProviderMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.RegisterProviderRequest, com.runnershigh.tps.infrastructure.grpc.proto.RegisterProviderResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "RegisterProvider"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.RegisterProviderRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.RegisterProviderResponse.getDefaultInstance()))
              .setSchemaDescriptor(new ProviderServiceMethodDescriptorSupplier("RegisterProvider"))
              .build();
        }
      }
    }
    return getRegisterProviderMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.GetProviderRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.GetProviderResponse> getGetProviderMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "GetProvider",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.GetProviderRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.GetProviderResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.GetProviderRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.GetProviderResponse> getGetProviderMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.GetProviderRequest, com.runnershigh.tps.infrastructure.grpc.proto.GetProviderResponse> getGetProviderMethod;
    if ((getGetProviderMethod = ProviderServiceGrpc.getGetProviderMethod) == null) {
      synchronized (ProviderServiceGrpc.class) {
        if ((getGetProviderMethod = ProviderServiceGrpc.getGetProviderMethod) == null) {
          ProviderServiceGrpc.getGetProviderMethod = getGetProviderMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.GetProviderRequest, com.runnershigh.tps.infrastructure.grpc.proto.GetProviderResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetProvider"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.GetProviderRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.GetProviderResponse.getDefaultInstance()))
              .setSchemaDescriptor(new ProviderServiceMethodDescriptorSupplier("GetProvider"))
              .build();
        }
      }
    }
    return getGetProviderMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListProvidersRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.ListProvidersResponse> getListProvidersMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "ListProviders",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.ListProvidersRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.ListProvidersResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListProvidersRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.ListProvidersResponse> getListProvidersMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListProvidersRequest, com.runnershigh.tps.infrastructure.grpc.proto.ListProvidersResponse> getListProvidersMethod;
    if ((getListProvidersMethod = ProviderServiceGrpc.getListProvidersMethod) == null) {
      synchronized (ProviderServiceGrpc.class) {
        if ((getListProvidersMethod = ProviderServiceGrpc.getListProvidersMethod) == null) {
          ProviderServiceGrpc.getListProvidersMethod = getListProvidersMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.ListProvidersRequest, com.runnershigh.tps.infrastructure.grpc.proto.ListProvidersResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListProviders"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.ListProvidersRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.ListProvidersResponse.getDefaultInstance()))
              .setSchemaDescriptor(new ProviderServiceMethodDescriptorSupplier("ListProviders"))
              .build();
        }
      }
    }
    return getListProvidersMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.DeleteProviderRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.DeleteProviderResponse> getDeleteProviderMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "DeleteProvider",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.DeleteProviderRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.DeleteProviderResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.DeleteProviderRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.DeleteProviderResponse> getDeleteProviderMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.DeleteProviderRequest, com.runnershigh.tps.infrastructure.grpc.proto.DeleteProviderResponse> getDeleteProviderMethod;
    if ((getDeleteProviderMethod = ProviderServiceGrpc.getDeleteProviderMethod) == null) {
      synchronized (ProviderServiceGrpc.class) {
        if ((getDeleteProviderMethod = ProviderServiceGrpc.getDeleteProviderMethod) == null) {
          ProviderServiceGrpc.getDeleteProviderMethod = getDeleteProviderMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.DeleteProviderRequest, com.runnershigh.tps.infrastructure.grpc.proto.DeleteProviderResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "DeleteProvider"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.DeleteProviderRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.DeleteProviderResponse.getDefaultInstance()))
              .setSchemaDescriptor(new ProviderServiceMethodDescriptorSupplier("DeleteProvider"))
              .build();
        }
      }
    }
    return getDeleteProviderMethod;
  }

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static ProviderServiceStub newStub(io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<ProviderServiceStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<ProviderServiceStub>() {
        @java.lang.Override
        public ProviderServiceStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new ProviderServiceStub(channel, callOptions);
        }
      };
    return ProviderServiceStub.newStub(factory, channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static ProviderServiceBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<ProviderServiceBlockingStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<ProviderServiceBlockingStub>() {
        @java.lang.Override
        public ProviderServiceBlockingStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new ProviderServiceBlockingStub(channel, callOptions);
        }
      };
    return ProviderServiceBlockingStub.newStub(factory, channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static ProviderServiceFutureStub newFutureStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<ProviderServiceFutureStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<ProviderServiceFutureStub>() {
        @java.lang.Override
        public ProviderServiceFutureStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new ProviderServiceFutureStub(channel, callOptions);
        }
      };
    return ProviderServiceFutureStub.newStub(factory, channel);
  }

  /**
   */
  public interface AsyncService {

    /**
     */
    default void registerProvider(com.runnershigh.tps.infrastructure.grpc.proto.RegisterProviderRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.RegisterProviderResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getRegisterProviderMethod(), responseObserver);
    }

    /**
     */
    default void getProvider(com.runnershigh.tps.infrastructure.grpc.proto.GetProviderRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.GetProviderResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetProviderMethod(), responseObserver);
    }

    /**
     */
    default void listProviders(com.runnershigh.tps.infrastructure.grpc.proto.ListProvidersRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListProvidersResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListProvidersMethod(), responseObserver);
    }

    /**
     */
    default void deleteProvider(com.runnershigh.tps.infrastructure.grpc.proto.DeleteProviderRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.DeleteProviderResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getDeleteProviderMethod(), responseObserver);
    }
  }

  /**
   * Base class for the server implementation of the service ProviderService.
   */
  public static abstract class ProviderServiceImplBase
      implements io.grpc.BindableService, AsyncService {

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return ProviderServiceGrpc.bindService(this);
    }
  }

  /**
   * A stub to allow clients to do asynchronous rpc calls to service ProviderService.
   */
  public static final class ProviderServiceStub
      extends io.grpc.stub.AbstractAsyncStub<ProviderServiceStub> {
    private ProviderServiceStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected ProviderServiceStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new ProviderServiceStub(channel, callOptions);
    }

    /**
     */
    public void registerProvider(com.runnershigh.tps.infrastructure.grpc.proto.RegisterProviderRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.RegisterProviderResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getRegisterProviderMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     */
    public void getProvider(com.runnershigh.tps.infrastructure.grpc.proto.GetProviderRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.GetProviderResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getGetProviderMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     */
    public void listProviders(com.runnershigh.tps.infrastructure.grpc.proto.ListProvidersRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListProvidersResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getListProvidersMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     */
    public void deleteProvider(com.runnershigh.tps.infrastructure.grpc.proto.DeleteProviderRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.DeleteProviderResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getDeleteProviderMethod(), getCallOptions()), request, responseObserver);
    }
  }

  /**
   * A stub to allow clients to do synchronous rpc calls to service ProviderService.
   */
  public static final class ProviderServiceBlockingStub
      extends io.grpc.stub.AbstractBlockingStub<ProviderServiceBlockingStub> {
    private ProviderServiceBlockingStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected ProviderServiceBlockingStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new ProviderServiceBlockingStub(channel, callOptions);
    }

    /**
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.RegisterProviderResponse registerProvider(com.runnershigh.tps.infrastructure.grpc.proto.RegisterProviderRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getRegisterProviderMethod(), getCallOptions(), request);
    }

    /**
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.GetProviderResponse getProvider(com.runnershigh.tps.infrastructure.grpc.proto.GetProviderRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getGetProviderMethod(), getCallOptions(), request);
    }

    /**
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.ListProvidersResponse listProviders(com.runnershigh.tps.infrastructure.grpc.proto.ListProvidersRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getListProvidersMethod(), getCallOptions(), request);
    }

    /**
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.DeleteProviderResponse deleteProvider(com.runnershigh.tps.infrastructure.grpc.proto.DeleteProviderRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getDeleteProviderMethod(), getCallOptions(), request);
    }
  }

  /**
   * A stub to allow clients to do ListenableFuture-style rpc calls to service ProviderService.
   */
  public static final class ProviderServiceFutureStub
      extends io.grpc.stub.AbstractFutureStub<ProviderServiceFutureStub> {
    private ProviderServiceFutureStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected ProviderServiceFutureStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new ProviderServiceFutureStub(channel, callOptions);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.RegisterProviderResponse> registerProvider(
        com.runnershigh.tps.infrastructure.grpc.proto.RegisterProviderRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getRegisterProviderMethod(), getCallOptions()), request);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.GetProviderResponse> getProvider(
        com.runnershigh.tps.infrastructure.grpc.proto.GetProviderRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getGetProviderMethod(), getCallOptions()), request);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.ListProvidersResponse> listProviders(
        com.runnershigh.tps.infrastructure.grpc.proto.ListProvidersRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getListProvidersMethod(), getCallOptions()), request);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.DeleteProviderResponse> deleteProvider(
        com.runnershigh.tps.infrastructure.grpc.proto.DeleteProviderRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getDeleteProviderMethod(), getCallOptions()), request);
    }
  }

  private static final int METHODID_REGISTER_PROVIDER = 0;
  private static final int METHODID_GET_PROVIDER = 1;
  private static final int METHODID_LIST_PROVIDERS = 2;
  private static final int METHODID_DELETE_PROVIDER = 3;

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
        case METHODID_REGISTER_PROVIDER:
          serviceImpl.registerProvider((com.runnershigh.tps.infrastructure.grpc.proto.RegisterProviderRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.RegisterProviderResponse>) responseObserver);
          break;
        case METHODID_GET_PROVIDER:
          serviceImpl.getProvider((com.runnershigh.tps.infrastructure.grpc.proto.GetProviderRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.GetProviderResponse>) responseObserver);
          break;
        case METHODID_LIST_PROVIDERS:
          serviceImpl.listProviders((com.runnershigh.tps.infrastructure.grpc.proto.ListProvidersRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListProvidersResponse>) responseObserver);
          break;
        case METHODID_DELETE_PROVIDER:
          serviceImpl.deleteProvider((com.runnershigh.tps.infrastructure.grpc.proto.DeleteProviderRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.DeleteProviderResponse>) responseObserver);
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
          getRegisterProviderMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.RegisterProviderRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.RegisterProviderResponse>(
                service, METHODID_REGISTER_PROVIDER)))
        .addMethod(
          getGetProviderMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.GetProviderRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.GetProviderResponse>(
                service, METHODID_GET_PROVIDER)))
        .addMethod(
          getListProvidersMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.ListProvidersRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.ListProvidersResponse>(
                service, METHODID_LIST_PROVIDERS)))
        .addMethod(
          getDeleteProviderMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.DeleteProviderRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.DeleteProviderResponse>(
                service, METHODID_DELETE_PROVIDER)))
        .build();
  }

  private static abstract class ProviderServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    ProviderServiceBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return com.runnershigh.tps.infrastructure.grpc.proto.ProviderProto.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("ProviderService");
    }
  }

  private static final class ProviderServiceFileDescriptorSupplier
      extends ProviderServiceBaseDescriptorSupplier {
    ProviderServiceFileDescriptorSupplier() {}
  }

  private static final class ProviderServiceMethodDescriptorSupplier
      extends ProviderServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final java.lang.String methodName;

    ProviderServiceMethodDescriptorSupplier(java.lang.String methodName) {
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
      synchronized (ProviderServiceGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new ProviderServiceFileDescriptorSupplier())
              .addMethod(getRegisterProviderMethod())
              .addMethod(getGetProviderMethod())
              .addMethod(getListProvidersMethod())
              .addMethod(getDeleteProviderMethod())
              .build();
        }
      }
    }
    return result;
  }
}
