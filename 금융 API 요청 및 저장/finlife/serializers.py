# finlife/serializers.py

from rest_framework import serializers
from .models import DepositProducts, DepositOptions

# ----------------------------------------------------
# 1. 상품 Serializer (메인 목록 조회용)
# ----------------------------------------------------
class DepositProductsSerializer(serializers.ModelSerializer):
    # DepositProducts 모델에 Option 정보가 필요하므로,
    # 역참조(`depositproductoptions_set`) 관계를 활용하여 옵션 데이터를 중첩합니다.
    # 옵션이 여러 개일 수 있으므로 many=True 설정이 필요합니다.
    # depositproductoptions_set = DepositProductOptionsSerializer(
        # many=True, read_only=True
    # )

    class Meta:
        model = DepositProducts
        # F05에서는 상품 정보만 깔끔하게 보이면 되므로, 옵션 리스트는 제외하고 명시
        fields = (
            'fin_prdt_cd', 'kor_co_nm', 'fin_prdt_nm', 'join_way', 
            'join_member', 'etc_note', 'spcl_cnd',
        )
# ----------------------------------------------------
# 2. 옵션 Serializer (내부 중첩용)
# ----------------------------------------------------
class DepositProductOptionsSerializer(serializers.ModelSerializer):
    product = DepositProductsSerializer(read_only=True)
    
    class Meta:
        model = DepositOptions
        # 상품 옵션 테이블에서 필요한 필드를 모두 지정합니다.
        fields = '__all__'


