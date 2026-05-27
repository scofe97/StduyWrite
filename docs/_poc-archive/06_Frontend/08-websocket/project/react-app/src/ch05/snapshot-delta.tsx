/**
 * 실습: SNAPSHOT/DELTA 패턴 구현
 *
 * 목표: SNAPSHOT으로 초기 상태를 받고, DELTA로 업데이트하는 패턴을 구현합니다.
 *
 * TODO 주석을 따라 코드를 완성하세요.
 */

import { useCallback, useEffect, useState } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';

const WS_URL = 'ws://localhost:8070';

// 데이터 타입 정의
interface Item {
  id: number;
  name: string;
  status: 'active' | 'pending' | 'completed' | 'error';
  updatedAt?: string;
}

// 메시지 타입 정의
interface SnapshotMessage {
  type: 'SNAPSHOT';
  data: Item[];
}

interface DeltaMessage {
  type: 'DELTA';
  data: {
    id: number;
    changes: Partial<Item>;
  };
}

interface AckMessage {
  type: 'ACK';
  message: string;
}

interface ErrorMessage {
  type: 'ERROR';
  message: string;
}

type ServerMessage = SnapshotMessage | DeltaMessage | AckMessage | ErrorMessage;

/**
 * 실습 1: SNAPSHOT/DELTA 처리
 *
 * 학습 포인트:
 * - SNAPSHOT: 전체 상태를 교체
 * - DELTA: 특정 항목만 업데이트
 * - 메시지 타입에 따른 분기 처리
 */
export function SnapshotDeltaDemo() {
  const [items, setItems] = useState<Item[]>([]);
  const [isInitialized, setIsInitialized] = useState(false);
  const [lastError, setLastError] = useState<string | null>(null);

  const { sendMessage, lastMessage, readyState } = useWebSocket(WS_URL, {
    onOpen: () => {
      // 연결 시 구독 요청 → 서버에서 SNAPSHOT 응답
      sendMessage(JSON.stringify({ type: 'SUBSCRIBE', topic: 'items' }));
    },
  });

  // 메시지 처리 로직
  const handleMessage = useCallback((message: ServerMessage) => {
    switch (message.type) {
      case 'SNAPSHOT':
        console.log('SNAPSHOT 수신:', message.data);
        setItems(message.data);
        setIsInitialized(true);
        break;

      case 'DELTA':
        const { id, changes } = message.data;
        setItems(prevState => prevState.map(item =>
          item.id === id ? { ...item, ...changes } : item
        ));
        console.log('DELTA 수신:', message.data);
        break;

      case 'ERROR':
        console.error('서버 에러:', message.message);
        setLastError(message.message);
        break;

      case 'ACK':
        console.log('ACK:', message.message);
        break;
    }
  }, []);

  // lastMessage 변경 시 처리
  useEffect(() => {
    if (lastMessage !== null) {
      try {
        const parsed: ServerMessage = JSON.parse(lastMessage.data);
        handleMessage(parsed);
      } catch (error) {
        console.error('메시지 파싱 실패:', error);
      }
    }
  }, [lastMessage, handleMessage]);

  // 상태별 색상
  const statusColors: Record<Item['status'], string> = {
    active: '#4CAF50',
    pending: '#FFC107',
    completed: '#2196F3',
    error: '#F44336',
  };

  return (
    <div>
      <h2>실습 1: SNAPSHOT/DELTA 패턴</h2>

      <div style={{ marginBottom: '16px' }}>
        <p>연결 상태: {readyState === ReadyState.OPEN ? '연결됨' : '연결 안됨'}</p>
        <p>초기화: {isInitialized ? '완료' : '대기 중...'}</p>
        {lastError && <p style={{ color: 'red' }}>에러: {lastError}</p>}
      </div>

      {/* 아이템 목록 */}
      <div>
        <h3>아이템 목록 ({items.length}개)</h3>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {items.map((item) => (
            <li
              key={item.id}
              style={{
                padding: '12px',
                marginBottom: '8px',
                border: '1px solid #ccc',
                borderRadius: '4px',
                borderLeft: `4px solid ${statusColors[item.status]}`,
              }}
            >
              <strong>{item.name}</strong>
              <span
                style={{
                  marginLeft: '12px',
                  padding: '2px 8px',
                  borderRadius: '12px',
                  backgroundColor: statusColors[item.status],
                  color: 'white',
                  fontSize: '12px',
                }}
              >
                {item.status}
              </span>
              {item.updatedAt && (
                <span style={{ marginLeft: '12px', fontSize: '12px', color: '#666' }}>
                  {new Date(item.updatedAt).toLocaleTimeString()}
                </span>
              )}
            </li>
          ))}
        </ul>
      </div>

    </div>
  );
}

