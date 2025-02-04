from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Score
from products.models import Product
from django.db.models import Avg
from rest_framework import status

class ScoreCreateView(APIView):
    """ثبت یا ویرایش امتیاز کاربر"""
    
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        user = request.user
        score_value = request.data.get("score")

        if score_value is None or not (0 <= int(score_value) <= 5):
            return Response({"error": "امتیاز باید عددی بین 0 تا 5 باشد"}, status=status.HTTP_400_BAD_REQUEST)

        score, created = Score.objects.update_or_create(
            product=product, user=user,
            defaults={"score": score_value}
        )

        return Response(
            {"message": "امتیاز با موفقیت ثبت شد" if created else "امتیاز ویرایش شد"},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
class ProductScoreView(APIView):
    """نمایش امتیاز کاربر و میانگین امتیاز محصول"""
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        user = request.user
        
        if not product:
            return Response({"error": "محصول یافت نشد."}, status=404)

        # دریافت امتیاز کاربر
        user_score = Score.objects.filter(product=product, user=user).first()
        user_score_value = user_score.score if user_score else None  # اگر امتیازی نداده باشد، مقدار None باشد.

        # محاسبه میانگین امتیاز محصول
        avg_score = product.scores.aggregate(Avg("score"))["score__avg"]
        avg_score_value = round(float(avg_score), 2) if avg_score is not None else 0.0

        return Response({
            "product": product.product_name,
            "user_score": user_score_value,
            "average_score": avg_score_value
        })
