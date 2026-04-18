import { useState, useEffect, useCallback, useRef } from 'react';

/**
 * Ch08: 어댑티브 폴링 + Full Jitter
 *
 * 학습 목표:
 * - 서버 TTL 기반 동적 폴링 주기 조절
 * - Full Jitter로 요청 분산 (재접속 폭풍 방지)
 * - 지수 백오프 에러 재시도
 * - 리다이렉트 처리 (대기열 입장)
 * - cleanup (clearTimeout + stop/resume)
 */

export interface QueueStatus {
  position: number;
  total: number;
  ttl: number;
  redirect?: string;
}

export interface UseAdaptivePollingOptions {
  onRedirect?: (url: string) => void;
  onError?: (error: Error) => void;
  maxRetries?: number;
}

export interface UseAdaptivePollingReturn {
  status: QueueStatus | null;
  error: Error | null;
  isPolling: boolean;
  retryCount: number;
  nextPollIn: number | null;
  stop: () => void;
  resume: () => void;
}

export function useAdaptivePolling(
  url: string,
  token: string,
  options: UseAdaptivePollingOptions = {}
): UseAdaptivePollingReturn {
  const { maxRetries = 5 } = options;

  const [status, setStatus] = useState<QueueStatus | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [isPolling, setIsPolling] = useState(false);
  const [retryCount, setRetryCount] = useState(0);
  const [nextPollIn, setNextPollIn] = useState<number | null>(null);

  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const retryCountRef = useRef(0);
  const isPollingRef = useRef(false);

  // Full Jitter 계산: AWS 권장 알고리즘
  // 기본 지수 백오프(base + jitter)는 base만큼 항상 대기하지만,
  // Full Jitter는 0부터 ceiling까지 균등 분포하여 요청을 시간축에 골고루 분산
  const calculateFullJitter = useCallback((attempt: number, baseMs: number = 1000, ceiling: number = 30000): number => {
    const calculatedCeiling = Math.min(ceiling, baseMs * Math.pow(2, attempt));
    return Math.random() * calculatedCeiling;
  }, []);

  // 서버 TTL 기반 다음 폴링 시간 계산
  // ±20% Jitter를 적용하여 동일 TTL을 받은 클라이언트들의 요청이 동시에 몰리지 않도록 분산
  const calculateNextPollTime = useCallback((ttl: number): number => {
    const jitter = ttl * 0.2 * (Math.random() * 2 - 1);
    return Math.max(500, ttl + jitter);
  }, []);

  // poll: fetch → 응답 파싱 → 다음 폴링 스케줄링
  const poll = useCallback(async () => {
    if (!isPollingRef.current) return;

    try {
      const response = await fetch(`${url}?token=${token}`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data: QueueStatus = await response.json();

      setStatus(data);
      setError(null);
      retryCountRef.current = 0;
      setRetryCount(0);

      // 리다이렉트: 대기열 통과 → 서비스 입장
      if (data.redirect) {
        setIsPolling(false);
        isPollingRef.current = false;
        options.onRedirect?.(data.redirect);
        return;
      }

      // 서버 TTL + Jitter로 다음 폴링 스케줄링
      const nextTime = calculateNextPollTime(data.ttl);
      setNextPollIn(nextTime);
      timeoutRef.current = setTimeout(poll, nextTime);
    } catch (err) {
      const error = err instanceof Error ? err : new Error(String(err));
      setError(error);
      options.onError?.(error);

      // 최대 재시도 초과 시 폴링 중단
      if (retryCountRef.current >= maxRetries) {
        setIsPolling(false);
        isPollingRef.current = false;
        return;
      }

      // Full Jitter로 에러 재시도 (고정 간격 대신 분산)
      const jitterDelay = calculateFullJitter(retryCountRef.current);
      retryCountRef.current++;
      setRetryCount(retryCountRef.current);
      setNextPollIn(jitterDelay);
      timeoutRef.current = setTimeout(poll, jitterDelay);
    }
  }, [url, token, maxRetries, options, calculateFullJitter, calculateNextPollTime]);

  // stop: 폴링 중단 + 타이머 정리
  const stop = useCallback(() => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
    isPollingRef.current = false;
    setIsPolling(false);
    setNextPollIn(null);
  }, []);

  // resume: 폴링 재개 (상태 초기화 후 시작)
  const resume = useCallback(() => {
    if (isPollingRef.current) return;
    isPollingRef.current = true;
    setIsPolling(true);
    retryCountRef.current = 0;
    setRetryCount(0);
    setError(null);
    poll();
  }, [poll]);

  // cleanup: 언마운트 시 타이머 정리
  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  return {
    status,
    error,
    isPolling,
    retryCount,
    nextPollIn,
    stop,
    resume,
  };
}
