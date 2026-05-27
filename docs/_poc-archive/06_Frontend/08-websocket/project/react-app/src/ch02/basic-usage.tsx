/**
 * 실습: react-use-websocket 기본 사용법
 *
 * 목표: useWebSocket 훅의 기본적인 사용법을 익힙니다.
 *
 * TODO 주석을 따라 코드를 완성하세요.
 */

import  { useEffect, useState } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';

const WS_URL = 'ws://localhost:8070';

interface Message {
  type: string;
  data?: unknown;
  message?: string;
}

/**
 * 실습 1: 기본 연결
 */
export function BasicConnection() {
  // 반환값: sendMessage, lastMessage, readyState
  const [messageList, setMessageList] = useState<string[]>([])

  const { sendMessage, lastMessage, readyState } = useWebSocket(WS_URL, {
    onMessage: (event) => {
      console.log(event.data)
      setMessageList(prevState => {
        return [...prevState, event.data]
      })
    }
  });

  useEffect(() => {
    if (lastMessage !== null) {
      // 여기서 라스트 메시지 받아서 설정해도됨
    }
  }, [lastMessage]);


  const connectionStatus = {
    [ReadyState.CONNECTING]: '연결 중...',
    [ReadyState.OPEN]: '연결됨',
    [ReadyState.CLOSING]: '연결 종료 중...',
    [ReadyState.CLOSED]: '연결 종료',
    [ReadyState.UNINSTANTIATED]: '초기화 안됨',
  }[readyState];

  const handleSendMessage = () => {
    sendMessage(JSON.stringify({ type: 'PING' }));
  };

  return (
    <div>
      <h2>기본 연결 테스트</h2>
      <p>상태: {connectionStatus}</p>

      <button onClick={handleSendMessage} disabled={readyState !== ReadyState.OPEN}>
        PING 전송
      </button>

      {lastMessage && (
        <div>
          <h3>마지막 메시지:</h3>
          <pre>{lastMessage.data}</pre>
        </div>
      )}
    </div>
  );
}

/**
 * 실습 2: 메시지 히스토리 관리
 */
export function MessageHistory() {
  const [messageHistory, setMessageHistory] = useState<Message[]>([]);

  const { sendMessage, lastMessage, readyState } = useWebSocket(WS_URL, {
    onMessage: (event) => {
      // 힌트: setMessageHistory((prev) => [...prev, JSON.parse(event.data)]);
      setMessageHistory((prev) => [...prev, JSON.parse(event.data)]);
    },
  });

  // 위의 onMessage와 이 방법 중 하나만 선택하여 사용
  useEffect(() => {
    if (lastMessage !== null) {
      // setMessageHistory((prev) => [...prev, JSON.parse(lastMessage.data)]);
    }
  }, [lastMessage]);

  const handleSubscribe = () => {
    sendMessage(JSON.stringify({ type: 'SUBSCRIBE', topic: 'updates' }));
  };

  return (
    <div>
      <h2>메시지 히스토리</h2>
      <button onClick={handleSubscribe} disabled={readyState !== ReadyState.OPEN}>
        구독 시작
      </button>

      <div>
        <h3>수신 메시지 ({messageHistory.length}개)</h3>
        <ul>
          {messageHistory.map((msg, idx) => (
            <li key={idx}>
              <code>{JSON.stringify(msg)}</code>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

/**
 * 실습 3: 콜백 옵션 활용
 */
export function WithCallbacks() {
  const [log, setLog] = useState<string[]>([]);

  const addLog = (message: string) => {
    setLog((prev) => [...prev, `[${new Date().toLocaleTimeString()}] ${message}`]);
  };

  const { sendMessage, readyState } = useWebSocket(WS_URL, {
    // TODO: 각 콜백에서 로그 추가
    onOpen: () => {
      addLog('연결됨');
    },
    onClose: (event) => {
      addLog(`연결 종료: code=${event.code}`);
    },
    onMessage: (event) => {
      addLog(`메시지 수신: ${event.data}`);
    },
    onError: () => {
      addLog('에러 발생');
    },
  });

  return (
    <div>
      <h2>콜백 로그</h2>
      <button onClick={() => sendMessage(JSON.stringify({ type: 'PING' }))} disabled={readyState !== ReadyState.OPEN}>
        PING
      </button>
      <pre>{log.join('\n')}</pre>
    </div>
  );
}
