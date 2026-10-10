# 타입 스펙: type-swimlane — 같은 설치를 cilium CLI 와 helm 두 경로로 낼 때 명령·값·차트 단계가 갈리고 같은 Helm 릴리스로 모인다.
# 사실 출처: cil3.txt 줄 226~414 (cilium install --dry-run-helm-values, helm install -n kube-system --version, cilium status DaemonSet 3/3·Deployment 1/1), github.com/cilium/cilium-cli README (install 이 Helm 릴리스를 만든다, helm list·helm get values).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 380
d = D(W, H, "CILIUM UP AND RUNNING · 03-01 §3", "설치 두 경로가 한 릴리스로 모인다",
      "cilium CLI 는 값을 자동으로 채우고 helm 은 값 파일을 직접 쓴다",
      "두 경로가 만드는 결과는 kube-system 의 Helm 릴리스 하나")

Y0, LANE_H = 104, 112
COLS = [(160, 168), (344, 168), (528, 168)]   # (x, w): 명령 · 값 · 차트
X_REL, W_REL = 720, 176

# 열 머리
for (x, w), lab in zip(COLS, ["명령", "값", "차트"]):
    d.t(x + w / 2, Y0 + 14, lab, 12, SOFT, KR, "middle", 600)
d.t(X_REL + W_REL / 2, Y0 + 14, "결과", 12, SOFT, KR, "middle", 600)

lanes = [
    ("CLI 경로", INFO, ["cilium install", "cilium upgrade"], ["자동 감지", "--dry-run-helm-values"]),
    ("Helm 경로", ACC, ["helm install", "helm upgrade"], ["값 파일", "helm-values.yaml"]),
]
for k, (name, col, cmds, vals) in enumerate(lanes):
    y = Y0 + 28 + k * (LANE_H + 8)
    d.box(24, y, 124, LANE_H, PAPER2, RULE, sw=0.9, r=6)
    d.t(86, y + LANE_H / 2 + 4, name, 12, col, KR, "middle", 600)
    # 명령
    x, w = COLS[0]
    d.box(x, y, w, LANE_H, PAPER, RULE, sw=0.8, r=6)
    d.t(x + w / 2, y + 44, cmds[0], 11, INK, MONO, "middle", 600)
    d.t(x + w / 2, y + 72, cmds[1], 11, MUTED, MONO, "middle")
    # 값
    x, w = COLS[1]
    d.box(x, y, w, LANE_H, PAPER, RULE, sw=0.8, r=6)
    d.t(x + w / 2, y + 44, vals[0], 12, INK, KR, "middle", 600)
    d.t(x + w / 2, y + 72, vals[1], 11, MUTED, MONO, "middle")
    # 차트
    x, w = COLS[2]
    d.box(x, y, w, LANE_H, PAPER, RULE, sw=0.8, r=6)
    d.t(x + w / 2, y + 44, "Helm 차트", 12, INK, KR, "middle", 600)
    d.t(x + w / 2, y + 72, "--version 1.20.2", 11, MUTED, MONO, "middle")
    ym = y + LANE_H / 2
    d.arrow([(COLS[0][0] + COLS[0][1] + 2, ym), (COLS[1][0] - 2, ym)], MUTED, "ar", 1.3)
    d.arrow([(COLS[1][0] + COLS[1][1] + 2, ym), (COLS[2][0] - 2, ym)], MUTED, "ar", 1.3)
    d.arrow([(COLS[2][0] + COLS[2][1] + 2, ym), (X_REL - 2, ym)], col, "acc" if col == ACC else "info", 1.5)

# 결과: 두 레인에 걸친 릴리스 상자 (focal)
yr, hr = Y0 + 28, 2 * LANE_H + 8
d.tone(X_REL, yr, W_REL, hr, ACC, r=6, op="12", sw=1.4)
d.t(X_REL + W_REL / 2, yr + 36, "Helm 릴리스", 12, ACC, KR, "middle", 600)
d.t(X_REL + W_REL / 2, yr + 60, "cilium", 12, INK, MONO, "middle", 600)
d.t(X_REL + W_REL / 2, yr + 80, "kube-system", 11, MUTED, MONO, "middle")
d.line(X_REL + 14, yr + 100, X_REL + W_REL - 14, yr + 100, RULE, 0.6)
d.t(X_REL + W_REL / 2, yr + 128, "cilium  3/3", 11, INK, MONO, "middle")
d.t(X_REL + W_REL / 2, yr + 152, "cilium-envoy  3/3", 11, INK, MONO, "middle")
d.t(X_REL + W_REL / 2, yr + 176, "cilium-operator  1/1", 11, INK, MONO, "middle")
d.t(X_REL + W_REL / 2, yr + 200, "(노드 3 기준)", 11, MUTED, KR, "middle")

d.save("03-01.cilium-install-cli-vs-helm.svg")
