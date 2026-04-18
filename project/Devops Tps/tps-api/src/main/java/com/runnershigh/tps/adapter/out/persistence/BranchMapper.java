package com.runnershigh.tps.adapter.out.persistence;

import com.runnershigh.tps.domain.branch.Branch;
import com.runnershigh.tps.domain.branch.BranchStatus;
import com.runnershigh.tps.domain.branch.BranchType;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;
import java.util.UUID;

@Mapper
public interface BranchMapper {

    void insert(Branch branch);

    void update(Branch branch);

    Branch findById(@Param("id") UUID id);

    List<Branch> findByRepositoryId(@Param("repositoryId") UUID repositoryId);

    List<Branch> findByRepositoryIdAndStatus(@Param("repositoryId") UUID repositoryId,
                                              @Param("status") BranchStatus status);

    List<Branch> findByRepositoryIdAndType(@Param("repositoryId") UUID repositoryId,
                                            @Param("branchType") BranchType type);

    Branch findByRepositoryIdAndName(@Param("repositoryId") UUID repositoryId,
                                      @Param("name") String name);

    void deleteById(@Param("id") UUID id);

    void deleteByRepositoryId(@Param("repositoryId") UUID repositoryId);

    int countById(@Param("id") UUID id);
}
