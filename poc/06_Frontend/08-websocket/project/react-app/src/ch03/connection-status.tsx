/**
 * 실습: 연결 상태 관리 및 시각화
 *
 * 목표: readyState에 따른 UI 분기와 상태 시각화를 구현합니다.
 *
 * TODO 주석을 따라 코드를 완성하세요.
 */

import React, {useEffect, useState} from 'react';
import useWebSocket, {ReadyState} from 'react-use-websocket';
import * as timers from "node:timers";

const WS_URL = 'ws://localhost:8070';

/**
 * 실습 1: 상태 인디케이터 컴포넌트
 *
 * readyState 값에 따라 색상과 텍스트를 표시하는 컴포넌트를 만드세요.
 *
 * 요구사항:
 * - CONNECTING: 주황색, "연결 중..."
 * - OPEN: 초록색, "연결됨"
 * - CLOSING: 노란색, "종료 중..."
 * - CLOSED: 빨간색, "연결 끊김"
 * - UNINSTANTIATED: 회색, "초기화 안됨"
 */
interface StatusIndicatorProps {
  readyState: ReadyState;
}

export function StatusIndicator({ readyState }: StatusIndicatorProps) {
  // TODO: 상태별 색상 정의 (Record<ReadyState, string> 타입 사용)
  const statusColors: Record<ReadyState, string> = {
    // 여기에 각 상태별 색상을 정의하세요
      [ReadyState.CONNECTING]: "#FFA500",
      [ReadyState.OPEN]: "#00FF00",
      [ReadyState.CLOSING]: "#FFFF00",
      [ReadyState.CLOSED]: "#FF0000",
      [ReadyState.UNINSTANTIATED]: "#808080",
  };

  // TODO: 상태별 텍스트 정의 (Record<ReadyState, string> 타입 사용)
  const statusText: Record<ReadyState, string> = {
      [ReadyState.CONNECTING]: "연결 중...",
      [ReadyState.OPEN]: "연결됨",
      [ReadyState.CLOSING]: "종료 중...",
      [ReadyState.CLOSED]: "연결 끊김",
      [ReadyState.UNINSTANTIATED]: "초기화 안됨",
  };

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
      {/* TODO: 상태 표시 원 (12x12px, 둥근 원, 배경색은 statusColors에서) */}
        <span style={{
            width: '12px',
            height: '12px',
            borderRadius: '50%',
            backgroundColor: statusColors[readyState],
            display: 'inline-block',  // 추가!
        }}/>
      {/* TODO: 상태 텍스트 (statusText에서) */}
        <span>{statusText[readyState]}</span>
    </div>
  );
}

/**
 * 실습 2: 상태별 UI 분기
 *
 * 연결 상태에 따라 다른 UI를 보여주는 컴포넌트를 만드세요.
 *
 * 요구사항:
 * - CONNECTING: "서버에 연결하는 중입니다..." 메시지
 * - OPEN: 메시지 전송 버튼 + 연결 해제 버튼
 * - CLOSED: "연결이 종료되었습니다." + 재연결 버튼
 * - UNINSTANTIATED: "WebSocket이 초기화되지 않았습니다." + 연결 시작 버튼
 */
export function ConnectionStateDemo() {
  const [shouldConnect, setShouldConnect] = useState(true);

  const { sendJsonMessage, lastMessage, readyState, getWebSocket } = useWebSocket(
    shouldConnect ? WS_URL : null,
    {
      onOpen: () => console.log('연결됨'),
      onMessage: (event) => console.log(event.data),
      onClose: (event) => console.log('종료됨:', event.code),
    }
  );

  // TODO: 수동으로 연결 종료하는 함수
  // - getWebSocket()으로 원본 WebSocket 가져오기
  // - ws.close(1000, 'User requested disconnect') 호출
  // - setShouldConnect(false) 호출
  const handleDisconnect = () => {
    const webSocket = getWebSocket();

    if(webSocket){
        webSocket.close(1000, "User Requested disconnect")
        setShouldConnect(false)
    }
  };

  // TODO: 재연결 함수
  // - setShouldConnect(true) 호출
  const handleReconnect = () => {
      setShouldConnect(true)
  };

  return (
    <div>
      <h2>연결 상태 관리</h2>

      {/* 상태 인디케이터 */}
      <StatusIndicator readyState={readyState} />

      {/* TODO: 상태별 UI 분기 */}
      <div style={{ marginTop: '20px' }}>
        {/* TODO: CONNECTING 상태일 때 로딩 메시지 표시 */}
          {readyState === ReadyState.CONNECTING && <span>로딩중</span>}

        {/* TODO: OPEN 상태일 때 메시지 전송/연결 해제 버튼 표시 */}
          {readyState === ReadyState.OPEN && <>
              <button onClick={() => sendJsonMessage({ type: 'ECHO', message: '테스트' })}>
                  메시지 전송
              </button>
              <button onClick={handleDisconnect}>메시지 전송/연결 해제</button>
          </>}

        {/* TODO: CLOSED 상태일 때 재연결 버튼 표시 */}
          {readyState === ReadyState.CLOSED && <button onClick={handleReconnect}>재연결</button>}

        {/* TODO: UNINSTANTIATED 상태일 때 연결 시작 버튼 표시 */}
          {readyState === ReadyState.UNINSTANTIATED && <button onClick={handleReconnect}>연결 시작</button>}

      </div>

      {/* 마지막 메시지 */}
      {lastMessage && (
        <div style={{ marginTop: '20px' }}>
          <h3>마지막 메시지:</h3>
          <pre>{lastMessage.data}</pre>
        </div>
      )}
    </div>
  );
}

