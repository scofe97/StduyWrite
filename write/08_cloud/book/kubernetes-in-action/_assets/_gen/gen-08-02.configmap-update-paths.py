# 08-02 §5 — 한 번의 수정이 세 갈래로 갈린다
# 짝 도식(env-vs-file-choice)이 선택 기준을 맡으므로 이쪽은 '수정한 뒤 무슨 일이 나는가'만
# 본다. 그래서 표가 아니라 수정 하나에서 뻗는 갈래여야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 620, "KUBERNETES IN ACTION · 08-02",
      "같은 수정인데 반영이 셋으로 갈린다",
      "ConfigMap 을 고치는 일은 한 번이지만, 그 값이 컨테이너에 어떻게 놓여 있었느냐에 따라 "
      "반영되는지도 반영하는 방법도 달라진다.",
      "kubectl edit configmap kiada-config")

ddx.node(d, 150, 320, "ConfigMap 수정", "값 한 줄을 고쳤다", 220, 88, INFO)

PATHS = [("환경변수로 받았다면", "기존 값 그대로", "Pod 롤링 교체", 190, BAD),
         ("일반 볼륨으로 받았다면", "kubelet 동기화 후 파일 갱신", "앱이 파일을 다시 읽기", 320, ACC),
         ("subPath 로 받았다면", "파일이 갱신되지 않는다", "Pod 를 새로 생성", 450, WARN)]
for t, res, fix, cy, c in PATHS:
    d.box(420, cy - 40, 340, 80, PAPER2, c, 1.1, 6)
    d.t(440, cy - 12, t, 12, c, KR, "start", 600)
    d.t(440, cy + 14, res, 11, MUTED, KR, "start")
    d.path(f"M 262 320 L 414 {cy}", c, 1.4, m="acc" if c is ACC else ("bad" if c is BAD else "warn"))
    ddx.node(d, 940, cy, fix, "새 설정을 적용하려면", 280, 68, c)
    d.path(f"M 762 {cy} L 794 {cy}", c, 1.3, m="acc" if c is ACC else ("bad" if c is BAD else "warn"))

d.t(24, 528, "가운데 갈래만 파드를 건드리지 않는다. 다만 즉시가 아니라 kubelet 동기화 주기만큼 늦고, "
             "파일이 바뀌어도 앱이 다시 읽지 않으면 실제 동작은 그대로다.", 11, MUTED, KR, "start")
d.legend(552, [("바뀌지 않는다", BAD), ("파일만 갱신된다", ACC), ("갱신조차 안 된다", WARN)])
d.save("08-02-configmap-update-paths.svg")
print("ok")
