package com.runnershigh.tps.adapter.out.grpc;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.runnershigh.tps.application.port.out.ConnectionRepository;
import com.runnershigh.tps.application.port.out.GitProviderPort;
import com.runnershigh.tps.domain.connection.Connection;
import com.runnershigh.tps.domain.branchcomparison.BranchComparison;
import com.runnershigh.tps.domain.branchcomparison.CommitInfo;
import com.runnershigh.tps.domain.branchcomparison.DiffStat;
import com.runnershigh.tps.domain.branchcomparison.MergedBranchInfo;
import com.runnershigh.tps.domain.contents.ContentEntry;
import com.runnershigh.tps.domain.contents.ContentType;
import com.runnershigh.tps.domain.contents.TreeEntry;
import com.runnershigh.tps.domain.mergerequest.MergeRequest;
import com.runnershigh.tps.infrastructure.grpc.proto.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import net.devh.boot.grpc.client.inject.GrpcClient;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

/**
 * Git Provider gRPC 어댑터
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class GitProviderGrpcAdapter implements GitProviderPort {

    @GrpcClient("git-provider")
    private GitServiceGrpc.GitServiceBlockingStub gitServiceStub;

    @GrpcClient("git-provider")
    private ContentsServiceGrpc.ContentsServiceBlockingStub contentsServiceStub;

    @GrpcClient("git-provider")
    private BranchServiceGrpc.BranchServiceBlockingStub branchServiceStub;

    @GrpcClient("git-provider")
    private MergeRequestServiceGrpc.MergeRequestServiceBlockingStub mergeRequestServiceStub;

    private final ConnectionRepository connectionRepository;
    private final ObjectMapper objectMapper;

    // ========================================
    // Repository Operations
    // ========================================

    @Override
    public List<GitProviderPort.RemoteRepository> listRepositories(UUID connectionId) {
        Connection connection = getConnection(connectionId);
        ProviderConfig providerConfig = buildProviderConfig(connection);

        ListRepositoriesRequest request = ListRepositoriesRequest.newBuilder()
                .setProvider(providerConfig)
                .build();

        ListRepositoriesResponse response = gitServiceStub.listRepositories(request);

        return response.getRepositoriesList().stream()
                .map(this::convertToRemoteRepository)
                .collect(Collectors.toList());
    }

    @Override
    public GitProviderPort.RemoteRepository getRepository(UUID connectionId, String namespace, String repo) {
        Connection connection = getConnection(connectionId);
        ProviderConfig providerConfig = buildProviderConfig(connection);

        GetRepositoryRequest request = GetRepositoryRequest.newBuilder()
                .setProvider(providerConfig)
                .setNamespace(namespace)
                .setRepository(repo)
                .build();

        GetRepositoryResponse response = gitServiceStub.getRepository(request);
        return convertToRemoteRepository(response.getRepository());
    }

    // ========================================
    // Branch Operations
    // ========================================

    @Override
    public List<GitProviderPort.RemoteBranch> listBranches(UUID connectionId, String namespace, String repo) {
        Connection connection = getConnection(connectionId);
        ProviderConfig providerConfig = buildProviderConfig(connection);

        ListBranchesRequest request = ListBranchesRequest.newBuilder()
                .setProvider(providerConfig)
                .setNamespace(namespace)
                .setRepository(repo)
                .build();

        ListBranchesResponse response = gitServiceStub.listBranches(request);

        return response.getBranchesList().stream()
                .map(this::convertToRemoteBranch)
                .collect(Collectors.toList());
    }

    @Override
    public GitProviderPort.RemoteBranch getBranch(UUID connectionId, String namespace, String repo, String branch) {
        Connection connection = getConnection(connectionId);
        ProviderConfig providerConfig = buildProviderConfig(connection);

        GetBranchRequest request = GetBranchRequest.newBuilder()
                .setProvider(providerConfig)
                .setNamespace(namespace)
                .setRepository(repo)
                .setBranch(branch)
                .build();

        GetBranchResponse response = gitServiceStub.getBranch(request);
        return convertToRemoteBranch(response.getBranch());
    }

    @Override
    public GitProviderPort.RemoteBranch createBranch(UUID connectionId, String namespace, String repo, String branch, String ref) {
        Connection connection = getConnection(connectionId);
        ProviderConfig providerConfig = buildProviderConfig(connection);

        CreateBranchRequest request = CreateBranchRequest.newBuilder()
                .setProvider(providerConfig)
                .setNamespace(namespace)
                .setRepository(repo)
                .setBranch(branch)
                .setRef(ref)
                .build();

        CreateBranchResponse response = gitServiceStub.createBranch(request);
        return convertToRemoteBranch(response.getBranch());
    }

    @Override
    public void deleteBranch(UUID connectionId, String namespace, String repo, String branch) {
        Connection connection = getConnection(connectionId);
        ProviderConfig providerConfig = buildProviderConfig(connection);

        DeleteBranchRequest request = DeleteBranchRequest.newBuilder()
                .setProvider(providerConfig)
                .setNamespace(namespace)
                .setRepository(repo)
                .setBranch(branch)
                .build();

        gitServiceStub.deleteBranch(request);
    }

    // ========================================
    // Contents Operations
    // ========================================

    @Override
    public ContentEntry getContents(UUID connectionId, String namespace, String repo, String path, String ref) {
        Connection connection = getConnection(connectionId);
        ProviderConfig providerConfig = buildProviderConfig(connection);

        GetContentsRequest.Builder requestBuilder = GetContentsRequest.newBuilder()
                .setProvider(providerConfig)
                .setNamespace(namespace)
                .setRepository(repo)
                .setPath(path != null ? path : "");

        if (ref != null && !ref.isEmpty()) {
            requestBuilder.setRef(ref);
        }

        GetContentsResponse response = contentsServiceStub.getContents(requestBuilder.build());
        return convertToContentEntry(response.getContent());
    }

    @Override
    public List<TreeEntry> getTree(UUID connectionId, String namespace, String repo, String ref, boolean recursive) {
        Connection connection = getConnection(connectionId);
        ProviderConfig providerConfig = buildProviderConfig(connection);

        GetTreeRequest.Builder requestBuilder = GetTreeRequest.newBuilder()
                .setProvider(providerConfig)
                .setNamespace(namespace)
                .setRepository(repo)
                .setRecursive(recursive);

        if (ref != null && !ref.isEmpty()) {
            requestBuilder.setRef(ref);
        }

        GetTreeResponse response = contentsServiceStub.getTree(requestBuilder.build());

        return response.getEntriesList().stream()
                .map(this::convertToTreeEntry)
                .collect(Collectors.toList());
    }

    // ========================================
    // MergeRequest Operations
    // ========================================

    @Override
    public List<MergeRequest> listMergeRequests(UUID connectionId, String namespace, String repo, String state) {
        Connection connection = getConnection(connectionId);
        ProviderConfig providerConfig = buildProviderConfig(connection);

        ListMergeRequestsRequest.Builder requestBuilder =
                ListMergeRequestsRequest.newBuilder()
                        .setProvider(providerConfig)
                        .setNamespace(namespace)
                        .setRepository(repo);

        if (state != null && !state.isEmpty()) {
            requestBuilder.setState(convertToMergeRequestState(state));
        }

        ListMergeRequestsResponse response =
                mergeRequestServiceStub.listMergeRequests(requestBuilder.build());

        return response.getMergeRequestsList().stream()
                .map(this::convertToMergeRequest)
                .collect(Collectors.toList());
    }

    @Override
    public MergeRequest getMergeRequest(UUID connectionId, String namespace, String repo, Integer number) {
        Connection connection = getConnection(connectionId);
        ProviderConfig providerConfig = buildProviderConfig(connection);

        GetMergeRequestRequest request =
                GetMergeRequestRequest.newBuilder()
                        .setProvider(providerConfig)
                        .setNamespace(namespace)
                        .setRepository(repo)
                        .setNumber(number)
                        .build();

        GetMergeRequestResponse response =
                mergeRequestServiceStub.getMergeRequest(request);

        return convertToMergeRequest(response.getMergeRequest());
    }

    @Override
    public MergeRequest createMergeRequest(UUID connectionId, String namespace, String repo,
                                            String title, String description,
                                            String sourceBranch, String targetBranch) {
        Connection connection = getConnection(connectionId);
        ProviderConfig providerConfig = buildProviderConfig(connection);

        CreateMergeRequestRequest.Builder requestBuilder =
                CreateMergeRequestRequest.newBuilder()
                        .setProvider(providerConfig)
                        .setNamespace(namespace)
                        .setRepository(repo)
                        .setTitle(title)
                        .setSourceBranch(sourceBranch)
                        .setTargetBranch(targetBranch);

        if (description != null) {
            requestBuilder.setDescription(description);
        }

        CreateMergeRequestResponse response =
                mergeRequestServiceStub.createMergeRequest(requestBuilder.build());

        return convertToMergeRequest(response.getMergeRequest());
    }

    @Override
    public MergeRequest mergeMergeRequest(UUID connectionId, String namespace, String repo,
                                           Integer number, String commitMessage, boolean squash) {
        Connection connection = getConnection(connectionId);
        ProviderConfig providerConfig = buildProviderConfig(connection);

        MergeMergeRequestRequest.Builder requestBuilder =
                MergeMergeRequestRequest.newBuilder()
                        .setProvider(providerConfig)
                        .setNamespace(namespace)
                        .setRepository(repo)
                        .setNumber(number);

        if (commitMessage != null) {
            requestBuilder.setCommitMessage(commitMessage);
        }

        if (squash) {
            requestBuilder.setMergeMethod(MergeMethod.MERGE_METHOD_SQUASH);
        } else {
            requestBuilder.setMergeMethod(MergeMethod.MERGE_METHOD_MERGE);
        }

        MergeMergeRequestResponse response =
                mergeRequestServiceStub.mergeMergeRequest(requestBuilder.build());

        return convertToMergeRequest(response.getMergeRequest());
    }

    // ========================================
    // Branch Comparison Operations
    // ========================================

    @Override
    public GitProviderPort.BranchComparisonResult compareBranches(UUID connectionId, String namespace, String repo,
                                                   String base, String compare) {
        Connection connection = getConnection(connectionId);
        ProviderConfig providerConfig = buildProviderConfig(connection);

        CompareBranchesRequest request = CompareBranchesRequest.newBuilder()
                .setProvider(providerConfig)
                .setNamespace(namespace)
                .setRepository(repo)
                .setBase(base)
                .setCompare(compare)
                .build();

        CompareBranchesResponse response = branchServiceStub.compareBranches(request);
        return convertToBranchComparisonResult(response);
    }

    @Override
    public GitProviderPort.CommitDiffResult listCommitsDiff(UUID connectionId, String namespace, String repo,
                                             String base, String compare, int page, int perPage) {
        Connection connection = getConnection(connectionId);
        ProviderConfig providerConfig = buildProviderConfig(connection);

        ListCommitsDiffRequest request = ListCommitsDiffRequest.newBuilder()
                .setProvider(providerConfig)
                .setNamespace(namespace)
                .setRepository(repo)
                .setBase(base)
                .setCompare(compare)
                .setPage(page)
                .setPerPage(perPage)
                .build();

        ListCommitsDiffResponse response = branchServiceStub.listCommitsDiff(request);
        return convertToCommitDiffResult(response);
    }

    @Override
    public List<MergedBranchInfo> listMergedBranches(UUID connectionId, String namespace, String repo, String base) {
        Connection connection = getConnection(connectionId);
        ProviderConfig providerConfig = buildProviderConfig(connection);

        ListMergedBranchesRequest request = ListMergedBranchesRequest.newBuilder()
                .setProvider(providerConfig)
                .setNamespace(namespace)
                .setRepository(repo)
                .setBase(base != null ? base : "main")
                .build();

        ListMergedBranchesResponse response = branchServiceStub.listMergedBranches(request);
        return response.getBranchesList().stream()
                .map(this::convertToMergedBranchInfo)
                .collect(Collectors.toList());
    }

    @Override
    public List<com.runnershigh.tps.domain.branchcomparison.StaleBranchInfo> listStaleBranches(
            UUID connectionId, String namespace, String repo, int staleDays) {
        Connection connection = getConnection(connectionId);
        ProviderConfig providerConfig = buildProviderConfig(connection);

        ListStaleBranchesRequest request = ListStaleBranchesRequest.newBuilder()
                .setProvider(providerConfig)
                .setNamespace(namespace)
                .setRepository(repo)
                .setStaleDays(staleDays > 0 ? staleDays : 30)
                .build();

        ListStaleBranchesResponse response = branchServiceStub.listStaleBranches(request);
        return response.getBranchesList().stream()
                .map(this::convertToStaleBranchInfo)
                .collect(Collectors.toList());
    }

    @Override
    public com.runnershigh.tps.domain.branchcomparison.CleanupResult cleanupBranches(
            UUID connectionId, String namespace, String repo,
            boolean dryRun, List<String> excludePatterns,
            int staleDays, boolean includeMerged, boolean includeStale) {
        Connection connection = getConnection(connectionId);
        ProviderConfig providerConfig = buildProviderConfig(connection);

        CleanupBranchesRequest.Builder requestBuilder = CleanupBranchesRequest.newBuilder()
                .setProvider(providerConfig)
                .setNamespace(namespace)
                .setRepository(repo)
                .setDryRun(dryRun)
                .setStaleDays(staleDays > 0 ? staleDays : 30)
                .setIncludeMerged(includeMerged)
                .setIncludeStale(includeStale);

        if (excludePatterns != null) {
            requestBuilder.addAllExcludePatterns(excludePatterns);
        }

        CleanupBranchesResponse response = branchServiceStub.cleanupBranches(requestBuilder.build());
        return convertToCleanupResult(response.getResult());
    }

    // ========================================
    // Helper Methods
    // ========================================

    private Connection getConnection(UUID connectionId) {
        return connectionRepository.findById(connectionId)
                .orElseThrow(() -> new IllegalArgumentException("Connection not found: " + connectionId));
    }

    private ProviderConfig buildProviderConfig(Connection connection) {
        ProviderConfig.Builder configBuilder = ProviderConfig.newBuilder();

        switch (connection.getProviderType()) {
            case GITHUB -> {
                GitHubConfig.Builder githubBuilder = GitHubConfig.newBuilder()
                        .setToken(connection.getApiToken());
                if (connection.getBaseUrl() != null && !connection.getBaseUrl().isEmpty()) {
                    githubBuilder.setBaseUrl(connection.getBaseUrl());
                }
                configBuilder.setGithub(githubBuilder.build());
            }
            case GITLAB -> {
                GitLabConfig.Builder gitlabBuilder = GitLabConfig.newBuilder()
                        .setToken(connection.getApiToken());
                if (connection.getBaseUrl() != null && !connection.getBaseUrl().isEmpty()) {
                    gitlabBuilder.setBaseUrl(connection.getBaseUrl());
                }
                configBuilder.setGitlab(gitlabBuilder.build());
            }
            case BITBUCKET -> {
                String email = "";
                String workspace = "";
                if (connection.getMetadata() != null && !connection.getMetadata().isEmpty()) {
                    try {
                        JsonNode metadata = objectMapper.readTree(connection.getMetadata());
                        email = metadata.path("email").asText("");
                        workspace = metadata.path("workspace").asText("");
                    } catch (Exception e) {
                        log.warn("Failed to parse bitbucket metadata: {}", e.getMessage());
                    }
                }
                configBuilder.setBitbucket(BitbucketConfig.newBuilder()
                        .setEmail(email)
                        .setApiToken(connection.getApiToken())
                        .setWorkspace(workspace)
                        .build());
            }
        }

        return configBuilder.build();
    }

    private GitProviderPort.RemoteRepository convertToRemoteRepository(Repository repo) {
        return new GitProviderPort.RemoteRepository(
                repo.getId(),
                repo.getName(),
                repo.getFullName(),
                repo.getDescription(),
                repo.getUrl(),
                repo.getCloneUrl(),
                repo.getSshUrl(),
                repo.getDefaultBranch(),
                repo.getPrivate()
        );
    }

    private GitProviderPort.RemoteBranch convertToRemoteBranch(Branch branch) {
        return new GitProviderPort.RemoteBranch(
                branch.getName(),
                branch.getSha(),
                branch.getProtected(),
                branch.getIsDefault()
        );
    }

    private TreeEntry convertToTreeEntry(com.runnershigh.tps.infrastructure.grpc.proto.TreeEntry entry) {
        return TreeEntry.builder()
                .path(entry.getPath())
                .type(entry.getType())
                .sha(entry.getSha())
                .size(entry.getSize())
                .mode(entry.getMode())
                .build();
    }

    private ContentEntry convertToContentEntry(com.runnershigh.tps.infrastructure.grpc.proto.ContentEntry entry) {
        List<ContentEntry> children = null;
        if (entry.getEntriesCount() > 0) {
            children = entry.getEntriesList().stream()
                    .map(this::convertToContentEntry)
                    .collect(Collectors.toList());
        }

        return ContentEntry.builder()
                .type(convertContentType(entry.getType()))
                .name(entry.getName())
                .path(entry.getPath())
                .size(entry.getSize())
                .sha(entry.getSha())
                .content(entry.getContent())
                .encoding(entry.getEncoding())
                .entries(children)
                .build();
    }

    private ContentType convertContentType(com.runnershigh.tps.infrastructure.grpc.proto.ContentType type) {
        return switch (type) {
            case CONTENT_TYPE_FILE -> ContentType.FILE;
            case CONTENT_TYPE_DIRECTORY -> ContentType.DIRECTORY;
            case CONTENT_TYPE_SYMLINK -> ContentType.SYMLINK;
            case CONTENT_TYPE_SUBMODULE -> ContentType.SUBMODULE;
            default -> ContentType.FILE;
        };
    }

    // ========================================
    // Branch Comparison Conversion Helpers
    // ========================================

    private GitProviderPort.BranchComparisonResult convertToBranchComparisonResult(CompareBranchesResponse response) {
        com.runnershigh.tps.infrastructure.grpc.proto.BranchComparison comp = response.getComparison();

        BranchComparison comparison = BranchComparison.builder()
                .baseBranch(comp.getBaseBranch())
                .compareBranch(comp.getCompareBranch())
                .aheadBy(comp.getAheadBy())
                .behindBy(comp.getBehindBy())
                .mergeable(convertMergeableState(comp.getMergeable()))
                .mergeStatus(comp.getMergeStatus())
                .suggestedAction(convertSuggestedAction(comp.getSuggestedAction()))
                .baseSha(comp.getBaseSha())
                .compareSha(comp.getCompareSha())
                .mergeBaseSha(comp.getMergeBaseSha())
                .build();

        DiffStat diffStat = null;
        if (response.hasDiffStat()) {
            com.runnershigh.tps.infrastructure.grpc.proto.DiffStat ds = response.getDiffStat();
            diffStat = DiffStat.builder()
                    .filesChanged(ds.getFilesChanged())
                    .additions(ds.getAdditions())
                    .deletions(ds.getDeletions())
                    .build();
        }

        return new GitProviderPort.BranchComparisonResult(comparison, diffStat);
    }

    private GitProviderPort.CommitDiffResult convertToCommitDiffResult(ListCommitsDiffResponse response) {
        List<CommitInfo> commits = response.getCommitsList().stream()
                .map(this::convertToCommitInfo)
                .collect(Collectors.toList());

        return new GitProviderPort.CommitDiffResult(commits, response.getTotalCount());
    }

    private CommitInfo convertToCommitInfo(com.runnershigh.tps.infrastructure.grpc.proto.CommitInfo commit) {
        return CommitInfo.builder()
                .sha(commit.getSha())
                .message(commit.getMessage())
                .authorName(commit.getAuthorName())
                .authorEmail(commit.getAuthorEmail())
                .date(commit.getDate())
                .build();
    }

    private MergedBranchInfo convertToMergedBranchInfo(com.runnershigh.tps.infrastructure.grpc.proto.MergedBranchInfo info) {
        return MergedBranchInfo.builder()
                .name(info.getName())
                .mergedAt(info.getMergedAt())
                .mergedBy(info.getMergedBy())
                .lastCommitSha(info.getLastCommitSha())
                .mergedInto(info.getMergedInto())
                .build();
    }

    private com.runnershigh.tps.domain.branchcomparison.StaleBranchInfo convertToStaleBranchInfo(
            com.runnershigh.tps.infrastructure.grpc.proto.StaleBranchInfo info) {
        return com.runnershigh.tps.domain.branchcomparison.StaleBranchInfo.builder()
                .name(info.getName())
                .lastCommitSha(info.getLastCommitSha())
                .lastCommitDate(info.getLastCommitDate())
                .daysInactive(info.getDaysInactive())
                .build();
    }

    private com.runnershigh.tps.domain.branchcomparison.CleanupResult convertToCleanupResult(
            com.runnershigh.tps.infrastructure.grpc.proto.CleanupResult result) {
        return new com.runnershigh.tps.domain.branchcomparison.CleanupResult(
            result.getDeletedList(),
            result.getSkippedList(),
            result.getFailedList(),
            result.getDryRun()
        );
    }

    private com.runnershigh.tps.domain.branchcomparison.MergeableState convertMergeableState(
            com.runnershigh.tps.infrastructure.grpc.proto.MergeableState state) {
        return switch (state) {
            case MERGEABLE_STATE_MERGEABLE -> com.runnershigh.tps.domain.branchcomparison.MergeableState.MERGEABLE;
            case MERGEABLE_STATE_CONFLICTING -> com.runnershigh.tps.domain.branchcomparison.MergeableState.CONFLICTING;
            case MERGEABLE_STATE_UNKNOWN -> com.runnershigh.tps.domain.branchcomparison.MergeableState.UNKNOWN;
            default -> com.runnershigh.tps.domain.branchcomparison.MergeableState.UNSPECIFIED;
        };
    }

    private com.runnershigh.tps.domain.branchcomparison.SuggestedAction convertSuggestedAction(
            com.runnershigh.tps.infrastructure.grpc.proto.SuggestedAction action) {
        return switch (action) {
            case SUGGESTED_ACTION_CREATE_MR -> com.runnershigh.tps.domain.branchcomparison.SuggestedAction.CREATE_MR;
            case SUGGESTED_ACTION_REBASE -> com.runnershigh.tps.domain.branchcomparison.SuggestedAction.REBASE;
            case SUGGESTED_ACTION_MERGE_BASE -> com.runnershigh.tps.domain.branchcomparison.SuggestedAction.MERGE_BASE;
            case SUGGESTED_ACTION_RESOLVE_CONFLICTS -> com.runnershigh.tps.domain.branchcomparison.SuggestedAction.RESOLVE_CONFLICTS;
            case SUGGESTED_ACTION_UP_TO_DATE -> com.runnershigh.tps.domain.branchcomparison.SuggestedAction.UP_TO_DATE;
            default -> com.runnershigh.tps.domain.branchcomparison.SuggestedAction.UNSPECIFIED;
        };
    }

    // ========================================
    // MergeRequest Conversion Helpers
    // ========================================

    private MergeRequest convertToMergeRequest(com.runnershigh.tps.infrastructure.grpc.proto.MergeRequest mr) {
        if (mr == null) {
            return null;
        }

        return MergeRequest.builder()
                .externalId(mr.getId())
                .number(mr.getNumber())
                .title(mr.getTitle())
                .description(mr.getDescription())
                .status(convertToMergeRequestStatus(mr.getState()))
                .sourceBranch(mr.getSourceBranch())
                .targetBranch(mr.getTargetBranch())
                .authorName(mr.getAuthor() != null ? mr.getAuthor().getLogin() : null)
                .authorEmail(mr.getAuthor() != null ? mr.getAuthor().getEmail() : null)
                .url(mr.getUrl())
                .mergedAt(mr.getMergedAt().isEmpty() ? null : mr.getMergedAt())
                .closedAt(mr.getClosedAt().isEmpty() ? null : mr.getClosedAt())
                .build();
    }

    private com.runnershigh.tps.domain.mergerequest.MergeRequestStatus convertToMergeRequestStatus(
            MergeRequestState state) {
        return switch (state) {
            case MERGE_REQUEST_STATE_OPEN -> com.runnershigh.tps.domain.mergerequest.MergeRequestStatus.OPEN;
            case MERGE_REQUEST_STATE_CLOSED -> com.runnershigh.tps.domain.mergerequest.MergeRequestStatus.CLOSED;
            case MERGE_REQUEST_STATE_MERGED -> com.runnershigh.tps.domain.mergerequest.MergeRequestStatus.MERGED;
            case MERGE_REQUEST_STATE_DRAFT -> com.runnershigh.tps.domain.mergerequest.MergeRequestStatus.DRAFT;
            default -> com.runnershigh.tps.domain.mergerequest.MergeRequestStatus.OPEN;
        };
    }

    private MergeRequestState convertToMergeRequestState(String state) {
        if (state == null || state.isEmpty()) {
            return MergeRequestState.MERGE_REQUEST_STATE_UNSPECIFIED;
        }
        return switch (state.toLowerCase()) {
            case "open" -> MergeRequestState.MERGE_REQUEST_STATE_OPEN;
            case "closed" -> MergeRequestState.MERGE_REQUEST_STATE_CLOSED;
            case "merged" -> MergeRequestState.MERGE_REQUEST_STATE_MERGED;
            case "draft" -> MergeRequestState.MERGE_REQUEST_STATE_DRAFT;
            default -> MergeRequestState.MERGE_REQUEST_STATE_UNSPECIFIED;
        };
    }
}
