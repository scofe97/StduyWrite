package com.runnershigh.poc.grpc.generated;

import static io.grpc.MethodDescriptor.generateFullMethodName;

/**
 */
@javax.annotation.Generated(
    value = "by gRPC proto compiler (version 1.68.2)",
    comments = "Source: v1/provider.proto")
@io.grpc.stub.annotations.GrpcGenerated
public final class GitServiceGrpc {

  private GitServiceGrpc() {}

  public static final java.lang.String SERVICE_NAME = "gitprovider.v1.GitService";

  // Static method descriptors that strictly reflect the proto.
  private static volatile io.grpc.MethodDescriptor<com.runnershigh.poc.grpc.generated.ListRepositoriesRequest,
      com.runnershigh.poc.grpc.generated.ListRepositoriesResponse> getListRepositoriesMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "ListRepositories",
      requestType = com.runnershigh.poc.grpc.generated.ListRepositoriesRequest.class,
      responseType = com.runnershigh.poc.grpc.generated.ListRepositoriesResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.poc.grpc.generated.ListRepositoriesRequest,
      com.runnershigh.poc.grpc.generated.ListRepositoriesResponse> getListRepositoriesMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.poc.grpc.generated.ListRepositoriesRequest, com.runnershigh.poc.grpc.generated.ListRepositoriesResponse> getListRepositoriesMethod;
    if ((getListRepositoriesMethod = GitServiceGrpc.getListRepositoriesMethod) == null) {
      synchronized (GitServiceGrpc.class) {
        if ((getListRepositoriesMethod = GitServiceGrpc.getListRepositoriesMethod) == null) {
          GitServiceGrpc.getListRepositoriesMethod = getListRepositoriesMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.poc.grpc.generated.ListRepositoriesRequest, com.runnershigh.poc.grpc.generated.ListRepositoriesResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListRepositories"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.poc.grpc.generated.ListRepositoriesRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.poc.grpc.generated.ListRepositoriesResponse.getDefaultInstance()))
              .setSchemaDescriptor(new GitServiceMethodDescriptorSupplier("ListRepositories"))
              .build();
        }
      }
    }
    return getListRepositoriesMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.poc.grpc.generated.GetRepositoryRequest,
      com.runnershigh.poc.grpc.generated.GetRepositoryResponse> getGetRepositoryMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "GetRepository",
      requestType = com.runnershigh.poc.grpc.generated.GetRepositoryRequest.class,
      responseType = com.runnershigh.poc.grpc.generated.GetRepositoryResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.poc.grpc.generated.GetRepositoryRequest,
      com.runnershigh.poc.grpc.generated.GetRepositoryResponse> getGetRepositoryMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.poc.grpc.generated.GetRepositoryRequest, com.runnershigh.poc.grpc.generated.GetRepositoryResponse> getGetRepositoryMethod;
    if ((getGetRepositoryMethod = GitServiceGrpc.getGetRepositoryMethod) == null) {
      synchronized (GitServiceGrpc.class) {
        if ((getGetRepositoryMethod = GitServiceGrpc.getGetRepositoryMethod) == null) {
          GitServiceGrpc.getGetRepositoryMethod = getGetRepositoryMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.poc.grpc.generated.GetRepositoryRequest, com.runnershigh.poc.grpc.generated.GetRepositoryResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetRepository"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.poc.grpc.generated.GetRepositoryRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.poc.grpc.generated.GetRepositoryResponse.getDefaultInstance()))
              .setSchemaDescriptor(new GitServiceMethodDescriptorSupplier("GetRepository"))
              .build();
        }
      }
    }
    return getGetRepositoryMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.poc.grpc.generated.CreateRepositoryRequest,
      com.runnershigh.poc.grpc.generated.CreateRepositoryResponse> getCreateRepositoryMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "CreateRepository",
      requestType = com.runnershigh.poc.grpc.generated.CreateRepositoryRequest.class,
      responseType = com.runnershigh.poc.grpc.generated.CreateRepositoryResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.poc.grpc.generated.CreateRepositoryRequest,
      com.runnershigh.poc.grpc.generated.CreateRepositoryResponse> getCreateRepositoryMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.poc.grpc.generated.CreateRepositoryRequest, com.runnershigh.poc.grpc.generated.CreateRepositoryResponse> getCreateRepositoryMethod;
    if ((getCreateRepositoryMethod = GitServiceGrpc.getCreateRepositoryMethod) == null) {
      synchronized (GitServiceGrpc.class) {
        if ((getCreateRepositoryMethod = GitServiceGrpc.getCreateRepositoryMethod) == null) {
          GitServiceGrpc.getCreateRepositoryMethod = getCreateRepositoryMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.poc.grpc.generated.CreateRepositoryRequest, com.runnershigh.poc.grpc.generated.CreateRepositoryResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "CreateRepository"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.poc.grpc.generated.CreateRepositoryRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.poc.grpc.generated.CreateRepositoryResponse.getDefaultInstance()))
              .setSchemaDescriptor(new GitServiceMethodDescriptorSupplier("CreateRepository"))
              .build();
        }
      }
    }
    return getCreateRepositoryMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.poc.grpc.generated.DeleteRepositoryRequest,
      com.runnershigh.poc.grpc.generated.DeleteRepositoryResponse> getDeleteRepositoryMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "DeleteRepository",
      requestType = com.runnershigh.poc.grpc.generated.DeleteRepositoryRequest.class,
      responseType = com.runnershigh.poc.grpc.generated.DeleteRepositoryResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.poc.grpc.generated.DeleteRepositoryRequest,
      com.runnershigh.poc.grpc.generated.DeleteRepositoryResponse> getDeleteRepositoryMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.poc.grpc.generated.DeleteRepositoryRequest, com.runnershigh.poc.grpc.generated.DeleteRepositoryResponse> getDeleteRepositoryMethod;
    if ((getDeleteRepositoryMethod = GitServiceGrpc.getDeleteRepositoryMethod) == null) {
      synchronized (GitServiceGrpc.class) {
        if ((getDeleteRepositoryMethod = GitServiceGrpc.getDeleteRepositoryMethod) == null) {
          GitServiceGrpc.getDeleteRepositoryMethod = getDeleteRepositoryMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.poc.grpc.generated.DeleteRepositoryRequest, com.runnershigh.poc.grpc.generated.DeleteRepositoryResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "DeleteRepository"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.poc.grpc.generated.DeleteRepositoryRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.poc.grpc.generated.DeleteRepositoryResponse.getDefaultInstance()))
              .setSchemaDescriptor(new GitServiceMethodDescriptorSupplier("DeleteRepository"))
              .build();
        }
      }
    }
    return getDeleteRepositoryMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.poc.grpc.generated.ListBranchesRequest,
      com.runnershigh.poc.grpc.generated.ListBranchesResponse> getListBranchesMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "ListBranches",
      requestType = com.runnershigh.poc.grpc.generated.ListBranchesRequest.class,
      responseType = com.runnershigh.poc.grpc.generated.ListBranchesResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.poc.grpc.generated.ListBranchesRequest,
      com.runnershigh.poc.grpc.generated.ListBranchesResponse> getListBranchesMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.poc.grpc.generated.ListBranchesRequest, com.runnershigh.poc.grpc.generated.ListBranchesResponse> getListBranchesMethod;
    if ((getListBranchesMethod = GitServiceGrpc.getListBranchesMethod) == null) {
      synchronized (GitServiceGrpc.class) {
        if ((getListBranchesMethod = GitServiceGrpc.getListBranchesMethod) == null) {
          GitServiceGrpc.getListBranchesMethod = getListBranchesMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.poc.grpc.generated.ListBranchesRequest, com.runnershigh.poc.grpc.generated.ListBranchesResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListBranches"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.poc.grpc.generated.ListBranchesRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.poc.grpc.generated.ListBranchesResponse.getDefaultInstance()))
              .setSchemaDescriptor(new GitServiceMethodDescriptorSupplier("ListBranches"))
              .build();
        }
      }
    }
    return getListBranchesMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.poc.grpc.generated.GetBranchRequest,
      com.runnershigh.poc.grpc.generated.GetBranchResponse> getGetBranchMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "GetBranch",
      requestType = com.runnershigh.poc.grpc.generated.GetBranchRequest.class,
      responseType = com.runnershigh.poc.grpc.generated.GetBranchResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.poc.grpc.generated.GetBranchRequest,
      com.runnershigh.poc.grpc.generated.GetBranchResponse> getGetBranchMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.poc.grpc.generated.GetBranchRequest, com.runnershigh.poc.grpc.generated.GetBranchResponse> getGetBranchMethod;
    if ((getGetBranchMethod = GitServiceGrpc.getGetBranchMethod) == null) {
      synchronized (GitServiceGrpc.class) {
        if ((getGetBranchMethod = GitServiceGrpc.getGetBranchMethod) == null) {
          GitServiceGrpc.getGetBranchMethod = getGetBranchMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.poc.grpc.generated.GetBranchRequest, com.runnershigh.poc.grpc.generated.GetBranchResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetBranch"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.poc.grpc.generated.GetBranchRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.poc.grpc.generated.GetBranchResponse.getDefaultInstance()))
              .setSchemaDescriptor(new GitServiceMethodDescriptorSupplier("GetBranch"))
              .build();
        }
      }
    }
    return getGetBranchMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.poc.grpc.generated.CreateBranchRequest,
      com.runnershigh.poc.grpc.generated.CreateBranchResponse> getCreateBranchMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "CreateBranch",
      requestType = com.runnershigh.poc.grpc.generated.CreateBranchRequest.class,
      responseType = com.runnershigh.poc.grpc.generated.CreateBranchResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.poc.grpc.generated.CreateBranchRequest,
      com.runnershigh.poc.grpc.generated.CreateBranchResponse> getCreateBranchMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.poc.grpc.generated.CreateBranchRequest, com.runnershigh.poc.grpc.generated.CreateBranchResponse> getCreateBranchMethod;
    if ((getCreateBranchMethod = GitServiceGrpc.getCreateBranchMethod) == null) {
      synchronized (GitServiceGrpc.class) {
        if ((getCreateBranchMethod = GitServiceGrpc.getCreateBranchMethod) == null) {
          GitServiceGrpc.getCreateBranchMethod = getCreateBranchMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.poc.grpc.generated.CreateBranchRequest, com.runnershigh.poc.grpc.generated.CreateBranchResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "CreateBranch"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.poc.grpc.generated.CreateBranchRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.poc.grpc.generated.CreateBranchResponse.getDefaultInstance()))
              .setSchemaDescriptor(new GitServiceMethodDescriptorSupplier("CreateBranch"))
              .build();
        }
      }
    }
    return getCreateBranchMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.poc.grpc.generated.DeleteBranchRequest,
      com.runnershigh.poc.grpc.generated.DeleteBranchResponse> getDeleteBranchMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "DeleteBranch",
      requestType = com.runnershigh.poc.grpc.generated.DeleteBranchRequest.class,
      responseType = com.runnershigh.poc.grpc.generated.DeleteBranchResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.poc.grpc.generated.DeleteBranchRequest,
      com.runnershigh.poc.grpc.generated.DeleteBranchResponse> getDeleteBranchMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.poc.grpc.generated.DeleteBranchRequest, com.runnershigh.poc.grpc.generated.DeleteBranchResponse> getDeleteBranchMethod;
    if ((getDeleteBranchMethod = GitServiceGrpc.getDeleteBranchMethod) == null) {
      synchronized (GitServiceGrpc.class) {
        if ((getDeleteBranchMethod = GitServiceGrpc.getDeleteBranchMethod) == null) {
          GitServiceGrpc.getDeleteBranchMethod = getDeleteBranchMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.poc.grpc.generated.DeleteBranchRequest, com.runnershigh.poc.grpc.generated.DeleteBranchResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "DeleteBranch"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.poc.grpc.generated.DeleteBranchRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.poc.grpc.generated.DeleteBranchResponse.getDefaultInstance()))
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
   */
  public interface AsyncService {

    /**
     * <pre>
     * 저장소
     * </pre>
     */
    default void listRepositories(com.runnershigh.poc.grpc.generated.ListRepositoriesRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.poc.grpc.generated.ListRepositoriesResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListRepositoriesMethod(), responseObserver);
    }

    /**
     */
    default void getRepository(com.runnershigh.poc.grpc.generated.GetRepositoryRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.poc.grpc.generated.GetRepositoryResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetRepositoryMethod(), responseObserver);
    }

    /**
     */
    default void createRepository(com.runnershigh.poc.grpc.generated.CreateRepositoryRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.poc.grpc.generated.CreateRepositoryResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getCreateRepositoryMethod(), responseObserver);
    }

    /**
     */
    default void deleteRepository(com.runnershigh.poc.grpc.generated.DeleteRepositoryRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.poc.grpc.generated.DeleteRepositoryResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getDeleteRepositoryMethod(), responseObserver);
    }

    /**
     * <pre>
     * 브랜치
     * </pre>
     */
    default void listBranches(com.runnershigh.poc.grpc.generated.ListBranchesRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.poc.grpc.generated.ListBranchesResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListBranchesMethod(), responseObserver);
    }

    /**
     */
    default void getBranch(com.runnershigh.poc.grpc.generated.GetBranchRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.poc.grpc.generated.GetBranchResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetBranchMethod(), responseObserver);
    }

    /**
     */
    default void createBranch(com.runnershigh.poc.grpc.generated.CreateBranchRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.poc.grpc.generated.CreateBranchResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getCreateBranchMethod(), responseObserver);
    }

    /**
     */
    default void deleteBranch(com.runnershigh.poc.grpc.generated.DeleteBranchRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.poc.grpc.generated.DeleteBranchResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getDeleteBranchMethod(), responseObserver);
    }
  }

  /**
   * Base class for the server implementation of the service GitService.
   */
  public static abstract class GitServiceImplBase
      implements io.grpc.BindableService, AsyncService {

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return GitServiceGrpc.bindService(this);
    }
  }

  /**
   * A stub to allow clients to do asynchronous rpc calls to service GitService.
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
     * 저장소
     * </pre>
     */
    public void listRepositories(com.runnershigh.poc.grpc.generated.ListRepositoriesRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.poc.grpc.generated.ListRepositoriesResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getListRepositoriesMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     */
    public void getRepository(com.runnershigh.poc.grpc.generated.GetRepositoryRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.poc.grpc.generated.GetRepositoryResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getGetRepositoryMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     */
    public void createRepository(com.runnershigh.poc.grpc.generated.CreateRepositoryRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.poc.grpc.generated.CreateRepositoryResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getCreateRepositoryMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     */
    public void deleteRepository(com.runnershigh.poc.grpc.generated.DeleteRepositoryRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.poc.grpc.generated.DeleteRepositoryResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getDeleteRepositoryMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * 브랜치
     * </pre>
     */
    public void listBranches(com.runnershigh.poc.grpc.generated.ListBranchesRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.poc.grpc.generated.ListBranchesResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getListBranchesMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     */
    public void getBranch(com.runnershigh.poc.grpc.generated.GetBranchRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.poc.grpc.generated.GetBranchResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getGetBranchMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     */
    public void createBranch(com.runnershigh.poc.grpc.generated.CreateBranchRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.poc.grpc.generated.CreateBranchResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getCreateBranchMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     */
    public void deleteBranch(com.runnershigh.poc.grpc.generated.DeleteBranchRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.poc.grpc.generated.DeleteBranchResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getDeleteBranchMethod(), getCallOptions()), request, responseObserver);
    }
  }

  /**
   * A stub to allow clients to do synchronous rpc calls to service GitService.
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
     * 저장소
     * </pre>
     */
    public com.runnershigh.poc.grpc.generated.ListRepositoriesResponse listRepositories(com.runnershigh.poc.grpc.generated.ListRepositoriesRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getListRepositoriesMethod(), getCallOptions(), request);
    }

    /**
     */
    public com.runnershigh.poc.grpc.generated.GetRepositoryResponse getRepository(com.runnershigh.poc.grpc.generated.GetRepositoryRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getGetRepositoryMethod(), getCallOptions(), request);
    }

    /**
     */
    public com.runnershigh.poc.grpc.generated.CreateRepositoryResponse createRepository(com.runnershigh.poc.grpc.generated.CreateRepositoryRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getCreateRepositoryMethod(), getCallOptions(), request);
    }

    /**
     */
    public com.runnershigh.poc.grpc.generated.DeleteRepositoryResponse deleteRepository(com.runnershigh.poc.grpc.generated.DeleteRepositoryRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getDeleteRepositoryMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * 브랜치
     * </pre>
     */
    public com.runnershigh.poc.grpc.generated.ListBranchesResponse listBranches(com.runnershigh.poc.grpc.generated.ListBranchesRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getListBranchesMethod(), getCallOptions(), request);
    }

    /**
     */
    public com.runnershigh.poc.grpc.generated.GetBranchResponse getBranch(com.runnershigh.poc.grpc.generated.GetBranchRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getGetBranchMethod(), getCallOptions(), request);
    }

    /**
     */
    public com.runnershigh.poc.grpc.generated.CreateBranchResponse createBranch(com.runnershigh.poc.grpc.generated.CreateBranchRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getCreateBranchMethod(), getCallOptions(), request);
    }

    /**
     */
    public com.runnershigh.poc.grpc.generated.DeleteBranchResponse deleteBranch(com.runnershigh.poc.grpc.generated.DeleteBranchRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getDeleteBranchMethod(), getCallOptions(), request);
    }
  }

  /**
   * A stub to allow clients to do ListenableFuture-style rpc calls to service GitService.
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
     * 저장소
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.poc.grpc.generated.ListRepositoriesResponse> listRepositories(
        com.runnershigh.poc.grpc.generated.ListRepositoriesRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getListRepositoriesMethod(), getCallOptions()), request);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.poc.grpc.generated.GetRepositoryResponse> getRepository(
        com.runnershigh.poc.grpc.generated.GetRepositoryRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getGetRepositoryMethod(), getCallOptions()), request);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.poc.grpc.generated.CreateRepositoryResponse> createRepository(
        com.runnershigh.poc.grpc.generated.CreateRepositoryRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getCreateRepositoryMethod(), getCallOptions()), request);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.poc.grpc.generated.DeleteRepositoryResponse> deleteRepository(
        com.runnershigh.poc.grpc.generated.DeleteRepositoryRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getDeleteRepositoryMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * 브랜치
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.poc.grpc.generated.ListBranchesResponse> listBranches(
        com.runnershigh.poc.grpc.generated.ListBranchesRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getListBranchesMethod(), getCallOptions()), request);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.poc.grpc.generated.GetBranchResponse> getBranch(
        com.runnershigh.poc.grpc.generated.GetBranchRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getGetBranchMethod(), getCallOptions()), request);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.poc.grpc.generated.CreateBranchResponse> createBranch(
        com.runnershigh.poc.grpc.generated.CreateBranchRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getCreateBranchMethod(), getCallOptions()), request);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.poc.grpc.generated.DeleteBranchResponse> deleteBranch(
        com.runnershigh.poc.grpc.generated.DeleteBranchRequest request) {
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
          serviceImpl.listRepositories((com.runnershigh.poc.grpc.generated.ListRepositoriesRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.poc.grpc.generated.ListRepositoriesResponse>) responseObserver);
          break;
        case METHODID_GET_REPOSITORY:
          serviceImpl.getRepository((com.runnershigh.poc.grpc.generated.GetRepositoryRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.poc.grpc.generated.GetRepositoryResponse>) responseObserver);
          break;
        case METHODID_CREATE_REPOSITORY:
          serviceImpl.createRepository((com.runnershigh.poc.grpc.generated.CreateRepositoryRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.poc.grpc.generated.CreateRepositoryResponse>) responseObserver);
          break;
        case METHODID_DELETE_REPOSITORY:
          serviceImpl.deleteRepository((com.runnershigh.poc.grpc.generated.DeleteRepositoryRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.poc.grpc.generated.DeleteRepositoryResponse>) responseObserver);
          break;
        case METHODID_LIST_BRANCHES:
          serviceImpl.listBranches((com.runnershigh.poc.grpc.generated.ListBranchesRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.poc.grpc.generated.ListBranchesResponse>) responseObserver);
          break;
        case METHODID_GET_BRANCH:
          serviceImpl.getBranch((com.runnershigh.poc.grpc.generated.GetBranchRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.poc.grpc.generated.GetBranchResponse>) responseObserver);
          break;
        case METHODID_CREATE_BRANCH:
          serviceImpl.createBranch((com.runnershigh.poc.grpc.generated.CreateBranchRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.poc.grpc.generated.CreateBranchResponse>) responseObserver);
          break;
        case METHODID_DELETE_BRANCH:
          serviceImpl.deleteBranch((com.runnershigh.poc.grpc.generated.DeleteBranchRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.poc.grpc.generated.DeleteBranchResponse>) responseObserver);
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
              com.runnershigh.poc.grpc.generated.ListRepositoriesRequest,
              com.runnershigh.poc.grpc.generated.ListRepositoriesResponse>(
                service, METHODID_LIST_REPOSITORIES)))
        .addMethod(
          getGetRepositoryMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.poc.grpc.generated.GetRepositoryRequest,
              com.runnershigh.poc.grpc.generated.GetRepositoryResponse>(
                service, METHODID_GET_REPOSITORY)))
        .addMethod(
          getCreateRepositoryMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.poc.grpc.generated.CreateRepositoryRequest,
              com.runnershigh.poc.grpc.generated.CreateRepositoryResponse>(
                service, METHODID_CREATE_REPOSITORY)))
        .addMethod(
          getDeleteRepositoryMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.poc.grpc.generated.DeleteRepositoryRequest,
              com.runnershigh.poc.grpc.generated.DeleteRepositoryResponse>(
                service, METHODID_DELETE_REPOSITORY)))
        .addMethod(
          getListBranchesMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.poc.grpc.generated.ListBranchesRequest,
              com.runnershigh.poc.grpc.generated.ListBranchesResponse>(
                service, METHODID_LIST_BRANCHES)))
        .addMethod(
          getGetBranchMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.poc.grpc.generated.GetBranchRequest,
              com.runnershigh.poc.grpc.generated.GetBranchResponse>(
                service, METHODID_GET_BRANCH)))
        .addMethod(
          getCreateBranchMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.poc.grpc.generated.CreateBranchRequest,
              com.runnershigh.poc.grpc.generated.CreateBranchResponse>(
                service, METHODID_CREATE_BRANCH)))
        .addMethod(
          getDeleteBranchMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.poc.grpc.generated.DeleteBranchRequest,
              com.runnershigh.poc.grpc.generated.DeleteBranchResponse>(
                service, METHODID_DELETE_BRANCH)))
        .build();
  }

  private static abstract class GitServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    GitServiceBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return com.runnershigh.poc.grpc.generated.GitProviderProto.getDescriptor();
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
