# 생성기

이 폴더의 `gen-*.py` 가 `../*.svg` 의 **정본**이다. SVG 는 산출물이므로 손으로 고치지 않는다.
고칠 일이 생기면 생성기를 고쳐 다시 돌린다.

각 스크립트 머리말에 *왜 그 형태를 골랐는지* 가 적혀 있다. 대개 본문이 형태를 지정하기 때문이다 —
예컨대 `07-01.external-to-cluster-ladder` 는 본문이 "네 사다리를 순서대로" 라 적고,
`14-01.role-binding-scope` 는 "위 도식의 점선" 이라며 도식을 직접 가리킨다.

## 돌리는 법

```bash
cp ~/claude/.claude/skills/writing-method/assets/scripts/dd-primitives.py ./dd.py
python3 gen-<이름>.py                     # 같은 폴더에 svg 를 뱉는다
python3 ~/claude/.claude/skills/writing-method/assets/scripts/dd-overflow-check.py <svg>
~/claude/.claude/skills/writing-method/assets/scripts/dd-render.sh <svg>   # shots/ 에 png
```

`dd.py` 는 정본이 바뀔 수 있으므로 커밋하지 않는다. `ddx.py` 는 이 저장소의 공용 헬퍼로,
`../../kubernetes-in-action/_assets/_gen/ddx.py` 와 같은 파일이다.

**오버플로 검사가 0 건이어도 눈으로 봐야 한다.** 검사기는 viewBox 밖만 본다 —
상자 안쪽 넘침, 화살표가 주석을 관통하는 것, 안쪽 상자가 바깥 상자를 뚫고 나가는 것은
전부 통과시킨다. 이 책에서도 실제로 그 셋이 나왔다.
