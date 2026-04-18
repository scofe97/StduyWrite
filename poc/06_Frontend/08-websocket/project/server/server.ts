/**
 * Mock WebSocket Server
 *
 * mock-socket 라이브러리를 사용하여 WebSocket 서버를 시뮬레이션합니다.
 * 실제 서버 없이 WebSocket 통신을 테스트할 수 있습니다.
 *
 * 사용법:
 * - 브라우저 환경: import하여 자동으로 모킹
 * - Node.js 환경: ts-node mock-server/server.ts
 */

import { Server } from 'mock-socket';
import { routeMessage, generateDelta, setSendMessageCallback, ServerMessage } from './handlers';

const MOCK_URL = 'ws://localhost:8070';

// Mock WebSocket 서버 인스턴스
let mockServer: Server | null = null;

/**
 * Mock 서버 시작
 */
export function startMockServer(): Server {
  if (mockServer) {
    console.log('[Mock Server] Server already running');
    return mockServer;
  }

  mockServer = new Server(MOCK_URL);

  mockServer.on('connection', (socket) => {
    console.log('[Mock Server] Client connected');

    // 비동기 메시지 전송 콜백 설정 (Bulk Registration 등에서 사용)
    setSendMessageCallback((msg: ServerMessage) => {
      socket.send(JSON.stringify(msg));
    });

    // 클라이언트 메시지 수신
    socket.on('message', (data) => {
      try {
        const message = JSON.parse(data as string);
        console.log('[Mock Server] Received:', message);

        const response = routeMessage(message);
        if (response) {
          socket.send(JSON.stringify(response));
        }
      } catch (error) {
        console.error('[Mock Server] Parse error:', error);
      }
    });

    // 연결 해제
    socket.on('close', () => {
      console.log('[Mock Server] Client disconnected');
      setSendMessageCallback(() => {}); // 콜백 초기화
    });
  });

  console.log(`[Mock Server] Started at ${MOCK_URL}`);
  return mockServer;
}

/**
 * Mock 서버 중지
 */
export function stopMockServer(): void {
  if (mockServer) {
    mockServer.stop();
    mockServer = null;
    console.log('[Mock Server] Stopped');
  }
}

/**
 * 주기적으로 DELTA 메시지 전송 시작
 * 실시간 업데이트 시뮬레이션
 */
export function startDeltaSimulation(intervalMs = 3000): NodeJS.Timer {
  return setInterval(() => {
    if (mockServer) {
      const delta = generateDelta();
      mockServer.clients().forEach((client) => {
        client.send(JSON.stringify(delta));
      });
      console.log('[Mock Server] Sent DELTA:', delta);
    }
  }, intervalMs);
}

/**
 * 특정 클라이언트에게 메시지 전송
 */
export function broadcast(message: ServerMessage): void {
  if (mockServer) {
    mockServer.clients().forEach((client) => {
      client.send(JSON.stringify(message));
    });
  }
}

// Mock URL export (클라이언트에서 사용)
export { MOCK_URL };

// 직접 실행 시 서버 시작 (Node.js 환경에서만 동작)
if (typeof require !== 'undefined' && require.main === module) {
  startMockServer();
  startDeltaSimulation(5000); // 5초마다 DELTA 전송

  console.log('\nMock WebSocket Server is running...');
  console.log('Press Ctrl+C to stop\n');
}
