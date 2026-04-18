package com.runnershigh.tps.infrastructure.grpc.proto;

import static io.grpc.MethodDescriptor.generateFullMethodName;

/**
 */
@javax.annotation.Generated(
    value = "by gRPC proto compiler (version 1.60.1)",
    comments = "Source: v1/mergerequest.proto")
@io.grpc.stub.annotations.GrpcGenerated
public final class MergeRequestServiceGrpc {

  private MergeRequestServiceGrpc() {}

  public static final java.lang.String SERVICE_NAME = "gitprovider.v1.MergeRequestService";

  // Static method descriptors that strictly reflect the proto.
  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListMergeRequestsRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.ListMergeRequestsResponse> getListMergeRequestsMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "ListMergeRequests",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.ListMergeRequestsRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.ListMergeRequestsResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListMergeRequestsRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.ListMergeRequestsResponse> getListMergeRequestsMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListMergeRequestsRequest, com.runnershigh.tps.infrastructure.grpc.proto.ListMergeRequestsResponse> getListMergeRequestsMethod;
    if ((getListMergeRequestsMethod = MergeRequestServiceGrpc.getListMergeRequestsMethod) == null) {
      synchronized (MergeRequestServiceGrpc.class) {
        if ((getListMergeRequestsMethod = MergeRequestServiceGrpc.getListMergeRequestsMethod) == null) {
          MergeRequestServiceGrpc.getListMergeRequestsMethod = getListMergeRequestsMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.ListMergeRequestsRequest, com.runnershigh.tps.infrastructure.grpc.proto.ListMergeRequestsResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListMergeRequests"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.ListMergeRequestsRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.ListMergeRequestsResponse.getDefaultInstance()))
              .setSchemaDescriptor(new MergeRequestServiceMethodDescriptorSupplier("ListMergeRequests"))
              .build();
        }
      }
    }
    return getListMergeRequestsMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestResponse> getGetMergeRequestMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "GetMergeRequest",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestResponse> getGetMergeRequestMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestRequest, com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestResponse> getGetMergeRequestMethod;
    if ((getGetMergeRequestMethod = MergeRequestServiceGrpc.getGetMergeRequestMethod) == null) {
      synchronized (MergeRequestServiceGrpc.class) {
        if ((getGetMergeRequestMethod = MergeRequestServiceGrpc.getGetMergeRequestMethod) == null) {
          MergeRequestServiceGrpc.getGetMergeRequestMethod = getGetMergeRequestMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestRequest, com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetMergeRequest"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestResponse.getDefaultInstance()))
              .setSchemaDescriptor(new MergeRequestServiceMethodDescriptorSupplier("GetMergeRequest"))
              .build();
        }
      }
    }
    return getGetMergeRequestMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.CreateMergeRequestRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.CreateMergeRequestResponse> getCreateMergeRequestMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "CreateMergeRequest",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.CreateMergeRequestRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.CreateMergeRequestResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.CreateMergeRequestRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.CreateMergeRequestResponse> getCreateMergeRequestMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.CreateMergeRequestRequest, com.runnershigh.tps.infrastructure.grpc.proto.CreateMergeRequestResponse> getCreateMergeRequestMethod;
    if ((getCreateMergeRequestMethod = MergeRequestServiceGrpc.getCreateMergeRequestMethod) == null) {
      synchronized (MergeRequestServiceGrpc.class) {
        if ((getCreateMergeRequestMethod = MergeRequestServiceGrpc.getCreateMergeRequestMethod) == null) {
          MergeRequestServiceGrpc.getCreateMergeRequestMethod = getCreateMergeRequestMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.CreateMergeRequestRequest, com.runnershigh.tps.infrastructure.grpc.proto.CreateMergeRequestResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "CreateMergeRequest"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.CreateMergeRequestRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.CreateMergeRequestResponse.getDefaultInstance()))
              .setSchemaDescriptor(new MergeRequestServiceMethodDescriptorSupplier("CreateMergeRequest"))
              .build();
        }
      }
    }
    return getCreateMergeRequestMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.UpdateMergeRequestRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.UpdateMergeRequestResponse> getUpdateMergeRequestMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "UpdateMergeRequest",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.UpdateMergeRequestRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.UpdateMergeRequestResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.UpdateMergeRequestRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.UpdateMergeRequestResponse> getUpdateMergeRequestMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.UpdateMergeRequestRequest, com.runnershigh.tps.infrastructure.grpc.proto.UpdateMergeRequestResponse> getUpdateMergeRequestMethod;
    if ((getUpdateMergeRequestMethod = MergeRequestServiceGrpc.getUpdateMergeRequestMethod) == null) {
      synchronized (MergeRequestServiceGrpc.class) {
        if ((getUpdateMergeRequestMethod = MergeRequestServiceGrpc.getUpdateMergeRequestMethod) == null) {
          MergeRequestServiceGrpc.getUpdateMergeRequestMethod = getUpdateMergeRequestMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.UpdateMergeRequestRequest, com.runnershigh.tps.infrastructure.grpc.proto.UpdateMergeRequestResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "UpdateMergeRequest"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.UpdateMergeRequestRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.UpdateMergeRequestResponse.getDefaultInstance()))
              .setSchemaDescriptor(new MergeRequestServiceMethodDescriptorSupplier("UpdateMergeRequest"))
              .build();
        }
      }
    }
    return getUpdateMergeRequestMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.MergeMergeRequestRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.MergeMergeRequestResponse> getMergeMergeRequestMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "MergeMergeRequest",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.MergeMergeRequestRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.MergeMergeRequestResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.MergeMergeRequestRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.MergeMergeRequestResponse> getMergeMergeRequestMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.MergeMergeRequestRequest, com.runnershigh.tps.infrastructure.grpc.proto.MergeMergeRequestResponse> getMergeMergeRequestMethod;
    if ((getMergeMergeRequestMethod = MergeRequestServiceGrpc.getMergeMergeRequestMethod) == null) {
      synchronized (MergeRequestServiceGrpc.class) {
        if ((getMergeMergeRequestMethod = MergeRequestServiceGrpc.getMergeMergeRequestMethod) == null) {
          MergeRequestServiceGrpc.getMergeMergeRequestMethod = getMergeMergeRequestMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.MergeMergeRequestRequest, com.runnershigh.tps.infrastructure.grpc.proto.MergeMergeRequestResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "MergeMergeRequest"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.MergeMergeRequestRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.MergeMergeRequestResponse.getDefaultInstance()))
              .setSchemaDescriptor(new MergeRequestServiceMethodDescriptorSupplier("MergeMergeRequest"))
              .build();
        }
      }
    }
    return getMergeMergeRequestMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestDiffRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestDiffResponse> getGetMergeRequestDiffMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "GetMergeRequestDiff",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestDiffRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestDiffResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestDiffRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestDiffResponse> getGetMergeRequestDiffMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestDiffRequest, com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestDiffResponse> getGetMergeRequestDiffMethod;
    if ((getGetMergeRequestDiffMethod = MergeRequestServiceGrpc.getGetMergeRequestDiffMethod) == null) {
      synchronized (MergeRequestServiceGrpc.class) {
        if ((getGetMergeRequestDiffMethod = MergeRequestServiceGrpc.getGetMergeRequestDiffMethod) == null) {
          MergeRequestServiceGrpc.getGetMergeRequestDiffMethod = getGetMergeRequestDiffMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestDiffRequest, com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestDiffResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetMergeRequestDiff"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestDiffRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestDiffResponse.getDefaultInstance()))
              .setSchemaDescriptor(new MergeRequestServiceMethodDescriptorSupplier("GetMergeRequestDiff"))
              .build();
        }
      }
    }
    return getGetMergeRequestDiffMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListReviewsRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.ListReviewsResponse> getListReviewsMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "ListReviews",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.ListReviewsRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.ListReviewsResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListReviewsRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.ListReviewsResponse> getListReviewsMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListReviewsRequest, com.runnershigh.tps.infrastructure.grpc.proto.ListReviewsResponse> getListReviewsMethod;
    if ((getListReviewsMethod = MergeRequestServiceGrpc.getListReviewsMethod) == null) {
      synchronized (MergeRequestServiceGrpc.class) {
        if ((getListReviewsMethod = MergeRequestServiceGrpc.getListReviewsMethod) == null) {
          MergeRequestServiceGrpc.getListReviewsMethod = getListReviewsMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.ListReviewsRequest, com.runnershigh.tps.infrastructure.grpc.proto.ListReviewsResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListReviews"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.ListReviewsRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.ListReviewsResponse.getDefaultInstance()))
              .setSchemaDescriptor(new MergeRequestServiceMethodDescriptorSupplier("ListReviews"))
              .build();
        }
      }
    }
    return getListReviewsMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.SubmitReviewRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.SubmitReviewResponse> getSubmitReviewMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "SubmitReview",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.SubmitReviewRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.SubmitReviewResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.SubmitReviewRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.SubmitReviewResponse> getSubmitReviewMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.SubmitReviewRequest, com.runnershigh.tps.infrastructure.grpc.proto.SubmitReviewResponse> getSubmitReviewMethod;
    if ((getSubmitReviewMethod = MergeRequestServiceGrpc.getSubmitReviewMethod) == null) {
      synchronized (MergeRequestServiceGrpc.class) {
        if ((getSubmitReviewMethod = MergeRequestServiceGrpc.getSubmitReviewMethod) == null) {
          MergeRequestServiceGrpc.getSubmitReviewMethod = getSubmitReviewMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.SubmitReviewRequest, com.runnershigh.tps.infrastructure.grpc.proto.SubmitReviewResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "SubmitReview"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.SubmitReviewRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.SubmitReviewResponse.getDefaultInstance()))
              .setSchemaDescriptor(new MergeRequestServiceMethodDescriptorSupplier("SubmitReview"))
              .build();
        }
      }
    }
    return getSubmitReviewMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListCommentsRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.ListCommentsResponse> getListCommentsMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "ListComments",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.ListCommentsRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.ListCommentsResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListCommentsRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.ListCommentsResponse> getListCommentsMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.ListCommentsRequest, com.runnershigh.tps.infrastructure.grpc.proto.ListCommentsResponse> getListCommentsMethod;
    if ((getListCommentsMethod = MergeRequestServiceGrpc.getListCommentsMethod) == null) {
      synchronized (MergeRequestServiceGrpc.class) {
        if ((getListCommentsMethod = MergeRequestServiceGrpc.getListCommentsMethod) == null) {
          MergeRequestServiceGrpc.getListCommentsMethod = getListCommentsMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.ListCommentsRequest, com.runnershigh.tps.infrastructure.grpc.proto.ListCommentsResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListComments"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.ListCommentsRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.ListCommentsResponse.getDefaultInstance()))
              .setSchemaDescriptor(new MergeRequestServiceMethodDescriptorSupplier("ListComments"))
              .build();
        }
      }
    }
    return getListCommentsMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.CreateCommentRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.CreateCommentResponse> getCreateCommentMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "CreateComment",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.CreateCommentRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.CreateCommentResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.CreateCommentRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.CreateCommentResponse> getCreateCommentMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.CreateCommentRequest, com.runnershigh.tps.infrastructure.grpc.proto.CreateCommentResponse> getCreateCommentMethod;
    if ((getCreateCommentMethod = MergeRequestServiceGrpc.getCreateCommentMethod) == null) {
      synchronized (MergeRequestServiceGrpc.class) {
        if ((getCreateCommentMethod = MergeRequestServiceGrpc.getCreateCommentMethod) == null) {
          MergeRequestServiceGrpc.getCreateCommentMethod = getCreateCommentMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.CreateCommentRequest, com.runnershigh.tps.infrastructure.grpc.proto.CreateCommentResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "CreateComment"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.CreateCommentRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.CreateCommentResponse.getDefaultInstance()))
              .setSchemaDescriptor(new MergeRequestServiceMethodDescriptorSupplier("CreateComment"))
              .build();
        }
      }
    }
    return getCreateCommentMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.UpdateCommentRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.UpdateCommentResponse> getUpdateCommentMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "UpdateComment",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.UpdateCommentRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.UpdateCommentResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.UpdateCommentRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.UpdateCommentResponse> getUpdateCommentMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.UpdateCommentRequest, com.runnershigh.tps.infrastructure.grpc.proto.UpdateCommentResponse> getUpdateCommentMethod;
    if ((getUpdateCommentMethod = MergeRequestServiceGrpc.getUpdateCommentMethod) == null) {
      synchronized (MergeRequestServiceGrpc.class) {
        if ((getUpdateCommentMethod = MergeRequestServiceGrpc.getUpdateCommentMethod) == null) {
          MergeRequestServiceGrpc.getUpdateCommentMethod = getUpdateCommentMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.UpdateCommentRequest, com.runnershigh.tps.infrastructure.grpc.proto.UpdateCommentResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "UpdateComment"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.UpdateCommentRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.UpdateCommentResponse.getDefaultInstance()))
              .setSchemaDescriptor(new MergeRequestServiceMethodDescriptorSupplier("UpdateComment"))
              .build();
        }
      }
    }
    return getUpdateCommentMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.DeleteCommentRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.DeleteCommentResponse> getDeleteCommentMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "DeleteComment",
      requestType = com.runnershigh.tps.infrastructure.grpc.proto.DeleteCommentRequest.class,
      responseType = com.runnershigh.tps.infrastructure.grpc.proto.DeleteCommentResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.DeleteCommentRequest,
      com.runnershigh.tps.infrastructure.grpc.proto.DeleteCommentResponse> getDeleteCommentMethod() {
    io.grpc.MethodDescriptor<com.runnershigh.tps.infrastructure.grpc.proto.DeleteCommentRequest, com.runnershigh.tps.infrastructure.grpc.proto.DeleteCommentResponse> getDeleteCommentMethod;
    if ((getDeleteCommentMethod = MergeRequestServiceGrpc.getDeleteCommentMethod) == null) {
      synchronized (MergeRequestServiceGrpc.class) {
        if ((getDeleteCommentMethod = MergeRequestServiceGrpc.getDeleteCommentMethod) == null) {
          MergeRequestServiceGrpc.getDeleteCommentMethod = getDeleteCommentMethod =
              io.grpc.MethodDescriptor.<com.runnershigh.tps.infrastructure.grpc.proto.DeleteCommentRequest, com.runnershigh.tps.infrastructure.grpc.proto.DeleteCommentResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "DeleteComment"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.DeleteCommentRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.runnershigh.tps.infrastructure.grpc.proto.DeleteCommentResponse.getDefaultInstance()))
              .setSchemaDescriptor(new MergeRequestServiceMethodDescriptorSupplier("DeleteComment"))
              .build();
        }
      }
    }
    return getDeleteCommentMethod;
  }

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static MergeRequestServiceStub newStub(io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<MergeRequestServiceStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<MergeRequestServiceStub>() {
        @java.lang.Override
        public MergeRequestServiceStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new MergeRequestServiceStub(channel, callOptions);
        }
      };
    return MergeRequestServiceStub.newStub(factory, channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static MergeRequestServiceBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<MergeRequestServiceBlockingStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<MergeRequestServiceBlockingStub>() {
        @java.lang.Override
        public MergeRequestServiceBlockingStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new MergeRequestServiceBlockingStub(channel, callOptions);
        }
      };
    return MergeRequestServiceBlockingStub.newStub(factory, channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static MergeRequestServiceFutureStub newFutureStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<MergeRequestServiceFutureStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<MergeRequestServiceFutureStub>() {
        @java.lang.Override
        public MergeRequestServiceFutureStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new MergeRequestServiceFutureStub(channel, callOptions);
        }
      };
    return MergeRequestServiceFutureStub.newStub(factory, channel);
  }

  /**
   */
  public interface AsyncService {

    /**
     * <pre>
     * MR 목록 조회
     * </pre>
     */
    default void listMergeRequests(com.runnershigh.tps.infrastructure.grpc.proto.ListMergeRequestsRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListMergeRequestsResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListMergeRequestsMethod(), responseObserver);
    }

    /**
     * <pre>
     * MR 상세 조회
     * </pre>
     */
    default void getMergeRequest(com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetMergeRequestMethod(), responseObserver);
    }

    /**
     * <pre>
     * MR 생성
     * </pre>
     */
    default void createMergeRequest(com.runnershigh.tps.infrastructure.grpc.proto.CreateMergeRequestRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.CreateMergeRequestResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getCreateMergeRequestMethod(), responseObserver);
    }

    /**
     * <pre>
     * MR 수정
     * </pre>
     */
    default void updateMergeRequest(com.runnershigh.tps.infrastructure.grpc.proto.UpdateMergeRequestRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.UpdateMergeRequestResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getUpdateMergeRequestMethod(), responseObserver);
    }

    /**
     * <pre>
     * MR 머지
     * </pre>
     */
    default void mergeMergeRequest(com.runnershigh.tps.infrastructure.grpc.proto.MergeMergeRequestRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.MergeMergeRequestResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getMergeMergeRequestMethod(), responseObserver);
    }

    /**
     * <pre>
     * MR Diff 조회
     * </pre>
     */
    default void getMergeRequestDiff(com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestDiffRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestDiffResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetMergeRequestDiffMethod(), responseObserver);
    }

    /**
     * <pre>
     * 리뷰 목록 조회
     * </pre>
     */
    default void listReviews(com.runnershigh.tps.infrastructure.grpc.proto.ListReviewsRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListReviewsResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListReviewsMethod(), responseObserver);
    }

    /**
     * <pre>
     * 리뷰 제출
     * </pre>
     */
    default void submitReview(com.runnershigh.tps.infrastructure.grpc.proto.SubmitReviewRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.SubmitReviewResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getSubmitReviewMethod(), responseObserver);
    }

    /**
     * <pre>
     * 댓글 목록 조회
     * </pre>
     */
    default void listComments(com.runnershigh.tps.infrastructure.grpc.proto.ListCommentsRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListCommentsResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListCommentsMethod(), responseObserver);
    }

    /**
     * <pre>
     * 댓글 생성
     * </pre>
     */
    default void createComment(com.runnershigh.tps.infrastructure.grpc.proto.CreateCommentRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.CreateCommentResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getCreateCommentMethod(), responseObserver);
    }

    /**
     * <pre>
     * 댓글 수정
     * </pre>
     */
    default void updateComment(com.runnershigh.tps.infrastructure.grpc.proto.UpdateCommentRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.UpdateCommentResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getUpdateCommentMethod(), responseObserver);
    }

    /**
     * <pre>
     * 댓글 삭제
     * </pre>
     */
    default void deleteComment(com.runnershigh.tps.infrastructure.grpc.proto.DeleteCommentRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.DeleteCommentResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getDeleteCommentMethod(), responseObserver);
    }
  }

  /**
   * Base class for the server implementation of the service MergeRequestService.
   */
  public static abstract class MergeRequestServiceImplBase
      implements io.grpc.BindableService, AsyncService {

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return MergeRequestServiceGrpc.bindService(this);
    }
  }

  /**
   * A stub to allow clients to do asynchronous rpc calls to service MergeRequestService.
   */
  public static final class MergeRequestServiceStub
      extends io.grpc.stub.AbstractAsyncStub<MergeRequestServiceStub> {
    private MergeRequestServiceStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected MergeRequestServiceStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new MergeRequestServiceStub(channel, callOptions);
    }

    /**
     * <pre>
     * MR 목록 조회
     * </pre>
     */
    public void listMergeRequests(com.runnershigh.tps.infrastructure.grpc.proto.ListMergeRequestsRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListMergeRequestsResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getListMergeRequestsMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * MR 상세 조회
     * </pre>
     */
    public void getMergeRequest(com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getGetMergeRequestMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * MR 생성
     * </pre>
     */
    public void createMergeRequest(com.runnershigh.tps.infrastructure.grpc.proto.CreateMergeRequestRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.CreateMergeRequestResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getCreateMergeRequestMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * MR 수정
     * </pre>
     */
    public void updateMergeRequest(com.runnershigh.tps.infrastructure.grpc.proto.UpdateMergeRequestRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.UpdateMergeRequestResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getUpdateMergeRequestMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * MR 머지
     * </pre>
     */
    public void mergeMergeRequest(com.runnershigh.tps.infrastructure.grpc.proto.MergeMergeRequestRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.MergeMergeRequestResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getMergeMergeRequestMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * MR Diff 조회
     * </pre>
     */
    public void getMergeRequestDiff(com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestDiffRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestDiffResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getGetMergeRequestDiffMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * 리뷰 목록 조회
     * </pre>
     */
    public void listReviews(com.runnershigh.tps.infrastructure.grpc.proto.ListReviewsRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListReviewsResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getListReviewsMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * 리뷰 제출
     * </pre>
     */
    public void submitReview(com.runnershigh.tps.infrastructure.grpc.proto.SubmitReviewRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.SubmitReviewResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getSubmitReviewMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * 댓글 목록 조회
     * </pre>
     */
    public void listComments(com.runnershigh.tps.infrastructure.grpc.proto.ListCommentsRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListCommentsResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getListCommentsMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * 댓글 생성
     * </pre>
     */
    public void createComment(com.runnershigh.tps.infrastructure.grpc.proto.CreateCommentRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.CreateCommentResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getCreateCommentMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * 댓글 수정
     * </pre>
     */
    public void updateComment(com.runnershigh.tps.infrastructure.grpc.proto.UpdateCommentRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.UpdateCommentResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getUpdateCommentMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * 댓글 삭제
     * </pre>
     */
    public void deleteComment(com.runnershigh.tps.infrastructure.grpc.proto.DeleteCommentRequest request,
        io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.DeleteCommentResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getDeleteCommentMethod(), getCallOptions()), request, responseObserver);
    }
  }

  /**
   * A stub to allow clients to do synchronous rpc calls to service MergeRequestService.
   */
  public static final class MergeRequestServiceBlockingStub
      extends io.grpc.stub.AbstractBlockingStub<MergeRequestServiceBlockingStub> {
    private MergeRequestServiceBlockingStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected MergeRequestServiceBlockingStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new MergeRequestServiceBlockingStub(channel, callOptions);
    }

    /**
     * <pre>
     * MR 목록 조회
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.ListMergeRequestsResponse listMergeRequests(com.runnershigh.tps.infrastructure.grpc.proto.ListMergeRequestsRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getListMergeRequestsMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * MR 상세 조회
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestResponse getMergeRequest(com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getGetMergeRequestMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * MR 생성
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.CreateMergeRequestResponse createMergeRequest(com.runnershigh.tps.infrastructure.grpc.proto.CreateMergeRequestRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getCreateMergeRequestMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * MR 수정
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.UpdateMergeRequestResponse updateMergeRequest(com.runnershigh.tps.infrastructure.grpc.proto.UpdateMergeRequestRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getUpdateMergeRequestMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * MR 머지
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.MergeMergeRequestResponse mergeMergeRequest(com.runnershigh.tps.infrastructure.grpc.proto.MergeMergeRequestRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getMergeMergeRequestMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * MR Diff 조회
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestDiffResponse getMergeRequestDiff(com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestDiffRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getGetMergeRequestDiffMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * 리뷰 목록 조회
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.ListReviewsResponse listReviews(com.runnershigh.tps.infrastructure.grpc.proto.ListReviewsRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getListReviewsMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * 리뷰 제출
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.SubmitReviewResponse submitReview(com.runnershigh.tps.infrastructure.grpc.proto.SubmitReviewRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getSubmitReviewMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * 댓글 목록 조회
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.ListCommentsResponse listComments(com.runnershigh.tps.infrastructure.grpc.proto.ListCommentsRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getListCommentsMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * 댓글 생성
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.CreateCommentResponse createComment(com.runnershigh.tps.infrastructure.grpc.proto.CreateCommentRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getCreateCommentMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * 댓글 수정
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.UpdateCommentResponse updateComment(com.runnershigh.tps.infrastructure.grpc.proto.UpdateCommentRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getUpdateCommentMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * 댓글 삭제
     * </pre>
     */
    public com.runnershigh.tps.infrastructure.grpc.proto.DeleteCommentResponse deleteComment(com.runnershigh.tps.infrastructure.grpc.proto.DeleteCommentRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getDeleteCommentMethod(), getCallOptions(), request);
    }
  }

  /**
   * A stub to allow clients to do ListenableFuture-style rpc calls to service MergeRequestService.
   */
  public static final class MergeRequestServiceFutureStub
      extends io.grpc.stub.AbstractFutureStub<MergeRequestServiceFutureStub> {
    private MergeRequestServiceFutureStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected MergeRequestServiceFutureStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new MergeRequestServiceFutureStub(channel, callOptions);
    }

    /**
     * <pre>
     * MR 목록 조회
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.ListMergeRequestsResponse> listMergeRequests(
        com.runnershigh.tps.infrastructure.grpc.proto.ListMergeRequestsRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getListMergeRequestsMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * MR 상세 조회
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestResponse> getMergeRequest(
        com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getGetMergeRequestMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * MR 생성
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.CreateMergeRequestResponse> createMergeRequest(
        com.runnershigh.tps.infrastructure.grpc.proto.CreateMergeRequestRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getCreateMergeRequestMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * MR 수정
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.UpdateMergeRequestResponse> updateMergeRequest(
        com.runnershigh.tps.infrastructure.grpc.proto.UpdateMergeRequestRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getUpdateMergeRequestMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * MR 머지
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.MergeMergeRequestResponse> mergeMergeRequest(
        com.runnershigh.tps.infrastructure.grpc.proto.MergeMergeRequestRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getMergeMergeRequestMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * MR Diff 조회
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestDiffResponse> getMergeRequestDiff(
        com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestDiffRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getGetMergeRequestDiffMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * 리뷰 목록 조회
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.ListReviewsResponse> listReviews(
        com.runnershigh.tps.infrastructure.grpc.proto.ListReviewsRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getListReviewsMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * 리뷰 제출
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.SubmitReviewResponse> submitReview(
        com.runnershigh.tps.infrastructure.grpc.proto.SubmitReviewRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getSubmitReviewMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * 댓글 목록 조회
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.ListCommentsResponse> listComments(
        com.runnershigh.tps.infrastructure.grpc.proto.ListCommentsRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getListCommentsMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * 댓글 생성
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.CreateCommentResponse> createComment(
        com.runnershigh.tps.infrastructure.grpc.proto.CreateCommentRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getCreateCommentMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * 댓글 수정
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.UpdateCommentResponse> updateComment(
        com.runnershigh.tps.infrastructure.grpc.proto.UpdateCommentRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getUpdateCommentMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * 댓글 삭제
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.runnershigh.tps.infrastructure.grpc.proto.DeleteCommentResponse> deleteComment(
        com.runnershigh.tps.infrastructure.grpc.proto.DeleteCommentRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getDeleteCommentMethod(), getCallOptions()), request);
    }
  }

  private static final int METHODID_LIST_MERGE_REQUESTS = 0;
  private static final int METHODID_GET_MERGE_REQUEST = 1;
  private static final int METHODID_CREATE_MERGE_REQUEST = 2;
  private static final int METHODID_UPDATE_MERGE_REQUEST = 3;
  private static final int METHODID_MERGE_MERGE_REQUEST = 4;
  private static final int METHODID_GET_MERGE_REQUEST_DIFF = 5;
  private static final int METHODID_LIST_REVIEWS = 6;
  private static final int METHODID_SUBMIT_REVIEW = 7;
  private static final int METHODID_LIST_COMMENTS = 8;
  private static final int METHODID_CREATE_COMMENT = 9;
  private static final int METHODID_UPDATE_COMMENT = 10;
  private static final int METHODID_DELETE_COMMENT = 11;

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
        case METHODID_LIST_MERGE_REQUESTS:
          serviceImpl.listMergeRequests((com.runnershigh.tps.infrastructure.grpc.proto.ListMergeRequestsRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListMergeRequestsResponse>) responseObserver);
          break;
        case METHODID_GET_MERGE_REQUEST:
          serviceImpl.getMergeRequest((com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestResponse>) responseObserver);
          break;
        case METHODID_CREATE_MERGE_REQUEST:
          serviceImpl.createMergeRequest((com.runnershigh.tps.infrastructure.grpc.proto.CreateMergeRequestRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.CreateMergeRequestResponse>) responseObserver);
          break;
        case METHODID_UPDATE_MERGE_REQUEST:
          serviceImpl.updateMergeRequest((com.runnershigh.tps.infrastructure.grpc.proto.UpdateMergeRequestRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.UpdateMergeRequestResponse>) responseObserver);
          break;
        case METHODID_MERGE_MERGE_REQUEST:
          serviceImpl.mergeMergeRequest((com.runnershigh.tps.infrastructure.grpc.proto.MergeMergeRequestRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.MergeMergeRequestResponse>) responseObserver);
          break;
        case METHODID_GET_MERGE_REQUEST_DIFF:
          serviceImpl.getMergeRequestDiff((com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestDiffRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestDiffResponse>) responseObserver);
          break;
        case METHODID_LIST_REVIEWS:
          serviceImpl.listReviews((com.runnershigh.tps.infrastructure.grpc.proto.ListReviewsRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListReviewsResponse>) responseObserver);
          break;
        case METHODID_SUBMIT_REVIEW:
          serviceImpl.submitReview((com.runnershigh.tps.infrastructure.grpc.proto.SubmitReviewRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.SubmitReviewResponse>) responseObserver);
          break;
        case METHODID_LIST_COMMENTS:
          serviceImpl.listComments((com.runnershigh.tps.infrastructure.grpc.proto.ListCommentsRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.ListCommentsResponse>) responseObserver);
          break;
        case METHODID_CREATE_COMMENT:
          serviceImpl.createComment((com.runnershigh.tps.infrastructure.grpc.proto.CreateCommentRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.CreateCommentResponse>) responseObserver);
          break;
        case METHODID_UPDATE_COMMENT:
          serviceImpl.updateComment((com.runnershigh.tps.infrastructure.grpc.proto.UpdateCommentRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.UpdateCommentResponse>) responseObserver);
          break;
        case METHODID_DELETE_COMMENT:
          serviceImpl.deleteComment((com.runnershigh.tps.infrastructure.grpc.proto.DeleteCommentRequest) request,
              (io.grpc.stub.StreamObserver<com.runnershigh.tps.infrastructure.grpc.proto.DeleteCommentResponse>) responseObserver);
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
          getListMergeRequestsMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.ListMergeRequestsRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.ListMergeRequestsResponse>(
                service, METHODID_LIST_MERGE_REQUESTS)))
        .addMethod(
          getGetMergeRequestMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestResponse>(
                service, METHODID_GET_MERGE_REQUEST)))
        .addMethod(
          getCreateMergeRequestMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.CreateMergeRequestRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.CreateMergeRequestResponse>(
                service, METHODID_CREATE_MERGE_REQUEST)))
        .addMethod(
          getUpdateMergeRequestMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.UpdateMergeRequestRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.UpdateMergeRequestResponse>(
                service, METHODID_UPDATE_MERGE_REQUEST)))
        .addMethod(
          getMergeMergeRequestMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.MergeMergeRequestRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.MergeMergeRequestResponse>(
                service, METHODID_MERGE_MERGE_REQUEST)))
        .addMethod(
          getGetMergeRequestDiffMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestDiffRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.GetMergeRequestDiffResponse>(
                service, METHODID_GET_MERGE_REQUEST_DIFF)))
        .addMethod(
          getListReviewsMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.ListReviewsRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.ListReviewsResponse>(
                service, METHODID_LIST_REVIEWS)))
        .addMethod(
          getSubmitReviewMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.SubmitReviewRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.SubmitReviewResponse>(
                service, METHODID_SUBMIT_REVIEW)))
        .addMethod(
          getListCommentsMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.ListCommentsRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.ListCommentsResponse>(
                service, METHODID_LIST_COMMENTS)))
        .addMethod(
          getCreateCommentMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.CreateCommentRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.CreateCommentResponse>(
                service, METHODID_CREATE_COMMENT)))
        .addMethod(
          getUpdateCommentMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.UpdateCommentRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.UpdateCommentResponse>(
                service, METHODID_UPDATE_COMMENT)))
        .addMethod(
          getDeleteCommentMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.runnershigh.tps.infrastructure.grpc.proto.DeleteCommentRequest,
              com.runnershigh.tps.infrastructure.grpc.proto.DeleteCommentResponse>(
                service, METHODID_DELETE_COMMENT)))
        .build();
  }

  private static abstract class MergeRequestServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    MergeRequestServiceBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return com.runnershigh.tps.infrastructure.grpc.proto.MergeRequestProto.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("MergeRequestService");
    }
  }

  private static final class MergeRequestServiceFileDescriptorSupplier
      extends MergeRequestServiceBaseDescriptorSupplier {
    MergeRequestServiceFileDescriptorSupplier() {}
  }

  private static final class MergeRequestServiceMethodDescriptorSupplier
      extends MergeRequestServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final java.lang.String methodName;

    MergeRequestServiceMethodDescriptorSupplier(java.lang.String methodName) {
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
      synchronized (MergeRequestServiceGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new MergeRequestServiceFileDescriptorSupplier())
              .addMethod(getListMergeRequestsMethod())
              .addMethod(getGetMergeRequestMethod())
              .addMethod(getCreateMergeRequestMethod())
              .addMethod(getUpdateMergeRequestMethod())
              .addMethod(getMergeMergeRequestMethod())
              .addMethod(getGetMergeRequestDiffMethod())
              .addMethod(getListReviewsMethod())
              .addMethod(getSubmitReviewMethod())
              .addMethod(getListCommentsMethod())
              .addMethod(getCreateCommentMethod())
              .addMethod(getUpdateCommentMethod())
              .addMethod(getDeleteCommentMethod())
              .build();
        }
      }
    }
    return result;
  }
}
