# 타입 스펙: type-sequence
# 사실 출처: NPG Ch.4 Listing 4-1 (read_test.go), p.2-4
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.4, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 8, label, 11, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 16, sub, 11, MUTED, _kr(sub), "middle")

W, H = 880, 540
d = SeqKR(W, H, "FIXED BUFFER READ",
          "고정 버퍼 수신과 스트림 분할 읽기",
          "16MB 전송에 대해 512KB 버퍼로 반복 읽으며 n < 버퍼 크기 및 io.EOF 감지",
          "수신 소켓 버퍼 준비량에 따른 즉시 반환과 정상 종료 판별")

# Participants (Client left, Server right)
lx = d.lanes([("Client (수신측)", "buf := make([]byte, 1<<19)"),
              ("Server (송신측)", "payload := make([]byte, 1<<24)")],
             y0=96, lane_w=240)

# Lifeline rails
d.rails(452)

sx = lx["Server (송신측)"]
cx = lx["Client (수신측)"]

# 1. Server initiates stream write (16MB)
d.state("Server (송신측)", "conn.Write(16MB)", 158, INFO)
d.t(sx - 12, 182, "16,777,216B 스트림 송신 시작", 11, MUTED, KR, "end")

# Combined Fragment: LOOP Frame
frame_x = cx - 28
frame_w = (sx - cx) + 56
frame_y = 198
frame_h = 176
d.o.append(f'<rect x="{frame_x}" y="{frame_y}" width="{frame_w}" height="{frame_h}" rx="4" fill="rgba(245,245,245,0.02)" stroke="{RULE}" stroke-width="1"/>')
d.o.append(f'<rect x="{frame_x}" y="{frame_y}" width="46" height="18" rx="2" fill="{PAPER2}" stroke="{RULE}" stroke-width="1"/>')
d.t(frame_x + 23, frame_y + 13, "LOOP", 8, INK, MONO, "middle", 600)
d.t(frame_x + 56, frame_y + 14, "[16MB 수신 반복]", 11, MUTED, KR, "start")

# Loop iteration 1: Full 512KB read
d.msg("Client (수신측)", "Server (송신측)", "conn.Read(buf)", 226, MUTED)
d.msg("Server (송신측)", "Client (수신측)", "n ≤ 524,288 B (버퍼 한도)", 254, OK, mk="ok", dash="4,3",
      sub="buf[:n] 완충 소비 · 수신 버퍼 완충 반환")

# Loop iteration 2: Partial read (n < 512KB, focal!)
d.msg("Client (수신측)", "Server (송신측)", "conn.Read(buf)", 296, MUTED)
d.msg("Server (송신측)", "Client (수신측)", "n < 512 KB (도착분만)", 326, ACC, mk="acc", dash="4,3",
      sub="소켓 버퍼 도착분만 즉시 반환 (블로킹 없이 리턴)")

# Loop ellipsis
d.t((cx + sx) / 2, 360, "· · · 16MB 누적 수신 반복 · · ·", 11, SOFT, KR, "middle")

# 2. End of Stream (Outside loop)
d.msg("Server (송신측)", "Client (수신측)", "conn.Close() (FIN 세그먼트 전송)", 396, WARN, mk="warn")

# 3. Client detects io.EOF
d.msg("Client (수신측)", "Server (송신측)", "conn.Read(buf)", 424, MUTED)
d.msg("Server (송신측)", "Client (수신측)", "n = 0, err = io.EOF", 450, INFO, mk="info", dash="4,3",
      sub="정상 스트림 종료 감지 → for 루프 break 탈출")

# Legend (bottom margin >= 16px)
d.legend(480, [
    ("버퍼 미달 반환", ACC),
    ("버퍼 완충 반환", OK),
    ("연결 종료", WARN),
    ("스트림 끝 신호", INFO),
])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "04-01.fixed-buffer-reads.svg"))
d.save(out_path)
print(f"Generated: {out_path}")
