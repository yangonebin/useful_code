# 실행순서 (내 나름대로 이해한 버전)

실행 순서

1. SDK 로드와 권한 확인 (Initial Load)

mapScript.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${API_KEY}&autoload=false&libraries=services`;


2. main.js 동적 로드

// ✅ 핵심: 카카오 API 로드가 완료되면 main.js를 동적으로 로드합니다.
            mapScript.onload = () => {
                const mainScript = document.createElement('script');
                mainScript.src = 'js/main.js';
                document.body.appendChild(mainScript);
            };
						
            document.head.appendChild(mapScript);

3. kakao맵 로드

kakao.maps.load(() => { ....

- / F04: 장소 검색 서비스 객체를 생성합니다.
    ps = new kakao.maps.services.Places();

- fetch('./data.json')
        .then(response => { ... : 데이터 로드

4. 검색 버튼 이벤트 리스너

document.getElementById('search-button').addEventListener('click', searchPlaces);
            

5. 검색 요청 
function searchPlaces()
->
ps.keywordSearch(searchKeyword, placesSearchCB);

참고)
ps.keywordSearch(검색어, 검색이_완료되면_실행할_함수);
- https://dapi.kakao.com/v2/local/search/keyword.json?query=...)로 요청

- kakao 서버 응답
- placesSearchCB 함수 실행

6.  placesSearchCB 함수 

장소 검색 콜백 함수. 검색 결과를 처리하고 마커를 표시

function placesSearchCB(data, status, pagination) {

---
# 실행순서 (GPT 첨삭버전)


### 1단계: 초기 환경 설정 및 API 권한 확인 (동기적 실행)

브라우저가 `index.html` 파일을 위에서부터 순서대로 파싱하며 실행되는 단계입니다.

1.  **`apikey.js` 로드:**
    * `<script src="js/apikey.js"></script>` 태그가 실행되어 전역 변수 **`API_KEY`**가 메모리에 정의됩니다. (**보안 목표 달성**)

2.  **API Key 변수 확인:**
    * 인라인 `<script>` 블록이 실행되어 `if (typeof API_KEY !== 'undefined')` 조건문을 통해 `API_KEY` 변수의 존재를 확인합니다.

3.  **SDK 로드 및 권한 요청 (비동기 시작):**
    * JavaScript 코드가 `<script>` DOM 객체를 생성하고 `mapScript.src = ... &libraries=services`를 통해 **Kakao 서버에 지도 및 장소 검색 API 사용 권한**을 요청합니다.
    * `document.head.appendChild(mapScript);`를 통해 **Kakao SDK 파일 다운로드를 비동기적으로 시작**합니다.

---

### 2단계: 핵심 라이브러리 로드 및 메인 로직 실행 준비 (비동기 완료)

Kakao SDK 파일 다운로드 및 실행이 완료되어 `kakao` 객체가 정의된 후, 다음 로직이 실행됩니다.

4.  **`main.js` 동적 로드:**
    * **`mapScript.onload`** 이벤트 핸들러가 실행됩니다.
    * 이 콜백 함수 내부에서 **`js/main.js`** 파일이 동적으로 로드되고 즉시 실행됩니다. (**`kakao is not defined` 오류 해결**)

5.  **`kakao.maps.load()` 실행 (SDK 기능 활성화 대기):**
    * `main.js`가 실행되면서 **`kakao.maps.load(() => { ... })`** 함수가 호출됩니다.
    * 이는 Kakao API 내부의 모든 모듈(지도, 장소 검색 등)이 완전히 준비될 때까지 기다리는 **Kakao API 자체의 안전 장치**입니다.

---

### 3단계: 초기 기능 활성화 및 UI 구성 (지도, 데이터 로드)

`kakao.maps.load`의 콜백 함수 내부가 실행되며 프로젝트의 초기 기능이 활성화됩니다.

6.  **F02 지도 초기화 및 F04 서비스 객체 생성:**
    * `new kakao.maps.Map(...)`을 통해 강남역을 중심으로 한 **지도(`mapInstance`)를 생성**합니다.
    * `ps = new kakao.maps.services.Places();`를 통해 **장소 검색 서비스 객체(`ps`)**를 생성합니다.

7.  **F03 데이터 로드 및 UI 구성 (비동기):**
    * `fetch('./data.json')`을 통해 **은행/지역 정보 JSON 파일을 비동기적으로 로드**합니다.
    * 데이터 로드가 성공하면 (`.then` 체인), `initializeDropdowns`와 `setupCityProvinceHandler`가 실행되어 **광역시/도, 시/군/구, 은행명 드롭다운을 동적으로 채웁니다.**

8.  **F04 검색 리스너 등록:**
    * `document.getElementById('search-button').addEventListener('click', searchPlaces);` 코드가 실행되어 **`검색` 버튼에 `searchPlaces` 함수를 연결**합니다.

---

### 4단계: 사용자 상호 작용 및 검색 요청 (비동기 실행)

사용자가 `검색` 버튼을 클릭했을 때의 흐름입니다.

9.  **검색 요청 시작 (사용자 행동):**
    * 사용자가 드롭다운 선택 후 **`검색` 버튼을 클릭**합니다.
    * 이벤트 리스너에 의해 **`searchPlaces()` 함수가 실행**됩니다.

10. **API 검색 호출:**
    * `searchPlaces()` 내부에서 **`ps.keywordSearch(searchKeyword, placesSearchCB);`**가 호출됩니다.
    * 이 함수는 Kakao 서버로 검색 요청을 보냅니다. (**비동기 통신**)

11. **API 응답 및 마커 표시 (콜백 실행):**
    * Kakao 서버가 검색 결과를 JSON으로 반환합니다.
    * 콜백 함수 **`placesSearchCB(data, status, pagination)`**가 자동으로 실행됩니다.
    * 이 함수는 **`data`**를 기반으로 반복문을 돌며 지도에 **마커를 표시**하고, **지도 경계를 재설정**합니다.

