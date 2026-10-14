# 타입 스펙: type-uml-class
# 사실 출처: NPG Ch.4 p.1-2 (Using the net.Conn Interface), §1 코드·본문
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 880, 480
d = D(W, H, "NPG CH.4 · STREAM ABSTRACTION",
      "net.Conn 과 os.File 의 표준 입출력 호환",
      "io.Reader·Writer·Closer 인터페이스를 매개로 소켓과 파일을 동일 함수에 전달",
      "표준 인터페이스 다형성을 통한 재사용성과 테스트 용이성")

# UML markers definition
d.o.append('<defs>')
# Realization marker (hollow triangle)
d.o.append(f'<marker id="uml-tri" markerWidth="14" markerHeight="10" refX="13" refY="5" orient="auto" markerUnits="userSpaceOnUse"><polygon points="0 0, 14 5, 0 10" fill="{PAPER}" stroke="{INK}" stroke-width="1.1"/></marker>')
d.o.append(f'<marker id="uml-tri-acc" markerWidth="14" markerHeight="10" refX="13" refY="5" orient="auto" markerUnits="userSpaceOnUse"><polygon points="0 0, 14 5, 0 10" fill="{PAPER}" stroke="{ACC}" stroke-width="1.2"/></marker>')
# Dependency marker (open arrowhead)
d.o.append(f'<marker id="uml-open" markerWidth="9" markerHeight="8" refX="8" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L8,4 L0,8" fill="none" stroke="{MUTED}" stroke-width="1.2"/></marker>')
d.o.append('</defs>')

# --- 1. Top Caller Box: io.Copy / bufio.NewReader ---
call_x, call_y, call_w, call_h = 320, 88, 240, 56
d.box(call_x, call_y, call_w, call_h, fill=PAPER2, stroke=RULE, r=6)
d.t(call_x + call_w / 2, call_y + 14, "«caller»", 8, SOFT, MONO, "middle")
d.t(call_x + call_w / 2, call_y + 28, "io.Copy / bufio", 12, INK, KR, "middle", 600)
d.line(call_x, call_y + 35, call_x + call_w, call_y + 35, RULE, 0.8)
d.t(call_x + call_w / 2, call_y + 48, "+ Copy(dst, src): (int64, error)", 9, MUTED, MONO, "middle")

# --- 2. Center Column: Interfaces (io.Reader, io.Writer, io.Closer) ---
# io.Reader
r_x, r_y, r_w, r_h = 320, 172, 240, 60
d.box(r_x, r_y, r_w, r_h, fill=PAPER2, stroke=INFO, sw=1.1, r=6)
d.t(r_x + r_w / 2, r_y + 14, "«interface»", 8, INFO, MONO, "middle")
d.t(r_x + r_w / 2, r_y + 29, "io.Reader", 12, INK, KR, "middle", 600)
d.line(r_x, r_y + 36, r_x + r_w, r_y + 36, RULE, 0.8)
d.t(r_x + 14, r_y + 50, "+ Read(b []byte): (int, error)", 9, INK, MONO, "start")

# io.Writer
w_x, w_y, w_w, w_h = 320, 248, 240, 60
d.box(w_x, w_y, w_w, w_h, fill=PAPER2, stroke=INFO, sw=1.1, r=6)
d.t(w_x + w_w / 2, w_y + 14, "«interface»", 8, INFO, MONO, "middle")
d.t(w_x + w_w / 2, w_y + 29, "io.Writer", 12, INK, KR, "middle", 600)
d.line(w_x, w_y + 36, w_x + w_w, w_y + 36, RULE, 0.8)
d.t(w_x + 14, w_y + 50, "+ Write(b []byte): (int, error)", 9, INK, MONO, "start")

# io.Closer
c_x, c_y, c_w, c_h = 320, 324, 240, 56
d.box(c_x, c_y, c_w, c_h, fill=PAPER2, stroke=INFO, sw=1.1, r=6)
d.t(c_x + c_w / 2, c_y + 14, "«interface»", 8, INFO, MONO, "middle")
d.t(c_x + c_w / 2, c_y + 29, "io.Closer", 12, INK, KR, "middle", 600)
d.line(c_x, c_y + 36, c_x + c_w, c_y + 36, RULE, 0.8)
d.t(c_x + 14, c_y + 49, "+ Close(): error", 9, INK, MONO, "start")