/**
 * 실습 2: 버전 기반 동기화 (DELTA 누락 감지)
 *
 * 학습 포인트:
 * - 버전 번호로 메시지 순서 관리
 * - 버전 갭 감지 시 SNAPSHOT 재요청
 */
interface VersionedItem extends Item {
  version: number;
}

interface VersionedSnapshotMessage {
  type: 'SNAPSHOT';
  version: number;
  data: VersionedItem[];
}

interface VersionedDeltaMessage {
  type: 'DELTA';
  version: number;
  data: {
    id: number;
    changes: Partial<VersionedItem>;
  };
}

export function VersionedSnapshotDelta() {
  const [items, setItems] = useState<VersionedItem[]>([]);
  const [currentVersion, setCurrentVersion] = useState(0);
  const [missedUpdates, setMissedUpdates] = useState<number[]>([]);

  const { sendMessage, lastMessage, readyState } = useWebSocket(WS_URL, {
    onOpen: () => {
      sendMessage(JSON.stringify({ type: 'SUBSCRIBE', topic: 'versioned-items' }));
    },
  });

  // 버전 기반 메시지 처리
  useEffect(() => {
    if (lastMessage !== null) {
      try {
        const parsed = JSON.parse(lastMessage.data);

        if (parsed.type === 'SNAPSHOT') {
          const snapshot = parsed as VersionedSnapshotMessage;
          setItems(snapshot.data);
          setCurrentVersion(snapshot.version);
          setMissedUpdates([]);
          console.log('SNAPSHOT 수신:', snapshot);
        }

        if (parsed.type === 'DELTA') {
          const delta = parsed as VersionedDeltaMessage;

          // 버전 갭 감지
          if (delta.version - currentVersion > 1) {
            const missed: number[] = [];
            for (let v = currentVersion + 1; v < delta.version; v++) {
              missed.push(v);
            }
            setMissedUpdates(prev => [...prev, ...missed]);
            sendMessage(JSON.stringify({ type: 'RESYNC' }));
            return;
          }

          console.log('DELTA 수신:', delta, '현재 버전:', currentVersion);

          // 정상적인 DELTA 적용
          setItems(prevState => prevState.map(item =>
            item.id === delta.data.id
              ? { ...item, ...delta.data.changes }
              : item
          ));
          setCurrentVersion(delta.version);
        }
      } catch (error) {
        console.error('메시지 파싱 실패:', error);
      }
    }
  }, [lastMessage, currentVersion, sendMessage]);

  return (
    <div>
      <h2>실습 2: 버전 기반 동기화</h2>

      <div style={{ marginBottom: '16px' }}>
        <p>연결 상태: {readyState === ReadyState.OPEN ? '연결됨' : '연결 안됨'}</p>
        <p>현재 버전: {currentVersion}</p>
        {missedUpdates.length > 0 && (
          <p style={{ color: 'orange' }}>
            누락된 업데이트: {missedUpdates.join(', ')}
          </p>
        )}
      </div>

      <ul>
        {items.map((item) => (
          <li key={item.id}>
            {item.name} (v{item.version}) - {item.status}
          </li>
        ))}
      </ul>

    </div>
  );
}

