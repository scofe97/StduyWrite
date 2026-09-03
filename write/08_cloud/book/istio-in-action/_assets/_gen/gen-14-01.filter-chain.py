# 14-01 §2 리스너 안의 필터, 그 필터 안의 필터 — 원문 그림 14.2 · 14.3 · 14.4.
# 본문(원문 14.1.1): 리스너는 네트워크 인터페이스에 포트를 열고 들어오는 트래픽을 듣기 시작하는 방법이다.
#       Envoy 는 결국 L3/L4 프록시로 네트워크 연결에서 바이트를 떼어 처리한다. 리스너는 스트림에서 바이트를
#       읽어 여러 필터를 통과시킨다. 가장 기본은 네트워크 필터이고 여럿을 순서로 묶은 것이 필터 체인이다.
#       기본 네트워크 필터에 MongoDB · Redis · Thrift · Kafka · HttpConnectionManager 가 있다.
#       HCM 은 바이트를 HTTP 헤더 · 본문 · 트레일러로 바꾸며, 그 자신도 필터 기반 아키텍처를 가져
#       HTTP 필터 체인을 품는다. HTTP 필터들은 반드시 업스트림 클러스터로 보내는 종단 필터로 끝나야 하고
#       그것이 라우터 필터다.
# 타입 스펙: type-nested — 포함으로 표현하는 계층. 링 3(3~5), 안쪽으로 갈수록 획이 진해진다.
#           링 라벨은 왼쪽 위 종이색 마스크 위 mono eyebrow, coral 은 가장 안쪽 초점 하나에만.
#           안쪽 상자 넷의 배열 순서는 원문이 정하지 않는다 — 원문이 규칙으로 적는 것은 라우터가
#           마지막이어야 한다는 것뿐이라, 앞의 넷은 예시 배치임을 각주 줄로 밝힌다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 660
d = D(W, H, "ISTIO IN ACTION · 14-01 §2",
      "필터 안에 또 필터가 있고 확장은 안쪽에 꽂힌다",
      "리스너가 바이트를 읽어 네트워크 필터 체인으로 넘기고, 그중 HCM 이 바이트를 HTTP 로 바꾼다. "
      "HCM 자신도 필터 체인을 품으며, 이 장의 확장이 전부 그 안쪽 체인에 들어간다.",
      "안쪽 체인은 반드시 라우터 필터로 끝나야 합니다")

def ring(x, y, w, h, tag, sub, stroke, fill, focal=False):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" '
               f'stroke="{stroke}" stroke-width="{1.4 if focal else 1.0}"/>')
    tw = len(tag) * 6 + 16
    d.o.append(f'<rect x="{x + 20}" y="{y - 7}" width="{tw}" height="14" fill="{PAPER}"/>')
    d.t(x + 28, y + 3, tag, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 28, y + 30, sub, 11, ACC if focal else MUTED, KR, "start")

ring(48, 132, 908, 396, "LISTENER · 포트를 열고 바이트를 읽는다", "Envoy 는 L3/L4 프록시다", f"{INK}30", f"{INK}04")
ring(84, 196, 832, 296, "NETWORK FILTER CHAIN", "바이트 스트림을 인코딩 · 디코딩한다 — MongoDB · Redis · Thrift · Kafka", MUTED, f"{INK}07")
ring(120, 260, 760, 196, "HTTP CONNECTION MANAGER", "바이트를 HTTP 헤더 · 본문 · 트레일러로 바꾼다", f"{INK}55", f"{INK}09")
ring(156, 324, 688, 108, "HTTP FILTER CHAIN", "요청 위에서 도는 필터들 — 이 장의 확장이 꽂히는 자리", ACC, f"{ACC}0E", focal=True)

BW, BH, BY = 140, 44, 364
labels = [("CORS · CSRF", MUTED), ("RateLimit", MUTED), ("Lua", MUTED), ("Wasm", MUTED), ("Router", ACC)]
for i, (lab, c) in enumerate(labels):
    x = 212 + i * 160
    if c is ACC:
        d.o.append(f'<rect x="{x}" y="{BY}" width="{BW - 24}" height="{BH}" rx="4" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.2"/>')
    else:
        d.box(x, BY, BW - 24, BH, PAPER2, RULE, 1.0, 4)
    d.t(x + (BW - 24) / 2, BY + 20, lab, 11, ACC if c is ACC else INK, MONO, "middle", 600)
    d.t(x + (BW - 24) / 2, BY + 36, "종단 필터" if c is ACC else "기본 제공", 11, MUTED, KR)
    if i < len(labels) - 1:
        d.path(f"M {x + BW - 24} {BY + BH / 2} H {x + 158}", MUTED, 1.0, m="ar")

d.t(28, 566, "안쪽 상자 넷의 배열 순서는 설정하기 나름이다 — 원문이 정하는 것은 라우터가 마지막이어야 한다는 규칙 하나뿐이다", 11, SOFT, KR, "start")
d.t(28, 590, "HCM 이 함께 맡는 것 — 액세스 로깅 · 요청 재시도 · 헤더 조작 · 헤더와 경로 접두사 기반 라우팅", 11, MUTED, KR, "start")
d.legend(610, [("확장이 꽂히는 안쪽 체인", ACC), ("그 위를 감싸는 층", MUTED)])
d.save("14-01.filter-chain.svg")
