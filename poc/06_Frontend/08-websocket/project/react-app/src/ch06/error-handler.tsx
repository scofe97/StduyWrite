/**
 * 실습: WebSocket 에러 처리
 *
 * 목표: 다양한 에러 상황에 대한 처리 전략을 구현합니다.
 *
 * TODO 주석을 따라 코드를 완성하세요.
 */

import React, { useCallback, useEffect, useState } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';

const WS_URL = 'ws://localhost:8080';

// 에러 타입 정의
interface AppError {
  type: 'connection' | 'protocol' | 'application' | 'network';
  message: string;
  timestamp: Date;
  recoverable: boolean;
}

/**
 * 실습 1: 기본 에러 처리
 */
export function BasicErrorHandling() {
  const [errors, setErrors] = useState<AppError[]>([]);
  const [connectionAttempts, setConnectionAttempts] = useState(0);

  const addError = useCallback((error: AppError) => {
    setErrors((prev) => [...prev, error]);
    console.error(`[${error.type}] ${error.message}`);
  }, []);

  const { sendMessage, lastMessage, readyState } = useWebSocket(WS_URL, {
    // TODO: onError 콜백 구현
    onError: (event) => {
      addError({
        type: 'connection',
        message: 'WebSocket 연결 에러가 발생했습니다.',
        timestamp: new Date(),
        recoverable: true,
      });
    },

    // TODO: onClose 콜백 구현
    onClose: (event) => {
      // Close Code에 따른 에러 분류
      if (event.code !== 1000) {
        addError({
          type: event.code === 1006 ? 'network' : 'protocol',
          message: `연결 종료: ${event.code} - ${event.reason || '알 수 없는 이유'}`,
          timestamp: new Date(),
          recoverable: event.code === 1006,
        });
      }
    },

    // TODO: onOpen 콜백 - 연결 성공 시 에러 카운터 리셋
    onOpen: () => {
      setConnectionAttempts(0);
    },

    shouldReconnect: (closeEvent) => {
      setConnectionAttempts((prev) => prev + 1);
      return closeEvent.code !== 1000 && connectionAttempts < 5;
    },

    reconnectAttempts: 5,
    reconnectInterval: 3000,
  });

  // 애플리케이션 에러 처리 (서버에서 보내는 ERROR 메시지)
  useEffect(() => {
    if (lastMessage !== null) {
      try {
        const parsed = JSON.parse(lastMessage.data);

        if (parsed.type === 'ERROR') {
          addError({
            type: 'application',
            message: parsed.message,
            timestamp: new Date(),
            recoverable: parsed.recoverable ?? false,
          });
        }
      } catch (error) {
        addError({
          type: 'protocol',
          message: '잘못된 메시지 형식',
          timestamp: new Date(),
          recoverable: false,
        });
      }
    }
  }, [lastMessage, addError]);

  const clearErrors = () => setErrors([]);

  return (
    <div>
      <h2>기본 에러 처리</h2>

      <div style={{ marginBottom: '16px' }}>
        <p>연결 상태: {readyState === ReadyState.OPEN ? '연결됨' : '연결 안됨'}</p>
        <p>연결 시도 횟수: {connectionAttempts}</p>
      </div>

      {/* 에러 목록 */}
      <div>
        <h3>
          에러 로그 ({errors.length}개)
          <button onClick={clearErrors} style={{ marginLeft: '8px', fontSize: '12px' }}>
            지우기
          </button>
        </h3>

        {errors.length === 0 ? (
          <p style={{ color: '#666' }}>에러 없음</p>
        ) : (
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {errors.map((error, idx) => (
              <li
                key={idx}
                style={{
                  padding: '8px',
                  marginBottom: '4px',
                  backgroundColor: error.recoverable ? '#FFF3CD' : '#F8D7DA',
                  borderRadius: '4px',
                }}
              >
                <strong>[{error.type}]</strong> {error.message}
                <span style={{ fontSize: '12px', color: '#666', marginLeft: '8px' }}>
                  {error.timestamp.toLocaleTimeString()}
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

/**
 * 실습 2: 사용자 친화적 에러 메시지
 */
function getErrorMessage(error: AppError): { title: string; description: string; action?: string } {
  switch (error.type) {
    case 'connection':
      return {
        title: '연결 문제',
        description: '서버와의 연결에 실패했습니다.',
        action: error.recoverable ? '자동으로 재연결을 시도합니다.' : '페이지를 새로고침해 주세요.',
      };

    case 'network':
      return {
        title: '네트워크 오류',
        description: '인터넷 연결을 확인해 주세요.',
        action: '연결이 복구되면 자동으로 재연결됩니다.',
      };

    case 'protocol':
      return {
        title: '통신 오류',
        description: '서버와의 통신에 문제가 발생했습니다.',
        action: '문제가 지속되면 고객센터에 문의해 주세요.',
      };

    case 'application':
      return {
        title: '요청 실패',
        description: error.message,
        action: error.recoverable ? '다시 시도해 주세요.' : undefined,
      };

    default:
      return {
        title: '오류 발생',
        description: '알 수 없는 오류가 발생했습니다.',
      };
  }
}

export function UserFriendlyErrors() {
  const [currentError, setCurrentError] = useState<AppError | null>(null);
  const [showError, setShowError] = useState(false);

  const { readyState } = useWebSocket(WS_URL, {
    onError: () => {
      setCurrentError({
        type: 'connection',
        message: 'WebSocket 에러',
        timestamp: new Date(),
        recoverable: true,
      });
      setShowError(true);
    },

    onClose: (event) => {
      if (event.code !== 1000) {
        setCurrentError({
          type: event.code === 1006 ? 'network' : 'protocol',
          message: `Close code: ${event.code}`,
          timestamp: new Date(),
          recoverable: event.code === 1006,
        });
        setShowError(true);
      }
    },

    onOpen: () => {
      setShowError(false);
      setCurrentError(null);
    },

    shouldReconnect: () => true,
    reconnectAttempts: 5,
    reconnectInterval: 3000,
  });

  // 자동 숨김 (recoverable 에러)
  useEffect(() => {
    if (currentError?.recoverable && showError) {
      const timer = setTimeout(() => setShowError(false), 5000);
      return () => clearTimeout(timer);
    }
  }, [currentError, showError]);

  const errorInfo = currentError ? getErrorMessage(currentError) : null;

  return (
    <div>
      <h2>사용자 친화적 에러</h2>

      <p>연결 상태: {readyState === ReadyState.OPEN ? '연결됨' : '연결 안됨'}</p>

      {/* Toast 스타일 에러 표시 */}
      {showError && errorInfo && (
        <div
          style={{
            position: 'fixed',
            bottom: '20px',
            right: '20px',
            maxWidth: '320px',
            padding: '16px',
            backgroundColor: '#F8D7DA',
            borderLeft: '4px solid #F44336',
            borderRadius: '4px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <strong>{errorInfo.title}</strong>
            <button
              onClick={() => setShowError(false)}
              style={{ border: 'none', background: 'none', cursor: 'pointer' }}
            >
              ✕
            </button>
          </div>
          <p style={{ margin: '8px 0', fontSize: '14px' }}>{errorInfo.description}</p>
          {errorInfo.action && (
            <p style={{ margin: 0, fontSize: '12px', color: '#666' }}>{errorInfo.action}</p>
          )}
        </div>
      )}
    </div>
  );
}

/**
 * 실습 3: HTTP 폴링 Fallback
 */
export function PollingFallback() {
  const [mode, setMode] = useState<'websocket' | 'polling'>('websocket');
  const [wsFailCount, setWsFailCount] = useState(0);
  const [data, setData] = useState<unknown>(null);
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);

  const MAX_WS_RETRIES = 3;

  // WebSocket 연결
  const { lastMessage, readyState } = useWebSocket(
    mode === 'websocket' ? WS_URL : null,
    {
      shouldReconnect: () => {
        const newCount = wsFailCount + 1;
        setWsFailCount(newCount);

        // 최대 재시도 횟수 초과 시 Polling으로 전환
        if (newCount >= MAX_WS_RETRIES) {
          console.log('WebSocket 실패, Polling으로 전환');
          setMode('polling');
          return false;
        }

        return true;
      },

      reconnectAttempts: MAX_WS_RETRIES,
      reconnectInterval: 2000,

      onOpen: () => {
        setWsFailCount(0);
      },
    }
  );

  // WebSocket 메시지 처리
  useEffect(() => {
    if (lastMessage !== null) {
      try {
        setData(JSON.parse(lastMessage.data));
        setLastUpdate(new Date());
      } catch (error) {
        console.error('메시지 파싱 실패:', error);
      }
    }
  }, [lastMessage]);

  // Polling 모드
  useEffect(() => {
    if (mode !== 'polling') return;

    const pollData = async () => {
      try {
        // 실제로는 API 엔드포인트를 호출
        console.log('Polling...');
        // const response = await fetch('/api/updates');
        // setData(await response.json());
        setLastUpdate(new Date());
      } catch (error) {
        console.error('Polling 실패:', error);
      }
    };

    // 즉시 한 번 실행
    pollData();

    // 5초마다 폴링
    const interval = setInterval(pollData, 5000);

    return () => clearInterval(interval);
  }, [mode]);

  // WebSocket으로 복귀 시도
  const retryWebSocket = () => {
    setWsFailCount(0);
    setMode('websocket');
  };

  return (
    <div>
      <h2>HTTP 폴링 Fallback</h2>

      <div
        style={{
          padding: '16px',
          marginBottom: '16px',
          backgroundColor: mode === 'websocket' ? '#D4EDDA' : '#FFF3CD',
          borderRadius: '4px',
        }}
      >
        <p>
          현재 모드: <strong>{mode === 'websocket' ? 'WebSocket' : 'HTTP Polling'}</strong>
        </p>

        {mode === 'websocket' && (
          <p>연결 상태: {readyState === ReadyState.OPEN ? '연결됨' : '연결 중...'}</p>
        )}

        {mode === 'polling' && (
          <>
            <p style={{ fontSize: '14px', color: '#666' }}>
              WebSocket 연결에 실패하여 HTTP Polling 모드로 전환되었습니다.
            </p>
            <button onClick={retryWebSocket}>WebSocket 재시도</button>
          </>
        )}
      </div>

      <div>
        <h3>데이터</h3>
        <pre>{JSON.stringify(data, null, 2) || '데이터 없음'}</pre>
        {lastUpdate && (
          <p style={{ fontSize: '12px', color: '#666' }}>
            마지막 업데이트: {lastUpdate.toLocaleTimeString()}
          </p>
        )}
      </div>
    </div>
  );
}
