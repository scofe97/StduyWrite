# [Spring Study] 05-xx. 파일 업로드

주제: Spring Study

- 참고
    
    [[Spring MVC] [2] 11. 파일 업로드](https://velog.io/@dbsrud11/Spring-MVC-2-11.-%ED%8C%8C%EC%9D%BC-%EC%97%85%EB%A1%9C%EB%93%9C)
    
    [Spring Boot - 파일 업로드 용량제한 설정](https://velog.io/@jinho_pca/Spring-Boot-%ED%8C%8C%EC%9D%BC-%EC%97%85%EB%A1%9C%EB%93%9C-%EC%9A%A9%EB%9F%89%EC%A0%9C%ED%95%9C-%EC%84%A4%EC%A0%95)
    

# **파일 업로드 소개**

---

<aside>
💡 **NOTE**

### HTML 폼 전송 방식

1. **application/x-www-form-urlencoded**
2. **multipart/form-data**
</aside>

## **application/x-www-form-urlencoded 방식**

<aside>
✍️ **NOTE**

> ***HTML 폼 데이터를 서버로 전송하는 가장 기본적인 방법!***
> 

![쿼리파라미터 방식으로 전송됨](%5BSpring%20Study%5D%2005-xx%20%ED%8C%8C%EC%9D%BC%20%EC%97%85%EB%A1%9C%EB%93%9C/Untitled.png)

쿼리파라미터 방식으로 전송됨

- **Form** 태그에 별도의 **enctype**옵션이 없다면, 요청 **HTTP**헤더에 자동으로 `Content-Type: application/x-www-form-urlencoded`를 추가한다.
- 하지만 파일 업로드는 문자가 아닌 바이너리 데이터를 전송해야 한다. 또한, 보통 폼을 전송할 때 파일만 전송하지 않는다는 점을 해결해야 한다.
    - **문자와 바이너리를 동시에 전송** → `multipart/form-data` 사용
</aside>

## **multipart/form-data**

<aside>
✍️ **NOTE**

![form의 enctype에 multipart/form-data 추가 (각 파트마다 헤더와 바디를 가진다.)](%5BSpring%20Study%5D%2005-xx%20%ED%8C%8C%EC%9D%BC%20%EC%97%85%EB%A1%9C%EB%93%9C/Untitled%201.png)

form의 enctype에 multipart/form-data 추가 (각 파트마다 헤더와 바디를 가진다.)

- 이 방식은 다른 종류의 여러 파일과 폼 내용을 함께 전달할 수 있다! (**multipart**)

### content-Disposition

- 항목별 헤더, 여기에 부가 정보가 포함된다.
- 이렇게 항목을 구분해서 한 번에 전송이 가능하다!
</aside>

# **스프링과 파일 업로드**

---

<aside>
💡 **NOTE**

> ***서블릿 방식도 같이 소개하지만, 사실 스프링방식만 알아도 상관없으므로 생략한다..***
> 

### Form(MultipartFile 타입) 받기!

```java
@Data
public class ItemForm {
    private Long itemId;
    private String itemName;
    private MultipartFile attachFile;
    private List<MultipartFile> imageFiles;
}
```

```java
@PostMapping("/items/new")
public String saveItem(@ModelAttribute ItemForm form, RedirectAttributes redirectAttributes) throws IOException {
    UploadFile attachFile = fileStore.storeFile(form.getAttachFile());
    List<UploadFile> storeImageFiles = fileStore.storeFiles(form.getImageFiles());

    // 데이터베이스에 저장
    // ...

    return "redirect:/items/{itemId}";
}
```

- 위와 같이 Form의 형식에 따라 DTO를 작성하고, 파일은 `MultipartFile` 타입으로 받는다.

### MultipartFile 주요 메서드

- `file.getOriginalFilename()` : 업로드 파일명
- `file.transferTo()` : 파일 저장
</aside>

# **예제로 구현하는 파일 업로드, 다운로드**

---

<aside>
💡 **NOTE**

> ***실제로 파일업로드 방식을 구현해보자!***
> 

### 요구사항

![Untitled](%5BSpring%20Study%5D%2005-xx%20%ED%8C%8C%EC%9D%BC%20%EC%97%85%EB%A1%9C%EB%93%9C/Untitled%202.png)

- 상품을 관리(상품 이름, 첨부파일 하나, 이미지파일 여러개)
- 첨부파일 업로드, 다운로드 기능
- 업로드한 이미지 웹 브라우저에서 확인
</aside>

## DTO

<aside>
✍️ **NOTE**

```java
@Data
public class ItemForm {
    private Long itemId;
    private String itemName;
    private MultipartFile attachFile;
    private List<MultipartFile> imageFiles;
}
```

</aside>

## Entity

<aside>
✍️ **NOTE**

```java
@Data
public class Item {

    private Long id;
    private String itemName;
    private UploadFile attachFile;
    private List<UploadFile> imageFiles;
}
```

```java
@Data
public class UploadFile {

    private String uploadFileName;
    private String storeFileName;

    public UploadFile(String uploadFileName, String storeFileName) {
        this.uploadFileName = uploadFileName;
        this.storeFileName = storeFileName;
    }
}
```

</aside>

## FileStore

<aside>
✍️ **NOTE**

- **전체코드!**
    
    ```java
    @Component
    public class FileStore {
    
        @Value("${file.dir}")
        private String fileDir;
    
        public String getFullPath(String filename) {
            return fileDir + filename;
        }
    
        public List<UploadFile> storeFiles(List<MultipartFile> multipartFiles) throws IOException {
            List<UploadFile> storeFileResult = new ArrayList<>();
            for (MultipartFile multipartFile : multipartFiles) {
                if(!multipartFile.isEmpty()){
                    UploadFile uploadFile = storeFile(multipartFile);
                    storeFileResult.add(uploadFile);
                }
            }
    
            return storeFileResult;
        }
    
        public UploadFile storeFile(MultipartFile multipartFile) throws IOException {
            if (multipartFile.isEmpty()) {
                return null;
            }
    
            String originalFilename = multipartFile.getOriginalFilename();
            String storeFileName = createStoreFileName(originalFilename);
    
            multipartFile.transferTo(new File(getFullPath(storeFileName)));
            return new UploadFile(originalFilename, storeFileName);
    
        }
    
        private String createStoreFileName(String originalFilename) {
            String uuid = UUID.randomUUID().toString();
            String ext = extracted(originalFilename);
            return uuid + "." + ext;
        }
    
        private String extracted(String originalFilename) {
            int pos = originalFilename.lastIndexOf(".");
            return originalFilename.substring(pos + 1);
        }
    
    }
    ```
    

### 첨부파일 저장

```java
// properties에 있는 경로값
@Value("${file.dir}")
private String fileDir;

// 파일을 어디다 저장할것인지
public String getFullPath(String filename) {
    return fileDir + filename;
}
```

```java
public UploadFile storeFile(MultipartFile multipartFile) throws IOException {
    if (multipartFile.isEmpty()) {
        return null;
    }

		// 저장할 파일명으로 변경
    String originalFilename = multipartFile.getOriginalFilename();
    String storeFileName = createStoreFileName(originalFilename);

		// 파일저장
    multipartFile.transferTo(new File(getFullPath(storeFileName)));
    return new UploadFile(originalFilename, storeFileName);

}
```

### 파일 리스트 저장

```java
public List<UploadFile> storeFiles(List<MultipartFile> multipartFiles) throws IOException {
    List<UploadFile> storeFileResult = new ArrayList<>();

		// 여러 파일 처리
    for (MultipartFile multipartFile : multipartFiles) {
        if(!multipartFile.isEmpty()){
            UploadFile uploadFile = storeFile(multipartFile);
            storeFileResult.add(uploadFile);
        }
    }

    return storeFileResult;
}
```

### 업로드 파일명 → DB에 저장할 파일명 변경

```java
// 저장할 파일이름 ex(UUID 랜덤값 + . + png )
private String createStoreFileName(String originalFilename) {
    String uuid = UUID.randomUUID().toString();
    String ext = extracted(originalFilename);
    return uuid + "." + ext;
}

// .png 형식 살리기
private String extracted(String originalFilename) {
    int pos = originalFilename.lastIndexOf(".");
    return originalFilename.substring(pos + 1);
}
```

</aside>

## Controller

<aside>
✍️ **NOTE**

- **전체코드!**
    
    ```java
    @Slf4j
    @Controller
    @RequiredArgsConstructor
    public class ItemController {
    
        private final ItemRepository itemRepository;
        private final FileStore fileStore;
    
        @GetMapping("/items/new")
        public String newItem(@ModelAttribute ItemForm form) {
            return "item-form";
        }
    
        @PostMapping("/items/new")
        public String saveItem(@ModelAttribute ItemForm form, RedirectAttributes redirectAttributes) throws IOException {
            UploadFile attachFile = fileStore.storeFile(form.getAttachFile());
            List<UploadFile> storeImageFiles = fileStore.storeFiles(form.getImageFiles());
    
            // 데이터베이스에 저장
            Item item = new Item();
            item.setItemName(form.getItemName());
            item.setAttachFile(attachFile);
            item.setImageFiles(storeImageFiles);
            itemRepository.save(item);
    
            redirectAttributes.addAttribute("itemId", item.getId());
    
            return "redirect:/items/{itemId}";
        }
    
        @GetMapping("/items/{id}")
        public String items(@PathVariable Long id, Model model) {
            Item item = itemRepository.findById(id);
            model.addAttribute("item", item);
            return "item-view";
        }
    
        @ResponseBody
        @GetMapping("/images/{filename}")
        public Resource downloadImage(@PathVariable String filename) throws MalformedURLException {
            return new UrlResource("file:" + fileStore.getFullPath(filename));
        }
    
        @GetMapping("/attach/{itemId}")
        public ResponseEntity<Resource> downloadAttach(@PathVariable Long itemId) throws MalformedURLException {
            Item item = itemRepository.findById(itemId);
            String storeFileName = item.getAttachFile().getStoreFileName();
            String uploadFileName = item.getAttachFile().getUploadFileName();
    
            UrlResource resource = new UrlResource("file:" + fileStore.getFullPath(storeFileName));
    
            log.info("uploadFileName={}", uploadFileName);
    
            String encodedUploadFileName = UriUtils.encode(uploadFileName, StandardCharsets.UTF_8);
            String contentDisposition = "attach; filename=\"" +  encodedUploadFileName + "\"";
    
            return ResponseEntity.ok()
                    .header(HttpHeaders.CONTENT_DISPOSITION, contentDisposition)
                    .body(resource);
        }
    }
    ```
    

### 이미지 반환

```java
@ResponseBody
@GetMapping("/images/{filename}")
public Resource downloadImage(@PathVariable String filename) throws MalformedURLException {
    return new UrlResource("file:" + fileStore.getFullPath(filename));
}
```

### 다운로드

```java
@GetMapping("/attach/{itemId}")
public ResponseEntity<Resource> downloadAttach(@PathVariable Long itemId) throws MalformedURLException {
    Item item = itemRepository.findById(itemId);
    String storeFileName = item.getAttachFile().getStoreFileName();
    String uploadFileName = item.getAttachFile().getUploadFileName();

		// 파일 다운로드 위한 생성
    UrlResource resource = new UrlResource("file:" + fileStore.getFullPath(storeFileName));
    log.info("uploadFileName={}", uploadFileName);

		// 파일명 인코딩 및 파일 다운로드 기능 추가
    String encodedUploadFileName = UriUtils.encode(uploadFileName, StandardCharsets.UTF_8);
    String contentDisposition = "attach; filename=\"" +  encodedUploadFileName + "\"";

    return ResponseEntity.ok()
            .header(HttpHeaders.CONTENT_DISPOSITION, contentDisposition)
            .body(resource);
}
```

</aside>

## ⚠️ 참고!

<aside>
✍️ **NOTE**

> ***MultipartFIle의 용량제한의 기본값은 1MB**이다. 이 제한을 해제하려면 **yaml**에서 설정을 해주어야 한다.*
> 

```yaml
spring:
  servlet:
    multipart:
      max-file-size: 10MB
      max-request-size: 10MB
```

</aside>