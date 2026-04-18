/**
 * 실습 4: 다중 유저 등록 + 재시도 (REST + WebSocket 혼합 패턴)
 *
 * 시나리오:
 * 1. WebSocket으로 BULK_REGISTER 메시지 전송 → ACK (jobId) 수신
 * 2. 각 유저별 상태(진행중/성공/실패) DELTA 수신
 * 3. 실패한 유저는 재시도 버튼으로 RETRY 메시지 전송
 * 4. 재시도 버튼 클릭 시 비활성화 → DELTA 수신 후 다시 활성화
 *
 * 학습 포인트:
 * - useWebSocket 훅 사용
 * - mock-socket 기반 Mock 서버 연동
 * - DELTA 메시지로 개별 유저 상태 업데이트
 * - 재시도 버튼 상태 관리 (isRetrying)
 */

import { useCallback, useEffect, useState } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';
import { startMockServer, stopMockServer, MOCK_URL } from '../../mock-server/server';

// ============================================================
// 타입 정의
// ============================================================

type UserStatus = 'pending' | 'processing' | 'success' | 'failed';

interface UserRegistration {
  userId: string;
  name: string;
  email: string;
  status: UserStatus;
  error?: string;
  isRetrying: boolean;
}

// WebSocket 메시지 타입
interface AckMessage {
  type: 'ACK';
  message: string;
  jobId?: string;
}

interface DeltaMessage {
  type: 'DELTA';
  data: {
    userId: string;
    status: UserStatus;
    error?: string;
  };
}

interface CompleteMessage {
  type: 'COMPLETE';
  jobId: string;
  summary: {
    total: number;
    success: number;
    failed: number;
  };
}

interface ErrorMessage {
  type: 'ERROR';
  message: string;
}

type ServerMessage = AckMessage | DeltaMessage | CompleteMessage | ErrorMessage;

// ============================================================
// 커스텀 훅: useBulkUserRegistration
// ============================================================

