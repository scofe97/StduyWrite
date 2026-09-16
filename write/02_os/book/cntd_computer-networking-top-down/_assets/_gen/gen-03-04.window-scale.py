# 03-04 §1 「칸은 그대로 두고 읽는 법을 바꿉니다」 — 윈도우 스케일이 실제로 무엇을 주고받는가.
# 2026-09-16: 의사결정 가지(「어느 쪽을 바꾸나」 다이아몬드 + 두 갈래)를 걷어내고 시퀀스로 다시 그렸다.
#       종전 도식은 무엇을 바꾸느냐만 갈랐을 뿐, 세그먼트가 오가며 배수가 정해지고 그 뒤 같은 칸 값이
#       다르게 읽히는 장면이 없었다. 움직이는 것을 지우면 같은 그림이 남는 비교표였다.
# 담는 흐름은 본문 세 소절의 사실만 쓴다 —
#   연결 수립: SYN 에 배수를 한 번 실어 보내고 SYNACK 로 서버 배수를 받아 양쪽이 기억한다.
#   데이터 구간: Window 칸은 16비트 숫자 그대로이고, 받는 쪽이 그 숫자에 배수를 곱해 읽는다.
#   같은 칸 값 24,576 이 ×1 이면 24,576 byte · ×128 이면 3 MiB (본문 「대가는 정밀도입니다」 문단).
#   대가: 창이 배수 단위로만 표현된다 — RFC 는 이를 granularity 라 부른다 (본문 [^rfc7323-gran]).
# 흐름 밖 주석 한 줄: 헤더 칸을 못 늘리는 이유 (본문 「헤더 칸을 왜 못 늘리나」 · [^rfc9293-hdr]).
# 제목 아래 한 줄이 이 흐름이 필요한 이유를 진다 — 필요한 창 = 대역폭 × RTT 가 16비트 칸을 넘는다.
# 타입 스펙: type-sequence — 참여자 레인 둘 + 시간축 왕복. 메시지는 전부 수평이고 되돌아오는 것은
#       파선 + 채운 마커다. 축약: 스펙의 combined fragment 대신 구분선과 구간 라벨로 두 구간을 가른다
#       (분기가 아니라 앞뒤 구간이라 alt 프레임이 맞지 않는다). 아래 읽기 격자는 시간축 밖의 확대 컷이라
#       레인 밖에 두고, 흐름과는 세로 화살표 하나로만 잇는다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO


def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


class SeqKR(Seq):
    """Seq 가 한글 라벨을 mono 로 찍는 자리를 한글 스택으로 가른다(계약 §프리미티브가 한글을 mono 로)."""

    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}; n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 13, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 12, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 13, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 18, sub, 12, MUTED, _kr(sub))

    def state(s, a, txt, y, c):
        """레인 위의 상태 칩. 파선 레일이 글자를 관통하지 않게 배경을 먼저 깐다."""
        x = s.LX[a]
        w = sum(12.0 if "가" <= ch <= "힣" else 7.0 for ch in str(txt)) + 24
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{PAPER}"/>')
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" '
                   f'fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 5, txt, 12, c, _kr(txt))


W, H = 880, 820
d = SeqKR(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-04 §1",
          "칸은 그대로 두고 읽는 법을 바꿉니다",
          "연결을 세울 때 SYN 과 SYNACK 에 윈도우 스케일 옵션이 한 번 실려 양쪽이 배수를 기억한다. "
          "그 뒤 데이터 구간에서 세그먼트의 Window 칸은 여전히 16비트 숫자 그대로이고, 받는 쪽이 그 "
          "숫자에 기억해 둔 배수를 곱해 읽는다. 같은 칸 값 24,576 이 배수 ×1 에서는 24,576 byte 로, "
          "×128 에서는 3 MiB 로 읽힌다. 대가는 창이 배수 단위로만 표현된다는 것이다.",
          "필요한 창은 대역폭 × RTT 이고 1 Gbps × 30 ms 면 3.75 MB 라 16비트 칸의 64 KiB 를 넘습니다")

