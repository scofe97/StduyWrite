/**
 * 실습: 조건부 WebSocket 연결
 *
 * 목표: 특정 조건에서만 WebSocket 연결을 활성화하는 패턴을 익힙니다.
 *
 * TODO 주석을 따라 코드를 완성하세요.
 */

import { useState } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';

const WS_URL = 'ws://localhost:8070';

/**
 * 실습 1: null URL 패턴
 *
 * URL에 null을 전달하면 WebSocket 연결이 시작되지 않습니다.
 */
export function NullUrlPattern() {
  const [isEnabled, setIsEnabled] = useState(false);
  
  // 힌트: 삼항 연산자 사용
  const socketUrl = isEnabled ? WS_URL : null;

  const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl);

  const connectionStatus = {
    [ReadyState.CONNECTING]: '연결 중...',
    [ReadyState.OPEN]: '연결됨',
    [ReadyState.CLOSING]: '연결 종료 중...',
    [ReadyState.CLOSED]: '연결 종료',
    [ReadyState.UNINSTANTIATED]: '비활성화',
  }[readyState];

  return (
    <div>
      <h2>Null URL 패턴</h2>
      <p>상태: {connectionStatus}</p>

      <button onClick={() => setIsEnabled(!isEnabled)}>
        {isEnabled ? '연결 해제' : '연결 시작'}
      </button>

      {readyState === ReadyState.OPEN && (
        <button onClick={() => sendMessage(JSON.stringify({ type: 'PING' }))}>
          PING 전송
        </button>
      )}

      {lastMessage && <pre>마지막 메시지: {lastMessage.data}</pre>}
    </div>
  );
}

/**
 * 실습 2: 조건부 연결 패턴 (null URL 방식)
 *
 * react-use-websocket 4.x에서는 shouldConnect 옵션이 없습니다.
 * 대신 null URL 패턴을 사용하여 연결 여부를 제어합니다.
 */
export function ShouldConnectPattern() {
  const [isConnected, setIsConnected] = useState(false);

  // null URL 패턴: isConnected가 false면 null을 전달하여 연결 안 함
  const { sendMessage, lastMessage, readyState } = useWebSocket(
    isConnected ? WS_URL : null
  );

  const connectionStatus = {
    [ReadyState.CONNECTING]: '연결 중...',
    [ReadyState.OPEN]: '연결됨',
    [ReadyState.CLOSING]: '연결 종료 중...',
    [ReadyState.CLOSED]: '연결 종료',
    [ReadyState.UNINSTANTIATED]: '비활성화',
  }[readyState];

  return (
    <div>
      <h2>조건부 연결 패턴</h2>
      <p>상태: {connectionStatus}</p>

      <button onClick={() => setIsConnected(!isConnected)}>
        {isConnected ? '연결 해제' : '연결 시작'}
      </button>

      {readyState === ReadyState.OPEN && (
        <button onClick={() => sendMessage(JSON.stringify({ type: 'PING' }))}>
          PING 전송
        </button>
      )}

      {lastMessage && <pre>마지막 메시지: {lastMessage.data}</pre>}
    </div>
  );
}

/**
 * 실습 3: 실제 사용 사례 - 로그인 상태에 따른 연결
 */
interface User {
  id: string;
  name: string;
}

export function LoginBasedConnection() {
  const [user, setUser] = useState<User | null>(null);

  // TODO: 로그인된 사용자가 있을 때만 연결
  // 힌트: user가 null이 아닐 때만 연결
  const { sendMessage, lastMessage, readyState } = useWebSocket(
    user ? WS_URL : null,
    {
      // TODO: 연결 시 사용자 정보와 함께 구독 요청
      onOpen: () => {
        if (user) {
          sendMessage(JSON.stringify({
            type: 'SUBSCRIBE',
            topic: `user:${user.id}`,
          }));
        }
      },
    }
  );

  const handleLogin = () => {
    setUser({ id: '123', name: '홍길동' });
  };

  const handleLogout = () => {
    setUser(null);
  };

  return (
    <div>
      <h2>로그인 기반 연결</h2>

      {user ? (
        <div>
          <p>로그인됨: {user.name}</p>
          <p>WebSocket 상태: {readyState === ReadyState.OPEN ? '연결됨' : '연결 중...'}</p>
          <button onClick={handleLogout}>로그아웃</button>
        </div>
      ) : (
        <div>
          <p>로그인이 필요합니다</p>
          <button onClick={handleLogin}>로그인</button>
        </div>
      )}

      {lastMessage && <pre>알림: {lastMessage.data}</pre>}
    </div>
  );
}

/**
 * 실습 4: 동적 URL 패턴
 *
 * URL이 동적으로 변경되는 경우의 연결 제어
 *
 * 예시: 다른 채팅방으로 이동 시 WebSocket URL 변경
 */
export function DynamicUrlPattern() {
  const [roomId, setRoomId] = useState<string | null>(null);

  // roomId가 있을 때만 연결, roomId에 따라 URL 변경
  const socketUrl = roomId ? `${WS_URL}?room=${roomId}` : null;

  const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl, {
    onOpen: () => {
      console.log(`Room ${roomId}에 연결됨`);
    },
  });

  const connectionStatus = {
    [ReadyState.CONNECTING]: '연결 중...',
    [ReadyState.OPEN]: '연결됨',
    [ReadyState.CLOSING]: '연결 종료 중...',
    [ReadyState.CLOSED]: '연결 종료',
    [ReadyState.UNINSTANTIATED]: '방 미선택',
  }[readyState];

  return (
    <div>
      <h2>동적 URL 패턴</h2>
      <p>상태: {connectionStatus}</p>
      <p>현재 방: {roomId || '없음'}</p>

      <div>
        <button onClick={() => setRoomId('room-1')}>Room 1 입장</button>
        <button onClick={() => setRoomId('room-2')}>Room 2 입장</button>
        <button onClick={() => setRoomId(null)}>방 나가기</button>
      </div>

      {readyState === ReadyState.OPEN && (
        <button onClick={() => sendMessage(JSON.stringify({ type: 'CHAT', message: '안녕!' }))}>
          메시지 전송
        </button>
      )}

      {lastMessage && <pre>마지막 메시지: {lastMessage.data}</pre>}
    </div>
  );
}
