# 타입 스펙: type-flowchart
# 사실 출처: NPG 04-03 §1 · Listing 4-23 (AcceptTCP), Listing 4-24 (DialTCP), p.32-33
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 880, 580
d = D(W, H, "TCPCONN RETRIEVAL",
      "net.TCPConn 추출 경로와 제어 손잡이",
      "net.Conn 타입 단언과 TCP 전용 함수(AcceptTCP·DialTCP)를 통한 *net.TCPConn 획득 흐름",
      "타입 단언(ok 검사)과 전용 생성 함수의 두 갈래 및 저수준 소켓 옵션 제어")

# 열 헤더 카드
d.box(70, 96, 360, 28, fill=PAPER2, stroke=RULE, r=4)
d.t(250, 114, "경로 1: 타입 단언", 12, INK, KR, "middle", 600)

d.box(470, 96, 360, 28, fill=PAPER2, stroke=RULE, r=4)
d.t(650, 114, "경로 2: TCP 전용 함수", 12, INK, KR, "middle", 600)

# --- 경로 1 (Left: cx = 250) ---
cx1 = 250

# 1-1. 시작 노드
d.box(cx1 - 90, 136, 180, 36, fill=PAPER2, stroke=RULE, r=18)
d.t(cx1, 154, "net.Conn 인터페이스", 12, INK, KR, "middle", 600)
d.t(cx1, 166, "net.Dial / net.Listen", 9, MUTED, MONO, "middle")

d.arrow([(cx1, 172), (cx1, 196)], MUTED, "ar", 1.2)

# 1-2. 타입 단언 단계
d.box(cx1 - 105, 196, 210, 42, fill=PAPER2, stroke=RULE, r=6)
d.t(cx1, 213, "conn.(*net.TCPConn)", 11, INK, MONO, "middle", 600)
d.t(cx1, 229, "구체 타입 단언", 11, MUTED, KR, "middle")

d.arrow([(cx1, 238), (cx1, 260)], MUTED, "ar", 1.2)

# 1-3. 분기 다이아몬드 (cx1=250, cy=284)
cy_d = 284
pts_d = f"{cx1},{cy_d - 24} {cx1 + 65},{cy_d} {cx1},{cy_d + 24} {cx1 - 65},{cy_d}"
d.o.append(f'<polygon points="{pts_d}" fill="{PAPER2}" stroke="{WARN}" stroke-width="1.2"/>')
d.t(cx1, cy_d + 4, "단언 성공 (ok)?", 11, WARN, KR, "middle", 600)

# 분기 1-실패 (왼쪽)
d.arrow([(cx1 - 65, cy_d), (cx1 - 110, cy_d)], BAD, "bad", 1.4)
d.t(cx1 - 88, cy_d - 8, "false", 10, BAD, MONO, "middle", 600)

d.box(30, cy_d - 18, 100, 36, fill=PAPER2, stroke=BAD, r=6)
d.t(80, cy_d - 2, "비-TCP 연결", 11, BAD, KR, "middle", 600)
d.t(80, cy_d + 12, "에러 처리", 11, BAD, KR, "middle")

# 분기 1-성공 (아래쪽)
d.arrow([(cx1, cy_d + 24), (cx1, 332)], OK, "ok", 1.4)
d.t(cx1 + 20, cy_d + 24, "true", 10, OK, MONO, "start", 600)

# 단언 성공 결과 상자
d.box(cx1 - 80, 332, 160, 32, fill=PAPER2, stroke=OK, r=6)
d.t(cx1, 352, "*net.TCPConn 획득", 11, OK, MONO, "middle", 600)
d.arrow([(cx1, 364), (cx1, 388)], OK, "ok", 1.4)

# --- 경로 2 (Right: cx = 650) ---
cx2 = 650

# 2-1. 시작 노드
d.box(cx2 - 100, 136, 200, 36, fill=PAPER2, stroke=RULE, r=18)
d.t(cx2, 154, "net.ResolveTCPAddr", 11, INK, MONO, "middle", 600)
d.t(cx2, 166, "TCP 주소 해석", 11, MUTED, KR, "middle")

# 2분기 (서버 vs 클라이언트)
d.line(cx2, 172, cx2, 184, MUTED, 1.2)
d.line(555, 184, 745, 184, MUTED, 1.2)
d.arrow([(555, 184), (555, 196)], MUTED, "ar", 1.2)
d.arrow([(745, 184), (745, 196)], MUTED, "ar", 1.2)

# 서버 박스
d.box(475, 196, 160, 46, fill=PAPER2, stroke=RULE, r=6)
d.t(555, 213, "ListenTCP → AcceptTCP", 11, INK, MONO, "middle", 600)
d.t(555, 231, "서버 수신 소켓", 11, MUTED, KR, "middle")

# 클라이언트 박스
d.box(665, 196, 160, 46, fill=PAPER2, stroke=RULE, r=6)
d.t(745, 213, "net.DialTCP", 11, INK, MONO, "middle", 600)
d.t(745, 231, "클라이언트 연결", 11, MUTED, KR, "middle")

# 합류선
d.line(555, 242, 555, 262, MUTED, 1.2)
d.line(745, 242, 745, 262, MUTED, 1.2)
d.line(555, 262, 745, 262, MUTED, 1.2)
d.o.append(f'<circle cx="{cx2}" cy="262" r="4" fill="{INK}"/>')

d.arrow([(cx2, 262), (cx2, 332)], OK, "ok", 1.4)

# 전용 함수 결과 상자
d.box(cx2 - 90, 332, 180, 32, fill=PAPER2, stroke=OK, r=6)
d.t(cx2, 352, "*net.TCPConn 직접 반환", 11, OK, MONO, "middle", 600)
d.arrow([(cx2, 364), (cx2, 388)], OK, "ok", 1.4)

# --- 수렴 노드: *net.TCPConn 저수준 조작 패널 ---
d.tone(70, 388, 760, 74, ACC, r=8, op="14", sw=1.4)
d.t(450, 410, "*net.TCPConn 저수준 손잡이", 13, ACC, KR, "middle", 600)
d.t(450, 430, "SetKeepAliveConfig() — 유휴 탐침  ·  SetLinger() — 잔여 데이터", 11, INK, KR, "middle")
d.t(450, 448, "SetReadBuffer() · SetWriteBuffer() — 커널 소켓 버퍼 수동 지정", 11, INK, KR, "middle")

# 대가 / 주의 경고 박스
d.box(70, 474, 760, 34, fill=PAPER2, stroke=WARN, r=6)
d.t(450, 495, "대가: OS 종속 이식성 저하 · 단위 테스트 시 Mock 대체 불가", 11, WARN, KR, "middle")

# 범례
d.legend(H - 44, [("구체 타입 획득 (성공)", OK), ("단언 실패 (비-TCP)", BAD), ("저수준 제어 손잡이", ACC), ("이식성·테스트 대가", WARN)])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "04-03.get-tcpconn.svg"))
d.save(out_path)
print(f"Generated: {out_path}")
