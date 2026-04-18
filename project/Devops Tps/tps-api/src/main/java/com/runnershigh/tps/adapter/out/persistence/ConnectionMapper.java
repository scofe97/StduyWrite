package com.runnershigh.tps.adapter.out.persistence;

import com.runnershigh.tps.domain.connection.Connection;
import com.runnershigh.tps.domain.connection.ConnectionStatus;
import com.runnershigh.tps.domain.connection.ProviderType;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;
import java.util.UUID;

@Mapper
public interface ConnectionMapper {

    void insert(Connection connection);

    void update(Connection connection);

    Connection findById(@Param("id") UUID id);

    List<Connection> findByProjectId(@Param("projectId") UUID projectId);

    List<Connection> findByProviderType(@Param("providerType") ProviderType providerType);

    List<Connection> findByStatus(@Param("status") ConnectionStatus status);

    List<Connection> findActiveConnections();

    void deleteById(@Param("id") UUID id);

    int countById(@Param("id") UUID id);
}
