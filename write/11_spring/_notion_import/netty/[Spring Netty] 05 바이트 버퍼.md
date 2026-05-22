# [Spring Netty] 05. 바이트 버퍼

주제: Spring Netty

- 참고
    
    [Netty 바이트 버퍼](https://shortstories.gitbook.io/studybook/netty/bc14_c774_d2b8_bc84_d37c)
    

# **바이트 버퍼**

---

<aside>
💡 **NOTE**

> *자바가 버퍼 패키지를 제공함에도 **Netty는 내부에서의 데이터 이동, 입출력에 자체 버퍼 API를 사용한다.***
> 
</aside>

## ***자바의 NIO 바이트 버퍼***

<aside>
✍️ **NOTE**

> 바이트 데이터를 저장하고 읽는 저장소
> 
- **저장되는 데이터 형에 따른 Byte Buffer 종류**
    - `ByteBuffer`, `CharBuffer`, `IntBuffer` …
- **ByteBuffer 클래스는 내부의 배열 상태를 관리하는 3가지 속성을 가진다.**
    - capacity
        - 버퍼에 저장가능한 최대 크기, 불변 값
    - position
        - 읽기/쓰기 작업 중인 위치
    - limit
        - 읽고 쓸 수 있는 공간의 최대치
</aside>

## ***네티의 바이트 버퍼***

<aside>
✍️ **NOTE**

> *자바 BytueBuffer보다 빠르며, 할당과 해제 부담을 줄였다.*
> 
- **특징**
    - 별도 읽기 인덱스, 쓰기 인덱스 보유
    - 가변 ByteBuffer
    - 각 데이터 형에 따른 읽기/쓰기 메서드 제공
- **생성방법**
    - ByteBufAllocator (인터페이스)
    - PooledByteBufAllocator (추상 구현체 사용)

### 네티 바이트 버퍼의 종류

- `PooledHeapByteBuf`
- `PooledDirectByteBuf`
- `UnpooledHeapByteBuf`
- `UnpooledDirectByteBuf`

### 네티 바이트 버퍼 생성 방법

- `PooledByteBufAllocator.DEFAULT.headBuffer()`
- `PooledByteBufAllocator.DEFAULT.directBuffer()`
- `Unpooled.buffer()`
- `Unpooled.directBuffer()`
</aside>