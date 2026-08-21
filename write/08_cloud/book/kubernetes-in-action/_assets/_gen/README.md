# 도식 생성 스크립트

이 폴더의 `gen-<도식이름>.py` 가 SSOT 다. `_assets/*.svg` 는 산출물이므로 **손으로 고치지 않는다.**
고칠 것이 있으면 생성 스크립트를 고쳐 다시 만든다.

## 실행

프리미티브 `dd.py` 는 저장소에 두지 않고 정본에서 가져다 쓴다.

```bash
cd _gen
cp ~/claude/.claude/skills/writing-method/assets/scripts/dd-primitives.py dd.py
python3 gen-11-01.chapter-overview.py            # 같은 폴더에 svg 생성
python3 ~/claude/.claude/skills/writing-method/assets/scripts/dd-overflow-check.py *.svg
~/claude/.claude/skills/writing-method/assets/scripts/dd-render.sh *.svg   # PNG 로 눈 확인 후 삭제
```

`ddx.py` 는 이 책이 반복해 쓰는 형태(띠·행렬·체인·시퀀스·넘침 가드)를 모아 둔 장 공용 헬퍼다.
`ddx.fit()` 은 박스 *안쪽* 넘침을 잡는다 — `dd-overflow-check.py` 는 viewBox 밖만 보므로 겹침과
박스 내부 넘침은 못 잡는다. 그래서 렌더한 PNG 를 반드시 눈으로 본다.
