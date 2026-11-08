# 타입 스펙: type-architecture
# 사실 출처: RFC 4254 §5·§7.1·§7.2, 2026-11-07 재현 (ssh -R 하나, 동시 요청 3건, 클라이언트 채널 0·1·2 ↔ 서버 쪽 2·3·4, 서버 0·1 은 수신 소켓)
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

W, H = 984, 450
PY, PH = 100, 270

def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO

d = D(W, H, "ARCHITECTURE · 09-01 REMOTE CHANNELS",
      "ssh -R 한 줄이 만드는 연결 1개와 채널 3개",
      "공개 서버에서는 요청 3건이 수신 포트 하나로 들어옵니다. 세 요청은 SSH 연결 1개 위의 forwarded-tcpip 채널 0·1·2 로 나뉘어 "
      "NAT 뒤 안쪽 장비의 ssh 클라이언트로 갑니다. 클라이언트는 안쪽 서비스에 연결 3개를 따로 맺습니다. 채널 번호는 클라이언트 쪽 0·1·2, 서버 쪽 2·3·4 입니다.",
      lead="채널 번호는 양 끝이 따로 매겨서 안쪽 번호 0·1·2 가 서버 쪽 2·3·4 와 짝을 이룹니다.")

# 양쪽 패널
d.box(24, PY, 300, PH)
d.t(174, PY + 24, "공개 서버", 13, INK, KR, "middle", 600)
d.box(660, PY, 300, PH)
d.t(810, PY + 24, "NAT 뒤 안쪽 장비", 13, INK, KR, "middle", 600)

# 서버 쪽: 요청 3건 → 수신 포트
for k in range(3):
    y = 150 + k * 66
    d.box(40, y, 104, 44)
    d.t(92, y + 19, "요청 %d" % (k + 1), 12, INK, KR, "middle", 600)
    d.t(92, y + 35, "curl", 11, MUTED, MONO, "middle")
    ty = 214 + k * 24
    d.arrow([(146, y + 22), (166, y + 22), (166, ty), (186, ty)], SOFT, "soft", 1.2)
d.tone(188, 198, 124, 80, INFO, 6, "14", 1.1)
d.t(250, 229, "수신 포트", 13, INFO, KR, "middle", 600)
d.t(250, 249, "127.0.0.1:2222", 11, MUTED, MONO, "middle")

# 가운데: SSH 연결 1개
d.tone(324, 160, 336, 150, OK, 6, "10", 1.1)
d.t(492, 182, "SSH 연결 1개 (TCP 연결 1개)", 12, OK, KR, "middle", 600)
for k in range(3):
    y = 220 + k * 30
    d.arrow([(316, y), (672, y)], ACC, "acc", 1.4)
    d.t(492, y - 7, "채널 %d (서버 쪽 %d)" % (k, k + 2), 11, ACC, KR, "middle", 600)

# 안쪽 장비: ssh 클라이언트 → 서비스 3 연결
d.tone(676, 195, 112, 100, OK, 6, "14", 1.1)
d.t(732, 238, "ssh 클라이언트", 13, OK, KR, "middle", 600)
d.t(732, 258, "프로세스 1개", 11, MUTED, KR, "middle")
d.tone(836, 195, 108, 100, ACC, 6, "14", 1.1)
d.t(890, 238, "안쪽 서비스", 13, ACC, KR, "middle", 600)
d.t(890, 258, "127.0.0.1:18099", 11, MUTED, MONO, "middle")
for k in range(3):
    y = 221 + k * 24
    d.arrow([(790, y), (832, y)], SOFT, "soft", 1.2)
d.t(812, 316, "연결 3개", 11, MUTED, KR, "middle", 600)

d.t(492, 304, "서버 쪽 0·1 번은 수신 소켓이 차지", 11, MUTED, KR, "middle")

d.legend(390, [("수신 지점", INFO), ("SSH 연결", OK), ("채널·목적지", ACC)])
svg_path = pathlib.Path(__file__).resolve().parent.parent / "09-01.reverse-channels.svg"
d.save(str(svg_path))
print("ok 09-01 reverse-channels")
