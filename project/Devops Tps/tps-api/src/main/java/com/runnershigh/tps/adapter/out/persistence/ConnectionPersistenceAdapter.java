package com.runnershigh.tps.adapter.out.persistence;

import com.runnershigh.tps.application.port.out.ConnectionRepository;
import com.runnershigh.tps.domain.connection.Connection;
import com.runnershigh.tps.domain.connection.ConnectionStatus;
import com.runnershigh.tps.domain.connection.ProviderType;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
@RequiredArgsConstructor
public class ConnectionPersistenceAdapter implements ConnectionRepository {

    private final ConnectionMapper connectionMapper;

    @Override
    public Connection save(Connection connection) {
        connectionMapper.insert(connection);
        return connection;
    }

    @Override
    public Connection update(Connection connection) {
        connection.updateTimestamp();
        connectionMapper.update(connection);
        return connection;
    }

    @Override
    public Optional<Connection> findById(UUID id) {
        return Optional.ofNullable(connectionMapper.findById(id));
    }

    @Override
    public List<Connection> findByProjectId(UUID projectId) {
        return connectionMapper.findByProjectId(projectId);
    }

    @Override
    public List<Connection> findByProviderType(ProviderType providerType) {
        return connectionMapper.findByProviderType(providerType);
    }

    @Override
    public List<Connection> findByStatus(ConnectionStatus status) {
        return connectionMapper.findByStatus(status);
    }

    @Override
    public List<Connection> findActiveConnections() {
        return connectionMapper.findActiveConnections();
    }

    @Override
    public void deleteById(UUID id) {
        connectionMapper.deleteById(id);
    }

    @Override
    public boolean existsById(UUID id) {
        return connectionMapper.countById(id) > 0;
    }
}
