# 사실 출처: gosuda/portal-tunnel 0a3b9c06 · portal/transport/reverse_framing.go:14-19,23,64,74 · portal/server.go:37,680,1037,1045 · sdk/listener.go:636,670 · portal/lease.go:33
# 타입 스펙: type-sequence
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 620
s = Seq(
    W, H,
    "SEQUENCE · REVERSE CONNECTION FRAMING & MARKERS",
    "단일 리버스 연결의 시간선 — 하트비트·0x02 활성화 마커·데이터 패스스루",
    "유휴 중에는 15초마다 0x00 하트비트가 전송되고, 공개 요청 인입 시 0x02 마커와 16바이트 바인딩으로 즉시 활성화됩니다",
    "시간축: 하이잭 대기 → 15초 주기 하트비트 → 인그레스 인입 → 0x02 바인딩 활성화 → 양방향 스트림"
)

# 3개 레인 정의 (중앙 집중 배치로 우측 selfmsg 여백 확보)
# s.lanes 오버라이드 대신 직접 계산
LANES = [
    ("외부 클라이언트", "Browser / Client", 140),
    ("릴레이 서버", "Relay (ReversePool)", 460),
    ("터널 에이전트", "Tunnel SDK (ReadStart)", 740)
]

s.LX = {}
lane_w = 210
y0 = 104
for nm, sub, x in LANES:
    s.LX[nm] = x
    s.box(x - lane_w // 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
    s.t(x, y0 + 20, nm, 12, INK, KR, "middle", 600)
    s.t(x, y0 + 37, sub, 11, MUTED, MONO)
s.lane_top = y0 + 44
s.rails(554)

# 단계 1: 사전 리버스 연결 개설 및 하이잭
s.msg("터널 에이전트", "릴레이 서버", "GET /sdk/connect (Upgrade: raw)", 180, INFO, "info", sub="사전 아웃바운드 연결 개설")
s.msg("릴레이 서버", "터널 에이전트", "101 Switching Protocols", 222, INFO, "info", sub="소켓 하이잭 및 풀 등록")
s.state("릴레이 서버", "ReversePool 대기", 260, OK)
s.state("터널 에이전트", "ReadStart() 대기", 260, OK)

# 단계 2: 유휴 유지 (15초 주기 0x00 keepalive)
s.msg("릴레이 서버", "터널 에이전트", "0x00 (markerKeepalive)", 302, OK, "ok", sub="15초 주기 반복 · NAT 매핑 유지")
s.selfmsg("터널 에이전트", "drop 0x00 & continue", 336, OK, sub="ReadStart 루프에서 소비 후 대기 지속")

# 단계 3: 공개 요청 인입 및 클레임
s.msg("외부 클라이언트", "릴레이 서버", "TLS ClientHello (SNI)", 380, ACC, "acc", sub="인그레스 도착 · ClaimTimeout 10s")
s.selfmsg("릴레이 서버", "Acquire() & close(stop)", 414, ACC, sub="대기열 선두 추출 · 하트비트 중단")

# 단계 4: 활성화 프레임 송신 (0x02 vs 0x01)
s.msg("릴레이 서버", "터널 에이전트", "0x02 (markerTLSStart) + binding(16B)", 456, ACC, "acc", sub="TLS 활성화 및 바인딩 전달 (Raw: 0x01)")
s.selfmsg("터널 에이전트", "Keyless TLS 종단 준비", 490, ACC, sub="ReadStart 반환 · 로컬 TLS 종단")

# 단계 5: 양방향 투명 스트림 패스스루
s.msg("외부 클라이언트", "터널 에이전트", "양방향 암호화 스트림 (s.proxy.bridge)", 532, OK, "ok", sub="투명 바이트 중계 · E2E 암호화 유지")

# 범례
s.legend(H - 42, [
    ("연결 개설·전환", INFO),
    ("유휴 하트비트·중계", OK),
    ("클레임·활성화 마커", ACC)
])

out_path = Path(__file__).parent.parent / "01-04-markers.svg"
s.save(str(out_path))
print(f"saved: {out_path}")
