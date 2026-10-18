# 타입 스펙: type-state — 단일 리버스 연결의 상태(HTTP 요청 · Hijack · 대기 Ready · Claim · 패스스루 · 종료).
# 사실 출처: docs/src/routes/architecture/+page.md Control Plane Flow §2,
#   docs/maintainer/architecture.md TCP bridge ownership 마지막 문단,
#   portal/api_server.go:518,558~577, portal/transport/reverse_framing.go:16,64,
#   sdk/listener.go:37 defaultReadyTarget = 2.
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

W, H = 1000, 560
d = D(W, H, "PORTAL-TUNNEL · REVERSE CONNECTION STATE MACHINE",
      "단일 리버스 연결의 상태 전이 — 요청·하이잭·대기·클레임·패스스루·종료",
      "터널이 HTTP/1.1 업그레이드로 리버스 연결을 맺고 소켓을 하이잭해 대기 풀(ready)에 넣습니다. 인그레스에 SNI 요청이 도착하면 0x02 바인딩으로 클레임해 패스스루로 전환하고, 스트림 완료나 unregister 시 종료됩니다.",
      "사전 대기 풀에서 클레임되어 테넌트 암호문 패스스루로 전이합니다")

# 박스 배치 파라미터 (BW=136으로 줄여 간격 56px 확보)
Y1 = 156
BH1 = 128
BW = 136

# 5개 상단 상태 x 좌표 (간격 56px)
XS = [40, 232, 424, 616, 808]

STATES_ROW1 = [
    ("HTTP 요청", INFO, [
        ("GET /sdk/connect", 11, MONO),
        ("HTTP/1.1 전용", 11, KR),
        ("Capability 헤더", 11, KR)
    ]),
    ("Hijack", INFO, [
        ("101 Switching", 11, MONO),
        ("Upgrade: raw", 11, MONO),
        ("소켓 제어권 전환", 11, KR)
    ]),
    ("대기 (Ready)", OK, [
        ("ready=2 풀 유지", 11, KR),
        ("0x00 keepalive", 11, MONO),
        ("클레임 대기", 11, KR)
    ]),
    ("Claim", ACC, [
        ("0x02 바인딩 수신", 11, KR),
        ("16B 세션 식별자", 11, KR),
        ("풀에서 즉시 인출", 11, KR)
    ]),
    ("패스스루", OK, [
        ("테넌트 TLS 중계", 11, KR),
        ("양방향 원시 바이트", 11, KR),
        ("E2E 암호화 유지", 11, KR)
    ]),
]

for x, (title, color, lines) in zip(XS, STATES_ROW1):
    d.tone(x, Y1, BW, BH1, color, 8, "16", 1.3)
    d.t(x + BW // 2, Y1 + 26, title, 14, color, KR, "middle", 600)
    for i, (txt, sz, fam) in enumerate(lines):
        d.t(x + BW // 2, Y1 + 54 + i * 22, txt, sz, INK if i == 0 else MUTED, fam, "middle")

# 시작 점
START_X = 12
MY1 = Y1 + BH1 // 2
d.o.append(f'<circle cx="{START_X}" cy="{MY1}" r="6" fill="{INK}"/>')
d.path(f"M {START_X + 6} {MY1} L {XS[0] - 2} {MY1}", MUTED, 1.4, m="ar")

# 상단 상태 간 전이 화살표 및 텍스트 라벨
TR_LABELS = [
    "101 전환",
    "풀 등록",
    "SNI 도착",
    "0x02 전달"
]

for i in range(4):
    x_from = XS[i] + BW
    x_to = XS[i+1]
    mid_x = (x_from + x_to) // 2
    d.path(f"M {x_from} {MY1} L {x_to - 2} {MY1}", MUTED, 1.4, m="ar")
    d.t(mid_x, MY1 - 10, TR_LABELS[i], 10, INK, KR, "middle")

# 대기 상태 상단 self-loop: 0x00 keepalive
LOOP_X = XS[2] + BW // 2
d.path(f"M {LOOP_X - 28} {Y1} C {LOOP_X - 28} {Y1 - 28}, {LOOP_X + 28} {Y1 - 28}, {LOOP_X + 28} {Y1 - 2}", MUTED, 1.3, m="ar")
d.t(LOOP_X, Y1 - 32, "0x00 keepalive", 10, MUTED, MONO, "middle")

# 하단 종료/취소 상태
Y2 = 368
BH2 = 100
BW2 = 196
X2 = 394

d.tone(X2, Y2, BW2, BH2, BAD, 8, "16", 1.3)
d.t(X2 + BW2 // 2, Y2 + 30, "종료 / 취소", 14, BAD, KR, "middle", 600)
d.t(X2 + BW2 // 2, Y2 + 58, "소켓 닫힘 (Close)", 11, INK, KR, "middle")
d.t(X2 + BW2 // 2, Y2 + 80, "자원 회수 및 정리", 11, MUTED, KR, "middle")

# 대기 상태 -> 종료/취소 (unregister 또는 만료)
d.path(f"M {XS[2] + BW // 2} {Y1 + BH1} L {XS[2] + BW // 2} {Y2 - 2}", BAD, 1.3, m="bad", dash="4 3")
d.t(XS[2] + BW // 2 + 72, (Y1 + BH1 + Y2) // 2 + 4, "unregister / 만료", 11, BAD, KR, "middle")

# 패스스루 -> 종료/취소 (스트림 완료)
PASS_MID_X = XS[4] + BW // 2
d.path(f"M {PASS_MID_X} {Y1 + BH1} L {PASS_MID_X} {Y2 + BH2 // 2} L {X2 + BW2 + 2} {Y2 + BH2 // 2}", MUTED, 1.3, m="ar")
d.t(PASS_MID_X - 70, Y2 + BH2 // 2 - 10, "스트림 완료 (FIN/EOF)", 11, MUTED, KR, "middle")

# 종료 상태 -> 종료 고리 (End Dot)
END_X = 280
MY2 = Y2 + BH2 // 2
d.path(f"M {X2} {MY2} L {END_X + 10} {MY2}", MUTED, 1.3, m="ar")
d.o.append(f'<circle cx="{END_X}" cy="{MY2}" r="8" fill="none" stroke="{INK}" stroke-width="1.4"/>')
d.o.append(f'<circle cx="{END_X}" cy="{MY2}" r="5" fill="{INK}"/>')
d.t(END_X - 32, MY2 + 4, "완료", 11, MUTED, KR, "middle")

d.legend(H - 48, [
    ("정상 스트림·대기", OK),
    ("클레임·활성화", ACC),
    ("연결 수립·전환", INFO),
    ("종료·취소", BAD)
])

out_path = _HERE.parent / "01-03-reverse-connect.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
