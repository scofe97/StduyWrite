package com.runnershigh.tps.infrastructure.grpc.proto;

import static io.grpc.MethodDescriptor.generateFullMethodName;

/**
 * <pre>
 * === 저장소 ===
 * </pre>
 */
@javax.annotation.Generated(
    value = "by gRPC proto compiler (version 1.60.1)",
    comments = "Source: v1/provider.proto")
@io.grpc.stub.annotations.GrpcGenerated
public final class GitServiceGrpc {

  private GitServiceGrpc() {}

  public static final java.lang.String SERVICE_NAME = "gitprovider.v1.GitService";

  // Static method descriptors that strictly reflect the proto.
  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListRepositoriesRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.ListRepositoriesResponse> getListRepositoriesMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "ListRepositories",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.ListRepositoriesRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.ListRepositoriesResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListRepositoriesRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.ListRepositoriesResponse> getListRepositoriesMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListRepositoriesRequest, com.runnershigh.tps.infrastructure.grpc.proto.ListRepositoriesResponse> getListRepositoriesMethod;
    if ((getListRepositoriesMethod = GitServiceGrpc.getListRepositoriesMethod) == null) {
      synchronized (GitServiceGrpc.class) {
        if ((getListRepositoriesMethod = GitServiceGrpc.getListRepositoriesMethod) == null) {
          GitServiceGrpc.getListRepositoriesMethod = getListRepositoriesMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.ListRepositoriesRequest, com.runnershigh.tps.infrastructure.grpc.proto.ListRepositoriesResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListRepositories"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.ListRepositoriesRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.ListRepositoriesResponse.getDefaultInstance()))
              .setSchemaDescriptor(new GitServiceMethodDescriptorSupplier("ListRepositories"))
              .build();
        }
      }
    }
    return getListRepositoriesMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.GetRepositoryRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.GetRepositoryResponse> getGetRepositoryMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "GetRepository",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.GetRepositoryRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.GetRepositoryResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.GetRepositoryRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.GetRepositoryResponse> getGetRepositoryMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.GetRepositoryRequest, com.runnershigh.tps.infrastructure.grpc.proto.GetRepositoryResponse> getGetRepositoryMethod;
    if ((getGetRepositoryMethod = GitServiceGrpc.getGetRepositoryMethod) == null) {
      synchronized (GitServiceGrpc.class) {
        if ((getGetRepositoryMethod = GitServiceGrpc.getGetRepositoryMethod) == null) {
          GitServiceGrpc.getGetRepositoryMethod = getGetRepositoryMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.GetRepositoryRequest, com.runnershigh.tps.infrastructure.grpc.proto.GetRepositoryResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetRepository"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.GetRepositoryRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.GetRepositoryResponse.getDefaultInstance()))
              .setSchemaDescriptor(new GitServiceMethodDescriptorSupplier("GetRepository"))
              .build();
        }
      }
    }
    return getGetRepositoryMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.CreateRepositoryRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.CreateRepositoryResponse> getCreateRepositoryMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "CreateRepository",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.CreateRepositoryRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.CreateRepositoryResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.CreateRepositoryRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.CreateRepositoryResponse> getCreateRepositoryMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.CreateRepositoryRequest, com.runnershigh.tps.infrastructure.grpc.proto.CreateRepositoryResponse> getCreateRepositoryMethod;
    if ((getCreateRepositoryMethod = GitServiceGrpc.getCreateRepositoryMethod) == null) {
      synchronized (GitServiceGrpc.class) {
        if ((getCreateRepositoryMethod = GitServiceGrpc.getCreateRepositoryMethod) == null) {
          GitServiceGrpc.getCreateRepositoryMethod = getCreateRepositoryMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.CreateRepositoryRequest, com.runnershigh.tps.infrastructure.grpc.proto.CreateRepositoryResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "CreateRepository"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.CreateRepositoryRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.CreateRepositoryResponse.getDefaultInstance()))
              .setSchemaDescriptor(new GitServiceMethodDescriptorSupplier("CreateRepository"))
              .build();
        }
      }
    }
    return getCreateRepositoryMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.DeleteRepositoryRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.DeleteRepositoryResponse> getDeleteRepositoryMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "DeleteRepository",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.DeleteRepositoryRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.DeleteRepositoryResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.DeleteRepositoryRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.DeleteRepositoryResponse> getDeleteRepositoryMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.DeleteRepositoryRequest, com.runnershigh.tps.infrastructure.grpc.proto.DeleteRepositoryResponse> getDeleteRepositoryMethod;
    if ((getDeleteRepositoryMethod = GitServiceGrpc.getDeleteRepositoryMethod) == null) {
      synchronized (GitServiceGrpc.class) {
        if ((getDeleteRepositoryMethod = GitServiceGrpc.getDeleteRepositoryMethod) == null) {
          GitServiceGrpc.getDeleteRepositoryMethod = getDeleteRepositoryMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.DeleteRepositoryRequest, com.runnershigh.tps.infrastructure.grpc.proto.DeleteRepositoryResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "DeleteRepository"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.DeleteRepositoryRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.DeleteRepositoryResponse.getDefaultInstance()))
              .setSchemaDescriptor(new GitServiceMethodDescriptorSupplier("DeleteRepository"))
              .build();
        }
      }
    }
    return getDeleteRepositoryMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListBranchesRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.ListBranchesResponse> getListBranchesMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "ListBranches",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.ListBranchesRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.ListBranchesResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListBranchesRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.ListBranchesResponse> getListBranchesMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListBranchesRequest, com.runnershigh.tps.infrastructure.grpc.proto.ListBranchesResponse> getListBranchesMethod;
    if ((getListBranchesMethod = GitServiceGrpc.getListBranchesMethod) == null) {
      synchronized (GitServiceGrpc.class) {
        if ((getListBranchesMethod = GitServiceGrpc.getListBranchesMethod) == null) {
          GitServiceGrpc.getListBranchesMethod = getListBranchesMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.ListBranchesRequest, com.runnershigh.tps.infrastructure.grpc.proto.ListBranchesResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListBranches"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.ListBranchesRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.ListBranchesResponse.getDefaultInstance()))
              .setSchemaDescriptor(new GitServiceMethodDescriptorSupplier("ListBranches"))
              .build();
        }
      }
    }
    return getListBranchesMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.GetBranchRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.GetBranchResponse> getGetBranchMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "GetBranch",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.GetBranchRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.GetBranchResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.GetBranchRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.GetBranchResponse> getGetBranchMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.GetBranchRequest, com.runnershigh.tps.infrastructure.grpc.proto.GetBranchResponse> getGetBranchMethod;
    if ((getGetBranchMethod = GitServiceGrpc.getGetBranchMethod) == null) {
      synchronized (GitServiceGrpc.class) {
        if ((getGetBranchMethod = GitServiceGrpc.getGetBranchMethod) == null) {
          GitServiceGrpc.getGetBranchMethod = getGetBranchMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.GetBranchRequest, com.runnershigh.tps.infrastructure.grpc.proto.GetBranchResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetBranch"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.GetBranchRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.GetBranchResponse.getDefaultInstance()))
              .setSchemaDescriptor(new GitServiceMethodDescriptorSupplier("GetBranch"))
              .build();
        }
      }
    }
    return getGetBranchMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.CreateBranchRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.CreateBranchResponse> getCreateBranchMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "CreateBranch",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.CreateBranchRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.CreateBranchResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.CreateBranchRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.CreateBranchResponse> getCreateBranchMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.CreateBranchRequest, com.runnershigh.tps.infrastructure.grpc.proto.CreateBranchResponse> getCreateBranchMethod;
    if ((getCreateBranchMethod = GitServiceGrpc.getCreateBranchMethod) == null) {
      synchronized (GitServiceGrpc.class) {
        if ((getCreateBranchMethod = GitServiceGrpc.getCreateBranchMethod) == null) {
          GitServiceGrpc.getCreateBranchMethod = getCreateBranchMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.CreateBranchRequest, com.runnershigh.tps.infrastructure.grpc.proto.CreateBranchResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "CreateBranch"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.CreateBranchRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.CreateBranchResponse.getDefaultInstance()))
              .setSchemaDescriptor(new GitServiceMethodDescriptorSupplier("CreateBranch"))
              .build();
        }
      }
    }
    return getCreateBranchMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.DeleteBranchRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.DeleteBranchResponse> getDeleteBranchMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "DeleteBranch",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.DeleteBranchRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.DeleteBranchResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.DeleteBranchRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.DeleteBranchResponse> getDeleteBranchMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.DeleteBranchRequest, com.runnershigh.tps.infrastructure.grpc.proto.DeleteBranchResponse> getDeleteBranchMethod;
    if ((getDeleteBranchMethod = GitServiceGrpc.getDeleteBranchMethod) == null) {
      synchronized (GitServiceGrpc.class) {
        if ((getDeleteBranchMethod = GitServiceGrpc.getDeleteBranchMethod) == null) {
          GitServiceGrpc.getDeleteBranchMethod = getDeleteBranchMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.DeleteBranchRequest, com.runnershigh.tps.infrastructure.grpc.proto.DeleteBranchResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "DeleteBranch"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.DeleteBranchRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.DeleteBranchResponse.getDefaultInstance()))
              .setSchemaDescriptor(new GitServiceMethodDescriptorSupplier("DeleteBranch"))
              .build();
        }
      }
    }
    return getDeleteBranchMethod;
  }

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static GitServiceStub newStub(io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<GitServiceStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<GitServiceStub>() {
        @java.lang.Override
        public GitServiceStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new GitServiceStub(channel, callOptions);
        }
      };
    return GitServiceStub.newStub(factory, channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static GitServiceBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<GitServiceBlockingStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<GitServiceBlockingStub>() {
        @java.lang.Override
        public GitServiceBlockingStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new GitServiceBlockingStub(channel, callOptions);
        }
      };
    return GitServiceBlockingStub.newStub(factory, channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static GitServiceFutureStub newFutureStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<GitServiceFutureStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<GitServiceFutureStub>() {
        @java.lang.Override
        public GitServiceFutureStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new GitServiceFutureStub(channel, callOptions);
        }
      };
    return GitServiceFutureStub.newStub(factory, channel);
  }

  /**
   * <pre>
   * === 저장소 ===
   * </pre>
   */
  public interface AsyncService {

    /**
     * <pre>
     * 저장소 목록 조회
     * </pre>
     */
    default void listRepositories(com.runnershigh.tps.infrastructure.grpc.proto.ListRepositoriesRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListRepositoriesResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListRepositoriesMethod(), responseObserver);
    }

    /**
     * <pre>
     * 저장소 상세 조회
     * </pre>
     */
    default void getRepository(com.runnershigh.tps.infrastructure.grpc.proto.GetRepositoryRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.GetRepositoryResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetRepositoryMethod(), responseObserver);
    }

    /**
     * <pre>
     * 저장소 생성
     * </pre>
     */
    default void createRepository(com.runnershigh.tps.infrastructure.grpc.proto.CreateRepositoryRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.CreateRepositoryResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getCreateRepositoryMethod(), responseObserver);
    }

    /**
     * <pre>
     * 저장소 삭제
     * </pre>
     */
    default void deleteRepository(com.runnershigh.tps.infrastructure.grpc.proto.DeleteRepositoryRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.DeleteRepositoryResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getDeleteRepositoryMethod(), responseObserver);
    }

    /**
     * <pre>
     * 브랜치 목록 조회
     * </pre>
     */
    default void listBranches(com.runnershigh.tps.infrastructure.grpc.proto.ListBranchesRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListBranchesResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListBranchesMethod(), responseObserver);
    }

    /**
     * <pre>
     * 브랜치 상세 조회
     * </pre>
     */
    default void getBranch(com.runnershigh.tps.infrastructure.grpc.proto.GetBranchRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.GetBranchResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetBranchMethod(), responseObserver);
    }

    /**
     * <pre>
     * 브랜치 생성
     * </pre>
     */
    default void createBranch(com.runnershigh.tps.infrastructure.grpc.proto.CreateBranchRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.CreateBranchResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getCreateBranchMethod(), responseObserver);
    }

    /**
     * <pre>
     * 브랜치 삭제
     * </pre>
     */
    default void deleteBranch(com.runnershigh.tps.infrastructure.grpc.proto.DeleteBranchRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.DeleteBranchResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getDeleteBranchMethod(), responseObserver);
    }
  }

  /**
   * Base class for the server implementation of the service GitService.
   * <pre>
   * === 저장소 ===
   * </pre>
   */
  public static abstract class GitServiceImplBase
      implements io.grpc.BindableService, AsyncService {

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return GitServiceGrpc.bindService(this);
    }
  }

  /**
   * A stub to allow clients to do asynchronous rpc calls to service GitService.
   * <pre>
   * === 저장소 ===
   * </pre>
   */
  public static final class GitServiceStub
      extends io.grpc.stub.AbstractAsyncStub<GitServiceStub> {
    private GitServiceStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected GitServiceStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new GitServiceStub(channel, callOptions);
    }

    /**
     * <pre>
     * 저장소 목록 조회
     * </pre>
     */
    public void listRepositories(com.runnershigh.tps.infrastructure.grpc.proto.ListRepositoriesRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListRepositoriesResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getListRepositoriesMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * 저장소 상세 조회
     * </pre>
     */
    public void getRepository(com.runnershigh.tps.infrastructure.grpc.proto.GetRepositoryRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.GetRepositoryResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getGetRepositoryMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * 저장소 생성
     * </pre>
     */
    public void createRepository(com.runnershigh.tps.infrastructure.grpc.proto.CreateRepositoryRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.CreateRepositoryResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getCreateRepositoryMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * 저장소 삭제
     * </pre>
     */
    public void deleteRepository(com.runnershigh.tps.infrastructure.grpc.proto.DeleteRepositoryRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.DeleteRepositoryResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getDeleteRepositoryMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * 브랜치 목록 조회
     * </pre>
     */
    public void listBranches(com.runnershigh.tps.infrastructure.grpc.proto.ListBranchesRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListBranchesResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getListBranchesMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * 브랜치 상세 조회
     * </pre>
     */
    public void getBranch(com.runnershigh.tps.infrastructure.grpc.proto.GetBranchRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.GetBranchResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getGetBranchMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * 브랜치 생성
     * </pre>
     */
    public void createBranch(com.runnershigh.tps.infrastructure.grpc.proto.CreateBranchRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.CreateBranchResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getCreateBranchMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * 브랜치 삭제
     * </pre>
     */
    public void deleteBranch(com.runnershigh.tps.infrastructure.grpc.proto.DeleteBranchRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.DeleteBranchResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getDeleteBranchMethod(), getCallOptions()), request, responseObserver);
    }
  }

  /**
   * A stub to allow clients to do synchronous rpc calls to service GitService.
   * <pre>
   * === 저장소 ===
   * </pre>
   */
  public static final class GitServiceBlockingStub
      extends io.grpc.stub.AbstractBlockingStub<GitServiceBlockingStub> {
    private GitServiceBlockingStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected GitServiceBlockingStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new GitServiceBlockingStub(channel, callOptions);
    }

    /**
     * <pre>
     * 저장소 목록 조회
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.ListRepositoriesResponse listRepositories(com.runnershigh.tps.infrastructure.grpc.proto.ListRepositoriesRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getListRepositoriesMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * 저장소 상세 조회
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.GetRepositoryResponse getRepository(com.runnershigh.tps.infrastructure.grpc.proto.GetRepositoryRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getGetRepositoryMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * 저장소 생성
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.CreateRepositoryResponse createRepository(com.runnershigh.tps.infrastructure.grpc.proto.CreateRepositoryRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getCreateRepositoryMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * 저장소 삭제
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.DeleteRepositoryResponse deleteRepository(com.runnershigh.tps.infrastructure.grpc.proto.DeleteRepositoryRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getDeleteRepositoryMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * 브랜치 목록 조회
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.ListBranchesResponse listBranches(com.runnershigh.tps.infrastructure.grpc.proto.ListBranchesRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getListBranchesMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * 브랜치 상세 조회
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.GetBranchResponse getBranch(com.runnershigh.tps.infrastructure.grpc.proto.GetBranchRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getGetBranchMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * 브랜치 생성
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.CreateBranchResponse createBranch(com.runnershigh.tps.infrastructure.grpc.proto.CreateBranchRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getCreateBranchMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * 브랜치 삭제
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.DeleteBranchResponse deleteBranch(com.runnershigh.tps.infrastructure.grpc.proto.DeleteBranchRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getDeleteBranchMethod(), getCallOptions(), request);
    }
  }

  /**
   * A stub to allow clients to do ListenableFuture-style rpc calls to service GitService.
   * <pre>
   * === 저장소 ===
   * </pre>
   */
  public static final class GitServiceFutureStub
      extends io.grpc.stub.AbstractFutureStub<GitServiceFutureStub> {
    private GitServiceFutureStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected GitServiceFutureStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new GitServiceFutureStub(channel, callOptions);
    }

    /**
     * <pre>
     * 저장소 목록 조회
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.ListRepositoriesResponse> listRepositories(
        com.runnershigh.tps.infrastructure.grpc.proto.ListRepositoriesRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getListRepositoriesMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * 저장소 상세 조회
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.GetRepositoryResponse> getRepository(
        com.runnershigh.tps.infrastructure.grpc.proto.GetRepositoryRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getGetRepositoryMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * 저장소 생성
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.CreateRepositoryResponse> createRepository(
        com.runnershigh.tps.infrastructure.grpc.proto.CreateRepositoryRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getCreateRepositoryMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * 저장소 삭제
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.DeleteRepositoryResponse> deleteRepository(
        com.runnershigh.tps.infrastructure.grpc.proto.DeleteRepositoryRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getDeleteRepositoryMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * 브랜치 목록 조회
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.ListBranchesResponse> listBranches(
        com.runnershigh.tps.infrastructure.grpc.proto.ListBranchesRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getListBranchesMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * 브랜치 상세 조회
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.GetBranchResponse> getBranch(
        com.runnershigh.tps.infrastructure.grpc.proto.GetBranchRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getGetBranchMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * 브랜치 생성
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.CreateBranchResponse> createBranch(
        com.runnershigh.tps.infrastructure.grpc.proto.CreateBranchRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getCreateBranchMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * 브랜치 삭제
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.DeleteBranchResponse> deleteBranch(
        com.runnershigh.tps.infrastructure.grpc.proto.DeleteBranchRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getDeleteBranchMethod(), getCallOptions()), request);
    }
  }

  private static final int METHODID_LIST_REPOSITORIES = 0;
  private static final int METHODID_GET_REPOSITORY = 1;
  private static final int METHODID_CREATE_REPOSITORY = 2;
  private static final int METHODID_DELETE_REPOSITORY = 3;
  private static final int METHODID_LIST_BRANCHES = 4;
  private static final int METHODID_GET_BRANCH = 5;
  private static final int METHODID_CREATE_BRANCH = 6;
  private static final int METHODID_DELETE_BRANCH = 7;

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
        case METHODID_LIST_REPOSITORIES:
          serviceImpl.listRepositories((com.runnershigh.tps.infrastructure.grpc.proto.ListRepositoriesRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListRepositoriesResponse>) responseObserver);
          break;
        case METHODID_GET_REPOSITORY:
          serviceImpl.getRepository((com.runnershigh.tps.infrastructure.grpc.proto.GetRepositoryRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.GetRepositoryResponse>) responseObserver);
          break;
        case METHODID_CREATE_REPOSITORY:
          serviceImpl.createRepository((com.runnershigh.tps.infrastructure.grpc.proto.CreateRepositoryRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.CreateRepositoryResponse>) responseObserver);
          break;
        case METHODID_DELETE_REPOSITORY:
          serviceImpl.deleteRepository((com.runnershigh.tps.infrastructure.grpc.proto.DeleteRepositoryRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.DeleteRepositoryResponse>) responseObserver);
          break;
        case METHODID_LIST_BRANCHES:
          serviceImpl.listBranches((com.runnershigh.tps.infrastructure.grpc.proto.ListBranchesRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListBranchesResponse>) responseObserver);
          break;
        case METHODID_GET_BRANCH:
          serviceImpl.getBranch((com.runnershigh.tps.infrastructure.grpc.proto.GetBranchRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.GetBranchResponse>) responseObserver);
          break;
        case METHODID_CREATE_BRANCH:
          serviceImpl.createBranch((com.runnershigh.tps.infrastructure.grpc.proto.CreateBranchRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.CreateBranchResponse>) responseObserver);
          break;
        case METHODID_DELETE_BRANCH:
          serviceImpl.deleteBranch((com.runnershigh.tps.infrastructure.grpc.proto.DeleteBranchRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.DeleteBranchResponse>) responseObserver);
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
          getListRepositoriesMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.ListRepositoriesRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.ListRepositoriesResponse>(
                service, METHODID_LIST_REPOSITORIES)))
        .addMethod(
          getGetRepositoryMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.GetRepositoryRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.GetRepositoryResponse>(
                service, METHODID_GET_REPOSITORY)))
        .addMethod(
          getCreateRepositoryMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.CreateRepositoryRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.CreateRepositoryResponse>(
                service, METHODID_CREATE_REPOSITORY)))
        .addMethod(
          getDeleteRepositoryMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.DeleteRepositoryRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.DeleteRepositoryResponse>(
                service, METHODID_DELETE_REPOSITORY)))
        .addMethod(
          getListBranchesMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.ListBranchesRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.ListBranchesResponse>(
                service, METHODID_LIST_BRANCHES)))
        .addMethod(
          getGetBranchMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.GetBranchRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.GetBranchResponse>(
                service, METHODID_GET_BRANCH)))
        .addMethod(
          getCreateBranchMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.CreateBranchRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.CreateBranchResponse>(
                service, METHODID_CREATE_BRANCH)))
        .addMethod(
          getDeleteBranchMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.DeleteBranchRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.DeleteBranchResponse>(
                service, METHODID_DELETE_BRANCH)))
        .build();
  }

  private static abstract class GitServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    GitServiceBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return com.runnershigh.tps.infrastructure.grpc.proto.ProviderProto.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("GitService");
    }
  }

  private static final class GitServiceFileDescriptorSupplier
      extends GitServiceBaseDescriptorSupplier {
    GitServiceFileDescriptorSupplier() {}
  }

  private static final class GitServiceMethodDescriptorSupplier
      extends GitServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final java.lang.String methodName;

    GitServiceMethodDescriptorSupplier(java.lang.String methodName) {
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
      synchronized (GitServiceGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new GitServiceFileDescriptorSupplier())
              .addMethod(getListRepositoriesMethod())
              .addMethod(getGetRepositoryMethod())
              .addMethod(getCreateRepositoryMethod())
              .addMethod(getDeleteRepositoryMethod())
              .addMethod(getListBranchesMethod())
              .addMethod(getGetBranchMethod())
              .addMethod(getCreateBranchMethod())
              .addMethod(getDeleteBranchMethod())
              .build();
        }
      }
    }
    return result;
  }
}
