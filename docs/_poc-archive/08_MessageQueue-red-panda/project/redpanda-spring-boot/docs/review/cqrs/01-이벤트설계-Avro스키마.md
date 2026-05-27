# 이벤트 설계 & Avro 스키마

---

## 구현 요약

| 항목 | 내용 |
|------|------|
| 실습 번호 | 1 |
| 주요 파일 | `src/main/avro/cqrs/PostCreated.avsc`, `PostLiked.avsc`, `UserFollowed.avsc`, `UserUnfollowed.avsc` |
| 테스트 파일 | 없음 (스키마 정의만, `./gradlew build`로 검증) |
| LEARN.md 위치 | `learning/06-cqrs-event-sourcing/02-event-sourcing-fundamentals.md` line 226~296 |

## 왜 이렇게 구현했는가

**namespace를 `com.study.redpanda.avro.social`로 분리한 이유.** 기존 ch02~ch10 스키마는 `com.study.redpanda.avro` 네임스페이스를 사용한다. CQRS 실습의 Social Feed 도메인은 기존 주문/SAGA 도메인과 완전히 다른 bounded context이므로 `.social` 서브 네임스페이스로 분리했다. 이렇게 하면 생성된 Java 클래스가 별도 패키지에 위치하여 기존 코드와 이름 충돌이 없다.

**디렉토리를 `src/main/avro/cqrs/`로 한 이유.** 기존 스키마는 `ch02/`, `ch03/` 등 챕터 단위로 나뉘어 있다. CQRS 실습은 여러 챕터에 걸친 통합 실습이므로 챕터 번호 대신 `cqrs/`라는 주제명을 사용했다. Gradle Avro plugin이 `src/main/avro/**/*.avsc`를 자동 스캔하므로 빌드 설정 변경 없이 바로 동작한다.

**필드를 최소화한 이유.** PoC 목적이므로 각 이벤트에 필수 필드만 포함했다. 예를 들어 PostCreated에 `title`, `tags`, `mediaUrls` 같은 필드를 추가할 수 있지만 CQRS 패턴 학습에는 불필요하다. 나중에 실습 4(Kafka Streams Topology)에서 State Store를 구성할 때 부족한 필드가 있으면 Avro 스키마 진화(backward compatible add)로 추가하면 된다.

**logicalType을 필드 레벨에 둔 이유.** ch02 OrderEvent와 동일한 패턴(`"logicalType": "timestamp-millis"` 필드 옆 배치)을 따랐다. Avro 1.11에서는 type 안에 nested하는 게 정식이지만, 기존 프로젝트 전체가 필드 레벨 패턴을 쓰고 있어 일관성을 우선했다. 빌드 시 경고가 나오지만 코드 생성은 정상 동작한다.

## 교차 검증 결과

### Claude 리뷰
- 4개 스키마 모두 기존 ch02 패턴(eventId, timestamp logicalType, doc 필드)과 일관됨
- 이벤트 네이밍이 과거 시제(Created, Liked, Followed, Unfollowed)를 올바르게 사용
- `eventId`가 모든 이벤트에 포함되어 멱등성 중복 감지 가능
- UserFollowed/UserUnfollowed에서 `followerId`/`followeeId` 네이밍이 도메인 언어를 잘 반영

### Codex 교차 리뷰
- (이 실습은 스키마 정의만이므로 Codex 리뷰 생략)

### 수정 사항
- 없음

## 핵심 학습 포인트

- **이벤트는 과거 시제로 명명한다.** Command는 명령형(CreatePost), Event는 과거형(PostCreated). 이벤트는 "이미 일어난 사실"을 기록하는 것이므로 과거 시제가 자연스럽다.
- **이벤트에는 Query Side가 상태를 재구성하는 데 충분한 정보가 있어야 한다.** PostCreated에 `content`가 없으면 Query Side에서 게시물 내용을 보여줄 수 없다. 이벤트가 곧 유일한 진실의 원천(Single Source of Truth)이 되기 때문이다.
- **eventId는 멱등성의 기반이다.** at-least-once 배달 환경에서 동일 이벤트가 중복 도착할 수 있으므로 eventId로 이미 처리한 이벤트인지 판별한다. 기존 ch03 SAGA에서 `(correlationId, eventType)` 복합 키로 멱등성을 구현했던 것과 같은 원리다.
- **Aggregate ID가 파티션 키가 된다.** PostCreated/PostLiked의 `postId`, UserFollowed/UserUnfollowed의 `followerId`가 각각 파티션 키 후보다. 같은 Aggregate의 이벤트가 같은 파티션에 들어가야 순서가 보장된다. 이 설계는 실습 3(Event Store 토픽 설계)에서 구체화된다.
