# Go Garbage Collection 완벽 가이드

> 면접 대비용 Go GC 이론 문서

---

## 목차

1. [Go GC 개요](#1-go-gc-개요)
2. [Go GC 알고리즘](#2-go-gc-알고리즘)
3. [Concurrent GC (동시성 GC)](#3-concurrent-gc-동시성-gc)
4. [GC 튜닝](#4-gc-튜닝)
5. [GC 모니터링](#5-gc-모니터링)
6. [면접 대비 핵심 포인트](#6-면접-대비-핵심-포인트)
7. [코드 예시](#7-코드-예시)

---

## 1. Go GC 개요

### 1.1 Go GC란?

Go의 Garbage Collector는 프로그래머가 명시적으로 메모리를 해제하지 않아도 사용하지 않는 메모리를 자동으로 회수하는 런타임 시스템이다. Go 1.5부터 도입된 Concurrent Mark-and-Sweep 알고리즘을 기반으로 한다.

### 1.2 Go GC의 설계 철학

```
┌─────────────────────────────────────────────────────────────┐
│                    Go GC 설계 우선순위                        │
├─────────────────────────────────────────────────────────────┤
│  1. Low Latency (낮은 지연 시간) - 최우선                     │
│  2. Simplicity (단순성) - 하나의 튜닝 파라미터                │
│  3. Throughput (처리량) - 적절한 수준 유지                    │
└─────────────────────────────────────────────────────────────┘
```

**핵심 목표**: STW(Stop-The-World) 시간을 **500us(마이크로초) 미만**으로 유지

Go 팀은 처리량(throughput)을 다소 희생하더라도 지연 시간을 최소화하는 것을 선택했다. 이는 Go가 주로 사용되는 웹 서버, 마이크로서비스 환경에서 응답 시간이 중요하기 때문이다.

### 1.3 JVM GC와의 비교

| 특성 | Go GC | JVM GC |
|------|-------|--------|
| **알고리즘** | Tri-color Mark-and-Sweep | 여러 알고리즘 선택 가능 (G1, ZGC, Shenandoah 등) |
| **세대 구분** | 없음 (Non-generational) | 있음 (Young/Old Generation) |
| **STW 시간** | ~500us 미만 목표 | 알고리즘에 따라 다름 (ms~수십ms) |
| **튜닝 복잡도** | 단순 (GOGC, GOMEMLIMIT) | 복잡 (수십 개 옵션) |
| **메모리 압축** | 없음 (Non-compacting) | 있음 (Compacting) |
| **설계 철학** | 단순성, 낮은 지연 | 처리량 최적화, 유연성 |

#### JVM이 세대별 GC를 사용하는 이유

JVM은 "대부분의 객체는 젊어서 죽는다(Weak Generational Hypothesis)"는 가설에 기반하여 Young Generation을 자주, 빠르게 수집한다.

#### Go가 세대별 GC를 사용하지 않는 이유

1. **컴파일러 최적화**: Go의 Escape Analysis가 힙 할당을 최소화
2. **값 타입 중심**: 구조체가 기본적으로 값으로 전달되어 힙 할당 감소
3. **단순성 유지**: 복잡한 세대 관리 없이도 충분한 성능 달성
4. **내부 포인터**: Go는 구조체 내부 필드를 가리키는 포인터를 허용하여 세대 이동이 복잡

```go
// Go의 Escape Analysis 예시
func example() {
    x := 42        // 스택 할당 (escape하지 않음)
    y := &x        // y도 스택에 남을 수 있음
    fmt.Println(y) // 컴파일러가 분석하여 최적화
}
```

---

## 2. Go GC 알고리즘

### 2.1 Tri-color Mark-and-Sweep 알고리즘

Go GC의 핵심은 **삼색 마킹(Tri-color Marking)** 알고리즘이다. 모든 객체를 세 가지 색상으로 분류한다.

```
┌─────────────────────────────────────────────────────────────┐
│                     삼색 객체 분류                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ⬜ White (흰색)                                           │
│   - 아직 방문하지 않은 객체                                  │
│   - GC 시작 시 모든 객체는 White                            │
│   - Mark 단계 후에도 White인 객체 = 가비지 (수거 대상)       │
│                                                             │
│   ⬛ Gray (회색)                                            │
│   - 방문했지만, 참조하는 객체들을 아직 검사하지 않은 객체     │
│   - "처리 대기열"에 있는 객체                                │
│   - 모든 참조를 검사하면 Black이 됨                          │
│                                                             │
│   ⚫ Black (검은색)                                         │
│   - 방문했고, 참조하는 모든 객체도 검사 완료                  │
│   - 확실히 살아있는 객체                                     │
│   - Black 객체가 White를 직접 참조하면 안 됨 (불변식)        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Mark 단계 상세

```
[GC 시작 전]
┌─────────────────────────────────────────┐
│  Root Set (스택, 전역변수)              │
│      │                                  │
│      ▼                                  │
│    ┌───┐    ┌───┐    ┌───┐             │
│    │ A │───▶│ B │───▶│ C │             │
│    └───┘    └───┘    └───┘             │
│      │                                  │
│      ▼                                  │
│    ┌───┐    ┌───┐                       │
│    │ D │    │ E │  (도달 불가)          │
│    └───┘    └───┘                       │
│                                         │
│  모든 객체: White                       │
└─────────────────────────────────────────┘

[Mark 단계 1: 루트 스캔]
┌─────────────────────────────────────────┐
│  Root에서 직접 참조하는 A, D를 Gray로   │
│                                         │
│    ┌───┐    ┌───┐    ┌───┐             │
│    │ A │───▶│ B │───▶│ C │             │
│    │Gray│   │White│  │White│            │
│    └───┘    └───┘    └───┘             │
│      │                                  │
│      ▼                                  │
│    ┌───┐    ┌───┐                       │
│    │ D │    │ E │                       │
│    │Gray│   │White│                     │
│    └───┘    └───┘                       │
└─────────────────────────────────────────┘

[Mark 단계 2: Gray 객체 처리]
┌─────────────────────────────────────────┐
│  A의 참조(B)를 Gray로, A는 Black으로    │
│                                         │
│    ┌───┐    ┌───┐    ┌───┐             │
│    │ A │───▶│ B │───▶│ C │             │
│    │Black│  │Gray│   │White│            │
│    └───┘    └───┘    └───┘             │
│      │                                  │
│      ▼                                  │
│    ┌───┐    ┌───┐                       │
│    │ D │    │ E │                       │
│    │Black│  │White│                     │
│    └───┘    └───┘                       │
└─────────────────────────────────────────┘

[Mark 완료]
┌─────────────────────────────────────────┐
│  Gray 객체가 없을 때까지 반복           │
│                                         │
│    ┌───┐    ┌───┐    ┌───┐             │
│    │ A │───▶│ B │───▶│ C │             │
│    │Black│  │Black│  │Black│            │
│    └───┘    └───┘    └───┘             │
│      │                                  │
│      ▼                                  │
│    ┌───┐    ┌───┐                       │
│    │ D │    │ E │ ◀── 가비지!          │
│    │Black│  │White│                     │
│    └───┘    └───┘                       │
└─────────────────────────────────────────┘
```

### 2.3 Sweep 단계

Mark 단계가 완료되면 White로 남은 객체들을 메모리에서 해제한다.

```
[Sweep 단계]
┌─────────────────────────────────────────┐
│                                         │
│  White 객체 (E) 메모리 해제             │
│                                         │
│  - 힙을 순회하며 White 객체 발견        │
│  - 해당 메모리 블록을 free list에 반환  │
│  - 다음 할당에서 재사용 가능            │
│                                         │
│  특징:                                  │
│  - 동시 실행 (Background Sweeping)      │
│  - 새 할당 요청 시 필요한 만큼만 sweep  │
│  - 전체 힙을 한 번에 sweep하지 않음     │
│                                         │
└─────────────────────────────────────────┘
```

### 2.4 Write Barrier (쓰기 장벽)

동시성 GC에서 가장 중요한 개념이다. GC가 실행되는 동안 애플리케이션도 실행되므로 참조 관계가 변경될 수 있다.

#### 문제 상황: Lost Object Problem

```
┌─────────────────────────────────────────────────────────────┐
│  Mutator(애플리케이션)와 GC가 동시 실행 시 문제              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [시점 1] GC가 A를 Black으로 마킹 완료                       │
│                                                             │
│    ┌───┐         ┌───┐                                     │
│    │ A │────────▶│ B │                                     │
│    │Black│       │Gray│                                     │
│    └───┘         └───┘                                     │
│                    │                                        │
│                    ▼                                        │
│                  ┌───┐                                      │
│                  │ C │                                      │
│                  │White│                                    │
│                  └───┘                                      │
│                                                             │
│  [시점 2] 애플리케이션이 A→C 참조 추가, B→C 참조 제거        │
│                                                             │
│    ┌───┐         ┌───┐                                     │
│    │ A │─ ─ ─ ─ ─│ B │  (B→C 참조 제거)                    │
│    │Black│       │Gray│                                     │
│    └───┘         └───┘                                     │
│      │                                                      │
│      │  (A→C 참조 추가)                                     │
│      ▼                                                      │
│    ┌───┐                                                    │
│    │ C │  ◀── 위험! Black이 White를 직접 참조               │
│    │White│                                                  │
│    └───┘                                                    │
│                                                             │
│  문제: C는 살아있지만 GC가 수거해버림!                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Write Barrier의 해결책

Go는 **Dijkstra-style insertion barrier**와 **Yuasa-style deletion barrier**를 결합한 **Hybrid Write Barrier**를 사용한다 (Go 1.8+).

```go
// 개념적인 Write Barrier 동작 (실제 구현은 컴파일러가 자동 삽입)

// 포인터 쓰기 전
func writePointer(slot *unsafe.Pointer, ptr unsafe.Pointer) {
    // Write Barrier가 활성화된 경우
    if writeBarrierEnabled {
        // 1. 새로 참조되는 객체를 Gray로 마킹 (insertion barrier)
        shade(ptr)

        // 2. 기존에 참조되던 객체도 Gray로 마킹 (deletion barrier)
        shade(*slot)
    }

    // 실제 포인터 쓰기
    *slot = ptr
}
```

#### Hybrid Write Barrier의 규칙

```
┌─────────────────────────────────────────────────────────────┐
│              Hybrid Write Barrier (Go 1.8+)                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 새로 할당되는 객체는 Black으로 시작                      │
│     - 스택의 모든 객체도 Black으로 간주                      │
│                                                             │
│  2. 포인터 쓰기 시:                                         │
│     - 힙의 포인터 슬롯에 쓸 때만 barrier 적용               │
│     - 스택 쓰기에는 barrier 불필요 (성능 최적화)            │
│                                                             │
│  3. Shade 규칙:                                             │
│     shade(new_ptr)  // 새 참조 대상을 Gray로                │
│     shade(old_ptr)  // 기존 참조 대상도 Gray로              │
│                                                             │
│  장점:                                                      │
│  - 스택 재스캔 불필요                                       │
│  - STW 시간 크게 감소                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Concurrent GC (동시성 GC)

### 3.1 GC 사이클 전체 흐름

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Go GC 사이클                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────┐                                                       │
│  │ GC OFF   │  애플리케이션 실행 (GC 없음)                          │
│  └────┬─────┘                                                       │
│       │ 트리거 조건 충족                                            │
│       ▼                                                             │
│  ┌──────────┐                                                       │
│  │ STW #1   │  Mark Setup (~10-30us)                               │
│  │          │  - Write Barrier 활성화                               │
│  │          │  - 모든 P의 mcache 플러시                             │
│  └────┬─────┘                                                       │
│       │                                                             │
│       ▼                                                             │
│  ┌──────────┐                                                       │
│  │Concurrent│  Mark Phase (대부분의 시간)                          │
│  │  Mark    │  - 루트 스캔 (스택, 전역변수)                         │
│  │          │  - 힙 객체 마킹                                       │
│  │          │  - 애플리케이션과 동시 실행                           │
│  │          │  - GC Worker 고루틴들이 수행                          │
│  └────┬─────┘                                                       │
│       │                                                             │
│       ▼                                                             │
│  ┌──────────┐                                                       │
│  │ STW #2   │  Mark Termination (~10-30us)                         │
│  │          │  - 남은 마킹 작업 완료                                │
│  │          │  - Write Barrier 비활성화                             │
│  │          │  - 다음 GC 목표 힙 크기 계산                          │
│  └────┬─────┘                                                       │
│       │                                                             │
│       ▼                                                             │
│  ┌──────────┐                                                       │
│  │Concurrent│  Sweep Phase                                         │
│  │  Sweep   │  - 백그라운드에서 실행                                │
│  │          │  - 새 할당 요청 시 필요한 만큼 sweep                  │
│  │          │  - 완전히 동시 실행                                   │
│  └────┬─────┘                                                       │
│       │                                                             │
│       ▼                                                             │
│  ┌──────────┐                                                       │
│  │ GC OFF   │  다음 사이클까지 대기                                 │
│  └──────────┘                                                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 STW (Stop-The-World) 최소화

Go GC는 두 번의 짧은 STW만 필요로 한다.

```
┌─────────────────────────────────────────────────────────────┐
│                    STW 시간 비교                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Go 1.4 이전:     [===================STW==================]│
│                   전체 GC가 STW (수백ms 가능)               │
│                                                             │
│  Go 1.5+:         [STW1]─────────동시실행─────────[STW2]    │
│                   ~10us        마이크로초         ~10us     │
│                                                             │
│  목표: 각 STW < 500us (0.5ms)                               │
│  실제: 대부분 10-30us 수준                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.3 GC Pacing과 Mark Assist

GC는 힙 성장 속도에 맞춰 마킹 속도를 조절한다.

```
┌─────────────────────────────────────────────────────────────┐
│                      GC Pacing                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  목표: GC가 끝나기 전에 힙이 목표 크기를 초과하지 않도록    │
│                                                             │
│  힙 크기                                                    │
│     ▲                                                       │
│     │                    목표 힙 크기                       │
│     │               ─ ─ ─ ─ ─ ─ ─ ─ ─ ─                    │
│     │             /                                         │
│     │           /   GC 진행                                 │
│     │         /                                             │
│     │       /                                               │
│     │     /                                                 │
│     │   / 트리거                                            │
│     │ /                                                     │
│     └──────────────────────────────────────▶ 시간           │
│                                                             │
│  Mark Assist:                                               │
│  - 할당 속도가 마킹 속도보다 빠르면                         │
│  - 할당하는 고루틴이 마킹 작업을 돕도록 강제               │
│  - 할당 전에 일정량의 마킹 작업 수행                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.4 Background Sweeping

```
┌─────────────────────────────────────────────────────────────┐
│                   Background Sweeping                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  특징:                                                      │
│  - 전용 고루틴이 백그라운드에서 sweep 수행                  │
│  - 새 할당 요청 시 필요하면 즉시 sweep (lazy sweep)         │
│  - STW 없이 완전히 동시 실행                                │
│                                                             │
│  과정:                                                      │
│  1. 힙을 span 단위로 순회                                   │
│  2. White 객체가 있는 span의 메모리 회수                    │
│  3. 회수된 span을 free list에 반환                          │
│                                                             │
│  최적화:                                                    │
│  - 전체 힙을 한 번에 sweep하지 않음                         │
│  - 다음 GC 사이클 전까지 점진적으로 완료                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. GC 튜닝

### 4.1 GOGC 환경 변수

GOGC는 GC 트리거 임계값을 설정한다. **기본값은 100**이다.

```
┌─────────────────────────────────────────────────────────────┐
│                        GOGC 동작                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  공식: 목표 힙 크기 = 라이브 힙 × (1 + GOGC/100)           │
│                                                             │
│  GOGC=100 (기본값):                                         │
│  - 라이브 힙이 100MB면, 200MB에서 GC 트리거                │
│  - 힙이 2배가 되면 GC 실행                                  │
│                                                             │
│  GOGC=50:                                                   │
│  - 라이브 힙 100MB → 150MB에서 GC 트리거                   │
│  - 더 자주 GC 실행 (메모리 절약, CPU 증가)                  │
│                                                             │
│  GOGC=200:                                                  │
│  - 라이브 힙 100MB → 300MB에서 GC 트리거                   │
│  - 덜 자주 GC 실행 (메모리 증가, CPU 절약)                  │
│                                                             │
│  GOGC=off:                                                  │
│  - GC 완전히 비활성화 (주의!)                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

```bash
# 환경 변수 설정
GOGC=50 ./myapp      # GC 더 자주 실행
GOGC=200 ./myapp     # GC 덜 자주 실행
GOGC=off ./myapp     # GC 비활성화 (위험!)
```

### 4.2 GOMEMLIMIT (Go 1.19+)

Go 1.19에서 도입된 **소프트 메모리 제한**이다.

```
┌─────────────────────────────────────────────────────────────┐
│                      GOMEMLIMIT                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  목적: 전체 Go 런타임 메모리 사용량 제한                    │
│                                                             │
│  동작:                                                      │
│  - 힙 + 스택 + 런타임 메타데이터 포함                       │
│  - 제한에 가까워지면 GC가 더 공격적으로 실행               │
│  - GOGC보다 우선순위 높음                                   │
│  - "소프트" 제한: 초과할 수 있지만 GC가 적극적으로 회수    │
│                                                             │
│  권장 패턴:                                                 │
│  - GOMEMLIMIT 설정 + GOGC=off                               │
│  - 컨테이너 환경에서 OOM 방지에 효과적                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

```bash
# 메모리 제한 설정
GOMEMLIMIT=1GiB ./myapp
GOMEMLIMIT=512MiB GOGC=off ./myapp  # 권장 패턴

# 단위: B, KiB, MiB, GiB, TiB
```

```go
// 코드에서 설정
import "runtime/debug"

func main() {
    // 1GB 메모리 제한
    debug.SetMemoryLimit(1 << 30)

    // GOGC 설정
    debug.SetGCPercent(100)
}
```

### 4.3 runtime/debug 패키지

```go
package main

import (
    "runtime"
    "runtime/debug"
)

func main() {
    // GC 퍼센트 설정 (GOGC와 동일)
    oldPercent := debug.SetGCPercent(50)

    // 메모리 제한 설정 (GOMEMLIMIT와 동일)
    oldLimit := debug.SetMemoryLimit(512 << 20) // 512MB

    // 수동 GC 트리거
    runtime.GC()

    // 가능한 많은 메모리를 OS에 반환
    debug.FreeOSMemory()

    // GC 통계 읽기
    var stats debug.GCStats
    debug.ReadGCStats(&stats)

    println("마지막 GC 시간:", stats.LastGC)
    println("총 GC 횟수:", stats.NumGC)
    println("총 GC 일시정지 시간:", stats.PauseTotal)
}
```

### 4.4 튜닝 가이드라인

```
┌─────────────────────────────────────────────────────────────┐
│                   GC 튜닝 가이드라인                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  시나리오 1: 메모리 부족, CPU 여유                          │
│  → GOGC 낮추기 (50 이하)                                    │
│  → 더 자주 GC 실행하여 메모리 사용량 감소                   │
│                                                             │
│  시나리오 2: 메모리 여유, CPU 부족                          │
│  → GOGC 높이기 (200 이상)                                   │
│  → GC 횟수 줄여 CPU 사용량 감소                             │
│                                                             │
│  시나리오 3: 컨테이너 환경 (메모리 제한 있음)               │
│  → GOMEMLIMIT=컨테이너_제한의_70-80%                        │
│  → GOGC=off (선택적)                                        │
│  → OOM Killer 방지                                          │
│                                                             │
│  시나리오 4: 지연 시간 민감 (웹 서버)                       │
│  → 기본값 유지 (GOGC=100)                                   │
│  → 객체 풀링, 할당 최소화에 집중                            │
│                                                             │
│  주의사항:                                                  │
│  - 먼저 측정하고, 그 다음 튜닝                              │
│  - 프로파일링 없이 튜닝하지 말 것                           │
│  - 기본값이 대부분의 경우에 적합                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. GC 모니터링

### 5.1 runtime.ReadMemStats

```go
package main

import (
    "fmt"
    "runtime"
)

func printMemStats() {
    var m runtime.MemStats
    runtime.ReadMemStats(&m)

    fmt.Printf("=== 메모리 통계 ===\n")

    // 힙 관련
    fmt.Printf("Alloc: %d MB (현재 할당된 힙 메모리)\n", m.Alloc/1024/1024)
    fmt.Printf("TotalAlloc: %d MB (누적 할당량)\n", m.TotalAlloc/1024/1024)
    fmt.Printf("Sys: %d MB (OS로부터 받은 총 메모리)\n", m.Sys/1024/1024)
    fmt.Printf("HeapAlloc: %d MB (힙에 할당된 메모리)\n", m.HeapAlloc/1024/1024)
    fmt.Printf("HeapSys: %d MB (힙용으로 OS에서 받은 메모리)\n", m.HeapSys/1024/1024)
    fmt.Printf("HeapIdle: %d MB (유휴 힙 메모리)\n", m.HeapIdle/1024/1024)
    fmt.Printf("HeapInuse: %d MB (사용 중인 힙 메모리)\n", m.HeapInuse/1024/1024)
    fmt.Printf("HeapReleased: %d MB (OS에 반환된 메모리)\n", m.HeapReleased/1024/1024)
    fmt.Printf("HeapObjects: %d (힙 객체 수)\n", m.HeapObjects)

    // GC 관련
    fmt.Printf("\n=== GC 통계 ===\n")
    fmt.Printf("NumGC: %d (GC 실행 횟수)\n", m.NumGC)
    fmt.Printf("NumForcedGC: %d (강제 GC 횟수)\n", m.NumForcedGC)
    fmt.Printf("GCCPUFraction: %.4f%% (GC가 사용한 CPU 비율)\n", m.GCCPUFraction*100)
    fmt.Printf("LastGC: %d ns (마지막 GC 시간)\n", m.LastGC)
    fmt.Printf("NextGC: %d MB (다음 GC 목표 힙 크기)\n", m.NextGC/1024/1024)
    fmt.Printf("PauseTotalNs: %d ms (총 STW 시간)\n", m.PauseTotalNs/1000000)

    // 최근 GC 일시정지 시간 (원형 버퍼)
    if m.NumGC > 0 {
        // 가장 최근 GC의 일시정지 시간
        lastPauseIdx := (m.NumGC + 255) % 256
        fmt.Printf("LastPauseNs: %d us (마지막 GC 일시정지)\n", m.PauseNs[lastPauseIdx]/1000)
    }
}

func main() {
    // 초기 상태
    printMemStats()

    // 메모리 할당
    data := make([]byte, 100*1024*1024) // 100MB
    _ = data

    fmt.Println("\n--- 100MB 할당 후 ---")
    printMemStats()

    // GC 실행
    runtime.GC()

    fmt.Println("\n--- GC 실행 후 ---")
    printMemStats()
}
```

### 5.2 GODEBUG=gctrace=1

가장 유용한 GC 디버깅 도구이다.

```bash
GODEBUG=gctrace=1 ./myapp
```

출력 예시:
```
gc 1 @0.012s 2%: 0.026+0.44+0.003 ms clock, 0.10+0.32/0.27/0+0.012 ms cpu, 4->4->0 MB, 5 MB goal, 4 P
gc 2 @0.025s 1%: 0.003+0.21+0.002 ms clock, 0.012+0.088/0.15/0+0.008 ms cpu, 4->4->1 MB, 5 MB goal, 4 P
```

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         gctrace 출력 해석                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  gc 1 @0.012s 2%: 0.026+0.44+0.003 ms clock, ...                           │
│  ▲ ▲  ▲       ▲   ▲     ▲     ▲                                            │
│  │ │  │       │   │     │     └─ STW #2 (mark termination)                 │
│  │ │  │       │   │     └─────── Concurrent mark 시간                      │
│  │ │  │       │   └───────────── STW #1 (mark setup)                       │
│  │ │  │       └───────────────── 총 CPU 시간 중 GC 비율                    │
│  │ │  └───────────────────────── 프로그램 시작 후 경과 시간                │
│  │ └──────────────────────────── GC 사이클 번호                            │
│  └────────────────────────────── gc 또는 scvg (scavenger)                  │
│                                                                             │
│  ... 4->4->0 MB, 5 MB goal, 4 P                                            │
│      ▲  ▲  ▲     ▲          ▲                                              │
│      │  │  │     │          └─ 사용된 프로세서 수                          │
│      │  │  │     └──────────── 목표 힙 크기                                │
│      │  │  └────────────────── GC 후 라이브 힙                             │
│      │  └───────────────────── GC 종료 시 힙                               │
│      └──────────────────────── GC 시작 시 힙                               │
│                                                                             │
│  CPU 시간 해석:                                                             │
│  0.10+0.32/0.27/0+0.012 ms cpu                                             │
│  ▲     ▲    ▲   ▲  ▲                                                       │
│  │     │    │   │  └─ STW #2 CPU 시간                                      │
│  │     │    │   └──── idle mark worker 시간                                │
│  │     │    └──────── fractional mark worker 시간                          │
│  │     └───────────── dedicated mark worker 시간                           │
│  └─────────────────── STW #1 CPU 시간                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.3 기타 모니터링 도구

```bash
# 메모리 프로파일링
go tool pprof http://localhost:6060/debug/pprof/heap

# GC 트레이스와 함께 스케줄러 트레이스
GODEBUG=gctrace=1,schedtrace=1000 ./myapp

# 메모리 반환 트레이스 (scavenger)
GODEBUG=gctrace=1,scavtrace=1 ./myapp
```

```go
// pprof HTTP 서버 활성화
import _ "net/http/pprof"
import "net/http"

func main() {
    go func() {
        http.ListenAndServe("localhost:6060", nil)
    }()
    // ... 애플리케이션 코드
}
```

---

## 6. 면접 대비 핵심 포인트

### 6.1 "Go GC를 설명해주세요" - 30초 답변

> "Go GC는 **Tri-color Mark-and-Sweep** 알고리즘을 사용하는 **동시성 가비지 컬렉터**입니다. 가장 큰 특징은 **STW 시간을 500 마이크로초 미만으로 유지**하면서 애플리케이션과 동시에 실행된다는 점입니다. JVM과 달리 **세대별 수집을 하지 않고**, **GOGC** 하나의 파라미터로 튜닝합니다."

### 6.2 "Go GC를 설명해주세요" - 1분 답변

> "Go GC는 **Concurrent Mark-and-Sweep** 방식의 가비지 컬렉터입니다.
>
> **알고리즘 측면**에서는 삼색 마킹을 사용합니다. 모든 객체를 White, Gray, Black으로 분류하고, 루트에서 시작해 도달 가능한 객체를 마킹한 뒤 White로 남은 객체를 수거합니다.
>
> **동시성 측면**에서는 STW 구간을 최소화했습니다. Mark Setup과 Mark Termination에서만 짧은 STW가 발생하고, 실제 마킹과 스위핑은 애플리케이션과 동시에 실행됩니다. **Hybrid Write Barrier**를 통해 동시 실행 중 참조 변경 문제를 해결합니다.
>
> **튜닝**은 GOGC와 GOMEMLIMIT 두 가지로 단순합니다. GOGC는 힙 성장 비율을, GOMEMLIMIT은 전체 메모리 상한을 설정합니다."

### 6.3 "Go GC를 설명해주세요" - 3분 답변

> "Go GC를 세 가지 관점에서 설명드리겠습니다.
>
> **첫째, 설계 철학입니다.** Go는 처리량보다 낮은 지연 시간을 우선시합니다. 웹 서버, 마이크로서비스 환경에서 응답 시간이 중요하기 때문입니다. 목표는 STW를 500 마이크로초 미만으로 유지하는 것이고, 실제로 대부분 10-30 마이크로초 수준입니다.
>
> **둘째, 알고리즘입니다.** Tri-color Mark-and-Sweep을 사용합니다. 객체를 White(미방문), Gray(방문했지만 참조 미검사), Black(완전 검사)으로 분류합니다. GC가 시작되면 루트에서 도달 가능한 객체를 Gray로 만들고, Gray 객체의 참조를 따라가며 모두 Black이 될 때까지 반복합니다. 최종적으로 White로 남은 객체가 가비지입니다.
>
> 동시성을 위해 **Hybrid Write Barrier**를 사용합니다. 이는 GC 실행 중 애플리케이션이 참조를 변경해도 살아있는 객체가 잘못 수거되지 않도록 보장합니다. Go 1.8부터 도입된 이 방식은 스택 재스캔이 필요 없어 STW 시간을 크게 줄였습니다.
>
> **셋째, 튜닝입니다.** GOGC는 힙이 얼마나 커지면 GC를 트리거할지 결정합니다. 기본값 100은 라이브 힙의 2배에서 GC가 실행됨을 의미합니다. Go 1.19의 GOMEMLIMIT은 전체 메모리 상한을 설정하여 컨테이너 환경에서 OOM을 방지합니다.
>
> JVM과 비교하면, Go는 세대별 GC를 사용하지 않습니다. Go의 Escape Analysis가 힙 할당을 최소화하고, 값 타입 중심 설계로 이미 할당이 적기 때문입니다. 튜닝도 JVM의 수십 개 옵션 대신 두 가지만 있어 단순합니다."

### 6.4 JVM과 비교 질문 대비

**Q: "Go가 세대별 GC를 사용하지 않는 이유는?"**

> "두 가지 이유가 있습니다. 첫째, Go의 컴파일러가 Escape Analysis를 통해 많은 객체를 스택에 할당하여 힙 할당 자체가 적습니다. 둘째, Go는 구조체가 값 타입이고 내부 포인터를 허용하기 때문에 세대 간 이동이 복잡해집니다. 이런 특성으로 단순한 Mark-and-Sweep으로도 충분한 성능을 달성합니다."

**Q: "Go GC의 단점은?"**

> "처리량 측면에서 JVM보다 불리할 수 있습니다. 동시성을 위한 Write Barrier 오버헤드가 있고, 세대별 수집의 이점을 못 누립니다. 또한 메모리 압축(compaction)을 하지 않아 메모리 단편화가 발생할 수 있습니다. 대용량 힙에서는 JVM의 G1GC나 ZGC가 더 적합할 수 있습니다."

**Q: "Write Barrier란?"**

> "동시성 GC에서 참조 무결성을 유지하기 위한 메커니즘입니다. GC가 마킹하는 동안 애플리케이션이 포인터를 수정하면 살아있는 객체가 잘못 수거될 수 있습니다. Write Barrier는 포인터 쓰기 시 새로 참조되는 객체와 기존 참조 객체를 모두 Gray로 마킹하여 이 문제를 방지합니다."

### 6.5 핵심 암기 포인트

```
┌─────────────────────────────────────────────────────────────┐
│                    면접 암기 포인트                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 알고리즘: Tri-color Mark-and-Sweep                      │
│  2. STW 목표: 500us 미만 (실제 10-30us)                     │
│  3. 색상: White(미방문), Gray(처리중), Black(완료)          │
│  4. Write Barrier: Hybrid (insertion + deletion)           │
│  5. 튜닝 파라미터: GOGC (기본 100), GOMEMLIMIT (Go 1.19+)   │
│  6. JVM 차이: 비세대별, 비압축, 단순 튜닝                   │
│  7. 설계 철학: 처리량보다 지연 시간 우선                    │
│  8. STW 발생 시점: Mark Setup, Mark Termination (2회만)     │
│  9. 디버깅: GODEBUG=gctrace=1                               │
│ 10. 모니터링: runtime.ReadMemStats()                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 7. 코드 예시

### 7.1 GC 동작 확인 코드

```go
package main

import (
    "fmt"
    "runtime"
    "time"
)

func main() {
    // GC 통계 출력 함수
    printGC := func(label string) {
        var m runtime.MemStats
        runtime.ReadMemStats(&m)
        fmt.Printf("[%s] HeapAlloc: %d MB, NumGC: %d, NextGC: %d MB\n",
            label, m.HeapAlloc/1024/1024, m.NumGC, m.NextGC/1024/1024)
    }

    printGC("시작")

    // 1. 메모리 할당
    data := make([]byte, 50*1024*1024) // 50MB
    for i := range data {
        data[i] = byte(i)
    }
    printGC("50MB 할당 후")

    // 2. 추가 할당으로 GC 트리거
    data2 := make([]byte, 100*1024*1024) // 100MB
    for i := range data2 {
        data2[i] = byte(i)
    }
    printGC("100MB 추가 할당 후")

    // 3. 참조 제거
    data = nil
    printGC("50MB 참조 제거 후 (GC 전)")

    // 4. 수동 GC
    runtime.GC()
    printGC("수동 GC 후")

    // 5. data2 유지 확인
    _ = data2[0]

    time.Sleep(time.Second)
}
```

**실행 (gctrace 활성화)**:
```bash
GODEBUG=gctrace=1 go run main.go
```

### 7.2 GC 일시정지 시간 측정

```go
package main

import (
    "fmt"
    "runtime"
    "time"
)

func main() {
    // 이전 GC 횟수 저장
    var prevNumGC uint32
    var m runtime.MemStats

    // GC 일시정지 시간 모니터링 고루틴
    go func() {
        for {
            runtime.ReadMemStats(&m)

            if m.NumGC > prevNumGC {
                // 새 GC 발생
                pauseIdx := (m.NumGC + 255) % 256
                pauseNs := m.PauseNs[pauseIdx]

                fmt.Printf("GC #%d: 일시정지 시간 = %d us\n",
                    m.NumGC, pauseNs/1000)

                prevNumGC = m.NumGC
            }

            time.Sleep(10 * time.Millisecond)
        }
    }()

    // 메모리 할당으로 GC 트리거
    for i := 0; i < 100; i++ {
        // 매번 10MB 할당
        data := make([]byte, 10*1024*1024)
        for j := range data {
            data[j] = byte(j)
        }
        time.Sleep(50 * time.Millisecond)
    }
}
```

### 7.3 메모리 할당 패턴과 GC 영향

```go
package main

import (
    "fmt"
    "runtime"
    "sync"
    "time"
)

// 나쁜 패턴: 빈번한 작은 할당
func badPattern() {
    start := time.Now()
    var m runtime.MemStats
    runtime.ReadMemStats(&m)
    startGC := m.NumGC

    for i := 0; i < 1000000; i++ {
        // 매번 새 슬라이스 할당
        data := make([]byte, 1024)
        _ = data
    }

    runtime.ReadMemStats(&m)
    fmt.Printf("[나쁜 패턴] 시간: %v, GC 횟수: %d\n",
        time.Since(start), m.NumGC-startGC)
}

// 좋은 패턴: 객체 풀링
func goodPattern() {
    start := time.Now()
    var m runtime.MemStats
    runtime.ReadMemStats(&m)
    startGC := m.NumGC

    // sync.Pool 사용
    pool := &sync.Pool{
        New: func() interface{} {
            return make([]byte, 1024)
        },
    }

    for i := 0; i < 1000000; i++ {
        // 풀에서 가져오기
        data := pool.Get().([]byte)
        _ = data
        // 풀에 반환
        pool.Put(data)
    }

    runtime.ReadMemStats(&m)
    fmt.Printf("[좋은 패턴] 시간: %v, GC 횟수: %d\n",
        time.Since(start), m.NumGC-startGC)
}

// 좋은 패턴: 미리 할당
func preallocPattern() {
    start := time.Now()
    var m runtime.MemStats
    runtime.ReadMemStats(&m)
    startGC := m.NumGC

    // 한 번에 큰 슬라이스 할당
    bigData := make([]byte, 1024*1000000)

    for i := 0; i < 1000000; i++ {
        // 이미 할당된 메모리의 일부 사용
        data := bigData[i*1024 : (i+1)*1024]
        _ = data
    }

    runtime.ReadMemStats(&m)
    fmt.Printf("[미리 할당] 시간: %v, GC 횟수: %d\n",
        time.Since(start), m.NumGC-startGC)
}

func main() {
    runtime.GC() // 초기화

    fmt.Println("=== 메모리 할당 패턴 비교 ===")
    badPattern()

    runtime.GC()
    goodPattern()

    runtime.GC()
    preallocPattern()
}
```

### 7.4 GOGC와 GOMEMLIMIT 효과 확인

```go
package main

import (
    "fmt"
    "runtime"
    "runtime/debug"
    "time"
)

func allocateAndMeasure(label string) {
    var m runtime.MemStats
    runtime.ReadMemStats(&m)
    startGC := m.NumGC

    start := time.Now()

    // 메모리 할당
    var data [][]byte
    for i := 0; i < 100; i++ {
        chunk := make([]byte, 10*1024*1024) // 10MB씩
        data = append(data, chunk)
    }

    runtime.ReadMemStats(&m)
    fmt.Printf("[%s]\n", label)
    fmt.Printf("  총 할당: %d MB\n", m.TotalAlloc/1024/1024)
    fmt.Printf("  힙 사용: %d MB\n", m.HeapAlloc/1024/1024)
    fmt.Printf("  GC 횟수: %d\n", m.NumGC-startGC)
    fmt.Printf("  소요 시간: %v\n", time.Since(start))

    // 메모리 해제
    data = nil
    runtime.GC()
}

func main() {
    // 1. 기본값 (GOGC=100)
    debug.SetGCPercent(100)
    debug.SetMemoryLimit(0) // 무제한
    allocateAndMeasure("GOGC=100, 제한 없음")

    // 2. GOGC=50 (더 자주 GC)
    debug.SetGCPercent(50)
    allocateAndMeasure("GOGC=50, 제한 없음")

    // 3. GOGC=200 (덜 자주 GC)
    debug.SetGCPercent(200)
    allocateAndMeasure("GOGC=200, 제한 없음")

    // 4. GOMEMLIMIT 설정
    debug.SetGCPercent(100)
    debug.SetMemoryLimit(500 * 1024 * 1024) // 500MB 제한
    allocateAndMeasure("GOGC=100, GOMEMLIMIT=500MB")

    // 5. GOGC=off + GOMEMLIMIT (권장 컨테이너 설정)
    debug.SetGCPercent(-1) // off
    debug.SetMemoryLimit(500 * 1024 * 1024)
    allocateAndMeasure("GOGC=off, GOMEMLIMIT=500MB")
}
```

### 7.5 Escape Analysis 확인

```go
package main

// go build -gcflags="-m" main.go 로 실행하여 escape 분석 확인

func noEscape() int {
    x := 42 // 스택에 할당됨
    return x
}

func escapeToHeap() *int {
    x := 42   // 힙에 할당됨 (포인터가 함수 밖으로 나감)
    return &x // "moved to heap" 메시지 출력됨
}

func sliceNoEscape() {
    data := make([]int, 100) // 크기가 작으면 스택 가능
    for i := range data {
        data[i] = i
    }
}

func sliceEscape() []int {
    data := make([]int, 100) // 반환되므로 힙에 할당
    for i := range data {
        data[i] = i
    }
    return data
}

type LargeStruct struct {
    data [10000]int
}

func largeStructEscape() {
    // 큰 구조체는 스택 제한으로 힙에 할당될 수 있음
    s := LargeStruct{}
    _ = s
}

func main() {
    _ = noEscape()
    _ = escapeToHeap()
    sliceNoEscape()
    _ = sliceEscape()
    largeStructEscape()
}
```

**Escape Analysis 확인 명령어**:
```bash
go build -gcflags="-m -m" main.go 2>&1 | grep escape

# 출력 예시:
# ./main.go:11:2: x escapes to heap
# ./main.go:11:2:   flow: ~r0 = &x:
# ./main.go:11:2:     from &x (address-of) at ./main.go:12:9
```

---

## 참고 자료

1. [Go GC Guide (공식)](https://go.dev/doc/gc-guide)
2. [Getting to Go: The Journey of Go's Garbage Collector](https://go.dev/blog/ismmkeynote)
3. [Go 1.5 Concurrent Garbage Collector](https://docs.google.com/document/d/1wmjrocXIWTr1JxU-3EQBI6BK6KgtiFArkG47XK73xIQ)
4. [GOGC and GOMEMLIMIT](https://weaviate.io/blog/gomemlimit-a-game-changer-for-high-memory-applications)

---

> 마지막 업데이트: 2025-01-17
