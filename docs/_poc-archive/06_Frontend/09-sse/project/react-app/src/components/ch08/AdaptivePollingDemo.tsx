import { useState } from 'react';
import { useAdaptivePolling } from '../../hooks/ch08/useAdaptivePolling';

export function AdaptivePollingDemo() {
  const [token] = useState(() => `user-${Math.random().toString(36).slice(2, 8)}`);

  const { status, error, isPolling, retryCount, nextPollIn, stop, resume } = useAdaptivePolling(
    '/api/queue',
    token,
    {
      onRedirect: (url) => {
        alert(`입장 가능! 리다이렉트: ${url}`);
      },
      onError: (err) => {
        console.error('Polling error:', err);
      },
    }
  );

  return (
    <div style={{ padding: '20px' }}>
      <h3 style={{ marginBottom: '16px' }}>어댑티브 폴링 데모</h3>

      {/* 연결 제어 */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '20px' }}>
        <button
          onClick={resume}
          disabled={isPolling}
          style={{
            padding: '8px 16px',
            borderRadius: '6px',
            border: 'none',
            background: isPolling ? '#ccc' : '#4CAF50',
            color: '#fff',
            cursor: isPolling ? 'default' : 'pointer',
          }}
        >
          폴링 시작
        </button>
        <button
          onClick={stop}
          disabled={!isPolling}
          style={{
            padding: '8px 16px',
            borderRadius: '6px',
            border: 'none',
            background: !isPolling ? '#ccc' : '#f44336',
            color: '#fff',
            cursor: !isPolling ? 'default' : 'pointer',
          }}
        >
          폴링 중단
        </button>
      </div>

      {/* 상태 표시 */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
        gap: '12px',
        marginBottom: '20px',
      }}>
        <StatusCard
          label="폴링 상태"
          value={isPolling ? '활성' : '중단'}
          color={isPolling ? '#4CAF50' : '#999'}
        />
        <StatusCard
          label="토큰"
          value={token}
          color="#2196F3"
        />
        <StatusCard
          label="재시도 횟수"
          value={`${retryCount}`}
          color={retryCount > 0 ? '#ff9800' : '#4CAF50'}
        />
        <StatusCard
          label="다음 폴링"
          value={nextPollIn !== null ? `${(nextPollIn / 1000).toFixed(1)}초` : '-'}
          color="#9C27B0"
        />
      </div>

      {/* 대기열 상태 */}
      {status && (
        <div style={{
          padding: '24px',
          borderRadius: '12px',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: '#fff',
          textAlign: 'center',
          marginBottom: '20px',
        }}>
          <div style={{ fontSize: '14px', opacity: 0.8, marginBottom: '8px' }}>내 앞 대기 인원</div>
          <div style={{ fontSize: '48px', fontWeight: 'bold', marginBottom: '8px' }}>
            {status.position.toLocaleString()}
          </div>
          <div style={{ fontSize: '14px', opacity: 0.8, marginBottom: '16px' }}>
            전체 {status.total.toLocaleString()}명 중
          </div>

          {/* 진행 바 */}
          <div style={{
            background: 'rgba(255,255,255,0.2)',
            borderRadius: '8px',
            height: '8px',
            overflow: 'hidden',
          }}>
            <div style={{
              width: `${Math.max(2, ((status.total - status.position) / status.total) * 100)}%`,
              background: '#fff',
              height: '100%',
              borderRadius: '8px',
              transition: 'width 0.5s ease',
            }} />
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '12px', fontSize: '12px', opacity: 0.7 }}>
            <span>예상 대기: ~{Math.ceil(status.position / 50)}분</span>
            <span>서버 TTL: {status.ttl}ms</span>
          </div>
        </div>
      )}

      {/* 에러 표시 */}
      {error && (
        <div style={{
          padding: '12px 16px',
          borderRadius: '8px',
          background: '#ffebee',
          color: '#c62828',
          marginBottom: '20px',
          border: '1px solid #ef9a9a',
        }}>
          에러: {error.message} (재시도 {retryCount}회)
        </div>
      )}

      {/* 학습 포인트 */}
      <div style={{
        padding: '16px',
        borderRadius: '8px',
        background: '#e8f5e9',
        borderLeft: '4px solid #4CAF50',
      }}>
        <h4 style={{ marginBottom: '12px', color: '#333' }}>학습 포인트</h4>
        <ol style={{ margin: 0, paddingLeft: '20px', color: '#555', lineHeight: 2 }}>
          <li><code>calculateFullJitter</code> - Full Jitter = random(0, min(ceiling, base * 2^attempt))</li>
          <li><code>calculateNextPollTime</code> - 서버 TTL ± 20% Jitter</li>
          <li><code>poll</code> - fetch → 파싱 → 다음 폴링 스케줄링</li>
          <li>에러 재시도에 Full Jitter 적용 (고정 3초 대신)</li>
          <li>stop/resume 제어 + cleanup</li>
        </ol>
        <div style={{ marginTop: '12px', padding: '8px 12px', background: '#e3f2fd', borderRadius: '4px', fontSize: '13px', color: '#1565c0' }}>
          핵심 공식: 연결 유지 비용 {'>'} 자주 묻는 비용 → 폴링이 유리한 구간
        </div>
      </div>
    </div>
  );
}

function StatusCard({ label, value, color }: { label: string; value: string; color: string }) {
  return (
    <div style={{
      padding: '12px 16px',
      borderRadius: '8px',
      background: '#fff',
      border: '1px solid #e0e0e0',
    }}>
      <div style={{ fontSize: '12px', color: '#999', marginBottom: '4px' }}>{label}</div>
      <div style={{ fontSize: '16px', fontWeight: 'bold', color }}>{value}</div>
    </div>
  );
}
