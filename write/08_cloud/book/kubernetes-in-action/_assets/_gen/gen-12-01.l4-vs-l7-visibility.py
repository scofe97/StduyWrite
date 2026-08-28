# 12-01 §1 — 같은 패킷, 다른 가시 범위
# 본문이 "커널이 보기에 완전히 같은 요청"이라고 못박는다. 그 '같음'은 계층 그림 하나로는
# 안 보이고, 같은 패킷 두 벌을 나란히 놓고 한쪽 층을 꺼야 드러난다.
# 타입 스펙: type-layers.md — 같은 패킷을 쌓아 올린 세 층을 두 벌 나란히 두고, 어느 층까지 보이는지를 대조한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1060, 592, "KUBERNETES IN ACTION · 12-01",
      "같은 패킷인데 보이는 층이 다르다",
      "봉투에 비유하면 커널은 겉면의 주소까지만 읽고, 프록시는 봉투를 열어 안에 적힌 글을 읽는다. "
      "가를 수 있는 것은 읽을 수 있는 것에 갇힌다.",
      "api.example.com/quote 로 온 요청 한 장")

LAY = [("IP 헤더", "src 203.0.113.7  ·  dst 11.22.33.44"),
       ("TCP 헤더", "dst port 80"),
       ("HTTP", "GET /quote   Host: api.example.com")]

def stack(cx, title, lit, note, note_c):
    d.t(cx, 148, title, 12, SOFT, KR)
    for i, (nm, val) in enumerate(LAY):
        y = 172 + i * 84
        on = i < lit
        if on and i == 2:
            d.o.append(f'<rect x="{cx-200}" y="{y}" width="400" height="72" rx="6" '
                       f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
            tc, vc = ACC, ACC
        elif on:
            d.box(cx - 200, y, 400, 72, PAPER2, RULE, 1.1, 6); tc, vc = INK, MUTED
        else:
            d.box(cx - 200, y, 400, 72, PAPER, RULE, 0.7, 6); tc, vc = SOFT, SOFT
        d.t(cx, y + 30, nm, 13, tc, KR, "middle", 600)
        d.t(cx, y + 52, val, 10, vc, MONO)
        if not on:
            d.t(cx, y + 68, "읽지 않는다", 10, SOFT, KR)
    d.t(cx, 452, note, 12, note_c, KR)

stack(280, "커널이 읽는 범위 — L4", 2, "/quote 와 /questions 가 같은 요청이다", MUTED)
stack(780, "프록시가 읽는 범위 — L7", 3, "경로로 가를 재료가 손에 있다", ACC)

d.t(24, 502, "그래서 Ingress 가 필요한 이유는 'IP 하나로 여러 곳에 못 보내서'가 아니다. "
             "cluster IP 하나가 파드 여럿을 뒷받침하는 일은 L4 에서도 된다.", 11, MUTED, KR, "start")
d.t(24, 524, "갈라지긴 하는데 기준을 정할 재료가 없다는 것이 문제다 — 커널이 파드를 고른 근거가 확률뿐이었던 이유다.",
     11, MUTED, KR, "start")
d.legend(544, [("읽히는 층", ACC)])
d.save("12-01-l4-vs-l7-visibility.svg")
print("ok")
