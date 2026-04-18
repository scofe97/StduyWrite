-- TPS API Database Schema
-- Phase 1 Step 2 & 3: User, Project, Workflow, Ticket

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    display_name VARCHAR(255),
    role VARCHAR(50) NOT NULL DEFAULT 'MEMBER',
    status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status);

-- Projects table
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    project_key VARCHAR(20) NOT NULL UNIQUE,
    owner_id UUID REFERENCES users(id) ON DELETE SET NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    metadata JSONB,
    ticket_sequence INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_projects_owner_id ON projects(owner_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE UNIQUE INDEX idx_projects_key ON projects(project_key);

-- Update connections table to reference projects
ALTER TABLE connections
    ADD CONSTRAINT fk_connections_project
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE;

-- Update repositories table to reference projects
ALTER TABLE repositories
    ADD CONSTRAINT fk_repositories_project
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE;

-- Workflows table (JSONB-based node/edge definitions)
CREATE TABLE workflows (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'DRAFT',
    nodes_json JSONB NOT NULL DEFAULT '[]',
    edges_json JSONB NOT NULL DEFAULT '[]',
    config_json JSONB,
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    version INT NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_workflows_project_id ON workflows(project_id);
CREATE INDEX idx_workflows_status ON workflows(status);
CREATE INDEX idx_workflows_default ON workflows(project_id, is_default) WHERE is_default = true;

-- Tickets table (7-stage lifecycle)
CREATE TABLE tickets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    workflow_id UUID REFERENCES workflows(id) ON DELETE SET NULL,
    ticket_number VARCHAR(50) NOT NULL UNIQUE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    type VARCHAR(50) NOT NULL DEFAULT 'TASK',
    priority VARCHAR(50) NOT NULL DEFAULT 'MEDIUM',
    stage VARCHAR(50) NOT NULL DEFAULT 'BACKLOG',
    assignee_id UUID REFERENCES users(id) ON DELETE SET NULL,
    reporter_id UUID REFERENCES users(id) ON DELETE SET NULL,
    branch_id UUID REFERENCES branches(id) ON DELETE SET NULL,
    due_date TIMESTAMP,
    story_points INT DEFAULT 0,
    labels_json JSONB DEFAULT '[]',
    custom_fields_json JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tickets_project_id ON tickets(project_id);
CREATE INDEX idx_tickets_workflow_id ON tickets(workflow_id);
CREATE INDEX idx_tickets_stage ON tickets(stage);
CREATE INDEX idx_tickets_type ON tickets(type);
CREATE INDEX idx_tickets_priority ON tickets(priority);
CREATE INDEX idx_tickets_assignee_id ON tickets(assignee_id);
CREATE INDEX idx_tickets_reporter_id ON tickets(reporter_id);
CREATE INDEX idx_tickets_branch_id ON tickets(branch_id);
CREATE INDEX idx_tickets_due_date ON tickets(due_date) WHERE due_date IS NOT NULL;
CREATE INDEX idx_tickets_ticket_number ON tickets(ticket_number);

-- Ticket stage transitions audit log
CREATE TABLE ticket_stage_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ticket_id UUID NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
    from_stage VARCHAR(50),
    to_stage VARCHAR(50) NOT NULL,
    changed_by UUID REFERENCES users(id),
    changed_at TIMESTAMP NOT NULL DEFAULT NOW(),
    comment TEXT
);

CREATE INDEX idx_ticket_stage_history_ticket_id ON ticket_stage_history(ticket_id);
CREATE INDEX idx_ticket_stage_history_changed_at ON ticket_stage_history(changed_at);

-- Comments
COMMENT ON TABLE users IS '사용자 정보';
COMMENT ON TABLE projects IS '프로젝트 정보';
COMMENT ON TABLE workflows IS '워크플로우 정의 (JSONB 기반 노드/엣지)';
COMMENT ON TABLE tickets IS '티켓 (7단계 라이프사이클)';
COMMENT ON TABLE ticket_stage_history IS '티켓 상태 변경 이력';

COMMENT ON COLUMN users.role IS 'ADMIN, MANAGER, MEMBER, VIEWER';
COMMENT ON COLUMN users.status IS 'ACTIVE, INACTIVE, PENDING';
COMMENT ON COLUMN projects.status IS 'ACTIVE, ARCHIVED, DELETED';
COMMENT ON COLUMN projects.ticket_sequence IS '티켓 번호 자동 증가용';
COMMENT ON COLUMN workflows.status IS 'DRAFT, ACTIVE, ARCHIVED';
COMMENT ON COLUMN workflows.nodes_json IS '워크플로우 노드 정의 (JSON 배열)';
COMMENT ON COLUMN workflows.edges_json IS '노드 간 연결 정의 (JSON 배열)';
COMMENT ON COLUMN tickets.type IS 'EPIC, STORY, TASK, BUG, SUBTASK, SPIKE';
COMMENT ON COLUMN tickets.priority IS 'CRITICAL, HIGH, MEDIUM, LOW, TRIVIAL';
COMMENT ON COLUMN tickets.stage IS 'BACKLOG, TODO, IN_PROGRESS, CODE_REVIEW, TESTING, DONE, DEPLOYED';
