/**
 * WebSocket 메시지 핸들러
 *
 * 각 메시지 타입에 대한 처리 로직을 정의합니다.
 */

export interface Message {
  type: string;
  [key: string]: unknown;
}

export interface ServerMessage {
  type: 'SNAPSHOT' | 'DELTA' | 'ERROR' | 'ACK' | 'COMPLETE';
  data?: unknown;
  message?: string;
  jobId?: string;
  summary?: {
    total: number;
    success: number;
    failed: number;
  };
}

// ============================================================
// Bulk Registration 타입 및 상태
// ============================================================

type UserStatus = 'pending' | 'processing' | 'success' | 'failed';

interface BulkUser {
  userId: string;
  name: string;
  email: string;
  status: UserStatus;
  error?: string;
}

interface BulkJob {
  jobId: string;
  users: BulkUser[];
  processedIndex: number;
  isComplete: boolean;
}

// 진행 중인 Bulk Job 저장소
const bulkJobs = new Map<string, BulkJob>();

// 메시지 전송 콜백 (server.ts에서 설정)
let sendMessageCallback: ((msg: ServerMessage) => void) | null = null;

export function setSendMessageCallback(callback: (msg: ServerMessage) => void) {
  sendMessageCallback = callback;
}

/**
 * BULK_REGISTER 메시지 처리
 * 다중 유저 등록 시작
 */
export function handleBulkRegister(
  users: Array<{ name: string; email: string }>
): ServerMessage {
  const jobId = `job-${Date.now()}`;

  const bulkUsers: BulkUser[] = users.map((u, i) => ({
    userId: `user-${i + 1}`,
    ...u,
    status: 'pending' as UserStatus,
  }));

  const job: BulkJob = {
    jobId,
    users: bulkUsers,
    processedIndex: 0,
    isComplete: false,
  };

  bulkJobs.set(jobId, job);
  console.log(`[Mock Server] Bulk registration started: ${jobId}`);

  // 비동기로 유저 처리 시작
  setTimeout(() => processBulkUsers(jobId), 500);

  return {
    type: 'ACK',
    message: 'Bulk registration started',
    jobId,
  };
}

/**
 * 유저들을 순차적으로 처리하고 DELTA 전송
 */
function processBulkUsers(jobId: string) {
  const job = bulkJobs.get(jobId);
  if (!job || job.isComplete || !sendMessageCallback) return;

  const currentIndex = job.processedIndex;
  if (currentIndex >= job.users.length) {
    // 모든 처리 완료
    job.isComplete = true;
    const summary = {
      total: job.users.length,
      success: job.users.filter(u => u.status === 'success').length,
      failed: job.users.filter(u => u.status === 'failed').length,
    };

    sendMessageCallback({
      type: 'COMPLETE',
      jobId,
      summary,
    });
    console.log(`[Mock Server] Bulk registration complete: ${jobId}`, summary);
    return;
  }

  const user = job.users[currentIndex];

  // 1. processing 상태 전송
  sendMessageCallback({
    type: 'DELTA',
    data: { userId: user.userId, status: 'processing' },
  });

  // 2. 1~2초 후 결과 전송
  setTimeout(() => {
    const isSuccess = Math.random() > 0.3; // 70% 성공률
    const newStatus: UserStatus = isSuccess ? 'success' : 'failed';
    const error = isSuccess ? undefined : '서버 오류: 중복된 이메일';

    job.users[currentIndex] = { ...user, status: newStatus, error };

    sendMessageCallback!({
      type: 'DELTA',
      data: { userId: user.userId, status: newStatus, error },
    });

    job.processedIndex++;
    processBulkUsers(jobId); // 다음 유저 처리
  }, 1000 + Math.random() * 1000);
}

/**
 * RETRY 메시지 처리
 * 실패한 유저 재시도
 */
export function handleRetry(jobId: string, userId: string): ServerMessage | null {
  const job = bulkJobs.get(jobId);
  if (!job) {
    return { type: 'ERROR', message: `Job not found: ${jobId}` };
  }

  const userIndex = job.users.findIndex(u => u.userId === userId);
  if (userIndex === -1) {
    return { type: 'ERROR', message: `User not found: ${userId}` };
  }

  console.log(`[Mock Server] Retry user: ${userId}`);

  // 비동기로 재시도 처리
  setTimeout(() => {
    if (!sendMessageCallback) return;

    // processing 상태
    sendMessageCallback({
      type: 'DELTA',
      data: { userId, status: 'processing' },
    });

    // 1~2초 후 결과
    setTimeout(() => {
      const isSuccess = Math.random() > 0.2; // 80% 성공률 (재시도는 더 높음)
      const newStatus: UserStatus = isSuccess ? 'success' : 'failed';
      const error = isSuccess ? undefined : '재시도 실패: 네트워크 오류';

      job.users[userIndex] = { ...job.users[userIndex], status: newStatus, error };

      sendMessageCallback!({
        type: 'DELTA',
        data: { userId, status: newStatus, error },
      });
    }, 1000 + Math.random() * 1000);
  }, 300);

  return { type: 'ACK', message: `Retry started for ${userId}` };
}

// 초기 데이터 (SNAPSHOT 전송용)
const initialData = [
  { id: 1, name: 'Item 1', status: 'active' },
  { id: 2, name: 'Item 2', status: 'pending' },
  { id: 3, name: 'Item 3', status: 'completed' },
];

// 구독 상태 관리
const subscriptions = new Set<string>();

/**
 * SUBSCRIBE 메시지 처리
 */
export function handleSubscribe(topic: string): ServerMessage {
  subscriptions.add(topic);
  console.log(`[Mock Server] Subscribed to: ${topic}`);

  return {
    type: 'SNAPSHOT',
    data: initialData,
  };
}

/**
 * UNSUBSCRIBE 메시지 처리
 */
export function handleUnsubscribe(topic: string): ServerMessage {
  subscriptions.delete(topic);
  console.log(`[Mock Server] Unsubscribed from: ${topic}`);

  return {
    type: 'ACK',
    message: `Unsubscribed from ${topic}`,
  };
}

/**
 * 랜덤 DELTA 메시지 생성
 * 실제 서버의 실시간 업데이트를 시뮬레이션
 */
export function generateDelta(): ServerMessage {
  const randomId = Math.floor(Math.random() * 3) + 1;
  const statuses = ['active', 'pending', 'completed', 'error'];
  const randomStatus = statuses[Math.floor(Math.random() * statuses.length)];

  return {
    type: 'DELTA',
    data: {
      id: randomId,
      changes: {
        status: randomStatus,
        updatedAt: new Date().toISOString(),
      },
    },
  };
}

/**
 * 에러 시뮬레이션 (테스트용)
 */
export function generateError(): ServerMessage {
  return {
    type: 'ERROR',
    message: 'Simulated server error for testing',
  };
}

/**
 * 메시지 라우터
 * 클라이언트로부터 받은 메시지를 적절한 핸들러로 전달
 */
export function routeMessage(message: Message): ServerMessage | null {
  switch (message.type) {
    case 'SUBSCRIBE':
      return handleSubscribe(message.topic as string);

    case 'UNSUBSCRIBE':
      return handleUnsubscribe(message.topic as string);

    case 'PING':
      return { type: 'ACK', message: 'PONG' };

    case 'BULK_REGISTER':
      return handleBulkRegister(message.users as Array<{ name: string; email: string }>);

    case 'RETRY':
      return handleRetry(message.jobId as string, message.userId as string);

    default:
      console.log(`[Mock Server] Unknown message type: ${message.type}`);
      return null;
  }
}
