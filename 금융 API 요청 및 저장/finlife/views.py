# finlife/views.py (save_deposit_products 함수 수정)

import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DepositProducts, DepositOptions
from .serializers import DepositProductsSerializer, DepositProductOptionsSerializer
from rest_framework import status

BASE_URL = 'http://finlife.fss.or.kr/finlifeapi'
API_KEY = settings.API_KEY # settings.py에서 불러온 키
PRODUCTS_SEARCH_URL = f'{BASE_URL}/depositProductsSearch.json'
@api_view(['GET']) 
def save_deposit_products(request):
    
    # 1. 환경 설정 및 API 호출 (이전과 동일)
    API_KEY = settings.API_KEY
    URL = PRODUCTS_SEARCH_URL
    params = {
        'auth': API_KEY, 
        'topFinGrpNo': '020000', 
        'pageNo': 1
    }
    
    response = requests.get(URL, params=params)
    data = response.json()
    result = data.get('result')
    
    if not result:
        # API 응답에 result 자체가 없는 경우 (치명적인 오류)
        return Response({'error': 'API 호출에 실패했거나 데이터가 없습니다.'}, status=400)
    
    # 수정된 부분: baseList와 optionList가 None인 경우 빈 리스트([])로 처리하여 오류 방지
    product_list = result.get('baseList', []) # <--- .get(key, default)를 사용
    options_list = result.get('optionList', []) # <--- .get(key, default)를 사용

    # ----------------------------------------------------
    # 2. 상품 (Products) 데이터 저장 (F01)
    # ----------------------------------------------------
    
    # 상품 코드와 저장된 Product 객체를 매핑하는 딕셔너리 생성 (DB 재조회 방지 목적)
    product_dict = {} 
    
    for product_data in product_list:
        save_data = {
            'fin_prdt_cd': product_data['fin_prdt_cd'],
            'kor_co_nm': product_data['kor_co_nm'],
            'fin_prdt_nm': product_data['fin_prdt_nm'],
            # ... (나머지 필드: 이전 뷰와 동일하게 구성)
            'join_way': product_data.get('join_way', ''),
            'join_member': product_data.get('join_member', ''),
            'join_deny': product_data.get('join_deny', 1),
            'max_limit': product_data.get('max_limit'),
            'etc_note': product_data.get('etc_note', ''),
            'spcl_cnd': product_data.get('spcl_cnd', '')
        }
        
        product, created = DepositProducts.objects.update_or_create(
            fin_prdt_cd=save_data['fin_prdt_cd'],
            defaults=save_data
        )
        
        # 딕셔너리에 저장하여 나중에 옵션 연결 시 사용 (DB 쿼리 방지)
        product_dict[product.fin_prdt_cd] = product


    # ----------------------------------------------------
    # 3. 옵션 (Options) 데이터 저장 (F01)
    # ----------------------------------------------------
    
    for option_data in options_list:
        fin_prdt_cd = option_data['fin_prdt_cd']
        
        # 딕셔너리에서 이미 저장된 Product 객체를 가져와 외래키로 사용
        product_instance = product_dict.get(fin_prdt_cd)
        
        if product_instance:
            # intr_rate, intr_rate2가 None일 경우 -1로 처리 (요구사항 F01 반영)
            intr_rate = option_data.get('intr_rate') if option_data.get('intr_rate') is not None else -1
            intr_rate2 = option_data.get('intr_rate2') if option_data.get('intr_rate2') is not None else -1
            
            DepositOptions.objects.update_or_create(
                # 외래키 연결을 위해 Product 객체 사용
                product=product_instance, 
                save_trm=option_data['save_trm'],
                defaults={
                    'intr_rate': intr_rate,
                    'intr_rate2': intr_rate2,
                    'intr_rate_type': option_data['intr_rate_type'],
                    'intr_rate_type_nm': option_data['intr_rate_type_nm'],
                }
            )
            
    return Response({'message': '정기예금 상품 및 옵션 데이터 저장이 완료되었습니다.'})


# [F02] 상품 목록 조회
@api_view(['GET', 'POST'])
def deposit_products(request):
    if request.method == 'GET':
        # F02 로직: 목록 조회
        products = DepositProducts.objects.all()
        serializer = DepositProductsSerializer(products, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # F03 로직: 상품 추가
        serializer = DepositProductsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({ 'message': '데이터 삽입 성공' }, status=status.HTTP_201_CREATED)

# [F04] 특정 상품 옵션 리스트 출력
@api_view(['GET'])
def deposit_product_options(request, fin_prdt_cd):
    # 1. 특정 상품 코드에 해당하는 상품 조회
    try:
        # get() 메서드를 사용하여 단 하나의 객체를 조회
        product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
    
    except DepositProducts.DoesNotExist:
        # 상품을 찾지 못했을 경우 404 Not Found 응답 반환
        return Response({ 'error': '상품을 찾을 수 없습니다.' }, status=status.HTTP_404_NOT_FOUND)

    # 2. Serializer를 사용하여 객체를 JSON 형태로 변환
    # F02에서 옵션 정보를 중첩하도록 구현했기 때문에, 이 Serializer 하나로 상품과 옵션이 모두 반환됩니다.
    serializer = DepositProductsSerializer(product)
    
    # 3. JSON 응답 반환
    return Response(serializer.data)

# [F05] 최고 금리 상품 조회
@api_view(['GET'])
def top_rate_product(request):
    # 1. 모든 옵션 중 intr_rate2가 가장 높은 단 하나의 객체를 조회
    try:
        # intr_rate2 필드를 기준으로 내림차순 정렬 후 첫 번째 객체 선택
        # intr_rate2가 NULL인 경우를 제외하기 위해 filter로 거르는 것이 좋습니다.
        top_option = DepositOptions.objects.filter(
            intr_rate2__isnull=False
        ).order_by('-intr_rate2').first() 
        # DepositOptions 모델을 사용하셨다면 모델 이름 변경

    except Exception:
        # 데이터가 없는 경우 (F01을 실행하지 않은 경우)
        return Response({ 'message': '저장된 상품 옵션 데이터가 없습니다.' }, status=status.HTTP_404_NOT_FOUND)

    # 2. 최고 금리 옵션이 없는 경우 처리
    if not top_option:
        return Response({ 'message': '유효한 최고 금리 데이터를 찾을 수 없습니다.' }, status=status.HTTP_404_NOT_FOUND)

    # 3. Serializer를 사용하여 옵션과 중첩된 상품 정보를 JSON으로 변환
    serializer = DepositProductOptionsSerializer(top_option)
    
    # 4. JSON 응답 반환
    return Response(serializer.data)