/**
 * 실습 3: 상태 변경 감지 및 액션 수행
 *
 * 연결 상태가 변경될 때마다 히스토리에 기록하는 컴포넌트를 만드세요.
 *
 * 요구사항:
 * - onOpen 콜백에서 "[시간] 연결됨" 형식으로 히스토리에 추가
 * - onClose 콜백에서 "[시간] 종료됨 (code: X)" 형식으로 히스토리에 추가
 * - useEffect로 OPEN 상태일 때 추가 작업 수행 (콘솔 로그)
 */
export function StateChangeActions() {
  const [connectionHistory, setConnectionHistory] = useState<string[]>([]);

  const { readyState } = useWebSocket(WS_URL, {
    // TODO: onOpen 콜백 - 히스토리에 연결 기록 추가
      onOpen: (event) => {
          console.log(`[${new Date().toLocaleTimeString()}] 연결됨`)
          setConnectionHistory(prevState => [...prevState, event.type])
      },

    // TODO: onClose 콜백 - 히스토리에 종료 기록 추가
    // 형식: `[${new Date().toLocaleTimeString()}] 종료됨 (code: ${event.code})`
      onClose: (event) => {
          console.log(`[${new Date().toLocaleTimeString()}] 종료됨 (code: ${event.code})`)
          setConnectionHistory(prevState => [...prevState, event.type])
      }
  });

  // TODO: useEffect로 상태 변경 감지
  // - readyState가 OPEN일 때 콘솔에 "연결 성공! 초기 데이터 요청 가능" 출력


  return (
    <div>
      <h2>상태 변경 히스토리</h2>
      <StatusIndicator readyState={readyState} />

      <div style={{ marginTop: '20px' }}>
        <h3>연결 히스토리:</h3>
        <ul>
          {connectionHistory.map((entry, idx) => (
            <li key={idx}>{entry}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

/**
 * 실습 4: 오래된 데이터 표시
 *
 * 연결이 끊어진 후에도 마지막 데이터를 보여주되,
 * 데이터가 오래되었음을 시각적으로 표시하세요.
 *
 * 요구사항:
 * - 연결이 OPEN이 아니거나 30초 이상 메시지가 없으면 "오래된 데이터"로 표시
 * - 오래된 데이터: 노란색 배경 + 경고 메시지
 * - 신선한 데이터: 녹색 배경
 */
export function StaleDataIndicator() {
  const [lastUpdateTime, setLastUpdateTime] = useState<Date | null>(null);
    const [now, setNow] = useState(Date.now());

    // 1초마다 리렌더링
    useEffect(() => {
        const id = setInterval(() => setNow(Date.now()), 1000);
        return () => clearInterval(id);
    }, []);

  const { lastMessage, readyState } = useWebSocket<Date>(WS_URL, {
      onOpen: () => setLastUpdateTime(new Date()),

      onMessage: () => {
          console.log('메시지 전송')
          setLastUpdateTime(new Date())
      }
  });

  // TODO: isStale 계산
  // - readyState가 OPEN이 아니면 stale
  // - 또는 lastUpdateTime이 30초 이상 지났으면 stale
    const isStale = readyState !== ReadyState.OPEN ||
        (lastUpdateTime !== null && now - lastUpdateTime.getTime() > 5000);

    // 디버깅용 - 추가
    console.log({
        readyState,
        isOpen: readyState === ReadyState.OPEN,
        lastUpdateTime: lastUpdateTime?.toLocaleTimeString(),
        timeDiff: lastUpdateTime ? now - lastUpdateTime.getTime() : null,
        isStale,
    });

  return (
    <div>
      <h2>실시간 데이터</h2>
      <StatusIndicator readyState={readyState} />

      {/* isStale에 따라 배경색 변경: 노란색(#FFF3CD) vs 녹색(#D4EDDA) */}
      {/* isStale일 때 "⚠️ 데이터가 최신이 아닐 수 있습니다" 경고 표시 */}
      <div
        style={{
          marginTop: '20px',
          padding: '16px',
          backgroundColor: isStale ? '#FFF3CD' : '#D4EDDA',
          border: `1px solid ${isStale ? '#FFEEBA' : '#C3E6CB'}`,
          borderRadius: '4px',
          color: '#000'
        }}
      >
        {/* TODO: isStale일 때 경고 메시지 */}
        {isStale &&  <div> 경고 </div>}

        <div>
          <strong>마지막 메시지:</strong>
          <pre>{lastMessage?.data || '메시지 없음'}</pre>
        </div>

        {/* TODO: lastUpdateTime 표시 */}
        {lastUpdateTime && <div>{lastUpdateTime.toLocaleTimeString()}</div>}
      </div>
    </div>
  );
}
