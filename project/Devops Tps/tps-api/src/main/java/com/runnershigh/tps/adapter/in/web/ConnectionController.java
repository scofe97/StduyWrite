package com.runnershigh.tps.adapter.in.web;

import com.runnershigh.tps.adapter.in.web.dto.connection.ConnectionRequest;
import com.runnershigh.tps.adapter.in.web.dto.connection.ConnectionResponse;
import com.runnershigh.tps.application.port.in.ConnectionUseCase;
import com.runnershigh.tps.domain.connection.Connection;
import com.runnershigh.tps.domain.connection.ProviderType;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/v1/connections")
@RequiredArgsConstructor
@Tag(name = "Connection API", description = "Git Provider 연결 관리 API")
public class ConnectionController {

    private final ConnectionUseCase connectionUseCase;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    @Operation(summary = "연결 생성", description = "새로운 Git Provider 연결을 생성합니다.")
    public ConnectionResponse createConnection(
            @Valid @RequestBody ConnectionRequest.Create request) {

        ConnectionUseCase.CreateConnectionCommand command = new ConnectionUseCase.CreateConnectionCommand(
                request.getProjectId(),
                request.getProviderType(),
                request.getName(),
                request.getBaseUrl(),
                request.getApiToken(),
                request.getMetadata()
        );

        Connection connection = connectionUseCase.createConnection(command);
        return ConnectionResponse.from(connection);
    }

    @PutMapping("/{id}")
    @Operation(summary = "연결 수정", description = "기존 연결 정보를 수정합니다.")
    public ConnectionResponse updateConnection(
            @PathVariable UUID id,
            @Valid @RequestBody ConnectionRequest.Update request) {

        ConnectionUseCase.UpdateConnectionCommand command = new ConnectionUseCase.UpdateConnectionCommand(
                request.getName(),
                request.getBaseUrl(),
                request.getApiToken(),
                request.getMetadata()
        );

        Connection connection = connectionUseCase.updateConnection(id, command);
        return ConnectionResponse.from(connection);
    }

    @GetMapping("/{id}")
    @Operation(summary = "연결 조회", description = "연결 상세 정보를 조회합니다.")
    public ConnectionResponse getConnection(@PathVariable UUID id) {
        Connection connection = connectionUseCase.getConnection(id);
        return ConnectionResponse.from(connection);
    }

    @GetMapping("/project/{projectId}")
    @Operation(summary = "프로젝트별 연결 목록", description = "프로젝트의 모든 연결을 조회합니다.")
    public List<ConnectionResponse> getConnectionsByProjectId(@PathVariable UUID projectId) {
        return connectionUseCase.getConnectionsByProjectId(projectId)
                .stream()
                .map(ConnectionResponse::from)
                .toList();
    }

    @GetMapping("/provider/{providerType}")
    @Operation(summary = "Provider 타입별 연결 목록", description = "특정 Provider 타입의 모든 연결을 조회합니다.")
    public List<ConnectionResponse> getConnectionsByProviderType(@PathVariable ProviderType providerType) {
        return connectionUseCase.getConnectionsByProviderType(providerType)
                .stream()
                .map(ConnectionResponse::from)
                .toList();
    }

    @GetMapping("/active")
    @Operation(summary = "활성 연결 목록", description = "활성 상태의 모든 연결을 조회합니다.")
    public List<ConnectionResponse> getActiveConnections() {
        return connectionUseCase.getActiveConnections()
                .stream()
                .map(ConnectionResponse::from)
                .toList();
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    @Operation(summary = "연결 삭제", description = "연결을 삭제합니다.")
    public void deleteConnection(@PathVariable UUID id) {
        connectionUseCase.deleteConnection(id);
    }

    @PostMapping("/{id}/activate")
    @Operation(summary = "연결 활성화", description = "연결을 활성화합니다.")
    public ConnectionResponse activateConnection(@PathVariable UUID id) {
        Connection connection = connectionUseCase.activateConnection(id);
        return ConnectionResponse.from(connection);
    }

    @PostMapping("/{id}/deactivate")
    @Operation(summary = "연결 비활성화", description = "연결을 비활성화합니다.")
    public ConnectionResponse deactivateConnection(@PathVariable UUID id) {
        Connection connection = connectionUseCase.deactivateConnection(id);
        return ConnectionResponse.from(connection);
    }

    @PostMapping("/{id}/test")
    @Operation(summary = "연결 테스트", description = "Git Provider 연결을 테스트합니다.")
    public boolean testConnection(@PathVariable UUID id) {
        return connectionUseCase.testConnection(id);
    }
}
