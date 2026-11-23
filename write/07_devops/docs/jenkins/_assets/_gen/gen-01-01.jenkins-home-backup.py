# 타입 스펙: type-tree
# 4절 JENKINS_HOME 과 master.key 백업 — 디렉터리 트리를 백업·따로 보관·빼도 됨으로 가르고 키 파일의 암호화 사슬을 옆에 둔다
"""01-01 JENKINS_HOME 백업 분류와 암호화 사슬 — 도식 생성기.

실행: cd ~/runners-high/write/07_devops/docs/jenkins/_assets && python3 -B _gen/gen-01-01.jenkins-home-backup.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import (D, PAPER, PAPER2, INK, MUTED, RULE, ACC,  # noqa: E402
                OK, INFO, KR, MONO)

W, H = 960, 580

d = D(
    W, H,
    "JENKINS · JENKINS_HOME BACKUP MAP",
    "JENKINS_HOME 에서 백업할 것과 따로 보관할 것",
    "JENKINS_HOME 아래 파일을 백업, 일반 백업과 분리, 빼도 됨으로 가르고 master.key 에서 자격 증명을 지키는 데이터까지 이어지는 암호화 순서를 함께 보인다",
    lead="왼쪽은 파일마다 갈린 백업 판단, 오른쪽은 키 파일이 자격 증명을 지키는 데이터를 감싸는 순서"
)


def fam(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


def chip_box(cx, cy, txt, c):
    w = len(txt) * 13.0 + 20
    cx = 584 - w / 2  # 오른쪽 끝을 맞춘다
    d.o.append(f'<rect x="{cx - w / 2}" y="{cy - 12}" width="{w}" height="24" rx="4" '
               f'fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
    d.t(cx, cy + 5, txt, 13, c, KR, "middle", 600)


# 행: (들여쓰기 단계, 경로, 설명, 분류)
TREE = [
    (0, "$JENKINS_HOME", "", None),
    (1, "*.xml", "전역 설정", "백업"),
    (1, "jobs/", "잡별 정보", "백업"),
    (2, "<잡>/builds/", "빌드 기록", "백업"),
    (2, "<잡>/builds/archive/", "보관한 산출물", "백업"),
    (1, "plugins/*.jpi · *.hpi", "플러그인 패키지", "백업"),
    (1, "secrets/master.key", "마스터 키", "따로 보관"),
    (1, "secrets/hudson.util.Secret", "controller key", "일반 백업 금지"),
    (1, "workspace/", "체크아웃한 파일", "빼도 됨"),
    (1, "plugins/<이름>/", "풀어 놓은 플러그인", "빼도 됨"),
    (1, "war/ · cache/ · tools/", "WAR · 캐시 · 도구", "빼도 됨"),
]
COL = {"백업": OK, "따로 보관": ACC, "일반 백업 금지": ACC, "빼도 됨": INFO}
Y0, STRIDE = 112, 36

# focal: 따로 보관 두 줄을 한 덩어리로
fy = Y0 + 6 * STRIDE
d.tone(28, fy - 2, 576, STRIDE * 2 - 4, ACC, r=6, op="12", sw=1.4)

# 세로 줄기
d.line(44, Y0 + 24, 44, Y0 + 10 * STRIDE + 16, RULE, 1.0)
d.line(76, Y0 + 2 * STRIDE + 24, 76, Y0 + 4 * STRIDE + 16, RULE, 1.0)
for i, (lv, path, desc, cat) in enumerate(TREE):
    y = Y0 + i * STRIDE
    cy = y + 18
    x = 40 + lv * 32
    if lv > 0:
        d.line(x - 16 if lv == 1 else x - 16, cy, x - 4, cy, RULE, 1.0)
    d.t(x, cy + 5, path, 13, INK, MONO, "start", 600 if lv == 0 else 400)
    if desc:
        d.t(330, cy + 5, desc, 13, MUTED, fam(desc), "start")
    if cat:
        chip_box(548, cy, cat, COL[cat])

# 오른쪽: 암호화 사슬
d.o.append(f'<rect x="640" y="100" width="296" height="404" rx="8" fill="{INK}05" stroke="{INK}1A" stroke-width="0.8"/>')
d.o.append(f'<rect x="652" y="106" width="92" height="18" rx="2" fill="{PAPER}"/>')
d.t(660, 120, "암호화 사슬", 13, MUTED, KR, "start", 600)
chain = [(148, "secrets/master.key", MONO), (264, "secrets/hudson.util.Secret", MONO), (380, "자격 증명을 지키는 데이터", KR)]
for k, (y, label, ff) in enumerate(chain):
    c = ACC if k == 0 else INFO
    d.box(660, y, 256, 56, PAPER2, c, 1.2, 6)
    d.t(788, y + 33, label, 13, INK, ff, "middle", 600)
for y in (204, 320):
    d.arrow([(788, y), (788, y + 60)], MUTED, "ar", 1.4)
    d.t(804, y + 36, "암호화", 13, MUTED, KR, "start")

d.legend(524, [
    ("백업", OK),
    ("일반 백업과 분리", ACC),
    ("빼도 됨", INFO),
])

out = pathlib.Path(__file__).resolve().parent.parent / "01-01.jenkins-home-backup.svg"
d.save(str(out))
print("saved", out)
