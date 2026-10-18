# 사실 출처: gosuda/portal-tunnel 0a3b9c06 · sdk/expose.go:90,125,254,285,999,1247 · sdk/listener.go:37,178,256,564,636,979 · sdk/proxy.go:21,30,41,135 · sdk/http.go:23,24,25,34
# 타입 스펙: type-data-flow
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1040, 560
d = D(
    W, H,
    "DATA FLOW · MULTI-RELAY EXPOSURE",
    "다중 릴레이 통합 및 로컬 전달",
    "릴레이 리스너 스트림이 Exposure 버퍼로 수렴해 Accept로 전달",
    lead="Relay A·B·C → listener → accepted 채널(명시 3개 시 12) → Accept() → RunHTTP / Proxy"
)

# 배경 구획 (Zone)
def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(245,245,245,0.02)" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="4 4"/>')
    d.t(x + 14, y + 20, label, 11, SOFT, KR, "start", 600)

zone(16, 96, 170, 366, "외부 릴레이")
zone(202, 96, 276, 366, "SDK 리스너 (listener.go)")
zone(494, 96, 230, 366, "통합 계층 (expose.go)")
zone(740, 96, 284, 366, "앱 및 로컬 프록시")

# 1. 외부 릴레이 (Relay A, B, C)
RY = [140, 260, 380]
RELAYS = [("Relay A", "relay-a.net"), ("Relay B", "relay-b.net"), ("Relay C", "relay-c.net")]

for i, (name, host) in enumerate(RELAYS):
    y = RY[i]
    d.tone(28, y, 146, 72, INFO, 6, "12", 1.1)
    d.t(38, y + 26, name, 12, INFO, KR, "start", 600)
    d.t(38, y + 46, host, 10, INK, MONO, "start")
    d.t(38, y + 62, "0x02 바인딩", 9.5, MUTED, KR, "start")

# 2. SDK 내부 listener (A, B, C)
for i in range(3):
    y = RY[i]
    d.box(214, y, 252, 72, PAPER2, RULE, 1.0)
    d.t(226, y + 22, f"listener {chr(65+i)}", 11, INK, MONO, "start", 600)
    d.t(370, y + 22, "TTL 120s (-30s)", 9.5, MUTED, KR, "start")
    
    # 2개 리버스 슬롯 칩
    d.tone(226, y + 36, 110, 26, OK, 4, "18", 0.9)
    d.t(281, y + 52, "슬롯 1 (ready)", 9.5, OK, KR, "middle")
    d.tone(344, y + 36, 110, 26, OK, 4, "18", 0.9)
    d.t(399, y + 52, "슬롯 2 (ready)", 9.5, OK, KR, "middle")

    # 릴레이 -> 리스너 화살표
    d.arrow([(174, y + 36), (214, y + 36)], INFO, "info", 1.2)

# 3. 통합 채널 (Exposure.accepted)
CHAN_X, CHAN_Y, CHAN_W, CHAN_H = 508, 140, 202, 192
d.tone(CHAN_X, CHAN_Y, CHAN_W, CHAN_H, ACC, 6, "10", 1.2)
d.t(CHAN_X + 16, CHAN_Y + 28, "accepted 채널 (:285)", 12, ACC, KR, "start", 600)
d.t(CHAN_X + 16, CHAN_Y + 48, "chan net.Conn (버퍼 12)", 10.5, INK, MONO, "start")
d.t(CHAN_X + 16, CHAN_Y + 66, "명시 릴레이 3개 기준", 9.5, MUTED, KR, "start")

# 슬롯 큐 시각화
for idx in range(4):
    bx = CHAN_X + 16 + idx * 42
    by = CHAN_Y + 84
    if idx < 3:
        d.tone(bx, by, 36, 28, ACC, 3, "24", 1.0)
        d.t(bx + 18, by + 18, f"C{idx+1}", 9.5, INK, MONO, "middle")
    else:
        d.box(bx, by, 36, 28, PAPER, RULE, 0.8)
        d.t(bx + 18, by + 18, "...", 9.5, MUTED, MONO, "middle")

