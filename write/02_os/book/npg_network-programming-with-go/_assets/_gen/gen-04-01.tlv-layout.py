# 타입 스펙: type-flowchart
# 04-01 TLV 디코딩 흐름과 바이트 소비 과정
# 사실 출처: NPG Ch.4 Listing 4-9 (Decode), Listing 4-7·4-8 ("hello world" 16B)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 880, 520
d = D(W, H, "LISTING 4-4 TLV DECODING",
      "TLV 디코딩과 바이트 소비",
      "Listing 4-9 디코딩 분기와 단계별 바이트 스트림 소비 흐름",
      "헤더 판독·크기 검증·페이로드 수신")

def draw_ribbon(x, y, t_col, l_col, v_col):
    d.tone(x, y, 48, 28, t_col, op="20", sw=1.0)
    d.t(x + 24, y + 18, "T:2", 9, t_col, MONO, "middle")
    d.tone(x + 54, y, 64, 28, l_col, op="20", sw=1.0)
    d.t(x + 86, y + 18, "L:11", 9, l_col, MONO, "middle")
    d.tone(x + 124, y, 160, 28, v_col, op="20", sw=1.0)
    d.t(x + 204, y + 18, "hello world", 9, v_col, MONO, "middle")

# 1. 시작 (Oval)
d.box(40, 104, 160, 36, fill=PAPER2, stroke=INFO, r=18)
d.t(120, 126, "수신 대기", 12, INFO, KR, "middle", 600)
draw_ribbon(300, 108, MUTED, MUTED, MUTED)
d.t(610, 126, "16B 스트림", 11, MUTED, KR, "start")

d.arrow([(120, 140), (120, 172)], MUTED, "ar", 1.4)

# 2. 타입 판독 (Rect)
d.box(40, 172, 160, 44, fill=PAPER2, stroke=RULE)
d.t(120, 192, "타입 1B 판독", 12, INK, KR, "middle", 600)
d.t(120, 208, "binary.Read", 10, MUTED, MONO, "middle")
draw_ribbon(300, 180, ACC, MUTED, MUTED)
d.t(610, 198, "1B 소비", 11, ACC, KR, "start")

d.arrow([(120, 216), (120, 248)], MUTED, "ar", 1.4)

# 3. 길이 판독 (Rect)
d.box(40, 248, 160, 44, fill=PAPER2, stroke=RULE)
d.t(120, 268, "길이 4B 판독", 12, INK, KR, "middle", 600)
d.t(120, 284, "BigEndian uint32", 10, MUTED, MONO, "middle")
draw_ribbon(300, 256, ACC, ACC, MUTED)
d.t(610, 274, "5B 소비", 11, ACC, KR, "start")

d.arrow([(120, 292), (120, 324)], MUTED, "ar", 1.4)

# 4. 크기 검증 (Diamond)
pts = f"{120},{324} {210},{350} {120},{376} {30},{350}"
d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="{WARN}" stroke-width="1.2"/>')
d.t(120, 354, "길이 > 10MB ?", 11, WARN, KR, "middle", 600)

# 분기 1: 초과 (오른쪽 화살표)
d.arrow([(210, 350), (284, 350)], BAD, "bad", 1.4)
d.t(248, 342, "초과", 11, BAD, KR, "middle")
d.box(284, 330, 140, 40, fill=PAPER2, stroke=BAD, r=20)
d.t(354, 347, "ErrMax-", 10, BAD, MONO, "middle")
d.t(354, 361, "PayloadSize", 10, BAD, MONO, "middle")

# 분기 2: 정상 (아래쪽 화살표)
d.arrow([(120, 376), (120, 412)], OK, "ok", 1.4)
d.t(150, 396, "정상", 11, OK, KR, "middle")

# 5. 페이로드 판독 (Rect)
d.box(40, 412, 160, 44, fill=PAPER2, stroke=RULE)
d.t(120, 432, "값 11B 판독", 12, INK, KR, "middle", 600)
d.t(120, 448, "r.Read", 10, MUTED, MONO, "middle")
draw_ribbon(300, 420, ACC, ACC, OK)

# 완료 화살표 -> 최종 결과
d.arrow([(594, 434), (640, 434)], OK, "ok", 1.4)
d.box(640, 416, 140, 36, fill=PAPER2, stroke=OK, r=18)
d.t(710, 438, "복원 완료", 11, OK, KR, "middle", 600)

d.legend(H - 46, [("소비 헤더", ACC), ("복원 페이로드", OK), ("오류 분기", BAD), ("미수신 바이트", MUTED)])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "04-01.tlv-layout.svg"))
d.save(out_path)
print(f"Generated: {out_path}")
