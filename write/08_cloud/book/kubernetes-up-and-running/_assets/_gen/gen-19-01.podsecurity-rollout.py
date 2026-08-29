# 19-01 §Pod Security — 강제하기 전에 재는 법
# 본문이 순서를 명시한다 — "낮은 표준으로 강제해 두고 높은 표준으로는 경고와 감사만 받는다.
# 무엇이 깨질지 목록을 모은 뒤 고치고, 그다음에 강제 수준을 올린다."
# 그러니 3표준·3모드를 격자로 늘어놓기만 하면 안 되고 *시간 순서* 가 형태로 있어야 한다.
# 위에 재료(표준·모드)를 두고 아래에 그 재료를 쓰는 4 단계 사다리를 둔다.
# 1 단계에 초점을 준다 — dry-run 평가가 이 장에서 실무적으로 가장 값한 명령이다.
# 타입 스펙: type-process.md — 네 단계가 같은 의미 슬롯(번호 · 하는 일 · 명령 · 돌아오는 것)으로
#           반복되고 단계 사이를 아래 화살표가 잇는다. 본문이 "재고 → 낮게 막고 높게 보고 →
#           고치고 → 올린다" 라고 순서를 명시하므로 3×3 격자로 늘어놓으면 안 된다.
#           어긋나는 지점: 정본의 lane=주체가 없다. 위 재료 띠(표준 셋 · 모드 셋)는 절차가 아니라
#           그 절차가 쓰는 어휘를 먼저 깔아 둔 것이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, SOFT, INK, PAPER2, PAPER, RULE, INFO, KR, MONO
import ddx

W, H = 1240, 756
d = D(W, H, "KUBERNETES UP AND RUNNING · 19-01",
      "강제하기 전에 무엇이 깨질지 먼저 잰다",
      "Pod Security 는 검증만 한다. 세 표준과 세 모드를 함께 걸어 낮은 쪽으로 막고 높은 쪽으로 "
      "관찰한 뒤, 고치고 나서 올린다.",
      "kind 로컬 클러스터 실측 — 서버 v1.35.0 · 경고 줄 수는 실제로 받은 값")

# --- 재료: 표준 3 · 모드 3 ---
d.t(24, 126, "표준 — 무엇을 요구하는가", 9, SOFT, KR, "start")
STD = [("Privileged", "열려 있고 제한 없음", MUTED),
       ("Baseline", "흔한 권한 상승을 막음", OK),
       ("Restricted", "모범 사례 전면. 깨질 수 있음", WARN)]
for i, (nm, sub, c) in enumerate(STD):
    x = 24 + i * 196
    d.tone(x, 140, 186, 52, c, 6, "0C", 1.1)
    d.t(x + 14, 162, nm, 12, c, KR, "start", 600)
    d.t(x + 14, 180, ddx.fit(sub, 9, 160, sub), 9, MUTED, KR, "start")

d.t(628, 126, "모드 — 위반을 어떻게 다루는가", 9, SOFT, KR, "start")
MODE = [("enforce", "거부한다", BAD), ("warn", "허용하고 알린다", WARN),
        ("audit", "감사 로그에만 남긴다", INFO)]
for i, (nm, sub, c) in enumerate(MODE):
    x = 628 + i * 196
    d.tone(x, 140, 186, 52, c, 6, "0C", 1.1)
    d.t(x + 14, 162, nm, 12, c, MONO, "start", 600)
    d.t(x + 14, 180, ddx.fit(sub, 9, 160, sub), 9, MUTED, KR, "start")

d.line(24, 212, W - 48, 212, RULE, 0.8)
d.t(24, 234, "이 둘을 네임스페이스 라벨로 조합해 아래 순서로 굴린다", 11, SOFT, KR, "start")

# --- 사다리: 4 단계 ---
Y0, SH, SG = 252, 88, 12
STEPS = [
    ("01", "재 본다", "kubectl label --dry-run=server --overwrite ns --all \\\n"
     "  pod-security.kubernetes.io/enforce=baseline",
     "아무것도 바꾸지 않고 기존 파드가 통과하는지만 본다", "baseline 위반 3묶음 · restricted 16줄", ACC, True),
    ("02", "낮게 막고 높게 본다", "enforce: baseline  +  warn/audit: restricted",
     "막는 선은 낮게 두고 목표 선은 관찰만 한다", "깨지는 것 없이 목록이 쌓인다", OK, False),
    ("03", "고친다", "runAsNonRoot · capabilities.drop:[ALL] · seccompProfile\n"
     "allowPrivilegeEscalation: false",
     "경고에 적힌 필드를 그대로 채운다", "거부 메시지가 필드 단위로 알려 준다", INFO, False),
    ("04", "올린다", "enforce: restricted",
     "이제 올려도 깨지지 않는다", "위반 파드는 Forbidden 으로 거부", WARN, False),
]
for i, (no, title, cmd, why, result, c, focal) in enumerate(STEPS):
    y = Y0 + i * (SH + SG)
    if focal:
        d.tone(24, y, W - 72, SH, c, 8, "0C", 1.4)
    else:
        d.box(24, y, W - 72, SH, PAPER2, RULE, 1.0, 8)
    d.t(44, y + 30, no, 11, c, MONO, "start", 600)
    d.t(76, y + 30, title, 13, c if focal else INK, KR, "start", 600)
    d.t(76, y + 52, ddx.fit(why, 10, 260, why), 10, MUTED, KR, "start")
    for j, ln in enumerate(cmd.split("\n")):
        d.t(360, y + 28 + j * 16, ddx.fit(ln, 10, 520, ln), 10,
            c if focal else INK, MONO, "start")
    d.t(W - 92, y + 30, "→ " + result, 10, c, KR, "end")
    if i < len(STEPS) - 1:
        d.arrow([(W / 2 - 24, y + SH + 1), (W / 2 - 24, y + SH + SG - 1)], SOFT, "soft", 1.2)

BY = Y0 + 4 * (SH + SG) + 6
d.line(24, BY, W - 48, BY, RULE, 0.8)
d.t(24, BY + 22, "버전을 고정하지 않으면 표준 내용이 릴리스마다 바뀌어 같은 워크로드의 판정이 "
                 "조용히 달라진다. enforce-version 을 함께 적는다.", 11, MUTED, KR, "start")
d.legend(BY + 38, [("먼저 재는 자리", ACC), ("막는 선", OK), ("목표 선", WARN),
                   ("거부", BAD), ("관찰·안내", INFO)])
d.save("19-01.podsecurity-rollout.svg")
print("필요 h:", BY + 38 + 48, "· 실제:", H)
