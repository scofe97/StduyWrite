import { useEffect, useState, useCallback, useRef } from 'react';
import { EventSourcePolyfill, EventSourcePolyfillInit } from 'event-source-polyfill';

/**
 * readyState 상수
 */
export const ReadyState = {
  CONNECTING: 0,
  OPEN: 1,
  CLOSED: 2,
} as const;

export type ReadyStateType = (typeof ReadyState)[keyof typeof ReadyState];

/**
 * useEventSource 훅 옵션
 */
interface UseEventSourceOptions {
  withCredentials?: boolean;
  headers?: Record<string, string>;
  heartbeatTimeout?: number;
  autoConnect?: boolean;
}

/**
 * useEventSource 훅 반환 타입
 */
interface UseEventSourceReturn<T> {
  data: T | null;
  error: Error | null;
  readyState: ReadyStateType;
  isConnected: boolean;
  close: () => void;
  connect: () => void;
}

/**
 * EventSource 커스텀 훅 (event-source-polyfill 사용)
 */
export function useEventSource<T = unknown>(
  url: string,
  options: UseEventSourceOptions = {}
): UseEventSourceReturn<T> {
  const {
    withCredentials = false,
    headers,
    heartbeatTimeout = 45000,
    autoConnect = true,
  } = options;

  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [readyState, setReadyState] = useState<ReadyStateType>(ReadyState.CLOSED);

  const eventSourceRef = useRef<EventSourcePolyfill | null>(null);

  const connect = useCallback(() => {
    if (eventSourceRef.current) {
      return;
    }

    const esOptions: EventSourcePolyfillInit = {
      withCredentials,
      heartbeatTimeout,
    };

    if (headers) {
      esOptions.headers = headers;
    }

    const es = new EventSourcePolyfill(url, esOptions);
    eventSourceRef.current = es;
    setReadyState(ReadyState.CONNECTING);

    es.onopen = () => {
      setReadyState(ReadyState.OPEN);
      setError(null);
    };

    es.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data) as T;
        setData(parsed);
      } catch {
        setData(event.data as unknown as T);
      }
    };

    es.onerror = () => {
      setReadyState(es.readyState as ReadyStateType);
      if (es.readyState === ReadyState.CLOSED) {
        setError(new Error('연결이 종료되었습니다'));
      }
    };
  }, [url, withCredentials, headers, heartbeatTimeout]);

  const close = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
      setReadyState(ReadyState.CLOSED);
    }
  }, []);

  useEffect(() => {
    if (autoConnect) {
      connect();
    }
    return () => {
      close();
    };
  }, [autoConnect, connect, close]);

  return {
    data,
    error,
    readyState,
    isConnected: readyState === ReadyState.OPEN,
    close,
    connect,
  };
}
