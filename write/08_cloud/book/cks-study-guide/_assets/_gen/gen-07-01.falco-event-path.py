# 07-01 §1 — Falco 는 시스템 콜 이벤트를 드라이버가 모아 규칙 엔진이 조건식과 대조하고, 맞으면 출력 채널로 경보를 낸다. 규칙 파일은 rules_files 순서대로 쌓인다.
# 본문 근거: 이 노트 ### 1 「Falco로 이상 행위 잡기」.
# 검증 근거: falcosecurity/falco:0.45.2 이미지를 modern eBPF 로 실행해 Terminal shell in container 와 Write below etc 경보가
#            override 한 출력으로 찍히고 file_output 이 /var/log/falco.log 에 덧붙는 것을 확인.
#            sandbox 파일 없이 Write below etc 를 override 하면 falco --validate 가 "no rule by that name already exists" 로 실패.
# 공식 근거: falco 0.45.2 falco.yaml 의 engine.kind·rules_files·*_output, falco-website overriding.md 의 적재 순서.
# 타입 스펙: type-swimlane — 이벤트 레인과 규칙 파일 레인.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 432
d = D(W, H, "CKS STUDY GUIDE · 07-01 §1",
      "Falco 가 시스템 콜 이벤트를 경보로 바꾸는 길과 규칙 파일이 쌓이는 순서",
      "위 레인은 컨테이너 프로세스의 시스템 콜을 드라이버가 모으고 규칙 엔진이 규칙의 조건식과 맞대어 보고 맞으면 출력 채널로 경보를 내보내는 흐름이고, "
      "아래 레인은 rules_files 에 적힌 순서대로 falco_rules.yaml, falco-sandbox_rules.yaml, falco_rules.local.yaml 이 적재되며 뒤 파일의 override 가 앞 파일의 규칙을 고치는 흐름이다.",
      "경보는 이벤트와 규칙이 맞을 때 나오고, 규칙 파일은 적힌 순서대로 쌓입니다")

BW, BH, PITCH, X0 = 190, 76, 212, 24
LANE_X, LANE_W, LANE_H = 12, 856, 132
A_Y, S_Y = 96, 244


def lane(y, name):
    d.o.append(f'<rect x="{LANE_X}" y="{y}" width="{LANE_W}" height="{LANE_H}" rx="8" fill="{SOFT}0A" stroke="{SOFT}" stroke-width="0.9"/>')
    d.t(LANE_X + 12, y + 20, name, 12, MUTED, KR, "start", 600)


def lane_steps(y, items):
    by = y + 40
    for i, (title, sub, c) in enumerate(items):
        x = X0 + i * PITCH
        d.tone(x, by, BW, BH, c, 6, "14", 1.4 if c == ACC else 1.1)
        d.t(x + BW / 2, by + 32, title, 13, INK, KR, "middle", 600)
        d.t(x + BW / 2, by + 56, sub, 11, MUTED, MONO)
        if i < len(items) - 1:
            d.path(f"M {x + BW + 2} {by + BH / 2} L {x + PITCH - 2} {by + BH / 2}", MUTED, 1.4, m="ar")


lane(A_Y, "이벤트가 경보가 되기까지")
lane_steps(A_Y, [
    ("컨테이너 프로세스", "openat · execve", INFO),
    ("드라이버", "engine.kind: modern_ebpf", INFO),
    ("규칙 엔진", "condition 과 대조", ACC),
    ("출력 채널", "stdout · file", SOFT),
])
lane(S_Y, "규칙 파일이 쌓이는 순서")
lane_steps(S_Y, [
    ("stable 규칙 파일", "falco_rules.yaml", INFO),
    ("sandbox 규칙 파일", "falco-sandbox_rules.yaml", WARN),
    ("로컬 규칙 파일", "falco_rules.local.yaml", ACC),
    ("규칙 엔진", "적재 끝, 이벤트 대조", SOFT),
])

d.legend(392, [("수집과 규칙 원본", INFO), ("추가로 적재해야 하는 파일", WARN), ("대조와 수정이 일어나는 자리", ACC), ("결과", SOFT)])
d.save("07-01.falco-event-path.svg")