LANE_W = 240
d.t(24, 96, "연결 수립 · 배수를 한 번만 주고받음", 13, INK, KR, "start", 600)
d.lanes([("보내는 쪽", "클라이언트"), ("받는 쪽", "서버")], y0=108, lane_w=LANE_W)
d.rails(468)
CX = (d.LX["보내는 쪽"] + d.LX["받는 쪽"]) / 2

d.msg("보내는 쪽", "받는 쪽", "SYN · Window Scale 옵션", 196, INFO, "info",
      sub="내 창에 곱할 배수 · 2 의 거듭제곱 지수")
d.msg("받는 쪽", "보내는 쪽", "SYNACK · Window Scale 옵션", 248, INFO, "info", dash="5 4",
      sub="서버도 자기 배수를 실어 답함")
d.state("보내는 쪽", "배수 ×128 기억", 292, INFO)
d.state("받는 쪽", "배수 ×128 기억", 292, INFO)

d.line(24, 320, W - 24, 320, RULE, 1.0)
d.t(24, 348, "데이터 구간 · 칸은 16비트 숫자 그대로", 13, INK, KR, "start", 600)

d.msg("보내는 쪽", "받는 쪽", "데이터 세그먼트", 384, MUTED, "ar",
      sub="창 안의 미확인 구간만큼만 보냄")
d.msg("받는 쪽", "보내는 쪽", "ACK · Window = 24,576", 440, INFO, "info", dash="5 4",
      sub="칸은 늘지 않음 · 적는 숫자도 그대로")

# ── 시간축 밖의 확대 컷 — 같은 칸 값 하나를 두 배수로 읽는다 ─────────────
d.arrow([(CX, 472), (CX, 504)], MUTED)
d.t(24, 524, "같은 칸 값 하나 · 배수에 따라 다른 창", 13, INK, KR, "start", 600)

C1X, C1W = 24, 248
C2X, C2W = 312, 176
C3X, C3W = 528, 304


def row(y, mul_c, mul, out_c, out, focal=False):
    d.tone(C1X, y, C1W, 48, INFO, 6, "14", 1.2)
    d.t(C1X + C1W / 2, y + 20, "Window 칸", 12, MUTED, KR)
    d.t(C1X + C1W / 2, y + 38, "24,576", 14, INK, MONO, "middle", 600)

    d.arrow([(C1X + C1W, y + 24), (C2X - 8, y + 24)], mul_c, "ok" if mul_c is OK else "ar")
    d.tone(C2X, y, C2W, 48, mul_c, 6, "14", 1.2)
    d.t(C2X + C2W / 2, y + 30, mul, 14, mul_c, MONO, "middle", 600)

    d.arrow([(C2X + C2W, y + 24), (C3X - 8, y + 24)], mul_c, "ok" if mul_c is OK else "ar")
    if focal:
        d.tone(C3X, y, C3W, 48, out_c, 6, "12", 1.4)
    else:
        d.box(C3X, y, C3W, 48, PAPER2, RULE, 1.0)
    d.t(C3X + C3W / 2, y + 20, "받는 쪽이 읽은 창", 12, MUTED, KR)
    d.t(C3X + C3W / 2, y + 38, out, 14, out_c, MONO, "middle", 600)


row(532, MUTED, "배수 ×1", INK, "24,576 byte")
row(592, OK, "배수 ×128", ACC, "3 MiB", focal=True)

d.arrow([(C3X + C3W / 2, 640), (C3X + C3W / 2, 668)], WARN, "warn")
d.tone(C3X, 670, C3W, 42, WARN, 6, "14", 1.2)
d.t(C3X + C3W / 2, 688, "대가 · 창은 128 byte 단위로만", 12, INK, KR)
d.t(C3X + C3W / 2, 705, "granularity", 12, MUTED, MONO)

d.t(24, 736, "흐름 밖 · 헤더 칸 확장은 막힌 길 · 뒤의 Checksum · Urgent Pointer 가 밀려 옛 구현이 깨짐",
     12, MUTED, KR, "start")

d.legend(756, [("배수와 창 값이 실리는 자리", INFO), ("배수를 곱해 읽음", OK),
               ("128배로 읽은 창", ACC), ("대가 · 표현 단위", WARN)])
d.save("03-04.window-scale.svg")
print("ok 03-04.window-scale")
