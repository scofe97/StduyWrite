# Java 직렬화: Deep Investigation
> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. 역직렬화 공격의 원리와 방어 전략은 무엇인가?

### 왜 이 질문이 중요한가
Java 직렬화 취약점은 Apache Commons Collections, Spring Framework, WebLogic 등 수많은 프레임워크에서 RCE(Remote Code Execution)로 이어진 역대 최악의 Java 보안 취약점 중 하나다. CVE-2015-7501을 비롯해 지금도 꾸준히 발견된다. 직렬화를 사용하는 시스템을 운영하거나 레거시 코드를 유지보수한다면 이 공격 원리를 반드시 알아야 한다.

### 답변

역직렬화 공격의 핵심은 **가젯 체인(Gadget Chain)**이다. 공격자는 악의적인 바이트 스트림을 전송하고, JVM이 `ObjectInputStream.readObject()`를 호출하는 순간 클래스패스에 있는 라이브러리들의 정상적인 메서드들이 연쇄 호출되어 최종적으로 임의 코드가 실행된다.

```
공격 흐름:
1. 공격자가 직렬화된 객체 바이트를 서버로 전송
2. 서버가 ObjectInputStream.readObject() 호출
3. 역직렬화 과정에서 readObject/readResolve/finalize 등 메서드 자동 호출
4. Apache Commons Collections의 InvokerTransformer 등이 가젯 역할
5. Runtime.exec("rm -rf /") 같은 임의 명령 실행
```

**방어 전략 1: 직렬화 필터(Serialization Filter, Java 9+)**

```java
// ObjectInputFilter로 허용할 클래스만 화이트리스트
ObjectInputStream ois = new ObjectInputStream(inputStream);
ois.setObjectInputFilter(info -> {
    Class<?> clazz = info.serialClass();
    if (clazz == null) return ObjectInputFilter.Status.UNDECIDED;
    // 허용 목록에 있는 클래스만 통과
    if (ALLOWED_CLASSES.contains(clazz.getName())) {
        return ObjectInputFilter.Status.ALLOWED;
    }
    return ObjectInputFilter.Status.REJECTED;
});
```

**방어 전략 2: 신뢰할 수 없는 데이터는 절대 역직렬화하지 않음.** 가장 확실한 방어다. 외부에서 받은 데이터는 JSON/Protobuf로 파싱하고, Java 직렬화 형식(매직 바이트 `0xAC 0xED`)이 감지되면 즉시 거부한다.

**방어 전략 3: SerialKiller 등 라이브러리 활용.** 알려진 가젯 체인 클래스들을 블랙리스트로 차단하는 `ObjectInputStream` 래퍼를 사용한다.

**방어 전략 4: JEP 290 글로벌 직렬화 필터.** JVM 시작 시 `-Djdk.serialFilter=com.example.**;!*`처럼 시스템 전체 필터를 설정한다.

---

## Q2. Java 직렬화 대신 JSON/Protobuf를 선택해야 하는 이유는 무엇인가?

### 왜 이 질문이 중요한가
레거시 시스템에서 Java 직렬화를 네트워크 통신이나 캐시에 사용하는 경우가 여전히 많다. "왜 바꿔야 하는가?"에 대한 명확한 기준이 없으면 마이그레이션 제안을 설득력 있게 할 수 없다. 성능, 보안, 유지보수성 세 가지 축으로 비교할 수 있어야 한다.

### 답변

Java 직렬화를 대체해야 하는 이유는 보안, 호환성, 성능 세 가지로 정리된다.

**보안**: 앞서 설명한 역직렬화 RCE 공격 외에도, `serialVersionUID` 불일치로 인한 `InvalidClassException`은 배포 중 서비스 장애로 이어진다. JSON/Protobuf는 구조가 명시적이라 임의 코드 실행 경로가 없다.

**언어/버전 호환성**: Java 직렬화 형식은 Java 전용이다. 마이크로서비스 환경에서 Python, Go 서비스와 통신하려면 JSON/Protobuf가 필수다. 또한 클래스 구조가 바뀌면(필드 추가/삭제/타입 변경) 기존 직렬화 데이터와 호환되지 않아 롤링 배포나 캐시 무효화가 복잡해진다.

**성능 비교**:

```
직렬화 크기 비교 (예: 간단한 POJO 100개):
Java 직렬화:  ~8KB (클래스 메타데이터 포함)
JSON:         ~4KB
Protobuf:     ~1.5KB (필드 번호 + 바이너리)

처리 속도 (JMH 측정 기준, 상대적):
Java 직렬화:  기준 1x
Jackson JSON: 2~3x 빠름
Protobuf:     5~10x 빠름
```

**선택 기준**:

| 상황 | 권장 포맷 | 이유 |
|------|----------|------|
| REST API, 범용 데이터 교환 | JSON (Jackson/Gson) | 사람이 읽을 수 있음, 디버깅 용이 |
| 고성능 RPC, 마이크로서비스 | Protobuf / gRPC | 스키마 강제, 바이너리 효율 |
| 이벤트 스트리밍 (Kafka) | Avro / Protobuf | 스키마 레지스트리 연동 |
| Java 내부 캐시(Redis 등) | JSON 또는 Kryo | Kryo는 Java 전용이지만 Java 직렬화보다 10x 빠름 |

Java 직렬화가 여전히 유효한 경우는 단 하나다. 완전히 신뢰할 수 있는 내부 Java 시스템 간에 임시 객체를 전달하고, 클래스 버전이 절대 바뀌지 않는 환경이다. 현대 시스템에서 이 조건을 만족하는 경우는 거의 없다.
