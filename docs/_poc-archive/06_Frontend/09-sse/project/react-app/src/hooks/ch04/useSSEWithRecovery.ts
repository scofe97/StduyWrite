import { useEffect, useState, useCallback, useRef } from 'react';
import {EventListener, EventSourcePolyfill, EventSourcePolyfillInit} from 'event-source-polyfill';

/**
 * Ch04 실습: SSE 재연결 및 Last-Event-ID
 *
 * 학습 목표:
 * - EventSourcePolyfill 설정 (headers, heartbeatTimeout)
 * - Last-Event-ID를 통한 이벤트 복구
 * - 수동 재연결 로직 (maxRetries, exponential backoff)
 * - cleanup 함수 구현
 */

export interface SSERecoveryEvent {
  id: string;
  data: string;
  timestamp: string;
  sequence: number;
}

export interface UseSSEWithRecoveryOptions {
  headers?: Record<string, string>;
  heartbeatTimeout?: number;
  maxRetries?: number;
  baseRetryInterval?: number;
}

export interface UseSSEWithRecoveryReturn {
  events: SSERecoveryEvent[];
  isConnected: boolean;
  reconnectCount: number;
  lastEventId: string | null;
  error: string | null;
  connect: () => void;
  disconnect: () => void;
  clearEvents: () => void;
}

export function useSSEWithRecovery(
  url: string,
  options: UseSSEWithRecoveryOptions = {}
): UseSSEWithRecoveryReturn {
  const {
    headers,
    heartbeatTimeout = 45000,
    maxRetries = 5,
    baseRetryInterval = 1000,
  } = options;

  const [events, setEvents] = useState<SSERecoveryEvent[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [_reconnectCount, _setReconnectCount] = useState(0);
  const [lastEventId, setLastEventId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const eventSourceRef = useRef<EventSourcePolyfill | null>(null);
  const reconnectTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const lastEventIdRef = useRef<string | null>(null);

  const connect = useCallback(() => {
    if (eventSourceRef.current) return;
    setError(null);

    const config: EventSourcePolyfillInit = {
      heartbeatTimeout,
      headers: lastEventIdRef.current ?{...headers, "Last-Event-ID": lastEventIdRef.current } : headers,
    };

    const es = new EventSourcePolyfill(url, config);
    eventSourceRef.current = es;

    es.onopen = () => {
      setIsConnected(true);
      setError(null);
      _setReconnectCount(0)
    };

    es.addEventListener('update', ((event: MessageEvent) => {
      try {
        const parsed = JSON.parse(event.data) as SSERecoveryEvent;
        setEvents(prev => [...prev, parsed]);
        const eventId = event.lastEventId || String(parsed.id);
        lastEventIdRef.current = eventId;
        setLastEventId(eventId);
      } catch {
        console.error('Failed to parse event data');
      }
    }) as EventListener);

    es.onerror = () => {
      setIsConnected(false);

      // readyState 2(CLOSED) = 서버가 연결을 끊음 → 수동 재연결 필요
      if (es.readyState === 2) {
        eventSourceRef.current = null;

        _setReconnectCount(prev => {
          if (prev >= maxRetries) {
            setError(`재연결 ${maxRetries}회 초과. 수동으로 다시 시도하세요.`);
            return prev;
          }

          const delay = baseRetryInterval * Math.pow(2, prev);
          setError(`재연결 대기 중... (${delay}ms 후 ${prev + 1}/${maxRetries})`);

          reconnectTimerRef.current = setTimeout(() => {
            reconnectTimerRef.current = null;
            connect();
          }, delay);

          return prev + 1;
        });
      }
    };
  }, [url, headers, heartbeatTimeout, maxRetries, baseRetryInterval]);

  const disconnect = useCallback(() => {
    // 1. 재연결 타이머 정리 (백오프 대기 중이면 취소)
    if (reconnectTimerRef.current) {
      clearTimeout(reconnectTimerRef.current);
      reconnectTimerRef.current = null;
    }
    // 2. EventSource 연결 종료
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
    // 3. 상태 초기화
    setIsConnected(false);
    setError(null);
  }, []);

  const clearEvents = useCallback(() => {
    setEvents([]);
    setLastEventId(null);
    lastEventIdRef.current = null;
  }, []);

  useEffect(() => {
    return () => { disconnect(); };
  }, [disconnect]);

  return {
    events,
    isConnected,
    reconnectCount: _reconnectCount,
    lastEventId,
    error,
    connect,
    disconnect,
    clearEvents,
  };
}
