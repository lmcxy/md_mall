from django.conf.urls import url

from verifications import views


urlpatterns = [
    # 短信验证码
    url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$',views.SMSCodeView.as_view()),
]