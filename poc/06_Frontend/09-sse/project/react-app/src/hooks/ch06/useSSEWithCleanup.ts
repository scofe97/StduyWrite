import { useEffect, useState, useCallback, useRef } from 'react';
import { EventSourcePolyfill, EventSourcePolyfillInit } from 'event-source-polyfill';

/**
 * Ch06 실습: React SSE 통합
 *
 * 학습 목표:
 * - useRef + AbortController로 연결 관리
 * - React 18 Strict Mode 대응 (mount/unmount/remount)
 * - useEffect cleanup에서 정리
 * - useCallback으로 함수 메모이제이션
 * - isMountedRef로 언마운트 후 상태 업데이트 방지
 * - 의존성 배열 최적화
 */

export interface SSECleanupMessage {
  id: number;
  data: string;
  timestamp: string;
}

export interface UseSSEWithCleanupOptions {
  headers?: Record<string, string>;
  heartbeatTimeout?: number;
  autoConnect?: boolean;
}

export interface UseSSEWithCleanupReturn {
  messages: SSECleanupMessage[];
  isConnected: boolean;
  mountCount: number;
  error: string | null;
  connect: () => void;
  disconnect: () => void;
  clearMessages: () => void;
}

export function useSSEWithCleanup(
  url: string,
  options: UseSSEWithCleanupOptions = {}
): UseSSEWithCleanupReturn {
  const {
    headers,
    heartbeatTimeout = 45000,
    autoConnect = false,
  } = options;

  const [messages, setMessages] = useState<SSECleanupMessage[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [mountCount, setMountCount] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const eventSourceRef = useRef<EventSourcePolyfill | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);
  const isMountedRef = useRef(false);

  const connect = useCallback(() => {
    if (eventSourceRef.current) return;

    const controller = new AbortController();
    abortControllerRef.current = controller;

    if (controller.signal.aborted) return;

    setError(null);

    const config: EventSourcePolyfillInit = {
      heartbeatTimeout,
    };
    if (headers) {
      config.headers = { ...headers };
    }

    const es = new EventSourcePolyfill(url, config);
    eventSourceRef.current = es;

    es.onopen = () => {
      if (!isMountedRef.current) return;
      setIsConnected(true);
      setError(null);
    };

    es.addEventListener('update', (event: any) => {
      if (!isMountedRef.current) return;
      try {
        const parsed = JSON.parse(event.data) as SSECleanupMessage;
        setMessages(prev => [...prev, parsed]);
      } catch {
        console.error('Failed to parse event data');
      }
    });

    es.onerror = () => {
      if (!isMountedRef.current) return;
      setIsConnected(false);
      if (es.readyState === 2) {
        setError('연결 종료됨');
      }
    };
  }, [url, headers, heartbeatTimeout]);

  const disconnect = useCallback(() => {
    abortControllerRef.current?.abort();
    abortControllerRef.current = null;

    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
      setIsConnected(false);
    }
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  useEffect(() => {
    isMountedRef.current = true;
    setMountCount(prev => prev + 1);

    if (autoConnect) {
      connect();
    }

    return () => {
      isMountedRef.current = false;
      disconnect();
    };
  }, [autoConnect, connect, disconnect]);

  return {
    messages,
    isConnected,
    mountCount,
    error,
    connect,
    disconnect,
    clearMessages,
  };
}