function useBulkUserRegistration() {
  const [users, setUsers] = useState<UserRegistration[]>([]);
  const [jobId, setJobId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);
  const [summary, setSummary] = useState<{
    total: number;
    success: number;
    failed: number;
  } | null>(null);

  // Mock 서버 시작
  useEffect(() => {
    startMockServer();
    return () => {
      stopMockServer();
    };
  }, []);

  // useWebSocket 훅 사용
  const { sendMessage, lastMessage, readyState } = useWebSocket(MOCK_URL, {
    shouldReconnect: () => true,
    reconnectAttempts: 5,
    reconnectInterval: 3000,
  });

  // 메시지 핸들러
  const handleMessage = useCallback((message: ServerMessage) => {
    console.log('[WebSocket] 메시지 수신:', message);

    switch (message.type) {
      case 'ACK':
        // 등록 시작 ACK → jobId 저장
        if (message.jobId) {
          setJobId(message.jobId);
          console.log('[WebSocket] Job 시작:', message.jobId);
        }
        break;

      case 'DELTA':
        const data = message.data;
        setUsers(prevState =>
          prevState.map(prev => {
            if (prev.userId === data.userId) {
              return { ...prev, ...data, isRetrying: false };
            }
            return prev;
          })
        );
        break;

      case 'COMPLETE':
        setIsCompleted(true);
        setIsLoading(false);
        setSummary(message.summary);
        console.log('[WebSocket] 작업 완료:', message.summary);
        break;

      case 'ERROR':
        console.error('[WebSocket] 에러:', message.message);
        break;
    }
  }, []);

  // lastMessage 변경 시 처리
  useEffect(() => {
    if (lastMessage !== null) {
      try {
        const parsed: ServerMessage = JSON.parse(lastMessage.data);
        handleMessage(parsed);
      } catch (error) {
        console.error('메시지 파싱 실패:', error);
      }
    }
  }, [lastMessage, handleMessage]);

  // 등록 시작 함수
  const startRegistration = (userList: Array<{ name: string; email: string }>) => {
    if (readyState !== ReadyState.OPEN) {
      console.error('WebSocket이 연결되지 않았습니다.');
      return;
    }

    setIsLoading(true);
    setIsCompleted(false);
    setSummary(null);

    // 1. 초기 상태 설정
    const initialUsers: UserRegistration[] = userList.map((u, i) => ({
      userId: `user-${i + 1}`,
      ...u,
      status: 'pending' as UserStatus,
      isRetrying: false,
    }));
    setUsers(initialUsers);

    // 2. WebSocket으로 BULK_REGISTER 메시지 전송
    console.log('[WebSocket] BULK_REGISTER 전송');
    sendMessage(
      JSON.stringify({
        type: 'BULK_REGISTER',
        users: userList,
      })
    );
  };

  // 재시도 함수
  const retryUser = (userId: string) => {
    if (!jobId || readyState !== ReadyState.OPEN) return;

    // 1. 버튼 비활성화
    setUsers(prev =>
      prev.map(u =>
        u.userId === userId
          ? { ...u, isRetrying: true, status: 'pending' as UserStatus }
          : u
      )
    );

    // 2. WebSocket으로 RETRY 메시지 전송
    console.log('[WebSocket] RETRY 전송:', userId);
    sendMessage(
      JSON.stringify({
        type: 'RETRY',
        jobId,
        userId,
      })
    );
  };

  // 재시도 버튼 비활성화 조건
  const isRetryDisabled = (user: UserRegistration): boolean => {
    return (
      user.status === 'pending' ||
      user.status === 'processing' ||
      user.isRetrying ||
      readyState !== ReadyState.OPEN
    );
  };

  // 리셋
  const reset = () => {
    setUsers([]);
    setJobId(null);
    setIsLoading(false);
    setIsCompleted(false);
    setSummary(null);
  };

  return {
    users,
    jobId,
    isLoading,
    isCompleted,
    summary,
    readyState,
    startRegistration,
    retryUser,
    isRetryDisabled,
    reset,
  };
}

// ============================================================
// UI 컴포넌트
// ============================================================

const statusConfig: Record<
  UserStatus,
  { label: string; color: string; bgColor: string }
> = {
  pending: { label: '대기중', color: '#666', bgColor: '#f0f0f0' },
  processing: { label: '처리중', color: '#1976d2', bgColor: '#e3f2fd' },
  success: { label: '성공', color: '#2e7d32', bgColor: '#e8f5e9' },
  failed: { label: '실패', color: '#d32f2f', bgColor: '#ffebee' },
};

// 샘플 유저 데이터
const sampleUsers = [
  { name: '김철수', email: 'kim@example.com' },
  { name: '이영희', email: 'lee@example.com' },
  { name: '박민수', email: 'park@example.com' },
  { name: '최지은', email: 'choi@example.com' },
  { name: '정하나', email: 'jung@example.com' },
];

