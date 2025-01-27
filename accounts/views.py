from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import  APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from accounts.serializers import RegisterSerializer, LoginSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    
    def post(self, request):
        serializer = RegisterSerializer
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            },status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MobileNumberCheckView(APIView):
    """
    Public API to check if a given mobile number exists in the database.
    It applies DRF throttling to prevent abuse and only returns specific status codes.
    """
    
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    
    def post(self,request):
        """
        Check if the given mobile_number exists in the User model.
        Expects JSON like: {"mobile_number": "09123456789"}
        """
        # Extract the mobile number from the request data
        mobile_number = request.data.get("mobile_number")
        
        if not mobile_number or not mobile_number.isdigit() or len(mobile_number)!=11:
            return Response(
                {"error": "Invalid mobile number. it must be 11 digit."},
                status= status.HTTP_400_BAD_REQUEST
            )
        user_exists = User.objects.filter(mobile_number=mobile_number).exists()
        
        if user_exists:
            return Response({"message":"Mobile Number exists."},
                            status=status.HTTP_200_OK)
        else:
            return Response({"message":'Mobile Number not found.'},
                            status=status.HTTP_404_NOT_FOUND)
            

        