d.t(CHAN_X + 16, CHAN_Y + 134, "runListenerAcceptLoop", 9.5, INK, MONO, "start")
d.t(CHAN_X + 16, CHAN_Y + 152, "listener 연결 수집", 9.5, MUTED, KR, "start")
d.t(CHAN_X + 16, CHAN_Y + 172, "stateChanged 대기", 9.5, SOFT, KR, "start")

# 리스너들 -> accepted 채널 화살표
d.arrow([(466, 176), (508, 176)], OK, "ok", 1.2)
d.arrow([(466, 296), (488, 296), (488, 236), (508, 236)], OK, "ok", 1.2)
d.arrow([(466, 416), (488, 416), (488, 266), (508, 266)], OK, "ok", 1.2)

# Exposure.Accept() 메서드 상자
ACCEPT_X, ACCEPT_Y, ACCEPT_W, ACCEPT_H = 508, 364, 202, 88
d.box(ACCEPT_X, ACCEPT_Y, ACCEPT_W, ACCEPT_H, PAPER2, RULE, 1.0)
d.t(ACCEPT_X + 16, ACCEPT_Y + 28, "Exposure.Accept() (:999)", 11.5, INK, MONO, "start", 600)
d.t(ACCEPT_X + 16, ACCEPT_Y + 50, "wrapAccepted", 10, MUTED, MONO, "start")
d.t(ACCEPT_X + 16, ACCEPT_Y + 70, "net.Listener 반환", 9.5, OK, KR, "start")

# accepted -> Accept()
d.arrow([(CHAN_X + 101, CHAN_Y + CHAN_H), (CHAN_X + 101, ACCEPT_Y)], ACC, "acc", 1.2)

# 4. 앱 핸들러 및 프록시 (상단: RunHTTP, 하단: Proxy)
APP_X, HTTP_Y = 756, 140
d.tone(APP_X, HTTP_Y, 252, 130, OK, 6, "12", 1.1)
d.t(APP_X + 16, HTTP_Y + 26, "인프로세스 HTTP", 12, OK, KR, "start", 600)
d.t(APP_X + 16, HTTP_Y + 48, "sdk.RunHTTP (:34)", 10.5, INK, MONO, "start")
d.t(APP_X + 16, HTTP_Y + 68, "X-Forwarded-Proto: https", 9.5, MUTED, KR, "start")
d.t(APP_X + 16, HTTP_Y + 88, "http.HandlerFunc 처리", 9.5, MUTED, KR, "start")
d.t(APP_X + 16, HTTP_Y + 108, "TLS 종단 평문 스트림", 9.5, INFO, KR, "start")

PROXY_Y = 300
d.box(APP_X, PROXY_Y, 252, 152, PAPER2, RULE, 1.0)
d.t(APP_X + 16, PROXY_Y + 26, "로컬 포트 프록시", 12, INK, KR, "start", 600)
d.t(APP_X + 16, PROXY_Y + 48, "sdk.Proxy (:30)", 10.5, INK, MONO, "start")
d.t(APP_X + 16, PROXY_Y + 70, "maxTCPConnections=128", 9.5, WARN, KR, "start")
d.t(APP_X + 16, PROXY_Y + 92, "초과 시 즉시 Close", 9.5, BAD, KR, "start")

# 로컬 대상 칩
d.tone(APP_X + 16, PROXY_Y + 108, 220, 30, INFO, 4, "16", 1.0)
d.t(APP_X + 126, PROXY_Y + 128, "127.0.0.1:3000", 10, INFO, MONO, "middle")

# Accept() -> RunHTTP / Proxy 화살표 분기
d.arrow([(ACCEPT_X + ACCEPT_W, ACCEPT_Y + 24), (APP_X, HTTP_Y + 65)], OK, "ok", 1.2)
d.arrow([(ACCEPT_X + ACCEPT_W, ACCEPT_Y + 48), (APP_X, PROXY_Y + 65)], MUTED, "ar", 1.2)

# 범례
d.legend(480, [
    ("인그레스", INFO),
    ("리버스 슬롯", OK),
    ("통합 큐", ACC),
    ("워커 제한", WARN)
])

out_path = Path(__file__).parent.parent / "04-01-exposure.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
