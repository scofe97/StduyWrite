# 타입 스펙: type-swimlane
# 04-01 세 가지 메시지 프레이밍 방식 비교 (고정 버퍼 · 구분자 Scanner · TLV)
# 사실 출처: NPG Ch.4 Listing 4-1 (16MB 페이로드 · 512KB 버퍼), Listing 4-2·4-3 (ScanWords 단어 토큰), Listing 4-4·4-7 (StringType 2 · L:11 · hello world)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 880, 480
d = D(W, H, "LISTING 4-1 FRAMING",
      "세 가지 메시지 프레이밍",
      "경계 없는 TCP 바이트 스트림을 고정 버퍼, 구분자 스캐너, TLV 로 자르는 세 가지 방식",
      "스트림 절단 경계와 복원 방식")

lane_h = 88
lane_gap = 14
y0 = 104

# 1. 고정 버퍼 레인 (Listing 4-1: 16MB 페이로드를 512KB 버퍼로 반복 수신)
y1 = y0
d.box(24, y1, 154, lane_h, fill=PAPER2, stroke=RULE)
d.t(36, y1 + 22, "LANE 1", 9, SOFT, MONO, "start")
d.t(36, y1 + 44, "고정 버퍼", 13, INK, KR, "start", 600)
d.t(36, y1 + 64, "Read(buf)", 10, MUTED, MONO, "start")

d.box(188, y1, 474, lane_h, fill=PAPER2, stroke=RULE)
# 1회 수신 512KB 블록
d.tone(204, y1 + 18, 120, 34, OK, op="20", sw=1.0)
d.t(264, y1 + 39, "512KB", 11, OK, MONO, "middle", 600)

# 절단선 (512KB 경계)
d.line(328, y1 + 12, 328, y1 + 60, BAD, 1.6, "3 3")

# 미수신 잔여 블록 (15.5MB 잔여)
d.box(334, y1 + 18, 314, 34, fill=PAPER, stroke=RULE, sw=0.8)
d.t(491, y1 + 39, "15.5MB 잔여 페이로드", 11, MUTED, KR, "middle")

d.t(264, y1 + 72, "1회 512KB 수신", 11, OK, KR, "middle")

d.box(672, y1, 184, lane_h, fill=PAPER2, stroke=RULE)
d.t(688, y1 + 36, "임의 크기 절단", 12, WARN, KR, "start", 600)
d.t(688, y1 + 58, "32회 반복 수신", 11, MUTED, KR, "start")


# 2. 구분자 스캐너 레인 (Listing 4-2·4-3: 공백 구분자로 단어 토큰 분리)
y2 = y1 + lane_h + lane_gap
d.box(24, y2, 154, lane_h, fill=PAPER2, stroke=RULE)
d.t(36, y2 + 22, "LANE 2", 9, SOFT, MONO, "start")
d.t(36, y2 + 44, "구분자 스캐너", 13, INK, KR, "start", 600)
d.t(36, y2 + 64, "bufio.Scanner", 10, MUTED, MONO, "start")

d.box(188, y2, 474, lane_h, fill=PAPER2, stroke=RULE)
# 토큰 "The"
d.tone(204, y2 + 18, 64, 34, OK, op="20", sw=1.0)
d.t(236, y2 + 39, "The", 11, OK, MONO, "middle", 600)

# 구분자 공백 ' '
d.tone(272, y2 + 18, 44, 34, ACC, op="25", sw=1.2)
d.t(294, y2 + 39, "공백", 11, ACC, KR, "middle")

# 절단선
d.line(320, y2 + 12, 320, y2 + 60, ACC, 1.6, "3 3")

# 다음 토큰들
d.box(326, y2 + 18, 322, 34, fill=PAPER, stroke=RULE, sw=0.8)
d.t(487, y2 + 39, "bigger ...", 11, MUTED, MONO, "middle")

d.t(236, y2 + 72, "토큰 복원", 11, OK, KR, "middle")
d.t(294, y2 + 72, "구분자 소비", 11, ACC, KR, "middle")

d.box(672, y2, 184, lane_h, fill=PAPER2, stroke=RULE)
d.t(688, y2 + 36, "토큰 단위 분리", 12, OK, KR, "start", 600)
d.t(688, y2 + 58, "구분자 패턴 일치", 11, MUTED, KR, "start")


# 3. TLV 길이 헤더 레인 (Listing 4-4·4-7·4-8: StringType 2 + Length 11 + hello world)
y3 = y2 + lane_h + lane_gap
d.box(24, y3, 154, lane_h, fill=PAPER2, stroke=RULE)
d.t(36, y3 + 22, "LANE 3", 9, SOFT, MONO, "start")
d.t(36, y3 + 44, "TLV 길이 헤더", 13, INK, KR, "start", 600)
d.t(36, y3 + 64, "Type + Length", 10, MUTED, MONO, "start")

d.box(188, y3, 474, lane_h, fill=PAPER2, stroke=RULE)
# Type (1B: StringType = 2)
d.tone(204, y3 + 18, 52, 34, ACC, op="20", sw=1.0)
d.t(230, y3 + 39, "T:2", 11, ACC, MONO, "middle", 600)

# Length (4B: L:11)
d.tone(260, y3 + 18, 64, 34, ACC, op="20", sw=1.0)
d.t(292, y3 + 39, "L:11", 11, ACC, MONO, "middle", 600)

# 절단선 (5B 고정 헤더와 가변 값 경계)
d.line(328, y3 + 12, 328, y3 + 60, ACC, 1.6, "3 3")

# Value (11B: "hello world")
d.tone(332, y3 + 18, 316, 34, OK, op="20", sw=1.0)
d.t(490, y3 + 39, "hello world", 11, OK, MONO, "middle", 600)

d.t(262, y3 + 72, "5B 고정 헤더", 11, ACC, KR, "middle")
d.t(490, y3 + 72, "11B 페이로드", 11, OK, KR, "middle")

d.box(672, y3, 184, lane_h, fill=PAPER2, stroke=RULE)
d.t(688, y3 + 36, "동적 버퍼 할당", 12, ACC, KR, "start", 600)
d.t(688, y3 + 58, "정확한 경계 복원", 11, MUTED, KR, "start")

d.legend(H - 46, [("수신 데이터", OK), ("헤더·구분자", ACC), ("미수신 잔여분", MUTED)])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "04-01.three-ways-to-frame.svg"))
d.save(out_path)
print(f"Generated: {out_path}")
