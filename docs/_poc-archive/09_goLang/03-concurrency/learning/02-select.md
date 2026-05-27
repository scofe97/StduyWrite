# Select 문 학습

다중 채널을 동시에 처리하는 select 문을 학습합니다.

---

## 학습 목표

- select 문 기본 문법
- 타임아웃 처리
- 논블로킹 채널 연산
- default 케이스 활용

---

## 1. Select 기본 개념

### select란?
여러 채널 연산 중 준비된 것을 선택하여 실행합니다. switch와 비슷하지만 채널 전용입니다.

```go
select {
case msg := <-ch1:
    fmt.Println("ch1:", msg)
case msg := <-ch2:
    fmt.Println("ch2:", msg)
}
```

### 특징
- 여러 채널이 준비되면 **무작위**로 하나 선택
- 모든 채널이 블로킹되면 대기
- default가 있으면 블로킹 없이 즉시 실행

---

## 2. 타임아웃 처리

### time.After 사용
```go
select {
case result := <-ch:
    fmt.Println("결과:", result)
case <-time.After(3 * time.Second):
    fmt.Println("타임아웃!")
}
```

### context 사용 (권장)
```go
ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
defer cancel()

select {
case result := <-ch:
    fmt.Println("결과:", result)
case <-ctx.Done():
    fmt.Println("타임아웃:", ctx.Err())
}
```

---

## 3. 논블로킹 연산

### default 케이스
```go
select {
case msg := <-ch:
    fmt.Println("받음:", msg)
default:
    fmt.Println("데이터 없음, 다른 작업 수행")
}
```

### 논블로킹 전송
```go
select {
case ch <- msg:
    fmt.Println("전송 성공")
default:
    fmt.Println("채널이 가득 참, 나중에 재시도")
}
```

---

## 4. 무한 루프와 select

### 종료 신호 처리
```go
done := make(chan struct{})

go func() {
    for {
        select {
        case <-done:
            fmt.Println("종료")
            return
        case msg := <-ch:
            fmt.Println("처리:", msg)
        }
    }
}()

// 종료 시
close(done)
```

---

## 5. 다중 채널 수신

### 여러 소스에서 데이터 수집
```go
for {
    select {
    case msg := <-emailCh:
        sendEmail(msg)
    case msg := <-smsCh:
        sendSMS(msg)
    case msg := <-pushCh:
        sendPush(msg)
    case <-ctx.Done():
        return
    }
}
```

---

## 과제

### 과제 1: 기본 Select
`practices/01-basic-select/main.go`에서 두 채널 중 먼저 도착한 데이터를 처리하세요.

### 과제 2: 타임아웃
`practices/02-timeout/main.go`에서 API 호출에 타임아웃을 적용하세요.

### 과제 3: 논블로킹 연산
`practices/03-non-blocking/main.go`에서 채널이 비어있을 때 대체 동작을 구현하세요.

---

## 참조 자료

- **Learning Go, 2nd Edition**: 12_Concurrency_in_Go.md - select 섹션
- **Effective Go**: Concurrency 섹션
