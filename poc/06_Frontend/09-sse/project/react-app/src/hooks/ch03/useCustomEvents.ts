import { useState, useEffect, useCallback, useRef } from 'react';
import { EventListener, EventSource, EventSourcePolyfill, EventSourcePolyfillInit } from 'event-source-polyfill';

// 커스텀 이벤트 타입 정의
export interface NotificationEvent {
  type: 'info' | 'warning' | 'error';
  title: string;
  message: string;
}

export interface UpdateEvent {
  resource: string;
  action: 'created' | 'updated' | 'deleted';
  data: Record<string, unknown>;
}

export interface AlertEvent {
  level: 'low' | 'medium' | 'high' | 'critical';
  source: string;
  description: string;
}

// 연결 상태
export type ConnectionStatus = 'connecting' | 'connected' | 'disconnected' | 'error';

interface UseCustomEventsOptions {
  headers?: Record<string, string>;
  withCredentials?: boolean;
  heartbeatTimeout?: number;
  autoConnect?: boolean;
}

interface UseCustomEventsReturn {
  status: ConnectionStatus;
  error: string | null;
  notifications: NotificationEvent[];
  updates: UpdateEvent[];
  alerts: AlertEvent[];
  connect: () => void;
  disconnect: () => void;
  clearEvents: () => void;
}

export function useCustomEvents(
  url: string,
  options: UseCustomEventsOptions = {}
): UseCustomEventsReturn {
  const {
    headers = {},
    withCredentials = false,
    heartbeatTimeout = 45000,
    autoConnect = true,
  } = options;

  const [status, setStatus] = useState<ConnectionStatus>('disconnected');
  const [error, setError] = useState<string | null>(null);
  const [notifications, setNotifications] = useState<NotificationEvent[]>([]);
  const [updates, setUpdates] = useState<UpdateEvent[]>([]);
  const [alerts, setAlerts] = useState<AlertEvent[]>([]);

  const eventSourceRef = useRef<EventSourcePolyfill | null>(null);

  const connect = useCallback(() => {
    if (eventSourceRef.current) {
      return;
    }
    setStatus('connecting');
    setError(null);

    const config: EventSourcePolyfillInit = {
      withCredentials,
      heartbeatTimeout,
    };

    if (Object.keys(headers).length > 0) {
      config.headers = headers;
    }
    const es = new EventSourcePolyfill(url, config);
    eventSourceRef.current = es;

    es.onopen = () => {
      setStatus('connected');
      setError(null);
    };
    es.onmessage = (event) => console.log(event);

    es.addEventListener('notification', ((event: MessageEvent) => {
      try {
        const data = JSON.parse(event.data) as NotificationEvent;
        setNotifications(prev => [...prev, data]);
      } catch (e) {
        console.error('Failed to parse: ', e);
      }
    }) as EventListener);

    es.addEventListener('update', ((event: MessageEvent) => {
      try {
        const data = JSON.parse(event.data) as UpdateEvent;
        setUpdates(prev => [...prev, data]);
      } catch (e) {
        console.error('Failed to parse: ', e);
      }
    }) as EventListener);

    es.addEventListener('alert', ((event: MessageEvent) => {
      try {
        const data = JSON.parse(event.data) as AlertEvent;
        setAlerts(prev => [...prev, data]);
      } catch (e) {
        console.error('Failed to parse: ', e);
      }
    }) as EventListener);

    es.onerror = () => {
      if (es.readyState === EventSource.CLOSED) {
        setStatus('disconnected');
        setError('Connection closed');
      } else {
        setStatus('error');
        setError('reconnecting');
      }
    };
  }, [url, headers, withCredentials, heartbeatTimeout]);

  const disconnect = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
      setStatus('disconnected');
    }
  }, []);

  const clearEvents = useCallback(() => {
    setNotifications([]);
    setUpdates([]);
    setAlerts([]);
  }, []);

  useEffect(() => {
    if (autoConnect) {
      connect();
    }
    return disconnect;
  }, [autoConnect, connect, disconnect]);

  return {
    status,
    error,
    notifications,
    updates,
    alerts,
    connect,
    disconnect,
    clearEvents,
  };
}

// 인증이 필요한 커스텀 이벤트 훅
export function useCustomEventsWithAuth(
  url: string,
  token: string | null,
  options: Omit<UseCustomEventsOptions, 'headers'> = {}
): UseCustomEventsReturn & { isAuthenticated: boolean } {
  const headers = token
    ? { Authorization: `Bearer ${token}` }
    : ({} as Record<string, string>);

  const result = useCustomEvents(url, {
    ...options,
    headers,
    autoConnect: false,
  });

  useEffect(() => {
    if (token) {
      result.disconnect();
      result.connect();
    } else {
      result.disconnect();
    }
  }, [token]); // eslint-disable-line react-hooks/exhaustive-deps

  return {
    ...result,
    isAuthenticated: !!token,
  };
}
