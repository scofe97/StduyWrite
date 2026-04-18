package com.runnershigh.tps.infrastructure.grpc.proto;

import static io.grpc.MethodDescriptor.generateFullMethodName;

/**
 */
@javax.annotation.Generated(
    value = "by gRPC proto compiler (version 1.60.1)",
    comments = "Source: v1/branch.proto")
@io.grpc.stub.annotations.GrpcGenerated
public final class BranchServiceGrpc {

  private BranchServiceGrpc() {}

  public static final java.lang.String SERVICE_NAME = "gitprovider.v1.BranchService";

  // Static method descriptors that strictly reflect the proto.
  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.CompareBranchesRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.CompareBranchesResponse> getCompareBranchesMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "CompareBranches",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.CompareBranchesRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.CompareBranchesResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.CompareBranchesRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.CompareBranchesResponse> getCompareBranchesMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.CompareBranchesRequest, com.runnershigh.tps.infrastructure.grpc.proto.CompareBranchesResponse> getCompareBranchesMethod;
    if ((getCompareBranchesMethod = BranchServiceGrpc.getCompareBranchesMethod) == null) {
      synchronized (BranchServiceGrpc.class) {
        if ((getCompareBranchesMethod = BranchServiceGrpc.getCompareBranchesMethod) == null) {
          BranchServiceGrpc.getCompareBranchesMethod = getCompareBranchesMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.CompareBranchesRequest, com.runnershigh.tps.infrastructure.grpc.proto.CompareBranchesResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "CompareBranches"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.CompareBranchesRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.CompareBranchesResponse.getDefaultInstance()))
              .setSchemaDescriptor(new BranchServiceMethodDescriptorSupplier("CompareBranches"))
              .build();
        }
      }
    }
    return getCompareBranchesMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListCommitsDiffRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.ListCommitsDiffResponse> getListCommitsDiffMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "ListCommitsDiff",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.ListCommitsDiffRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.ListCommitsDiffResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListCommitsDiffRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.ListCommitsDiffResponse> getListCommitsDiffMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListCommitsDiffRequest, com.runnershigh.tps.infrastructure.grpc.proto.ListCommitsDiffResponse> getListCommitsDiffMethod;
    if ((getListCommitsDiffMethod = BranchServiceGrpc.getListCommitsDiffMethod) == null) {
      synchronized (BranchServiceGrpc.class) {
        if ((getListCommitsDiffMethod = BranchServiceGrpc.getListCommitsDiffMethod) == null) {
          BranchServiceGrpc.getListCommitsDiffMethod = getListCommitsDiffMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.ListCommitsDiffRequest, com.runnershigh.tps.infrastructure.grpc.proto.ListCommitsDiffResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListCommitsDiff"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.ListCommitsDiffRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.ListCommitsDiffResponse.getDefaultInstance()))
              .setSchemaDescriptor(new BranchServiceMethodDescriptorSupplier("ListCommitsDiff"))
              .build();
        }
      }
    }
    return getListCommitsDiffMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListMergedBranchesRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.ListMergedBranchesResponse> getListMergedBranchesMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "ListMergedBranches",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.ListMergedBranchesRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.ListMergedBranchesResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListMergedBranchesRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.ListMergedBranchesResponse> getListMergedBranchesMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListMergedBranchesRequest, com.runnershigh.tps.infrastructure.grpc.proto.ListMergedBranchesResponse> getListMergedBranchesMethod;
    if ((getListMergedBranchesMethod = BranchServiceGrpc.getListMergedBranchesMethod) == null) {
      synchronized (BranchServiceGrpc.class) {
        if ((getListMergedBranchesMethod = BranchServiceGrpc.getListMergedBranchesMethod) == null) {
          BranchServiceGrpc.getListMergedBranchesMethod = getListMergedBranchesMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.ListMergedBranchesRequest, com.runnershigh.tps.infrastructure.grpc.proto.ListMergedBranchesResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListMergedBranches"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.ListMergedBranchesRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.ListMergedBranchesResponse.getDefaultInstance()))
              .setSchemaDescriptor(new BranchServiceMethodDescriptorSupplier("ListMergedBranches"))
              .build();
        }
      }
    }
    return getListMergedBranchesMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListStaleBranchesRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.ListStaleBranchesResponse> getListStaleBranchesMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "ListStaleBranches",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.ListStaleBranchesRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.ListStaleBranchesResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListStaleBranchesRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.ListStaleBranchesResponse> getListStaleBranchesMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListStaleBranchesRequest, com.runnershigh.tps.infrastructure.grpc.proto.ListStaleBranchesResponse> getListStaleBranchesMethod;
    if ((getListStaleBranchesMethod = BranchServiceGrpc.getListStaleBranchesMethod) == null) {
      synchronized (BranchServiceGrpc.class) {
        if ((getListStaleBranchesMethod = BranchServiceGrpc.getListStaleBranchesMethod) == null) {
          BranchServiceGrpc.getListStaleBranchesMethod = getListStaleBranchesMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.ListStaleBranchesRequest, com.runnershigh.tps.infrastructure.grpc.proto.ListStaleBranchesResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListStaleBranches"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.ListStaleBranchesRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.ListStaleBranchesResponse.getDefaultInstance()))
              .setSchemaDescriptor(new BranchServiceMethodDescriptorSupplier("ListStaleBranches"))
              .build();
        }
      }
    }
    return getListStaleBranchesMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.CleanupBranchesRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.CleanupBranchesResponse> getCleanupBranchesMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "CleanupBranches",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.CleanupBranchesRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.CleanupBranchesResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.CleanupBranchesRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.CleanupBranchesResponse> getCleanupBranchesMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.CleanupBranchesRequest, com.runnershigh.tps.infrastructure.grpc.proto.CleanupBranchesResponse> getCleanupBranchesMethod;
    if ((getCleanupBranchesMethod = BranchServiceGrpc.getCleanupBranchesMethod) == null) {
      synchronized (BranchServiceGrpc.class) {
        if ((getCleanupBranchesMethod = BranchServiceGrpc.getCleanupBranchesMethod) == null) {
          BranchServiceGrpc.getCleanupBranchesMethod = getCleanupBranchesMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.CleanupBranchesRequest, com.runnershigh.tps.infrastructure.grpc.proto.CleanupBranchesResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "CleanupBranches"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.CleanupBranchesRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.CleanupBranchesResponse.getDefaultInstance()))
              .setSchemaDescriptor(new BranchServiceMethodDescriptorSupplier("CleanupBranches"))
              .build();
        }
      }
    }
    return getCleanupBranchesMethod;
  }

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static BranchServiceStub newStub(io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<BranchServiceStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<BranchServiceStub>() {
        @java.lang.Override
        public BranchServiceStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new BranchServiceStub(channel, callOptions);
        }
      };
    return BranchServiceStub.newStub(factory, channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static BranchServiceBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<BranchServiceBlockingStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<BranchServiceBlockingStub>() {
        @java.lang.Override
        public BranchServiceBlockingStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new BranchServiceBlockingStub(channel, callOptions);
        }
      };
    return BranchServiceBlockingStub.newStub(factory, channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static BranchServiceFutureStub newFutureStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<BranchServiceFutureStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<BranchServiceFutureStub>() {
        @java.lang.Override
        public BranchServiceFutureStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new BranchServiceFutureStub(channel, callOptions);
        }
      };
    return BranchServiceFutureStub.newStub(factory, channel);
  }

  /**
   */
  public interface AsyncService {

    /**
     * <pre>
     * 브랜치 비교
     * </pre>
     */
    default void compareBranches(com.runnershigh.tps.infrastructure.grpc.proto.CompareBranchesRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.CompareBranchesResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getCompareBranchesMethod(), responseObserver);
    }

    /**
     * <pre>
     * 커밋 차이 목록
     * </pre>
     */
    default void listCommitsDiff(com.runnershigh.tps.infrastructure.grpc.proto.ListCommitsDiffRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListCommitsDiffResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListCommitsDiffMethod(), responseObserver);
    }

    /**
     * <pre>
     * 머지된 브랜치 목록
     * </pre>
     */
    default void listMergedBranches(com.runnershigh.tps.infrastructure.grpc.proto.ListMergedBranchesRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListMergedBranchesResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListMergedBranchesMethod(), responseObserver);
    }

    /**
     * <pre>
     * Stale 브랜치 목록
     * </pre>
     */
    default void listStaleBranches(com.runnershigh.tps.infrastructure.grpc.proto.ListStaleBranchesRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListStaleBranchesResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListStaleBranchesMethod(), responseObserver);
    }

    /**
     * <pre>
     * 브랜치 정리
     * </pre>
     */
    default void cleanupBranches(com.runnershigh.tps.infrastructure.grpc.proto.CleanupBranchesRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.CleanupBranchesResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getCleanupBranchesMethod(), responseObserver);
    }
  }

  /**
   * Base class for the server implementation of the service BranchService.
   */
  public static abstract class BranchServiceImplBase
      implements io.grpc.BindableService, AsyncService {

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return BranchServiceGrpc.bindService(this);
    }
  }

  /**
   * A stub to allow clients to do asynchronous rpc calls to service BranchService.
   */
  public static final class BranchServiceStub
      extends io.grpc.stub.AbstractAsyncStub<BranchServiceStub> {
    private BranchServiceStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected BranchServiceStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new BranchServiceStub(channel, callOptions);
    }

    /**
     * <pre>
     * 브랜치 비교
     * </pre>
     */
    public void compareBranches(com.runnershigh.tps.infrastructure.grpc.proto.CompareBranchesRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.CompareBranchesResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getCompareBranchesMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * 커밋 차이 목록
     * </pre>
     */
    public void listCommitsDiff(com.runnershigh.tps.infrastructure.grpc.proto.ListCommitsDiffRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListCommitsDiffResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getListCommitsDiffMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * 머지된 브랜치 목록
     * </pre>
     */
    public void listMergedBranches(com.runnershigh.tps.infrastructure.grpc.proto.ListMergedBranchesRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListMergedBranchesResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getListMergedBranchesMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * Stale 브랜치 목록
     * </pre>
     */
    public void listStaleBranches(com.runnershigh.tps.infrastructure.grpc.proto.ListStaleBranchesRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListStaleBranchesResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getListStaleBranchesMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * 브랜치 정리
     * </pre>
     */
    public void cleanupBranches(com.runnershigh.tps.infrastructure.grpc.proto.CleanupBranchesRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.CleanupBranchesResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getCleanupBranchesMethod(), getCallOptions()), request, responseObserver);
    }
  }

  /**
   * A stub to allow clients to do synchronous rpc calls to service BranchService.
   */
  public static final class BranchServiceBlockingStub
      extends io.grpc.stub.AbstractBlockingStub<BranchServiceBlockingStub> {
    private BranchServiceBlockingStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected BranchServiceBlockingStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new BranchServiceBlockingStub(channel, callOptions);
    }

    /**
     * <pre>
     * 브랜치 비교
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.CompareBranchesResponse compareBranches(com.runnershigh.tps.infrastructure.grpc.proto.CompareBranchesRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getCompareBranchesMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * 커밋 차이 목록
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.ListCommitsDiffResponse listCommitsDiff(com.runnershigh.tps.infrastructure.grpc.proto.ListCommitsDiffRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getListCommitsDiffMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * 머지된 브랜치 목록
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.ListMergedBranchesResponse listMergedBranches(com.runnershigh.tps.infrastructure.grpc.proto.ListMergedBranchesRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getListMergedBranchesMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * Stale 브랜치 목록
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.ListStaleBranchesResponse listStaleBranches(com.runnershigh.tps.infrastructure.grpc.proto.ListStaleBranchesRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getListStaleBranchesMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * 브랜치 정리
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.CleanupBranchesResponse cleanupBranches(com.runnershigh.tps.infrastructure.grpc.proto.CleanupBranchesRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getCleanupBranchesMethod(), getCallOptions(), request);
    }
  }

  /**
   * A stub to allow clients to do ListenableFuture-style rpc calls to service BranchService.
   */
  public static final class BranchServiceFutureStub
      extends io.grpc.stub.AbstractFutureStub<BranchServiceFutureStub> {
    private BranchServiceFutureStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected BranchServiceFutureStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new BranchServiceFutureStub(channel, callOptions);
    }

    /**
     * <pre>
     * 브랜치 비교
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.CompareBranchesResponse> compareBranches(
        com.runnershigh.tps.infrastructure.grpc.proto.CompareBranchesRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getCompareBranchesMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * 커밋 차이 목록
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.ListCommitsDiffResponse> listCommitsDiff(
        com.runnershigh.tps.infrastructure.grpc.proto.ListCommitsDiffRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getListCommitsDiffMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * 머지된 브랜치 목록
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.ListMergedBranchesResponse> listMergedBranches(
        com.runnershigh.tps.infrastructure.grpc.proto.ListMergedBranchesRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getListMergedBranchesMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * Stale 브랜치 목록
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.ListStaleBranchesResponse> listStaleBranches(
        com.runnershigh.tps.infrastructure.grpc.proto.ListStaleBranchesRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getListStaleBranchesMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * 브랜치 정리
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.CleanupBranchesResponse> cleanupBranches(
        com.runnershigh.tps.infrastructure.grpc.proto.CleanupBranchesRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getCleanupBranchesMethod(), getCallOptions()), request);
    }
  }

  private static final int METHODID_COMPARE_BRANCHES = 0;
  private static final int METHODID_LIST_COMMITS_DIFF = 1;
  private static final int METHODID_LIST_MERGED_BRANCHES = 2;
  private static final int METHODID_LIST_STALE_BRANCHES = 3;
  private static final int METHODID_CLEANUP_BRANCHES = 4;

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
        case METHODID_COMPARE_BRANCHES:
          serviceImpl.compareBranches((com.runnershigh.tps.infrastructure.grpc.proto.CompareBranchesRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.CompareBranchesResponse>) responseObserver);
          break;
        case METHODID_LIST_COMMITS_DIFF:
          serviceImpl.listCommitsDiff((com.runnershigh.tps.infrastructure.grpc.proto.ListCommitsDiffRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListCommitsDiffResponse>) responseObserver);
          break;
        case METHODID_LIST_MERGED_BRANCHES:
          serviceImpl.listMergedBranches((com.runnershigh.tps.infrastructure.grpc.proto.ListMergedBranchesRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListMergedBranchesResponse>) responseObserver);
          break;
        case METHODID_LIST_STALE_BRANCHES:
          serviceImpl.listStaleBranches((com.runnershigh.tps.infrastructure.grpc.proto.ListStaleBranchesRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListStaleBranchesResponse>) responseObserver);
          break;
        case METHODID_CLEANUP_BRANCHES:
          serviceImpl.cleanupBranches((com.runnershigh.tps.infrastructure.grpc.proto.CleanupBranchesRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.CleanupBranchesResponse>) responseObserver);
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
          getCompareBranchesMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.CompareBranchesRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.CompareBranchesResponse>(
                service, METHODID_COMPARE_BRANCHES)))
        .addMethod(
          getListCommitsDiffMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.ListCommitsDiffRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.ListCommitsDiffResponse>(
                service, METHODID_LIST_COMMITS_DIFF)))
        .addMethod(
          getListMergedBranchesMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.ListMergedBranchesRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.ListMergedBranchesResponse>(
                service, METHODID_LIST_MERGED_BRANCHES)))
        .addMethod(
          getListStaleBranchesMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.ListStaleBranchesRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.ListStaleBranchesResponse>(
                service, METHODID_LIST_STALE_BRANCHES)))
        .addMethod(
          getCleanupBranchesMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.CleanupBranchesRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.CleanupBranchesResponse>(
                service, METHODID_CLEANUP_BRANCHES)))
        .build();
  }

  private static abstract class BranchServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    BranchServiceBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return com.runnershigh.tps.infrastructure.grpc.proto.BranchProto.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("BranchService");
    }
  }

  private static final class BranchServiceFileDescriptorSupplier
      extends BranchServiceBaseDescriptorSupplier {
    BranchServiceFileDescriptorSupplier() {}
  }

  private static final class BranchServiceMethodDescriptorSupplier
      extends BranchServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final java.lang.String methodName;

    BranchServiceMethodDescriptorSupplier(java.lang.String methodName) {
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
      synchronized (BranchServiceGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new BranchServiceFileDescriptorSupplier())
              .addMethod(getCompareBranchesMethod())
              .addMethod(getListCommitsDiffMethod())
              .addMethod(getListMergedBranchesMethod())
              .addMethod(getListStaleBranchesMethod())
              .addMethod(getCleanupBranchesMethod())
              .build();
        }
      }
    }
    return result;
  }
}
