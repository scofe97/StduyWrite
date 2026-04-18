-- TPS API Database Schema
-- Phase 1: Connection, Repository, Branch

-- Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Connections table (Git Provider connections)
CREATE TABLE connections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID,
    provider_type VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    base_url VARCHAR(500),
    api_token VARCHAR(1000),
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    metadata JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by VARCHAR(100),
    updated_by VARCHAR(100)
);

CREATE INDEX idx_connections_project_id ON connections(project_id);
CREATE INDEX idx_connections_provider_type ON connections(provider_type);
CREATE INDEX idx_connections_status ON connections(status);

-- Repositories table
CREATE TABLE repositories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID,
    connection_id UUID REFERENCES connections(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    git_protocol VARCHAR(20) NOT NULL DEFAULT 'https',
    git_host VARCHAR(255) NOT NULL,
    git_owner VARCHAR(255) NOT NULL,
    git_repo VARCHAR(255) NOT NULL,
    default_branch VARCHAR(100) NOT NULL DEFAULT 'main',
    strategy_type VARCHAR(50) NOT NULL DEFAULT 'GIT_FLOW',
    status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    last_sync_at TIMESTAMP,
    metadata JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by VARCHAR(100),
    updated_by VARCHAR(100)
);

CREATE INDEX idx_repositories_project_id ON repositories(project_id);
CREATE INDEX idx_repositories_connection_id ON repositories(connection_id);
CREATE INDEX idx_repositories_status ON repositories(status);
CREATE UNIQUE INDEX idx_repositories_project_name ON repositories(project_id, name);

-- Branches table
CREATE TABLE branches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    repository_id UUID NOT NULL REFERENCES repositories(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    branch_type VARCHAR(50) NOT NULL DEFAULT 'FEATURE',
    status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    source_branch_name VARCHAR(255),
    latest_commit_sha VARCHAR(100),
    metadata JSONB,
    is_protected BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by VARCHAR(100),
    updated_by VARCHAR(100)
);

CREATE INDEX idx_branches_repository_id ON branches(repository_id);
CREATE INDEX idx_branches_status ON branches(status);
CREATE INDEX idx_branches_branch_type ON branches(branch_type);
CREATE UNIQUE INDEX idx_branches_repo_name ON branches(repository_id, name);

-- Comments
COMMENT ON TABLE connections IS 'Git Provider 연결 정보 (GitHub, GitLab, Bitbucket 등)';
COMMENT ON TABLE repositories IS 'Git 저장소 정보';
COMMENT ON TABLE branches IS 'Git 브랜치 정보';

COMMENT ON COLUMN connections.provider_type IS 'GITHUB, GITLAB, BITBUCKET';
COMMENT ON COLUMN connections.status IS 'PENDING, TESTING, ACTIVE, INACTIVE, FAILED';
COMMENT ON COLUMN repositories.strategy_type IS 'GIT_FLOW, GITHUB_FLOW, TRUNK_BASED';
COMMENT ON COLUMN repositories.status IS 'ACTIVE, INACTIVE, SYNCING, ERROR';
COMMENT ON COLUMN branches.branch_type IS 'MAIN, DEVELOP, FEATURE, RELEASE, HOTFIX';
COMMENT ON COLUMN branches.status IS 'ACTIVE, MERGED, DELETED, STALE';
