import { useEffect, useState, useCallback, useRef } from 'react';
import { EventSourcePolyfill, EventSourcePolyfillInit } from 'event-source-polyfill';

/**
 * Ch05 실습: SSE 에러 처리
 *
 * 학습 목표:
 * - 연결 상태 머신 (connecting → connected → error → disconnected)
 * - 재시도 카운터 + 지수 백오프
 * - readyState 기반 에러 판단
 * - heartbeat 타임아웃 감지
 * - SSE → polling fallback 전환
 * - 에러 UI 상태 관리
 */

export type SSEConnectionState =
  | 'connecting'
  | 'connected'
  | 'error'
  | 'disconnected'
  | 'fallback-polling';

export interface ErrorInfo {
  type: 'network' | 'timeout' | 'server' | 'unknown';
  message: string;
  retryCount: number;
  canRetry: boolean;
}

export interface SSEMessage {
  id: number;
  data: string;
  timestamp: string;
}

export interface UseSSEWithErrorHandlingOptions {
  heartbeatTimeout?: number;
  maxRetries?: number;
  baseRetryInterval?: number;
  pollingInterval?: number;
  pollingUrl?: string;
}

export interface UseSSEWithErrorHandlingReturn {
  messages: SSEMessage[];
  connectionState: SSEConnectionState;
  errorInfo: ErrorInfo | null;
  connect: () => void;
  disconnect: () => void;
  clearMessages: () => void;
}

export function useSSEWithErrorHandling(
  url: string,
  options: UseSSEWithErrorHandlingOptions = {}
): UseSSEWithErrorHandlingReturn {
  const {
    heartbeatTimeout = 30000,
    maxRetries = 3,
    baseRetryInterval = 1000,
    pollingInterval = 5000,
    pollingUrl,
  } = options;

  const [messages, setMessages] = useState<SSEMessage[]>([]);
  const [connectionState, setConnectionState] = useState<SSEConnectionState>('disconnected');
  const [errorInfo, setErrorInfo] = useState<ErrorInfo | null>(null);

  const eventSourceRef = useRef<EventSourcePolyfill | null>(null);
  const retryCountRef = useRef(0);
  const retryTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const heartbeatTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const pollingTimerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const resetHeartbeatTimer = useCallback(() => {
    // 기존 타이머 정리
    if (heartbeatTimerRef.current) {
      clearTimeout(heartbeatTimerRef.current);
    }

    // 새 타이머: heartbeatTimeout 동안 응답 없으면 죽은 연결로 판단
    heartbeatTimerRef.current = setTimeout(() => {
      setConnectionState('error');
      setErrorInfo({
        type: 'timeout',
        message: `${heartbeatTimeout / 1000}초간 서버 응답 없음 (heartbeat timeout)`,
        retryCount: retryCountRef.current,
        canRetry: true,
      });
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
        eventSourceRef.current = null;
      }
      scheduleRetry();
    }, heartbeatTimeout);
  }, [heartbeatTimeout]);

  const startPollingFallback = useCallback(() => {
    setConnectionState('fallback-polling');
    setErrorInfo({
      type: 'network',
      message: `SSE 실패 → polling 모드 (${pollingInterval / 1000}초 간격)`,
      retryCount: retryCountRef.current,
      canRetry: false,
    });

    // pollingUrl이 없으면 SSE URL에서 추론 (/events/xxx → /api/xxx)
    const targetUrl = pollingUrl || url.replace('/events/', '/api/');

    const poll = async () => {
      try {
        const res = await fetch(targetUrl);
        if (!res.ok) return;
        const data = (await res.json()) as SSEMessage | SSEMessage[];
        const items = Array.isArray(data) ? data : [data];
        setMessages(prev => [...prev, ...items]);
      } catch {
        // polling 실패는 무시, 다음 주기에 재시도
      }
    };

    poll(); // 즉시 첫 요청
    pollingTimerRef.current = setInterval(poll, pollingInterval);
  }, [url, pollingUrl, pollingInterval]);

  const scheduleRetry = useCallback(() => {
    if (retryCountRef.current >= maxRetries) {
      startPollingFallback();
      return;
    }

    const delay = baseRetryInterval * Math.pow(2, retryCountRef.current);
    setConnectionState('error');
    setErrorInfo({
      type: 'network',
      message: `재연결 대기 중... (${delay}ms 후 ${retryCountRef.current + 1}/${maxRetries})`,
      retryCount: retryCountRef.current,
      canRetry: true,
    });

    retryTimerRef.current = setTimeout(() => {
      retryTimerRef.current = null;
      connect();
    }, delay);

    retryCountRef.current++;
  }, [maxRetries, baseRetryInterval, startPollingFallback]);

  const connect = useCallback(() => {
    if (eventSourceRef.current) return;

    setConnectionState('connecting');
    setErrorInfo(null);

    const config: EventSourcePolyfillInit = {
      heartbeatTimeout,
    };

    const es = new EventSourcePolyfill(url, config);
    eventSourceRef.current = es;

    es.onopen = () => {
      setConnectionState('connected');
      setErrorInfo(null);
      retryCountRef.current = 0;
      resetHeartbeatTimer();
    };

    es.addEventListener('update', (event: any) => {
      try {
        const parsed = JSON.parse(event.data) as SSEMessage;
        setMessages(prev => [...prev, parsed]);
        // heartbeat 타이머 리셋 (데이터 수신 = 연결 살아있음)
        resetHeartbeatTimer();
      } catch {
        console.error('Failed to parse event data');
      }
    });

    es.addEventListener('heartbeat', () => {
      resetHeartbeatTimer();
    });

    es.onerror = () => {
      if (heartbeatTimerRef.current) clearTimeout(heartbeatTimerRef.current);

      if (es.readyState === 2) {
        // CLOSED — 서버가 연결을 끊음. 수동 재연결 필요 → scheduleRetry가 판단
        eventSourceRef.current = null;
        scheduleRetry();
      } else if (es.readyState === 0) {
        // CONNECTING — 브라우저가 자동 재연결 중. 대기하면서 UI만 업데이트
        setConnectionState('error');
        setErrorInfo({
          type: 'network',
          message: '재연결 시도 중 (브라우저 자동)',
          retryCount: retryCountRef.current,
          canRetry: true,
        });
      }
    };
  }, [url, heartbeatTimeout, resetHeartbeatTimer, scheduleRetry]);

  const disconnect = useCallback(() => {
    if (retryTimerRef.current) clearTimeout(retryTimerRef.current);
    if (heartbeatTimerRef.current) clearTimeout(heartbeatTimerRef.current);
    if (pollingTimerRef.current) clearInterval(pollingTimerRef.current);
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
    retryCountRef.current = 0;
    setConnectionState('disconnected');
    setErrorInfo(null);
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  useEffect(() => {
    return () => { disconnect(); };
  }, [disconnect]);

  return {
    messages,
    connectionState,
    errorInfo,
    connect,
    disconnect,
    clearMessages,
  };
}
