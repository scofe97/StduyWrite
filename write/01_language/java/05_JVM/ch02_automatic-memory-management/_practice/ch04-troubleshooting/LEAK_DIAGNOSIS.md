# 누수 진단 실습 — jps → jstat → jmap

> 03-01 노트(명령줄 진단 도구)의 Phase 3 실습. *진단당할 JVM*(`LeakDemo`)을 일부러 띄우고
> 핵심 3도구로 메모리 누수를 추적한다. 노트가 설명한 "추세로 의심 → 스냅숏으로 확정" 순서를 실물로 재현한다.

## 관련 이론
- [03-01. 기본 문제 해결 도구 — 명령줄 도구](../../03-01.기본%20문제%20해결%20도구%20—%20명령줄%20도구.md)

## 실습 대상
- `LeakDemo.java` — static `List<byte[]>`에 1MB/라운드씩 누적, remove 없음.
  GC 루트(static)에서 도달 가능하므로 Full GC로도 회수 불가 = 누수.
- 실행: `java -Xmx256m -Xlog:gc:file=gc.log LeakDemo`
- JDK: Temurin 21.0.3 (Java 25 금지 규칙 준수)

## 진단 체인과 관측 결과

### ① jps -l — 프로세스 식별
여러 JVM(Gradle/IDEA/TPS operator) 사이에서 `-l`의 풀네임 덕에 `70805 LeakDemo`를 정확히 골랐다.
다른 모든 도구가 vmid를 인자로 받으므로 진단은 jps로 시작한다.

### ② jstat -gcutil <pid> 250 20 — 누수 추세 관찰 (256MB 회차 실측)
```
  S1      E      O      YGC   FGC   CGC
100.00   5.26  78.91    17    1    10    ← FGC 1회 이미 돌았음
100.00  89.47  79.43    18    1    10    ← 그래도 O 78→79%에서 안 빠짐
```
Eden(E)은 GC로 오르내리며 비워지는데 **Old(O)가 FGC=1 이후에도 78~79%에서 안 내려오고**,
Survivor(S1)는 100%로 꽉 차 객체가 계속 Old로 승격된다 = 누수.
(부하 증가였다면 Full GC 후 O가 함께 떨어졌어야 한다.)

### 256MB 힙 회차의 gc.log.4 — Full GC 회수 0 증거
```
GC(31) Pause Full (G1 Compaction Pause) 255M->255M(256M)   ← Full GC인데 255M→255M, 회수 0
GC(45) Pause Full (G1 Compaction Pause) 255M->255M(256M)   ← OOM 직전까지 연달아, 여전히 0
```
정상이면 `255M->50M`처럼 떨어진다. mark-compact(G1 Compaction)를 돌려도 안 줄면 누수 확정.
OOM 직전 구간에서 Full GC가 `GC(31)~GC(45)`로 폭발하는데도 전부 `255M->255M`이다 — 회수할 게 없다는 뜻.
(로그가 `gc.log.0~.4`로 갈린 건 -Xlog 로테이션. 전체는 `grep "Pause Full" gc.log*`로 본다.)

### ③ jmap — 범인 객체 확정
```
jmap -histo:live <pid>
 num   #instances     #bytes  class name
   1:      24705    23521104  [B          ← byte[]가 압도적 1위 = 범인 (수치는 관측 시점 따라 변동)
```
```
jmap -dump:live,format=b,file=leak.hprof <pid>
Unable to create .../leak.hprof: File exists   ← 덤프는 기존 파일을 덮어쓰지 않는다
```
`-histo`가 덤프 없이 빠르게 범인 클래스(`[B`=byte[])를 지목한다.
덤프(`-dump`)는 STW를 일으키는 무거운 작업이므로, 의심이 굳은 뒤에만 뜬다 —
단, 같은 파일명이 이미 있으면 `File exists`로 거부되니 회차마다 이름을 바꾸거나 지운 뒤 떠야 한다.
떠낸 .hprof는 운영 장비가 아니라 별도 장비의 Eclipse MAT/VisualVM으로 분석한다.

## 배운 점 (Phase 1 ↔ 실습 연결)
- "FGC 후에도 O 안 내려옴 = 누수"가 jstat의 `O 78→79% 고착`과 gc.log `255M->255M`으로 실증됐다.
- `-histo`가 덤프 없이 빠르게 범인 클래스를 지목 → 덤프는 더 깊은 분석이 필요할 때.
- `jmap -dump`의 `File exists` — 덤프는 덮어쓰지 않는다는 걸 직접 만났다.

## 비고
- `leak.hprof`·`gc*.log`는 실행 산출물이라 Drive에 올리지 않는다(~/jvm-practice 로컬에만).
- 재현: `javac LeakDemo.java && java -Xmx256m -Xlog:gc:file=gc.log LeakDemo` 후 10초 내 jps→jstat→jmap.
