# 생성기

이 폴더의 `gen-*.py` 가 `../*.svg` 의 **정본**이다. SVG 는 산출물이므로 손으로 고치지 않는다.
고칠 일이 생기면 생성기를 고쳐 다시 돌린다.

각 스크립트 머리말에 *왜 그 형태를 골랐는지* 가 적혀 있다. 대개 본문이 형태를 지정하기 때문이다 —
예컨대 `07-01.external-to-cluster-ladder` 는 본문이 "네 사다리를 순서대로" 라 적고,
`14-01.role-binding-scope` 는 "위 도식의 점선" 이라며 도식을 직접 가리킨다.

## 돌리는 법

생성기는 `_assets` 를 현재 디렉토리로 두고 돌린다. `dd.py` 를 저장소 밖 임시 폴더에 두고
`PYTHONPATH` 로 잡아 주면 `_gen/` 이 깨끗하게 남는다 — 자매 책 `kubernetes-in-action` 과 같은 규약이다.

```bash
SC=~/claude/.claude/skills/writing-method/assets/scripts
mkdir -p /tmp/ddmod && cp $SC/dd-primitives.py /tmp/ddmod/dd.py

cd _assets                                       # ← 여기서 돌린다
PYTHONPATH="/tmp/ddmod:_gen" python3 _gen/gen-<이름>.py    # 옆에 svg 를 뱉는다

python3 $SC/dd-overflow-check.py <svg>
python3 $SC/dd-lint.py <svg>
$SC/dd-render.sh <svg>                           # shots/ 에 png
```

`d.save()` 경로는 파일명만 적는다. 한때 열둘이 `"../이름.svg"` 로 적혀 있어 `_gen` 에서 돌려야
제자리에 떨어졌는데, 나머지 열셋과 규약이 갈려 `_assets` 에서 한 번에 돌리면 책 루트로
파일이 흘렀다. 2026-08-30 에 전부 파일명만 쓰도록 맞췄다.

`dd.py` 는 정본이 바뀔 수 있으므로 커밋하지 않는다. `ddx.py` 는 이 저장소의 공용 헬퍼로,
`../../kubernetes-in-action/_assets/_gen/ddx.py` 와 같은 파일이다.

**오버플로 검사가 0 건이어도 눈으로 봐야 한다.** 검사기는 viewBox 밖만 본다 —
상자 안쪽 넘침, 화살표가 주석을 관통하는 것, 안쪽 상자가 바깥 상자를 뚫고 나가는 것은
전부 통과시킨다. 이 책에서도 실제로 그 셋이 나왔다.
