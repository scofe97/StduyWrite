# 타입 스펙: type-sequence — 주체 사이의 시간순 메시지. 기기가 5G 망을 발견하고 붙기까지의 왕복.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.3.4 Figure 7.36 —
#   PSS·SSS·MIB·SIB1 의 순서와 5 msec · 80 ms · 중앙 127 부반송파는 원문 수치 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import Seq, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, WARN, KR, MONO


def kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    """Seq 프리미티브가 라벨 font 를 MONO 로 고정하므로 한글만 KR 로 돌려 씁니다."""

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dx = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dx} {y} L {x2 - 12 * dx} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 11, c, kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 11, MUTED, KR)

    def state(s, a, txt, y, c):
        x = s.LX[a]
        w = len(txt) * (11.0 if any("가" <= ch <= "힣" for ch in txt) else 7.0) + 18
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" '
                   f'fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 11, c, kr(txt))


W, H = 940, 700
d = SeqKR(W, H, "SECTION 7.3.4 · ATTACHING TO A 5G NETWORK",
          "비콘 하나로 끝나는 WiFi 와 달리 여러 걸음을 밟습니다",
          "기기는 동기 신호로 시계를 맞추고, 방송 블록으로 망의 성격을 읽은 뒤에야 연결을 요청한다.",
          "메시지 이름과 주기는 원문 §7.3.4 의 것입니다")

d.lanes([("무선 기기", "user device"), ("기지국", "base station")], y0=104, lane_w=280)
d.rails(420)

d.msg("기지국", "무선 기기", "PSS", 164, INFO, "info",
      sub="5 msec 마다 · 채널 중앙 127 부반송파 · 시계를 맞춥니다")
d.msg("기지국", "무선 기기", "SSS", 216, INFO, "info", sub="초기 망 식별자를 줍니다")
d.msg("기지국", "무선 기기", "MIB", 262, INFO, "info", sub="부반송파 간격과 접속 개방 여부")
d.msg("기지국", "무선 기기", "SIB1", 312, ACC, "acc",
      sub="80 ms 마다 · 사업자 코드 · 기지국 식별자 · 최소 수신 레벨")
d.msg("무선 기기", "기지국", "RRC setup request", 362, OK, "ok",
      sub="상향 임의 접속 채널로 보냅니다")
d.msg("기지국", "무선 기기", "RRC setup response", 412, OK, "ok")
d.state("무선 기기", "아직 5G 망에 가입한 것은 아닙니다", 452, WARN)

NY = 490
d.box(24, NY, 430, 108, PAPER2, RULE, 1.0)
d.t(44, NY + 26, "WiFi 는 세 걸음입니다", 12, INK, KR, "start", 600)
for i, ln in enumerate([
    "비콘을 수동으로 훑어 AP 를 고릅니다.",
    "연관 요청과 응답을 주고받습니다.",
    "DHCP 로 서브넷의 IP 주소를 받습니다.",
]):
    d.t(44, NY + 52 + i * 20, "·  " + ln, 11, MUTED, KR, "start")

d.box(474, NY, 430, 108, PAPER2, RULE, 1.0)
d.t(494, NY + 26, "5G 는 여기서 끝이 아닙니다", 12, INK, KR, "start", 600)
for i, ln in enumerate([
    "아직 신원을 밝히지도 인증하지도 않았고,",
    "IP 주소도 없습니다.",
    "코어망과의 등록이 남아 있습니다.",
]):
    d.t(494, NY + 52 + i * 20, "·  " + ln, 11, MUTED, KR, "start")

d.legend(632, [("방송되는 신호", INFO), ("가장 중요한 방송 블록", ACC),
               ("기기가 여는 연결", OK), ("아직 남은 일", WARN)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-04.attach-5g.svg"
d.save(out)
print("→", out)
