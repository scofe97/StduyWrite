# 08-02 §5 — 무중단이되 즉시가 아니다
# 본문이 실측값(kind v1.35 에서 약 56 초)과 "파드 UID·restartCount 는 그대로"를 함께 든다.
# 시간축 하나로는 그 둘이 안 보이므로, 지연 구간과 변하지 않은 것을 같이 얹는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 580, "KUBERNETES IN ACTION · 08-02",
      "파드를 건드리지 않지만 즉시도 아니다",
      "일반 볼륨의 파일 갱신은 파드를 교체하거나 컨테이너를 재시작하지 않고 일어난다. "
      "다만 kubelet 동기화 주기와 캐시 전파만큼 늦는다.",
      "kind-k8s-lab v1.35 실측 — 약 56 초")

X = lambda t: 130 + t * 15.4   # 0~70s 를 130~1208px 에
AX = 356

d.o.append(f'<rect x="{X(0)}" y="176" width="{X(56)-X(0)}" height="56" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t((X(0) + X(56)) / 2, 210, "옛 값이 파일에 그대로 남아 있다", 12, ACC, KR)
d.o.append(f'<rect x="{X(56)}" y="176" width="{X(70)-X(56)}" height="56" rx="6" '
           f'fill="{OK}12" stroke="{OK}" stroke-width="1.1"/>')
d.t((X(56) + X(70)) / 2, 210, "새 값", 12, OK, KR)

d.o.append(f'<rect x="{X(0)}" y="252" width="{X(70)-X(0)}" height="52" rx="6" '
           f'fill="{OK}0A" stroke="{OK}" stroke-width="1.0" stroke-dasharray="6 5"/>')
d.t((X(0) + X(70)) / 2, 284, "파드 UID 그대로  ·  restartCount 그대로 — 무중단", 11, OK, KR)

d.line(X(0) - 12, AX, X(70) + 16, AX, RULE, 1.0)
for t in (0, 10, 20, 30, 40, 50, 60, 70):
    d.line(X(t), AX - 5, X(t), AX + 5, RULE, 1.0)
    d.t(X(t), AX + 22, f"{t}s", 9, SOFT, MONO)
for t, lab in ((0, "ConfigMap 을 고쳤다"), (56, "마운트 파일이 바뀌었다")):
    d.line(X(t), 236, X(t), AX - 6, ACC if t else SOFT, 1.0, "4 4")
    d.t(X(t) + 8, 330, lab, 10, ACC if t else SOFT, KR, "start" if t == 0 else "end")

def span(t0, t1, y, label, c):
    x0, x1 = X(t0), X(t1)
    d.path(f"M {x0} {y-7} L {x0} {y} L {x1} {y} L {x1} {y-7}", c, 1.2)
    d.t((x0 + x1) / 2, y + 18, label, 10, c, KR)
span(0, 56, 412, "약 56 초 — kubelet 동기화 주기와 캐시 전파", ACC)

d.t(24, 476, "지연의 크기는 kubelet 의 configMapAndSecretChangeDetectionStrategy 를 따른다 — "
             "watch(기본) · ttl 기반 · API 서버 직접 조회 셋이다.", 11, MUTED, KR, "start")
d.t(24, 498, "그리고 이것은 파일 내용의 갱신일 뿐이다. 앱이 파일을 다시 읽지 않으면 실제 동작은 이전 설정을 계속 쓴다.",
     11, MUTED, KR, "start")
d.legend(520, [("옛 값이 남아 있는 구간", ACC), ("변하지 않은 것", OK)])
d.save("08-02-kubelet-sync-delay.svg")
print("ok")
