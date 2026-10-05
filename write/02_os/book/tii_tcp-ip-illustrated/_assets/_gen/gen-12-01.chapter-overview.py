# 12-01 학습 목표 뒤 전체 지도 — 12.1 의 일반 원리가 12.2·12.3 의 TCP 장치로 하나씩 옮겨 가는 대응.
# 원문 12.4 요약이 "TCP 헤더 필드 대부분이 신뢰 전달의 추상 개념과 직접 이어진다"고 적은 것을 행렬로 편다.
# 행 = 풀어야 할 문제, 열 = 일반 해법(12.1) · TCP 의 구현(12.2·12.3) · 더 깊이 다루는 장.
# 타입 스펙: type-dp-security-matrix — 행마다 같은 세 칸이 반복되고 칸끼리 화살표 없이 위치로 대응한다.
#           축약: 칸 문구가 한글 구절이라 role_col_w 148 → 200 으로 넓혔다. 나머지 상수·공식은 §2 그대로.
#           focal 은 이 장의 줄기인 "누적 ACK 를 쓰는 슬라이딩 윈도" 한 칸.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

left_pad, right_pad = 12, 48
comp_col_w, comp_role_gap = 208, 12
role_col_w, role_col_gap = 200, 16
header_h, row_h, row_stride = 52, 36, 40
roles = [("일반 해법", "12.1 · §1–§5"), ("TCP 의 구현", "12.2–12.3 · §6–§8"), ("더 깊이", "이 책의 다음 장")]
comps = ["손실 · 비트 오류", "같은 패킷이 두 번", "하나씩이면 망이 논다", "받는 쪽이 느리다",
         "가운데 망이 막힌다", "얼마나 기다리나"]
cells = {
    (0, 0): ("재전송 · ACK · 체크섬", "§1"), (0, 1): ("체크섬 틀리면 버리고 침묵", "§7"), (0, 2): ("14장 재전송", None),
    (1, 0): ("순서 번호", "§1"), (1, 1): ("바이트 단위 번호", "§7 · §8"), (1, 2): ("13장 ISN", None),
    (2, 0): ("여러 개를 띄우는 창", "§2 · §3"), (2, 1): ("누적 ACK 슬라이딩 윈도", "§7 · §8"), (2, 2): ("15장 창 관리", None),
    (3, 0): ("창 광고 = 흐름 제어", "§4"), (3, 1): ("Window Size 16비트", "§8"), (3, 2): ("15장 창 관리", None),
    (4, 0): ("망 신호로 줄임 = 혼잡 제어", "§4"), (4, 1): ("손실 짐작 · CWR·ECE", "§8"), (4, 2): ("16장 혼잡 제어", None),
    (5, 0): ("RTT 추정 · RTO", "§5"), (5, 1): ("창마다 타이머 하나", "§7"), (5, 2): ("14장 RTO 계산", None),
}
FOCAL = (2, 1)

n_roles, n_comp = len(roles), len(comps)
W = left_pad + comp_col_w + comp_role_gap + n_roles * role_col_w + (n_roles - 1) * role_col_gap + right_pad
header_y = 104                                   # 공식의 72 에 dd 헤더(제목·요약 줄) 높이 32 를 더했다
def row_y(k): return header_y + 68 + k * row_stride
rows_bottom = row_y(n_comp - 1) + row_h
legend_y = rows_bottom + 24
H = legend_y + 48
def role_x(j): return left_pad + comp_col_w + comp_role_gap + j * (role_col_w + role_col_gap)

d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 12-01",
      "12장 전체 지도 — 일반 원리가 TCP 장치가 되는 자리",
      "신뢰 전달이 풀어야 할 문제 여섯을 행으로 두고, 12.1 이 말하는 일반 해법과 TCP 가 그것을 구현한 장치, "
      "그리고 그 장치를 자세히 다루는 뒷장을 같은 행에 놓았다. 셀 아래 절 번호가 이 노트에서 그 칸을 다루는 곳이다.",
      "왼쪽 열을 먼저 익히면 오른쪽의 헤더 필드가 왜 거기 있는지 읽힙니다")

# 헤더 행
d.box(left_pad, header_y, comp_col_w, header_h, PAPER2, RULE, 0.8, 6)
d.t(left_pad + comp_col_w / 2, header_y + 22, "풀어야 할 문제", 13, INK, KR, "middle", 600)
d.t(left_pad + comp_col_w / 2, header_y + 40, "12.1.1 의 질문들", 11, MUTED, KR)
for j, (name, code) in enumerate(roles):
    x = role_x(j)
    d.box(x, header_y, role_col_w, header_h, "#2A3140", RULE, 0.8, 6)
    d.t(x + role_col_w / 2, header_y + 22, name, 13, INK, KR, "middle", 600)
    d.t(x + role_col_w / 2, header_y + 40, code, 11, MUTED, MONO if all(ord(c) < 128 or c in "–·§" for c in code) else KR)

# 데이터 행
for k, comp in enumerate(comps):
    y = row_y(k)
    d.box(left_pad, y, comp_col_w, row_h, PAPER2, RULE, 0.8, 4)
    d.t(left_pad + 12, y + 23, comp, 13, INK, KR, "start", 600)
    for j in range(n_roles):
        x = role_x(j); val, sec = cells[(k, j)]
        if (k, j) == FOCAL:
            d.o.append(f'<rect x="{x}" y="{y}" width="{role_col_w}" height="{row_h}" rx="4" '
                       f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
            c = ACC
        elif j == 2:
            d.box(x, y, role_col_w, row_h, PAPER, RULE, 0.6, 4); c = MUTED
        else:
            d.tone(x, y, role_col_w, row_h, INFO if j == 0 else OK, 4, "10", 0.8); c = INFO if j == 0 else OK
        d.t(x + 12, y + 23, val, 12, c, KR, "start", 600 if j < 2 else 400)
        if sec:
            d.t(x + role_col_w - 10, y + 23, sec, 11, SOFT, MONO, "end")

d.legend(legend_y, [("이 장의 줄기", ACC), ("일반 원리", INFO), ("TCP 장치", OK), ("뒷장 연결", MUTED)])
d.save("12-01.chapter-overview.svg")