export function BulkUserRegistrationDemo() {
  const {
    users,
    jobId,
    isLoading,
    isCompleted,
    summary,
    readyState,
    startRegistration,
    retryUser,
    isRetryDisabled,
    reset,
  } = useBulkUserRegistration();

  const isConnected = readyState === ReadyState.OPEN;

  const handleStart = () => {
    startRegistration(sampleUsers);
  };

  return (
    <div style={{ padding: '24px', maxWidth: '600px', margin: '0 auto' }}>
      <h2>실습 4: 다중 유저 등록 (useWebSocket + Mock Server)</h2>

      <p style={{ fontSize: '14px', color: '#666', marginBottom: '24px' }}>
        mock-socket 기반 Mock 서버와 useWebSocket 훅을 사용한 실시간 진행 상황 수신
      </p>

      {/* 상태 표시 */}
      <div
        style={{
          padding: '12px',
          backgroundColor: '#f5f5f5',
          borderRadius: '8px',
          marginBottom: '16px',
        }}
      >
        <div>
          <strong>WebSocket:</strong>{' '}
          <span style={{ color: isConnected ? '#2e7d32' : '#d32f2f' }}>
            {isConnected ? '연결됨' : '연결 안됨'}
          </span>
        </div>
        <div>
          <strong>Job ID:</strong> {jobId || '-'}
        </div>
        <div>
          <strong>상태:</strong>{' '}
          {isLoading ? '처리 중...' : isCompleted ? '완료' : '대기'}
        </div>
        {summary && (
          <div style={{ marginTop: '8px' }}>
            <strong>결과:</strong> 총 {summary.total}명 중{' '}
            <span style={{ color: '#2e7d32' }}>{summary.success}명 성공</span>,{' '}
            <span style={{ color: '#d32f2f' }}>{summary.failed}명 실패</span>
          </div>
        )}
      </div>

      {/* 버튼 */}
      <div style={{ marginBottom: '24px' }}>
        <button
          onClick={handleStart}
          disabled={isLoading || !isConnected}
          style={{
            padding: '12px 24px',
            fontSize: '16px',
            backgroundColor: isLoading || !isConnected ? '#ccc' : '#1976d2',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: isLoading || !isConnected ? 'not-allowed' : 'pointer',
            marginRight: '8px',
          }}
        >
          {isLoading ? '등록 중...' : '등록 시작'}
        </button>

        <button
          onClick={reset}
          style={{
            padding: '12px 24px',
            fontSize: '16px',
            backgroundColor: '#f5f5f5',
            color: '#333',
            border: '1px solid #ccc',
            borderRadius: '8px',
            cursor: 'pointer',
          }}
        >
          초기화
        </button>
      </div>

      {/* 유저 목록 */}
      {users.length > 0 && (
        <div>
          <h3>등록 현황</h3>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {users.map(user => {
              const config = statusConfig[user.status];
              return (
                <li
                  key={user.userId}
                  style={{
                    padding: '16px',
                    marginBottom: '8px',
                    backgroundColor: config.bgColor,
                    borderRadius: '8px',
                    borderLeft: `4px solid ${config.color}`,
                  }}
                >
                  <div
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                    }}
                  >
                    <div>
                      <div style={{ fontWeight: 'bold' }}>{user.name}</div>
                      <div style={{ fontSize: '14px', color: '#666' }}>
                        {user.email}
                      </div>
                      {user.error && (
                        <div
                          style={{
                            fontSize: '12px',
                            color: '#d32f2f',
                            marginTop: '4px',
                          }}
                        >
                          {user.error}
                        </div>
                      )}
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                      {/* 상태 배지 */}
                      <span
                        style={{
                          padding: '4px 12px',
                          borderRadius: '16px',
                          backgroundColor: config.color,
                          color: 'white',
                          fontSize: '12px',
                          fontWeight: 'bold',
                        }}
                      >
                        {user.isRetrying ? '재시도 중...' : config.label}
                        {user.status === 'processing' && ' ⏳'}
                      </span>

                      {/* 재시도 버튼 (실패한 경우에만 표시) */}
                      {user.status === 'failed' && (
                        <button
                          onClick={() => retryUser(user.userId)}
                          disabled={isRetryDisabled(user)}
                          style={{
                            padding: '6px 12px',
                            fontSize: '12px',
                            backgroundColor: isRetryDisabled(user)
                              ? '#ccc'
                              : '#ff9800',
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: isRetryDisabled(user)
                              ? 'not-allowed'
                              : 'pointer',
                          }}
                        >
                          {user.isRetrying ? '재시도 중...' : '재시도'}
                        </button>
                      )}
                    </div>
                  </div>
                </li>
              );
            })}
          </ul>
        </div>
      )}
    </div>
  );
}

// 기본 export
export default BulkUserRegistrationDemo;
