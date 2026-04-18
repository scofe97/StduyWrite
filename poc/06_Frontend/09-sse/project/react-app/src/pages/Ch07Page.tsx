export function Ch07Page() {
  return (
    <div style={{ padding: '32px', maxWidth: '800px' }}>
      <h2 style={{ fontSize: '24px', marginBottom: '8px', color: '#1a1a2e' }}>
        Ch07: WebSocket vs SSE 비교
      </h2>
      <span style={{
        display: 'inline-block',
        padding: '2px 8px',
        borderRadius: '4px',
        background: '#e3f2fd',
        color: '#1565c0',
        fontSize: '12px',
        marginBottom: '24px',
      }}>
        이론 챕터 (실습 없음)
      </span>

      <p style={{ color: '#666', lineHeight: 1.8, marginBottom: '24px' }}>
        이 챕터는 SSE와 WebSocket의 기술적 차이를 비교하는 이론 챕터입니다.
        별도의 코드 실습 없이 <code>LEARN.md</code>를 참고하세요.
      </p>

      {/* 핵심 비교표 */}
      <div style={{ marginBottom: '24px' }}>
        <h3 style={{ fontSize: '18px', marginBottom: '12px' }}>핵심 비교</h3>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px' }}>
          <thead>
            <tr style={{ background: '#f5f5f5' }}>
              <th style={thStyle}>항목</th>
              <th style={{ ...thStyle, color: '#4CAF50' }}>SSE</th>
              <th style={{ ...thStyle, color: '#2196F3' }}>WebSocket</th>
            </tr>
          </thead>
          <tbody>
            {comparisons.map(([item, sse, ws], i) => (
              <tr key={i}>
                <td style={tdStyle}><strong>{item}</strong></td>
                <td style={tdStyle}>{sse}</td>
                <td style={tdStyle}>{ws}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* 선택 가이드 */}
      <div style={{
        padding: '20px',
        borderRadius: '8px',
        background: '#fff',
        border: '1px solid #e0e0e0',
        marginBottom: '24px',
      }}>
        <h3 style={{ fontSize: '18px', marginBottom: '12px' }}>선택 가이드</h3>
        <div style={{ display: 'grid', gap: '12px' }}>
          <GuideCard
            color="#4CAF50"
            title="SSE 선택"
            items={[
              '서버 → 클라이언트 푸시만 필요',
              '자동 재연결이 중요',
              '기업 환경 방화벽 통과 필요',
              '빠른 구현 필요',
            ]}
          />
          <GuideCard
            color="#2196F3"
            title="WebSocket 선택"
            items={[
              '양방향 실시간 통신 필수 (채팅, 게임)',
              '바이너리 데이터 전송 필요',
              '빈번한 양방향 메시지',
            ]}
          />
          <GuideCard
            color="#ff9800"
            title="SSE + REST API (권장)"
            items={[
              '80%의 실시간 요구사항 커버',
              '서버 푸시(SSE) + 클라이언트 액션(REST)',
              'ChatGPT, GitHub Actions, Stripe가 이 패턴',
            ]}
          />
        </div>
      </div>

      {/* 실제 서비스 사례 */}
      <div style={{
        padding: '20px',
        borderRadius: '8px',
        background: '#fff',
        border: '1px solid #e0e0e0',
      }}>
        <h3 style={{ fontSize: '18px', marginBottom: '12px' }}>실제 서비스의 기술 선택</h3>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px' }}>
          <thead>
            <tr style={{ background: '#f5f5f5' }}>
              <th style={thStyle}>서비스</th>
              <th style={thStyle}>기술</th>
              <th style={thStyle}>이유</th>
            </tr>
          </thead>
          <tbody>
            {services.map(([service, tech, reason], i) => (
              <tr key={i}>
                <td style={tdStyle}><strong>{service}</strong></td>
                <td style={{ ...tdStyle, color: tech === 'SSE' ? '#4CAF50' : '#2196F3' }}>{tech}</td>
                <td style={tdStyle}>{reason}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const thStyle: React.CSSProperties = {
  padding: '10px 12px',
  textAlign: 'left',
  borderBottom: '2px solid #e0e0e0',
};

const tdStyle: React.CSSProperties = {
  padding: '8px 12px',
  borderBottom: '1px solid #f0f0f0',
};

const comparisons: [string, string, string][] = [
  ['통신 방향', '단방향 (서버→클라이언트)', '양방향 (Full-Duplex)'],
  ['프로토콜', 'HTTP/HTTPS', 'ws:// / wss://'],
  ['데이터 형식', 'UTF-8 텍스트만', '텍스트 + 바이너리'],
  ['재연결', '자동 (브라우저 내장)', '수동 구현 필요'],
  ['연결 제한', '도메인당 6개 (HTTP/1.1)', '제한 거의 없음'],
  ['방화벽 통과', '쉬움 (표준 HTTP)', '어려울 수 있음'],
  ['구현 복잡도', '낮음', '높음'],
];

const services: [string, string, string][] = [
  ['ChatGPT / Claude', 'SSE', '응답 스트리밍이 단방향'],
  ['Slack / Discord', 'WebSocket', '양방향 채팅 + 바이너리'],
  ['GitHub Actions', 'SSE', '로그 스트리밍이 단방향'],
  ['Figma / Google Docs', 'WebSocket', '협업 편집, 양방향 동기화'],
  ['Stripe Dashboard', 'SSE', '결제 이벤트 알림이 단방향'],
];

function GuideCard({ color, title, items }: { color: string; title: string; items: string[] }) {
  return (
    <div style={{
      padding: '12px 16px',
      borderLeft: `4px solid ${color}`,
      background: '#fafafa',
      borderRadius: '0 4px 4px 0',
    }}>
      <strong style={{ color }}>{title}</strong>
      <ul style={{ margin: '8px 0 0', paddingLeft: '20px', color: '#555', lineHeight: 1.8, fontSize: '13px' }}>
        {items.map((item, i) => <li key={i}>{item}</li>)}
      </ul>
    </div>
  );
}
