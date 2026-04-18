# Java Internals

> JVM 내부 구조, I/O, 빌드 도구를 다루는 토픽

## 챕터 목록
| # | 챕터 | 핵심 주제 |
|---|------|----------|
| 01 | JDK 구조와 바이트코드 | JDK/JRE/JVM, 클래스 로딩, 바이트코드 |
| 02 | 가상 머신 실행 서브시스템 | 스택 프레임, invoke 명령어, 디스패치 |
| 03 | 컴파일과 최적화 | JIT C1/C2, 인라이닝, 탈출 분석 |
| 04 | 효율적 동시성 | JMM, 락 최적화, CAS |
| 05 | GC 알고리즘과 튜닝 | G1GC, ZGC, Shenandoah, 튜닝 |
| 06 | Java 성능 | JMH, 프로파일링, 최적화 |
| 07 | Java 직렬화 | Serializable, 보안, 대안 |
| 08 | 문자 인코딩 | ASCII→Unicode, UTF-8/16, Compact Strings |
| 09 | NIO와 채널-버퍼 | Channel, Buffer, Selector, Path/Files |
| 10 | 소켓 프로그래밍 | TCP, 멀티스레드 서버, Virtual Thread 서버 |
| 11 | HTTP 서버 구현 | HTTP 파싱, 리플렉션 라우팅 |
| 12 | 빌드 도구 | Maven, Gradle, 의존성 관리 |

## 학습 순서
01~06 (JVM) → 07~11 (I/O & Network) → 12 (Build)
