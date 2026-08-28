# 09-03 §2 — ..data 하나만 튼다
# 본문이 물증을 든다 — 개별 파일 심링크의 mtime 은 그대로인데 두 파일 내용이 함께 바뀐다.
# 그러니 갱신 전후를 나란히 놓고 무엇이 바뀌고 무엇이 그대로인지가 보여야 한다.
# 타입 스펙: type-dp-security-matrix.md — 갱신 전과 후를 같은 슬롯(개별 심링크 · ..data · 가리켜지는 디렉터리)으로 나란히 둔다.
#           무엇이 그대로이고 무엇이 바뀌었는지가 같은 자리끼리의 대조로 읽힌다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 680, "KUBERNETES IN ACTION · 09-03",
      "링크 하나만 틀어 전부를 동시에 바꾼다",
      "개별 파일 심링크는 손대지 않고 ..data 만 새 디렉터리로 튼다. 그래서 여러 파일이 "
      "반쯤 갱신된 상태 없이 함께 바뀐다.",
      "kind 실측 — 고친 뒤 반영까지 약 62 초")

def stage(x0, label, tsdir, content, focal):
    d.box(x0, 176, 520, 300, PAPER, RULE, 0.9, 8)
    d.t(x0 + 260, 204, label, 11, SOFT, KR)
    d.t(x0 + 30, 248, "app.conf", 11, MUTED, MONO, "start")
    d.t(x0 + 160, 248, "->  ..data/app.conf", 11, MUTED, MONO, "start")
    d.t(x0 + 30, 274, "db.conf", 11, MUTED, MONO, "start")
    d.t(x0 + 160, 274, "->  ..data/db.conf", 11, MUTED, MONO, "start")
    d.t(x0 + 30, 300, "mtime 17:06 그대로", 10, SOFT, KR, "start")
    if focal:
        d.o.append(f'<rect x="{x0+24}" y="330" width="472" height="46" rx="5" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        d.t(x0 + 40, 358, f"..data  ->  {tsdir}", 11, ACC, MONO, "start")
    else:
        d.box(x0 + 24, 330, 472, 46, PAPER2, RULE, 1.0, 5)
        d.t(x0 + 40, 358, f"..data  ->  {tsdir}", 11, MUTED, MONO, "start")
    d.box(x0 + 24, 392, 472, 60, PAPER2, OK if focal else RULE, 1.0, 5)
    d.t(x0 + 40, 418, tsdir, 10, OK if focal else SOFT, MONO, "start")
    d.t(x0 + 40, 440, f"app.conf · db.conf  내용: {content}", 10, MUTED, MONO, "start")

stage(60, "갱신 전", "..2026_08_14_17_06_11.881", "before", False)
stage(660, "갱신 후 — 새 디렉터리가 생기고 대상만 바뀐다", "..2026_08_14_17_07_32.211", "after", True)
d.path("M 588 326 L 648 326", MUTED, 1.5, m="ar")

d.t(24, 528, "물증은 mtime 이다. app.conf·db.conf 심링크의 mtime 은 처음 그대로인데 두 파일 내용은 함께 바뀐다 — "
             "개별 링크를 건드리지 않았다는 뜻이다.", 11, MUTED, KR, "start")
d.t(24, 550, "여러 파일을 하나씩 덮어썼다면 그 사이에 반쯤 갱신된 상태가 보였을 것이다. 링크 하나를 트는 것은 "
             "그 중간 상태를 없앤다.", 11, MUTED, KR, "start")
d.t(24, 572, "반영은 즉시가 아니다. 같은 실측에서 약 62 초가 걸렸고, 08-02 에서 잰 56 초와 같은 계통이다.",
     11, MUTED, KR, "start")
d.legend(600, [("틀어지는 링크", ACC), ("가리켜지는 실체", OK)])
d.save("09-03-symlink-atomic-update.svg")
print("ok")
