# 타입 스펙: type-data-flow
# 사실 출처: NPG Ch.4 Listing 4-2·4-3 (scanner_test.go), p.4-7
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 920, 460
d = D(W, H, "SCANNER DATA FLOW",
      "구분자 기반 프레이밍과 bufio.Scanner 데이터 흐름",
      "공백 구분자 기준 스트림 분할 및 인접 문장부호 유지 단어 토큰 복원",
      "ScanWords 분할 함수를 통한 네트워크 바이트 스트림의 토큰화")

y0, box_h = 104, 240
bw = 174
gap_w = 54

# --- STAGE 1: 원시 바이트 송신 ---
s1_x = 24
d.box(s1_x, y0, bw, box_h, fill=PAPER2, stroke=INFO, sw=1.2, r=8)
d.t(s1_x + 16, y0 + 22, "STAGE 1", 9, INFO, MONO, "start", 600)
d.t(s1_x + bw / 2, y0 + 44, "원시 바이트 송신", 12, INK, KR, "middle", 600)
d.t(s1_x + bw / 2, y0 + 62, "TCP 스트림 (53B)", 11, MUTED, KR, "middle")

d.box(s1_x + 10, y0 + 74, bw - 20, 114, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(s1_x + 16, y0 + 94, "conn.Write(payload)", 9, INFO, MONO, "start", 600)
d.t(s1_x + 16, y0 + 114, '"The bigger the', 9, INK, MONO, "start")
d.t(s1_x + 16, y0 + 132, ' interface, the', 9, INK, MONO, "start")
d.t(s1_x + 16, y0 + 150, ' weaker the', 9, INK, MONO, "start")
d.t(s1_x + 16, y0 + 168, ' abstraction."', 9, INK, MONO, "start")

d.t(s1_x + bw / 2, y0 + 208, "53B 무경계 스트림", 11, MUTED, KR, "middle")
d.t(s1_x + bw / 2, y0 + 226, "자체 문장부호 부재", 11, SOFT, KR, "middle")

# 화살표 1 -> 2
a1_x = s1_x + bw
d.line(a1_x, y0 + 130, a1_x + gap_w, y0 + 130, c=MUTED, sw=1.4)
d.arrow([(a1_x + gap_w - 12, y0 + 130), (a1_x + gap_w, y0 + 130)], c=MUTED, m="ar", sw=1.4)
d.t(a1_x + gap_w / 2, y0 + 120, "53B 전달", 11, MUTED, KR, "middle")

# --- STAGE 2: 스캐너 내부 버퍼 ---
s2_x = a1_x + gap_w
d.box(s2_x, y0, bw, box_h, fill=PAPER2, stroke=WARN, sw=1.2, r=8)
d.t(s2_x + 16, y0 + 22, "STAGE 2", 9, WARN, MONO, "start", 600)
d.t(s2_x + bw / 2, y0 + 44, "스캐너 내부 버퍼", 12, INK, KR, "middle", 600)
d.t(s2_x + bw / 2, y0 + 62, "bufio.NewScanner", 10, MUTED, MONO, "middle")

d.box(s2_x + 10, y0 + 74, bw - 20, 114, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(s2_x + 16, y0 + 94, "io.Reader 입력", 11, WARN, KR, "start", 600)
d.t(s2_x + 16, y0 + 118, "내부 버퍼 적재", 11, INK, KR, "start")
d.t(s2_x + 16, y0 + 140, "구분자 탐색 대기", 11, INK, KR, "start")
d.t(s2_x + 16, y0 + 162, "Read 반복 자동화", 11, INK, KR, "start")

d.t(s2_x + bw / 2, y0 + 208, "수동 버퍼링 불필요", 11, MUTED, KR, "middle")
d.t(s2_x + bw / 2, y0 + 226, "다중 패킷 자동 흡수", 11, SOFT, KR, "middle")

# 화살표 2 -> 3
a2_x = s2_x + bw
d.line(a2_x, y0 + 130, a2_x + gap_w, y0 + 130, c=MUTED, sw=1.4)
d.arrow([(a2_x + gap_w - 12, y0 + 130), (a2_x + gap_w, y0 + 130)], c=MUTED, m="ar", sw=1.4)
d.t(a2_x + gap_w / 2, y0 + 120, "버퍼 전달", 11, MUTED, KR, "middle")

# --- STAGE 3: ScanWords 분할 (Focal!) ---
s3_x = a2_x + gap_w
d.tone(s3_x, y0, bw, box_h, ACC, r=8, op="10", sw=1.4)
d.t(s3_x + 16, y0 + 22, "STAGE 3", 9, ACC, MONO, "start", 600)
d.t(s3_x + bw / 2, y0 + 44, "ScanWords 분할", 12, INK, KR, "middle", 600)
d.t(s3_x + bw / 2, y0 + 62, "scanner.Split()", 10, ACC, MONO, "middle")

d.box(s3_x + 10, y0 + 74, bw - 20, 114, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(s3_x + 16, y0 + 94, "bufio.ScanWords", 9, ACC, MONO, "start", 600)
d.t(s3_x + 16, y0 + 116, "공백 문자 경계 절단", 11, INK, KR, "start")
d.t(s3_x + 16, y0 + 136, "인접 문장부호 유지", 11, ACC, KR, "start")
d.t(s3_x + 16, y0 + 154, '"interface,"', 9, MUTED, MONO, "start")
d.t(s3_x + 16, y0 + 172, '"abstraction."', 9, MUTED, MONO, "start")

d.t(s3_x + bw / 2, y0 + 208, "단어 경계 자동 분할", 11, ACC, KR, "middle")
d.t(s3_x + bw / 2, y0 + 226, "개행 대신 단어 사용", 11, SOFT, KR, "middle")

# 화살표 3 -> 4
a3_x = s3_x + bw
d.line(a3_x, y0 + 130, a3_x + gap_w, y0 + 130, c=OK, sw=1.4)
d.arrow([(a3_x + gap_w - 12, y0 + 130), (a3_x + gap_w, y0 + 130)], c=OK, m="ok", sw=1.4)
d.t(a3_x + gap_w / 2, y0 + 120, "토큰 추출", 11, OK, KR, "middle")

# --- STAGE 4: 토큰 슬라이스 산출 ---
s4_x = a3_x + gap_w
s4_w = W - 24 - s4_x
d.box(s4_x, y0, s4_w, box_h, fill=PAPER2, stroke=OK, sw=1.2, r=8)
d.t(s4_x + 16, y0 + 22, "STAGE 4", 9, OK, MONO, "start", 600)
d.t(s4_x + s4_w / 2, y0 + 44, "토큰 슬라이스", 12, INK, KR, "middle", 600)
d.t(s4_x + s4_w / 2, y0 + 62, "scanner.Text()", 10, MUTED, MONO, "middle")

d.box(s4_x + 10, y0 + 74, s4_w - 20, 114, fill=PAPER, stroke=RULE, sw=0.8, r=4)
# 8 tokens rendered as chips
tokens = [
    (s4_x + 14, y0 + 94, '"The"'),
    (s4_x + 14, y0 + 116, '"bigger"'),
    (s4_x + 14, y0 + 138, '"the"'),
    (s4_x + 14, y0 + 160, '"interface,"'),
    (s4_x + 88, y0 + 94, '"the"'),
    (s4_x + 88, y0 + 116, '"weaker"'),
    (s4_x + 88, y0 + 138, '"the"'),
    (s4_x + 88, y0 + 160, '"abstraction."'),
]
for tx, ty, tstr in tokens:
    c = ACC if ("," in tstr or "." in tstr) else OK
    d.t(tx, ty, tstr, 9, c, MONO, "start")

d.t(s4_x + s4_w / 2, y0 + 208, "8개 단어 토큰 복원", 11, OK, KR, "middle")
d.t(s4_x + s4_w / 2, y0 + 226, "io.EOF 시 루프 탈출", 11, SOFT, KR, "middle")

# 범례
d.legend(396, [
    ("원시 바이트 송신", INFO),
    ("스캐너 내부 버퍼", WARN),
    ("단어 분할 (ScanWords)", ACC),
    ("추출 토큰 슬라이스", OK),
])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "04-01.scanner-split-words.svg"))
d.save(out_path)
print(f"Generated: {out_path}")
