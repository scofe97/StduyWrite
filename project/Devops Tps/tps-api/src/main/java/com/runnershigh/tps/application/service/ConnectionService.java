package com.runnershigh.tps.application.service;

import com.runnershigh.tps.application.port.in.ConnectionUseCase;
import com.runnershigh.tps.application.port.out.ConnectionRepository;
import com.runnershigh.tps.domain.connection.Connection;
import com.runnershigh.tps.domain.connection.ConnectionStatus;
import com.runnershigh.tps.domain.connection.ProviderType;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
@Transactional
public class ConnectionService implements ConnectionUseCase {

    private final ConnectionRepository connectionRepository;

    @Override
    public Connection createConnection(CreateConnectionCommand command) {
        Connection connection = Connection.builder()
                .projectId(command.projectId())
                .providerType(command.providerType())
                .name(command.name())
                .baseUrl(command.baseUrl())
                .apiToken(command.apiToken())
                .status(ConnectionStatus.PENDING)
                .metadata(command.metadata())
                .build();

        return connectionRepository.save(connection);
    }

    @Override
    public Connection updateConnection(UUID id, UpdateConnectionCommand command) {
        Connection connection = getConnection(id);

        if (command.name() != null) {
            connection.setName(command.name());
        }
        if (command.baseUrl() != null) {
            connection.setBaseUrl(command.baseUrl());
        }
        if (command.apiToken() != null) {
            connection.setApiToken(command.apiToken());
        }
        if (command.metadata() != null) {
            connection.setMetadata(command.metadata());
        }

        return connectionRepository.update(connection);
    }

    @Override
    @Transactional(readOnly = true)
    public Connection getConnection(UUID id) {
        return connectionRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Connection not found: " + id));
    }

    @Override
    @Transactional(readOnly = true)
    public List<Connection> getConnectionsByProjectId(UUID projectId) {
        return connectionRepository.findByProjectId(projectId);
    }

    @Override
    @Transactional(readOnly = true)
    public List<Connection> getConnectionsByProviderType(ProviderType providerType) {
        return connectionRepository.findByProviderType(providerType);
    }

    @Override
    @Transactional(readOnly = true)
    public List<Connection> getActiveConnections() {
        return connectionRepository.findActiveConnections();
    }

    @Override
    public void deleteConnection(UUID id) {
        if (!connectionRepository.existsById(id)) {
            throw new IllegalArgumentException("Connection not found: " + id);
        }
        connectionRepository.deleteById(id);
    }

    @Override
    public Connection activateConnection(UUID id) {
        Connection connection = getConnection(id);
        connection.activate();
        return connectionRepository.update(connection);
    }

    @Override
    public Connection deactivateConnection(UUID id) {
        Connection connection = getConnection(id);
        connection.deactivate();
        return connectionRepository.update(connection);
    }

    @Override
    public boolean testConnection(UUID id) {
        Connection connection = getConnection(id);
        connection.markAsTesting();
        connectionRepository.update(connection);

        // TODO: Implement actual connection test with Git provider
        // For now, simulate successful test
        boolean success = true;

        if (success) {
            connection.activate();
        } else {
            connection.markAsFailed();
        }
        connectionRepository.update(connection);

        return success;
    }
}
