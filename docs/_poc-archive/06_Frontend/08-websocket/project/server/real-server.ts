/**
 * 실제 WebSocket 서버 (ws 라이브러리 사용)
 * 포트: 8070
 */
import { WebSocketServer, WebSocket } from 'ws';

const PORT = 8070;
const wss = new WebSocketServer({ port: PORT });

// 초기 데이터
const mockData = [
  { id: '1', name: 'Item 1', value: 100 },
  { id: '2', name: 'Item 2', value: 200 },
  { id: '3', name: 'Item 3', value: 300 },
];

wss.on('connection', (ws: WebSocket) => {
  console.log('[Server] Client connected');

  ws.on('message', (data: Buffer) => {
    try {
      const message = JSON.parse(data.toString());
      console.log('[Server] Received:', message);

      // 메시지 타입별 처리
      switch (message.type) {
        case 'SUBSCRIBE':
          // SNAPSHOT 응답
          ws.send(JSON.stringify({
            type: 'SNAPSHOT',
            data: mockData,
            timestamp: Date.now(),
          }));
          break;

        case 'PING':
          ws.send(JSON.stringify({
            type: 'PONG',
            timestamp: Date.now(),
          }));
          break;

        default:
          // 에코
          ws.send(JSON.stringify({
            type: 'ECHO',
            original: message,
            timestamp: Date.now(),
          }));
      }
    } catch (error) {
      console.error('[Server] Parse error:', error);
    }
  });

  ws.on('close', () => {
    console.log('[Server] Client disconnected');
  });

  ws.on('error', (error) => {
    console.error('[Server] Error:', error);
  });
});

console.log(`\n✅ WebSocket Server running at ws://localhost:${PORT}`);
console.log('Press Ctrl+C to stop\n');
