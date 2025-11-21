// js/main.js

let mapInstance; 
let mapData = {}; 
let markers = []; // F04: 마커 객체들을 저장할 배열
let ps; // F04: 장소 검색 서비스 객체

kakao.maps.load(() => {
    // 1. F02: 지도 생성 로직 (기존 코드)
    var container = document.getElementById('map');
    var options = {
        center: new kakao.maps.LatLng(37.49818, 127.027386), // 강남역 좌표
        level: 3
    };
    mapInstance = new kakao.maps.Map(container, options);
    console.log("✅ F02: 지도 생성 완료 (강남역 중심)");
    
    // F04: 장소 검색 서비스 객체를 생성합니다.
    ps = new kakao.maps.services.Places();
    
    // F03: 데이터 로드 및 UI 초기화 (기존 코드)
    fetch('./data.json')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Failed to fetch data.json: ${response.status} ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            mapData = data; 
            initializeDropdowns(data.mapInfo, data.bankInfo);
            setupCityProvinceHandler(data.mapInfo); 
            
            // ✅ F04: 검색 버튼 이벤트 리스너 설정
            document.getElementById('search-button').addEventListener('click', searchPlaces);
            
        })
        .catch(error => {
            console.error('❌ Data Load Error:', error);
            alert('은행 정보 데이터를 불러오는 데 실패했습니다. 콘솔을 확인하세요.');
        });
});

// --- F03 관련 함수 (유지) ---

function initializeDropdowns(mapInfo, bankInfo) {
    const cityProvinceSelect = document.getElementById('select-city-province');
    const bankSelect = document.getElementById('select-bank');
    
    mapInfo.forEach(cityProvince => {
        const option = document.createElement('option');
        option.value = cityProvince.name;
        option.textContent = cityProvince.name;
        cityProvinceSelect.appendChild(option);
    });

    bankInfo.forEach(bankName => {
        const option = document.createElement('option');
        option.value = bankName;
        option.textContent = bankName;
        bankSelect.appendChild(option);
    });

    console.log("✅ F03: 광역시/도 및 은행명 드롭다운 초기화 완료");
}

function setupCityProvinceHandler(mapInfo) {
    const cityProvinceSelect = document.getElementById('select-city-province');
    const districtSelect = document.getElementById('select-district');
    
    cityProvinceSelect.addEventListener('change', (event) => {
        const selectedCityProvince = event.target.value;
        
        districtSelect.innerHTML = '<option value="">시/군/구 선택</option>';
        
        if (!selectedCityProvince) {
            districtSelect.disabled = true;
            return;
        }
        
        districtSelect.disabled = false;
        
        const selectedInfo = mapInfo.find(info => info.name === selectedCityProvince);
        
        if (selectedInfo && selectedInfo.countries) {
            selectedInfo.countries.forEach(district => {
                const option = document.createElement('option');
                option.value = district;
                option.textContent = district;
                districtSelect.appendChild(option);
            });
        }
    });
}


// ----------------------------------------------------
// 3. F04: 은행 검색 및 마커 표시 로직
// ----------------------------------------------------

/**
 * 드롭다운 선택 값을 기반으로 장소 검색을 수행합니다.
 */
function searchPlaces() {
    const cityProvince = document.getElementById('select-city-province').value;
    const district = document.getElementById('select-district').value;
    const bankName = document.getElementById('select-bank').value;
    
    if (!cityProvince || !district || !bankName) {
        alert('광역시/도, 시/군/구, 은행명을 모두 선택해야 합니다.');
        return;
    }

    // 1. 검색어 생성 (예: '서울특별시 강남구 국민은행')
    const searchKeyword = `${cityProvince} ${district} ${bankName}`;
    console.log(`🔍 검색 시작: ${searchKeyword}`);
    
    // 2. 기존 마커 제거 (F04 요구사항)
    removeMarkers();

    // 3. 장소 검색 API 호출
    // keywordSearch(검색어, 콜백함수)
    ps.keywordSearch(searchKeyword, placesSearchCB);
}

/**
 * 장소 검색 콜백 함수. 검색 결과를 처리하고 마커를 표시합니다.
 */
function placesSearchCB(data, status, pagination) {
    if (status === kakao.maps.services.Status.OK) {
        console.log(`✅ 검색 결과 ${data.length}개 발견`);
        
        // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기 위해 LatLngBounds 객체에 좌표를 추가합니다.
        const bounds = new kakao.maps.LatLngBounds();
        
        for (let i = 0; i < data.length; i++) {
            displayMarker(data[i]);    
            bounds.extend(new kakao.maps.LatLng(data[i].y, data[i].x));
        }       

        // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다.
        mapInstance.setBounds(bounds);
        
    } else if (status === kakao.maps.services.Status.ZERO_RESULT) {
        alert('검색 결과가 존재하지 않습니다.');
        return;

    } else if (status === kakao.maps.services.Status.ERROR) {
        alert('검색 중 오류가 발생했습니다.');
        return;
    }
}

/**
 * 검색 결과 하나에 대해 마커와 인포윈도우 클릭 이벤트를 생성합니다.
 */
function displayMarker(place) {
    // 1. 마커 생성
    const marker = new kakao.maps.Marker({
        map: mapInstance,
        position: new kakao.maps.LatLng(place.y, place.x) 
    });
    
    // 생성된 마커를 배열에 추가 (제거를 위함)
    markers.push(marker);

    // 2. 인포윈도우 생성 (은행명과 주소)
    const infowindow = new kakao.maps.InfoWindow({
        content: `<div style="padding:5px;font-size:12px;">${place.place_name}<br>${place.address_name}</div>`
    });

    // 3. 마커에 클릭 이벤트 추가 (F04 요구사항: 마커 클릭 시 인포윈도우 출력)
    kakao.maps.event.addListener(marker, 'click', function() {
        // 기존의 열려있는 인포윈도우를 닫고 새 인포윈도우를 엽니다.
        // (현재 코드에서는 전역 인포윈도우 변수가 없으므로, 단순 토글 방식으로 구현)
        infowindow.open(mapInstance, marker);
    });
    
    // 인포윈도우 외부 클릭 시 닫기 이벤트 추가 (선택적)
    kakao.maps.event.addListener(mapInstance, 'click', function() {
        infowindow.close();
    });
}

/**
 * 기존 마커들을 지도에서 제거하고 배열을 비웁니다. (F04 요구사항)
 */
function removeMarkers() {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null); // 지도에서 마커 제거
    }   
    markers = []; // 마커 배열 초기화
    console.log("🧹 기존 마커 제거 완료");
}