/**
 * 실습: 네이티브 WebSocket API
 *
 * 목표: 브라우저 WebSocket API를 직접 사용하여 연결, 메시지 송수신, 종료를 구현합니다.
 *
 * TODO 주석을 따라 코드를 완성하세요.
 */

const MOCK_URL = 'ws://localhost:8070';

/**
 * 실습 1: 기본 WebSocket 연결
 */
function createBasicConnection(): WebSocket {
  const socket = new WebSocket(MOCK_URL)

  socket.onopen = () => {
    console.log('연결 성공!');
    socket.send(JSON.stringify({ type: 'SUBSCRIBE' }))
  };

  socket.onmessage = (event) => {
    console.log('메세지 전송 성공!');
    console.log(JSON.parse(event.data))
  };

  socket.onerror = (error) => {
    console.error('에러 발생:', error);
  };

  socket.onclose = (event) => {
    console.log(event.code, event.reason, event.wasClean)
  };

  return socket;
}

/**
 * 실습 2: 메시지 전송
 *
 * 주의: readyState가 OPEN일 때만 send() 호출 가능!
 */
function sendMessage(socket: WebSocket, message: object): boolean {
  if (socket.readyState === 1) {
    socket.send(JSON.stringify(message));
    return true;
  }

  console.warn('연결이 열려있지 않습니다. readyState:', socket.readyState);
  return false;
}

/**
 * 실습 3: 안전한 연결 종료
 */
function closeConnection(socket: WebSocket, code = 1000, reason = 'Normal closure'): void {
  // 힌트: CONNECTING(0) 또는 OPEN(1) 상태일 때만 close() 호출
  if(socket.readyState == 0 ||socket.readyState == 1){
    socket.close(code, reason)
  }

}

/**
 * 실습 4: readyState 상태 해석
 */
function getReadyStateLabel(readyState: number): string {
  // 0: CONNECTING, 1: OPEN, 2: CLOSING, 3: CLOSED
  switch (readyState) {
    case 0:
      return 'CONNECTING';
    case 1:
      return 'OPEN';
    case 2:
      return 'CLOSING';
    case 3:
      return 'CLOSED';
    default:
      return 'UNKNOWN';
  }
}

// 테스트 실행
function main() {
  console.log('=== WebSocket 기초 실습 ===\n');

  const socket = createBasicConnection();

  // 3초 후 메시지 전송 테스트
  setTimeout(() => {
    console.log('\n현재 상태:', getReadyStateLabel(socket.readyState));
    sendMessage(socket, { type: 'PING' });
  }, 3000);

  // 10초 후 연결 종료
  setTimeout(() => {
    closeConnection(socket);
  }, 10000);
}

// 브라우저 환경에서 실행
if (typeof window !== 'undefined') {
  main();
}

export { createBasicConnection, sendMessage, closeConnection, getReadyStateLabel };
