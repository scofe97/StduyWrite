# 타입 스펙: type-sequence — 수집기가 서비스 디스커버리에서 대상 목록을 받아 /metrics 를 당겨 오고(성공 up=1, 10초 안에 답이 없으면 up=0), 서비스 단위 배치 작업이 Pushgateway 에 POST 로 밀어 두고 수집기가 그곳을 당겨 가는 왕복(레인 5, 항목 8). 밀기 구간의 출발은 당겨지는 대상 앱이 아니라 별도의 배치 작업 레인이다.
# 사실 출처: Prometheus v3.15.0 docs/configuration/configuration.md L57(scrape_interval 기본 1m)·L61(scrape_timeout 기본 10s)·L347(metrics_path 기본 /metrics)·L2435(kubernetes_sd_config, 역할 pod 는 L2488 #### `pod`),
#   prometheus/docs 605cf81 docs/concepts/jobs_instances.md L33-L34(up 은 도달 가능하면 1, 스크레이프 실패면 0)·docs/practices/pushing.md L11-L37(Pushgateway 는 서비스 단위 배치 작업 결과용, 밀린 시리즈는 지우기 전까지 노출),
#   Pushgateway v1.11.4 README.md L76-L80(Pushgateway 를 수집 대상으로 설정)·L115(curl --data-binary 는 POST 이고 경로는 /metrics/job/<이름>)·L262-L266(경로 형식 /metrics/job/<JOB_NAME>)·L366-L370(PUT 은 그룹 전체를 교체)·L409-L411(POST 는 이름이 같은 메트릭만 교체).
# Layout conventions: 레인 5·폭 180·간격 187, 호출 한 건의 stride 60(라벨 y-9, 부라벨 y+17), 첫 메시지 y=192. 구분선은 마지막 메시지 +64, 자기 호출은 구분선 +64. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, Seq, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 13, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 13, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, sw=1.5, dx=0):
        x1, x2 = s.LX[a], s.LX[b]
        d_ = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d_} {y} L {x2 - 12 * d_} {y}", c, sw, m=mk, dash=dash)
        mx = (x1 + x2) / 2 + dx
        s.t(mx, y - 9, label, 13, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 13, MUTED, _kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None, mk="ar"):
        x = s.LX[a]
        s.path(f"M {x + 10} {y - 10} L {x + 58} {y - 10} L {x + 58} {y + 10} L {x + 13} {y + 10}", c, 1.4, m=mk)
        s.t(x + 68, y - 2, label, 13, c, _kr(label), "start", 600)
        if sub:
            s.t(x + 68, y + 15, sub, 13, MUTED, _kr(sub), "start")

    def divider(s, y, txt, c=MUTED):
        s.line(24, y, s.w - 24, y, c, 0.8, "6 5")
        kr = any("가" <= ch <= "힣" for ch in txt)
        w = len(txt) * (12.5 if kr else 7.4) + 24
        s.o.append(f'<rect x="{s.w / 2 - w / 2}" y="{y - 11}" width="{w}" height="22" rx="4" fill="#0D1117" stroke="{c}" stroke-width="0.8"/>')
        s.t(s.w / 2, y + 4, txt, 13, c, _kr(txt), "middle")


W, H = 1000, 860
d = SeqKR(W, H, "BYTEBYTEGO · 08-03 §3",
          "수집기는 목록을 받아 당기고 배치 작업은 밀어 둔 곳을 당긴다",
          "scrape 간격 기본 1m·제한 시간 기본 10s 와 up 값, Pushgateway 로 밀기까지 한 흐름에 놓았습니다.",
          "Prometheus v3.15.0 · Pushgateway v1.11.4 기준입니다")
P, S, T, G, B = "수집기", "서비스 디스커버리", "대상 앱", "Pushgateway", "배치 작업"
d.lanes([(P, "Prometheus"), (S, "kubernetes_sd_configs"), (T, "/metrics 노출"), (G, "배치 작업 결과"), (B, "서비스 단위")], 100, 180)
d.rails(H - 80)

Y0, ST = 192, 60
d.msg(P, S, "대상 목록 조회", Y0 + 0 * ST, INFO, "info", sub="role: pod")
d.msg(S, P, "대상 주소 목록", Y0 + 1 * ST, INFO, "info", dash="5 4", sub="클러스터가 바뀌면 갱신")
d.msg(P, T, "HTTP /metrics", Y0 + 2 * ST, MUTED, "ar", sub="scrape_interval 1m")
d.msg(T, P, "응답 · 텍스트 형식", Y0 + 3 * ST, OK, "ok", dash="5 4", sub="up = 1")
d.divider(Y0 + 4 * ST + 4, "10s 안에 답이 없으면", ACC)
d.selfmsg(P, "up = 0 기록", Y0 + 5 * ST + 8, BAD, sub="scrape_timeout 10s", mk="bad")
d.divider(Y0 + 6 * ST + 12, "밀기: 서비스 단위 배치 작업", ACC)
d.msg(B, G, "POST", Y0 + 7 * ST + 20, MUTED, "ar", sub="/metrics/job/<이름>")
d.msg(P, G, "HTTP /metrics", Y0 + 8 * ST + 20, MUTED, "ar", sub="Pushgateway 도 대상 하나")
d.msg(G, P, "밀린 값 그대로", Y0 + 9 * ST + 20, OK, "ok", dash="5 4", sub="지우기 전까지 계속 노출")

d.legend(H - 56, [("요청", MUTED), ("디스커버리", INFO), ("응답", OK), ("실패", BAD), ("분기", ACC)])
d.save("08-03.pull-push-sequence.svg")