/**
 * 실습 3: 낙관적 업데이트
 *
 * 학습 포인트:
 * - 서버 응답 전에 UI 먼저 업데이트
 * - 실패 시 롤백
 * - pending 상태 관리
 */
export function OptimisticUpdate() {
  const [items, setItems] = useState<Item[]>([
    { id: 1, name: 'Item 1', status: 'pending' },
    { id: 2, name: 'Item 2', status: 'active' },
    { id: 3, name: 'Item 3', status: 'completed' },
  ]);
  const [pendingUpdates, setPendingUpdates] = useState<Map<number, Item>>(new Map());

  const { sendMessage, lastMessage, readyState } = useWebSocket(WS_URL);

  // 서버 응답 처리
  useEffect(() => {
    if (lastMessage !== null) {
      try {
        const parsed = JSON.parse(lastMessage.data);

        if (parsed.type === 'ACK' && parsed.itemId) {
          // 성공 시 pending 상태 제거
          setPendingUpdates(prev => {
            const next = new Map(prev);
            next.delete(parsed.itemId);
            return next;
          });
          console.log('ACK 수신:', parsed.itemId);
        }

        if (parsed.type === 'ERROR' && parsed.itemId) {
          // 실패 시 롤백
          const previousItem = pendingUpdates.get(parsed.itemId);
          if (previousItem) {
            setItems(prev => prev.map(item =>
              item.id === parsed.itemId ? previousItem : item
            ));
          }
          // pending에서 제거
          setPendingUpdates(prev => {
            const next = new Map(prev);
            next.delete(parsed.itemId);
            return next;
          });
          console.error('ERROR 수신:', parsed.itemId, parsed.message);
        }
      } catch (error) {
        console.error('메시지 파싱 실패:', error);
      }
    }
  }, [lastMessage, pendingUpdates]);

  // 낙관적 업데이트 함수
  const updateItemStatus = (id: number, newStatus: Item['status']) => {
    // 1. 이전 상태 저장 (롤백용)
    const previousItem = items.find((item) => item.id === id);
    if (previousItem) {
      setPendingUpdates(prev => new Map(prev).set(id, previousItem));
    }

    // 2. 낙관적 업데이트 (즉시 UI 반영)
    setItems(prev => prev.map(item =>
      item.id === id ? { ...item, status: newStatus } : item
    ));

    // 3. 서버에 UPDATE 메시지 전송
    sendMessage(JSON.stringify({
      type: 'UPDATE',
      data: { id, changes: { status: newStatus } },
    }));
  };

  const statusOptions: Item['status'][] = ['active', 'pending', 'completed', 'error'];

  return (
    <div>
      <h2>실습 3: 낙관적 업데이트</h2>

      <p style={{ fontSize: '12px', color: '#666' }}>
        상태를 변경하면 서버 응답 전에 UI가 먼저 업데이트됩니다.
      </p>

      <ul style={{ listStyle: 'none', padding: 0 }}>
        {items.map((item) => (
          <li
            key={item.id}
            style={{
              padding: '12px',
              marginBottom: '8px',
              border: '1px solid #ccc',
              borderRadius: '4px',
              opacity: pendingUpdates.has(item.id) ? 0.7 : 1,
            }}
          >
            <span>{item.name}</span>
            {pendingUpdates.has(item.id) && (
              <span style={{ marginLeft: '8px', fontSize: '12px' }}>저장 중...</span>
            )}

            <div style={{ marginTop: '8px' }}>
              {statusOptions.map((status) => (
                <button
                  key={status}
                  onClick={() => updateItemStatus(item.id, status)}
                  disabled={item.status === status || readyState !== ReadyState.OPEN}
                  style={{
                    marginRight: '4px',
                    padding: '4px 8px',
                    backgroundColor: item.status === status ? '#4CAF50' : '#f0f0f0',
                    color: item.status === status ? 'white' : 'black',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer',
                  }}
                >
                  {status}
                </button>
              ))}
            </div>
          </li>
        ))}
      </ul>

    </div>
  );
}
