package com.runnershigh.tps.adapter.out.persistence;

import com.runnershigh.tps.domain.repository.Repository;
import com.runnershigh.tps.domain.repository.RepositoryStatus;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;
import java.util.UUID;

@Mapper
public interface RepositoryMapper {

    void insert(Repository repository);

    void update(Repository repository);

    Repository findById(@Param("id") UUID id);

    List<Repository> findByProjectId(@Param("projectId") UUID projectId);

    List<Repository> findByConnectionId(@Param("connectionId") UUID connectionId);

    List<Repository> findByStatus(@Param("status") RepositoryStatus status);

    Repository findByProjectIdAndName(@Param("projectId") UUID projectId, @Param("name") String name);

    void deleteById(@Param("id") UUID id);

    int countById(@Param("id") UUID id);

    List<Repository> findAll();
}
