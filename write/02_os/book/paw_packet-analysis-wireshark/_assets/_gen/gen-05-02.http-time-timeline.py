# 05-02 §3 — http.time 이 재는 구간. 연결 수립(SYN · SYN/ACK · ACK)은 연결마다 한 번이고, 그 뒤 같은 연결에
# 트랜잭션(요청 하나와 응답 하나)이 여럿 실린다. http.time 은 요청 프레임에서 응답 프레임까지다.
# 본문 요구: 학습자는 느린 요청을 SYN·ACK 간격으로 찾는다고 예측했다. 두 구간을 한 시간축에 나란히 두어
#            연결 수립 왕복(네트워크 지연)과 요청 → 응답 간격(서버 처리 포함)이 다른 막대임을, 둘째
#            트랜잭션 앞에는 SYN 이 없음을 보인다. 연결 재사용은 RFC 9112 §9.3, 필드 이름은 tshark 4.6.8.
#            시간축은 구간의 선후만 보이는 개략이다 — 막대 길이는 실측 비율이 아니다.
# 타입 스펙: type-gantt — 막대 길이가 곧 구간. focal 은 앞에 SYN 이 없는 둘째 트랜잭션의 http.time 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 496
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-02 §3",
      "http.time 은 어느 구간을 재나",
      "TCP 연결 하나의 시간축. SYN · SYN/ACK · ACK 로 연결을 세우는 왕복은 맨 앞에 한 번뿐이고, 그 연결 위에 요청과 응답의 짝이 여럿 실린다. http.time 은 요청 프레임에서 그 응답 프레임까지의 간격이라 서버가 처리한 시간이 들어 있다.",
      "연결 수립 왕복과 http.time 은 다른 막대입니다 — 둘째 요청 앞에는 SYN 이 없습니다")

LABEL_X = 24
TICKS = [("SYN", 232), ("SYN/ACK", 312), ("ACK", 392), ("GET", 440), ("200", 616), ("GET", 688), ("200", 848)]
AXIS_Y = 120
ROW0, STRIDE, BAR_H = 152, 64, 24
ROWS_END = ROW0 + 4 * STRIDE - 8

# 선 위의 프레임 — 눈금과 세로 안내선
for lab, x in TICKS:
    d.t(x, AXIS_Y, lab, 12, INK, MONO, "middle", 600)
    d.line(x, AXIS_Y + 12, x, ROWS_END, SOFT, 0.8, "2 5")
d.t(LABEL_X, AXIS_Y, "선 위의 프레임", 12, SOFT, KR, "start", 600)
d.line(LABEL_X, AXIS_Y + 12, 200, AXIS_Y + 12, RULE, 0.8)

def row_label(i, name, sub, c=None):
    y = ROW0 + i * STRIDE
    d.t(LABEL_X, y + 22, name, 13, INK, KR, "start", 600)
    d.t(LABEL_X, y + 40, sub, 12, c if c else MUTED, KR, "start", 600 if c else 400)

def bar(i, x1, x2, txt, c=None, focal=False):
    y = ROW0 + i * STRIDE + 8
    if focal:
        d.o.append(f'<rect x="{x1}" y="{y}" width="{x2 - x1}" height="{BAR_H}" rx="4" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        col = ACC
    elif c:
        d.tone(x1, y, x2 - x1, BAR_H, c, 4)
        col = c
    else:
        d.box(x1, y, x2 - x1, BAR_H, PAPER2, RULE, 1.0, 4)
        col = MUTED
    d.t(x1 + 10, y + 17, txt, 12, col, KR if any("가" <= ch <= "힣" for ch in txt) else MONO, "start", 600)

# 설명은 왼쪽 라벨의 부제로 둔다 — 막대 오른쪽에 두면 세로 안내선을 가로지른다
row_label(0, "TCP 연결", "연결 하나")
bar(0, 232, 896, "SYN 은 맨 앞 한 번 · 요청마다 오지 않음")
row_label(1, "연결 수립", "네트워크 왕복 · 연결마다 한 번")
bar(1, 232, 312, "왕복", INFO)
row_label(2, "트랜잭션 1", "요청 → 응답 · 서버 처리 포함")
bar(2, 440, 616, "http.time", OK)
row_label(3, "트랜잭션 2", "앞에 SYN 없음", ACC)
bar(3, 688, 848, "http.time", focal=True)

d.legend(H - 56, [("SYN 없이 재는 http.time", ACC), ("연결 수립 왕복", INFO), ("요청 → 응답", OK)])
d.save("05-02.http-time-timeline.svg")
