# 09-03 §2 — 심링크는 경로를 담은 파일이다
# 뒤 도식 둘(원자적 갱신·subPath)이 심링크 체인 위에 서 있으므로, 여기서 "무엇을 가리키는
# 포인터"라는 사실이 확실히 잡혀야 한다. 내용이 아니라 경로를 담는다는 점이 요점이다.
# 타입 스펙: type-architecture.md — 심링크 상자와 실파일 노드 둘, 그리고 커널이 따라가는 화살표 하나로 이뤄진 구성도다.
#           뒤 도식 둘이 이 체인 위에 서므로 여기서는 관계 하나만 확실히 세운다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1180, 600, "KUBERNETES IN ACTION · 09-03",
      "내용이 아니라 경로를 담는다",
      "심볼릭 링크는 다른 경로를 적어 둔 작은 파일이다. 열면 커널이 그 경로를 따라가 진짜 파일을 "
      "열어 주므로, 읽는 쪽은 링크인지 알 필요가 없다.",
      "ls -l 의 맨 앞 l 과 -> 가 그 표시다")

d.o.append(f'<rect x="90" y="200" width="360" height="96" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(270, 234, "app.conf", 14, ACC, MONO, "middle", 600)
d.t(270, 262, "담긴 것: \"..data/app.conf\"", 11, MUTED, MONO)
d.t(270, 284, "경로 한 줄", 10, SOFT, KR)
d.t(270, 176, "심링크", 11, SOFT, KR)

ddx.node(d, 830, 248, "..data/app.conf", "진짜 내용이 여기 있다", 320, 96, OK)
d.t(830, 176, "실파일", 11, SOFT, KR)
d.path("M 454 248 L 664 248", ACC, 1.6, m="acc")
d.t(559, 230, "커널이 따라간다", 11, ACC, KR)

d.t(90, 356, "ls -l", 11, SOFT, MONO, "start")
d.t(160, 356, "lrwxrwxrwx  app.conf -> ..data/app.conf", 11, ACC, MONO, "start")
d.t(90, 382, "cat", 11, SOFT, MONO, "start")
d.t(160, 382, "진짜 파일의 내용이 나온다 — 읽는 쪽은 링크인 줄 모른다", 11, MUTED, KR, "start")

d.t(24, 462, "그래서 링크가 가리키는 대상을 바꾸면, 같은 이름으로 다른 파일을 보게 만들 수 있다. "
             "configMap 볼륨의 원자적 갱신이 이 성질을 쓴다.", 11, MUTED, KR, "start")
d.t(24, 484, "링크 자신의 mtime 은 대상이 바뀌어도 그대로다 — 다음 도식에서 그것이 물증이 된다.",
     11, MUTED, KR, "start")
d.legend(512, [("경로를 담은 파일", ACC), ("내용을 담은 파일", OK)])
d.save("09-03-what-is-symlink.svg")
print("ok")
