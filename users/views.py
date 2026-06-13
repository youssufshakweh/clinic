from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from .serializers import (
    UserSerializer, 
    RegisterSerializer, 
    ForgotPasswordSerializer,
    VerifyOTPSerializer,
    ChangePasswordSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'register':
            return RegisterSerializer
        elif self.action == 'forgot_password':
            return ForgotPasswordSerializer
        elif self.action == 'verify_otp':
            return VerifyOTPSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action in ['register', 'forgot_password', 'verify_otp']:
            return [AllowAny()]
        return super().get_permissions()
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """تسجيل مستخدم جديد"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            try:
                otp_code = user.otp
                send_mail(
                    subject='رمز التحقق من البريد الالكتروني',
                    message=f'رمز التحقق الخاص بك: {otp_code}\nصلاحيته: 10 دقائق',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"خطأ في إرسال البريد: {e}")
            
            return Response({
                'message': 'تم إنشاء الحساب بنجاح. يرجى التحقق من البريد الالكتروني',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def forgot_password(self, request):
        """طلب استعادة كلمة المرور"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            
            otp_code = user.generate_otp()
            
            try:
                send_mail(
                    subject='رمز استعادة كلمة المرور',
                    message=f'رمز الاستعادة الخاص بك: {otp_code}\nصلاحيته: 10 دقائق',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"خطأ في إرسال البريد: {e}")
            
            return Response({
                'message': 'تم إرسال رمز الاستعادة إلى بريدك الالكتروني'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def verify_otp(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'تم التحقق بنجاح وتعيين كلمة المرور الجديدة',
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """تغيير كلمة المرور للمستخدم المسجل"""
        user = request.user
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # التحقق من كلمة المرور القديمة
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {'error': 'كلمة المرور الحالية غير صحيحة'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({'message': 'تم تغيير كلمة المرور بنجاح'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


from rest_framework.views import APIView
from patients.models import Patient


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response(
                {'error': 'البريد الالكتروني والرمز مطلوبان'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'البريد الالكتروني غير موجود'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.verify_otp(otp):
            return Response(
                {'error': 'الرمز غير صحيح أو انتهت صلاحيته'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.is_verified = True
        user.otp = None
        user.otp_created_at = None
        user.save()

        Patient.objects.get_or_create(user=user)

        return Response(
            {'message': 'تم التحقق من البريد الالكتروني بنجاح'},
            status=status.HTTP_200_OK
        )

