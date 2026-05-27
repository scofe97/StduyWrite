/**
 * 실습: 기본 재연결 로직
 *
 * 목표: react-use-websocket의 재연결 옵션을 이해하고 구현합니다.
 *
 * TODO 주석을 따라 코드를 완성하세요.
 */

import React, { useState } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';

const WS_URL = 'ws://localhost:8070';

// 재연결하면 안 되는 Close Code 목록
const NON_RETRYABLE_CODES = [
  1000, // Normal closure
  4001, // Authentication failed (커스텀)
  4002, // Forbidden (커스텀)
];

/**
 * 실습 1: 기본 재연결 설정
 *
 * 요구사항:
 * - shouldReconnect: NON_RETRYABLE_CODES에 포함된 코드면 재연결 안 함
 * - reconnectAttempts: 최대 5번
 * - reconnectInterval: 3초
 * - onOpen: 연결 성공 시 reconnectAttempt를 0으로 리셋
 * - onClose: reconnectAttempt 증가
 */
export function BasicReconnect() {
  const [reconnectAttempt, setReconnectAttempt] = useState(0);

  const { sendMessage, lastMessage, readyState } = useWebSocket(WS_URL, {
    // TODO: shouldReconnect 구현
    // - closeEvent.code가 NON_RETRYABLE_CODES에 포함되면 false
    // - 그 외에는 true
    shouldReconnect: (event) => {
      return !NON_RETRYABLE_CODES.includes(event.code);
    },

    // TODO: reconnectAttempts 설정 (5번)
    reconnectAttempts: 5,

    // TODO: reconnectInterval 설정 (3000ms)
    reconnectInterval: 3000,

    // TODO: onOpen - reconnectAttempt를 0으로 리셋
    onOpen: (event) => {
      setReconnectAttempt(0)
    },

    // TODO: onClose - reconnectAttempt 1 증가
    onClose: (event) => {
      setReconnectAttempt(prevState => prevState + 1)
    },

    onReconnectStop: (numAttempts) => {
      console.log(`재연결 중단: ${numAttempts}번 시도 후 포기`);
    },
  });

  const connectionStatus = {
    [ReadyState.CONNECTING]: '연결 중...',
    [ReadyState.OPEN]: '연결됨',
    [ReadyState.CLOSING]: '종료 중...',
    [ReadyState.CLOSED]: '연결 끊김',
    [ReadyState.UNINSTANTIATED]: '초기화 안됨',
  }[readyState];

  return (
    <div>
      <h2>기본 재연결</h2>
      <p>상태: {connectionStatus}</p>
      {readyState === ReadyState.CLOSED && (
        <p>재연결 시도: {reconnectAttempt}회</p>
      )}

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
 * 실습 2: Close Code 기반 재연결 결정
 *
 * 요구사항:
 * - 1000 (정상 종료): 재연결 안 함
 * - 1006 (비정상 종료): 재연결
 * - 1011 (서버 에러): 재연결
 * - 4001 (인증 실패): 재연결 안 함
 * - 기타: 재연결
 */
export function CloseCodeBasedReconnect() {
  const [lastCloseCode, setLastCloseCode] = useState<number | null>(null);

  const { readyState } = useWebSocket(WS_URL, {
    shouldReconnect: (closeEvent) => {
      setLastCloseCode(closeEvent.code);

      switch (lastCloseCode) {
        case 1000: return false
        case 1006: return true
        case 1011: return true
        case 4001: return false
        default: return false
      }
    },

    reconnectAttempts: 3,
    reconnectInterval: 2000,
  });

  return (
    <div>
      <h2>Close Code 기반 재연결</h2>
      <p>readyState: {readyState}</p>
      {lastCloseCode !== null && (
        <div>
          <p>마지막 Close Code: {lastCloseCode}</p>
          <p>의미: {getCloseCodeMeaning(lastCloseCode)}</p>
        </div>
      )}
    </div>
  );
}

// Close Code 의미 해석
function getCloseCodeMeaning(code: number): string {
  const meanings: Record<number, string> = {
    1000: '정상 종료',
    1001: '엔드포인트 종료 (브라우저 탭 닫기 등)',
    1002: '프로토콜 에러',
    1003: '지원하지 않는 데이터 타입',
    1006: '비정상 종료 (연결 끊김)',
    1007: '잘못된 데이터',
    1008: '정책 위반',
    1009: '메시지가 너무 큼',
    1010: '확장 협상 실패',
    1011: '서버 내부 에러',
    4001: '인증 실패 (커스텀)',
    4002: '접근 금지 (커스텀)',
  };

  return meanings[code] || '알 수 없는 코드';
}

/**
 * 실습 3: 수동 재연결 제공
 *
 * 요구사항:
 * - 자동 재연결 3번 실패 후 autoReconnect를 false로
 * - 수동 재연결 버튼 클릭 시 autoReconnect를 true로
 */
export function ManualReconnect() {
  const [autoReconnect, setAutoReconnect] = useState(true);

  const { readyState } = useWebSocket(WS_URL, {
    // TODO: shouldReconnect - autoReconnect 값 반환
    shouldReconnect: () => autoReconnect,
    reconnectAttempts: 3,
    reconnectInterval: 5000,

    // TODO: onReconnectStop - autoReconnect를 false로
    onReconnectStop: () => setAutoReconnect(false)

  });

  // TODO: handleManualReconnect - autoReconnect를 true로
  const handleManualReconnect = () => {
    setAutoReconnect(true)
  };

  return (
    <div>
      <h2>수동 재연결</h2>
      <p>readyState: {readyState}</p>
      <p>자동 재연결: {autoReconnect ? '활성화' : '비활성화'}</p>

      {readyState === ReadyState.CLOSED && !autoReconnect && (
        <div>
          <p>자동 재연결이 중단되었습니다.</p>
          <button onClick={handleManualReconnect}>
            수동으로 재연결
          </button>
        </div>
      )}
    </div>
  );
}
