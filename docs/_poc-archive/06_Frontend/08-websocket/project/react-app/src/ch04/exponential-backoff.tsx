/**
 * 실습: 지수 백오프 재연결
 *
 * 목표: 지수 백오프(Exponential Backoff) 알고리즘을 구현합니다.
 *
 * TODO 주석을 따라 코드를 완성하세요.
 */

import React, { useState, useEffect, useRef } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';

const WS_URL = 'ws://localhost:8070';

// 지수 백오프 설정
const BACKOFF_CONFIG = {
  baseDelay: 1000,   // 초기 대기 시간 (1초)
  maxDelay: 30000,   // 최대 대기 시간 (30초)
  maxAttempts: 10,   // 최대 재연결 시도 횟수
  jitterFactor: 0.3, // 지터 범위 (±30%)
};

/**
 * 실습 1: 지수 백오프 계산 함수
 *
 * 공식: min(baseDelay × 2^(attempts-1), maxDelay) + jitter
 *
 * @param attemptNumber 현재 시도 횟수 (1부터 시작)
 * @param config 백오프 설정
 * @returns 대기 시간 (ms)
 */
export function calculateBackoffDelay(
  attemptNumber: number,
  config = BACKOFF_CONFIG
): number {
  // TODO: 지수 백오프 계산 구현
  // 1. 기본 지수 계산: baseDelay * 2^(attemptNumber - 1)
  const exponentialDelay = BACKOFF_CONFIG.baseDelay * Math.pow(2, attemptNumber - 1)

  // 2. 최대값 제한: Math.min(계산값, maxDelay)
  const cappedDelay = Math.min(exponentialDelay, BACKOFF_CONFIG.maxDelay)

  // 3. 지터 추가: cappedDelay * jitterFactor * (Math.random() * 2 - 1)
  const jitter = cappedDelay * BACKOFF_CONFIG.jitterFactor * (Math.random() * 2 -1)

  // 4. Math.floor()로 정수 반환
  return Math.floor(cappedDelay + jitter)
}

/**
 * 실습 2: 지수 백오프 적용 컴포넌트
 */
export function ExponentialBackoff() {
  const [reconnectAttempt, setReconnectAttempt] = useState(0);
  const [nextRetryIn, setNextRetryIn] = useState<number | null>(null);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const { sendMessage, lastMessage, readyState } = useWebSocket(WS_URL, {
    shouldReconnect: (closeEvent) => {
      if (closeEvent.code === 1000) return false;
      return reconnectAttempt < BACKOFF_CONFIG.maxAttempts;
    },

    // TODO: reconnectInterval을 함수로 전달
    // - calculateBackoffDelay(attemptNumber) 호출
    // - 콘솔에 재연결 시도 정보 출력
    // - delay 값 반환
    reconnectInterval: calculateBackoffDelay,

    reconnectAttempts: BACKOFF_CONFIG.maxAttempts,

    onOpen: () => {
      console.log('연결됨');
      setReconnectAttempt(0);
      setNextRetryIn(null);
      if (timerRef.current) clearInterval(timerRef.current);
    },

    onClose: (event) => {
      if (event.code !== 1000) {
        const attempt = reconnectAttempt + 1;
        setReconnectAttempt(attempt);

        const delay = calculateBackoffDelay(attempt);
        setNextRetryIn(Math.floor(delay / 1000));

        // 카운트다운
        timerRef.current = setInterval(() => {
          setNextRetryIn((prev) => {
            if (prev === null || prev <= 1) {
              if (timerRef.current) clearInterval(timerRef.current);
              return null;
            }
            return prev - 1;
          });
        }, 1000);
      }
    },

    onReconnectStop: (numAttempts) => {
      console.log(`재연결 포기: ${numAttempts}번 시도 후`);
      setNextRetryIn(null);
    },
  });

  useEffect(() => {
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, []);

  const connectionStatus = {
    [ReadyState.CONNECTING]: '연결 중...',
    [ReadyState.OPEN]: '연결됨',
    [ReadyState.CLOSING]: '종료 중...',
    [ReadyState.CLOSED]: '연결 끊김',
    [ReadyState.UNINSTANTIATED]: '초기화 안됨',
  }[readyState];

  return (
    <div>
      <h2>지수 백오프 재연결</h2>

      <div style={{ marginBottom: '16px' }}>
        <p>상태: {connectionStatus}</p>
        {readyState === ReadyState.CLOSED && (
          <>
            <p>재연결 시도: {reconnectAttempt} / {BACKOFF_CONFIG.maxAttempts}</p>
            {nextRetryIn !== null && (
              <p>다음 시도: {nextRetryIn}초 후</p>
            )}
          </>
        )}
      </div>

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
 * 실습 3: 지수 백오프 시각화
 */
export function BackoffVisualization() {
  const [attempts, setAttempts] = useState<Array<{ attempt: number; delay: number }>>([]);

  const simulateBackoff = () => {
    const newAttempts: Array<{ attempt: number; delay: number }> = [];

    for (let i = 1; i <= BACKOFF_CONFIG.maxAttempts; i++) {
      const delay = calculateBackoffDelay(i);
      newAttempts.push({ attempt: i, delay });
    }

    setAttempts(newAttempts);
  };

  const maxDelay = BACKOFF_CONFIG.maxDelay;

  return (
    <div>
      <h2>지수 백오프 시각화</h2>
      <button onClick={simulateBackoff}>시뮬레이션 실행</button>

      <div style={{ marginTop: '20px' }}>
        {attempts.map(({ attempt, delay }) => (
          <div
            key={attempt}
            style={{
              display: 'flex',
              alignItems: 'center',
              marginBottom: '8px',
            }}
          >
            <span style={{ width: '60px' }}>#{attempt}</span>
            <div
              style={{
                width: `${(delay / maxDelay) * 300}px`,
                height: '24px',
                backgroundColor: '#4CAF50',
                marginRight: '8px',
                borderRadius: '4px',
              }}
            />
            <span>{(delay / 1000).toFixed(1)}초</span>
          </div>
        ))}
      </div>

      <div style={{ marginTop: '20px', fontSize: '12px', color: '#888' }}>
        <p>설정:</p>
        <ul>
          <li>기본 대기: {BACKOFF_CONFIG.baseDelay}ms</li>
          <li>최대 대기: {BACKOFF_CONFIG.maxDelay}ms</li>
          <li>지터: ±{BACKOFF_CONFIG.jitterFactor * 100}%</li>
        </ul>
      </div>
    </div>
  );
}