# --- 3. Left Column: net.Conn (Focal!) ---
conn_x, conn_y, conn_w, conn_h = 36, 172, 230, 208
d.tone(conn_x, conn_y, conn_w, conn_h, ACC, r=6, op="10", sw=1.3)
d.t(conn_x + conn_w / 2, conn_y + 16, "«interface»", 8, ACC, MONO, "middle")
d.t(conn_x + conn_w / 2, conn_y + 33, "net.Conn", 13, INK, KR, "middle", 600)
d.line(conn_x, conn_y + 41, conn_x + conn_w, conn_y + 41, ACC, 0.8)
d.t(conn_x + 12, conn_y + 58, "+ Read(b []byte): (int, error)", 9, INK, MONO, "start")
d.t(conn_x + 12, conn_y + 78, "+ Write(b []byte): (int, error)", 9, INK, MONO, "start")
d.t(conn_x + 12, conn_y + 98, "+ Close(): error", 9, INK, MONO, "start")
d.t(conn_x + 12, conn_y + 118, "+ SetDeadline(t): error", 9, MUTED, MONO, "start")
d.line(conn_x, conn_y + 134, conn_x + conn_w, conn_y + 134, RULE, 0.6)
d.t(conn_x + conn_w / 2, conn_y + 158, "소켓 입출력 구현", 11, ACC, KR, "middle")
d.t(conn_x + conn_w / 2, conn_y + 182, "io.Copy 인자 전달", 11, MUTED, KR, "middle")

# --- 4. Right Column: os.File ---
file_x, file_y, file_w, file_h = 614, 172, 230, 208
d.box(file_x, file_y, file_w, file_h, fill=PAPER2, stroke=OK, sw=1.2, r=6)
d.t(file_x + file_w / 2, file_y + 16, "«struct»", 8, SOFT, MONO, "middle")
d.t(file_x + file_w / 2, file_y + 33, "os.File", 13, INK, KR, "middle", 600)
d.line(file_x, file_y + 41, file_x + file_w, file_y + 41, RULE, 0.8)
d.t(file_x + 12, file_y + 58, "+ Read(b []byte): (int, error)", 9, INK, MONO, "start")
d.t(file_x + 12, file_y + 78, "+ Write(b []byte): (int, error)", 9, INK, MONO, "start")
d.t(file_x + 12, file_y + 98, "+ Close(): error", 9, INK, MONO, "start")
d.line(file_x, file_y + 134, file_x + file_w, file_y + 134, RULE, 0.6)
d.t(file_x + file_w / 2, file_y + 160, "파일 입출력 구현", 11, OK, KR, "middle")
d.t(file_x + file_w / 2, file_y + 182, "io.Copy 인자 전달", 11, MUTED, KR, "middle")

# --- 5. Relationships (Realization & Dependency) ---
# Dependency from io.Copy to io.Reader (straight vertical)
d.path(f"M {call_x + 60} {call_y + call_h} L {call_x + 60} {r_y - 2}", MUTED, 1.2, m="uml-open", dash="4,3")
d.t(call_x + 76, (call_y + call_h + r_y) / 2 + 3, "src", 9, MUTED, MONO, "start")

# Dependency from io.Copy to io.Writer (routes right, hops over os.File realization line, enters io.Writer)
d.path(f"M {call_x + call_w} {call_y + 26} H 584 V 196 A 6 6 0 0 1 584 208 V 276 H {w_x + w_w + 2}", MUTED, 1.2, m="uml-open", dash="4,3")
d.t(592, 160, "dst", 9, MUTED, MONO, "start")

# Realization: net.Conn -> interfaces (horizontal dashed lines with ACC triangle)
d.path(f"M {conn_x + conn_w} {r_y + 30} L {r_x - 2} {r_y + 30}", ACC, 1.2, m="uml-tri-acc", dash="5,4")
d.path(f"M {conn_x + conn_w} {w_y + 30} L {w_x - 2} {w_y + 30}", ACC, 1.2, m="uml-tri-acc", dash="5,4")
d.path(f"M {conn_x + conn_w} {c_y + 28} L {c_x - 2} {c_y + 28}", ACC, 1.2, m="uml-tri-acc", dash="5,4")

# Realization: os.File -> interfaces (horizontal dashed lines with INK triangle)
d.path(f"M {file_x} {r_y + 30} L {r_x + r_w + 2} {r_y + 30}", MUTED, 1.2, m="uml-tri", dash="5,4")
d.path(f"M {file_x} {w_y + 30} L {w_x + w_w + 2} {w_y + 30}", MUTED, 1.2, m="uml-tri", dash="5,4")
d.path(f"M {file_x} {c_y + 28} L {c_x + c_w + 2} {c_y + 28}", MUTED, 1.2, m="uml-tri", dash="5,4")

# Legend (bottom margin >= 16px)
d.legend(416, [
    ("소켓 인터페이스", ACC),
    ("표준 I/O 인터페이스", INFO),
    ("파일 구현체", OK),
])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "04-01.conn-like-file.svg"))
d.save(out_path)
print(f"Generated: {out_path}")
