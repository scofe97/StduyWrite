# 15. unsafe와 FFI

unsafe 키워드는 Rust의 안전성 보장을 우회하는 5가지 슈퍼파워를 제공하지만, 빌림 검사를 끄는 것이 아니라 추가 책임을 프로그래머에게 부여합니다. FFI(Foreign Function Interface)로 C 라이브러리를 호출할 때 필수이며, 원시 포인터와 함께 low-level 시스템 프로그래밍을 가능하게 합니다. 사운드니스(soundness)를 유지하는 것이 핵심입니다.

## 목표
- [ ] unsafe 블록의 필요성과 책임 이해
- [ ] unsafe가 허용하는 5가지 작업 설명
- [ ] 원시 포인터(*const T, *mut T) 사용
- [ ] extern "C"로 C 함수 호출
- [ ] #[no_mangle]과 C로의 함수 노출
- [ ] FFI에서 메모리 관리 책임 구분
- [ ] unsafe의 사운드니스(soundness) 개념 이해

## 1. unsafe 블록

## 2. unsafe가 허용하는 5가지

## 3. 원시 포인터(*const T, *mut T)

## 4. FFI(extern "C")

## 5. C 라이브러리 호출

## 6. #[no_mangle]

## 명령어 요약
| 개념 | 설명 |
|------|------|
| `unsafe {}` | 안전성 보장 우회 블록 |
| `*const T` | 불변 원시 포인터 |
| `*mut T` | 가변 원시 포인터 |
| `extern "C"` | C ABI 함수 선언/정의 |
| `#[no_mangle]` | 함수명 맹글링 방지 (C 호출 가능) |
| `std::ffi::CString` | Rust String → C char* 변환 |
| `as_ptr()` | 원시 포인터 얻기 |

## 체크포인트
- unsafe가 빌림 검사를 끄는 것이 아닌 이유는?
- unsafe가 허용하는 5가지 작업은 무엇인가?
- FFI에서 메모리 해제 책임은 누구에게 있는가?
- Java JNI vs Rust FFI의 차이는?
- &T에서 *const T로 변환은 안전하지만 역변환이 unsafe인 이유는?
- 사운드니스(soundness)란 무엇인가?
- unsafe 함수 내부에서 safe 함수를 호출할 때 주의할 점은?
