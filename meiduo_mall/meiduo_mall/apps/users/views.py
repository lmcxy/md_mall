from django.conf import settings
from django.shortcuts import render
from django.views import View
from itsdangerous import BadData
from itsdangerous import TimedJSONWebSignatureSerializer
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.views import ObtainJSONWebToken

from users import serializers
from users.models import User
from users.serializers import CreateUserSerializer, UserAddressSerializer


# 判断用户名是否存在
class UsernameCountView(APIView):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        # print(count)
        data = {
            "username": username,
            "count": count
        }
        return Response(data)


# 用户注册视图
class CreateUserView(CreateAPIView):
    serializer_class = CreateUserSerializer


# 登陆接口
class MyObtainJSONWebToken(ObtainJSONWebToken):
    pass
    # 登录接口(使用jwt的视图),因为只返回token一个值,所以需要自定义视图函数返回token,user_id,username
    # 要返回的token,user_id,username,被定义users/utils.py,不在使用继承的类的返回值

    # 用手机号也可以登录的方法定义在users/utils.py,不在使用继承的类的只允许用户名登录


# 用户中心展示信息 url(r'^user/$', views.UserDetailView.as_view()),
class UserDetailView(RetrieveAPIView):
    """用户中心展示信息"""
    # 指定序列化器
    serializer_class = serializers.UserDetailSerializer

    # 设置权限,登陆后才能调用此接口
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # 返回当前登陆用户对象
        return self.request.user


# 修改邮箱
class EmailView(UpdateAPIView):
    """"""
    # 设置权限,登陆后才能调用此接口
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.EmailSerializer

    # 重写GenericAPIView的方法，指定要修改的是哪一条用户数据
    def get_object(self):
        return self.request.user


# 激活邮箱view
# GET /email/verification/?token=xxx
class VerifyEmailView(APIView):
    """激活用户邮箱"""
    def get(self, request):
        # 1. 获取请求参数： token
        token = request.query_params.get('token')  #  jwt字符串

        # 2. 校验token合法性
        # {'user_id': 'xx', 'email': 'xxx'}
        if not token:
            return Response({'message': '缺少token参数'}, status=400)
        try:
            s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY)
            dict_data = s.loads(token)  # 返回字典
        except:
            return Response({'message': 'token无效'}, status=400)

        # 3. 从token中获取： user_id, email
        user_id = dict_data.get('user_id')
        email = dict_data.get('email')

        # 4. 查询出要激活的用户对象
        try:
            user = User.objects.get(id=user_id, email=email)
        except:
            return Response({'message': '用户不存在'}, status=400)

        # 5. 修改用户对象的激活字段为true:  email_active=True
        user.email_active = True
        user.save()

        # 6. 响应数据： {'message': 'ok'}
        return Response({'message': 'ok'})


# 用户地址管理
class AddressViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):

    """ 用户地址管理
    1. 用户地址的增删改查处理
    2. 设置默认地址: put
    3. 设置地址标题: put
    """
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated]

    # POST /addresses/
    def create(self, request, *args, **kwargs):
        """会调用此方法新增一个用户地址"""

        count = request.user.addresses.count()
        if count >= 5:  # 每个用户最多不能超过5个地址
            return Response({'message': '地址个数已达到上限'}, status=400)

        return super().create(request, *args, **kwargs)

    # GET /addresses/
    def list(self, request, *args, **kwargs):
        """ 用户地址列表数据 """
        queryset = self.get_queryset()  # 当前登录用户的所有地址
        serializer = self.get_serializer(queryset, many=True)  # serializer.data 列表
        return Response({
            'user_id': request.user.id, # 用户id
            'default_address_id': request.user.default_address_id, # 用户默认地址id
            'limit': 5, # 最大地址个数
            'addresses': serializer.data # 原有的地址列表数据
        })

    # query_set = Address.objects.all()
    # query_set = Address.objects.filter(user=self.request.user, is_deleted=False)

    def get_queryset(self):
        # 获取当前登录用户的地址
        # return Address.objects.filter(user=self.request.user, is_deleted=False)
        return self.request.user.addresses.filter(is_deleted=False)


    # delete /addresses/<pk>/
    def destroy(self,requset,*args,**kwargs):
        """删除数据"""

        address = self.get_object()

        # 逻辑删除
        address.is_deleted = True
        address.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


    # put /addresses/pk/status/
    @action(methods = ['put'],detail = True) # 为true的时候回根据传进来的pk值自动生成对应查找的路由
    def status(self,request,pk=None):
        """设置默认地址"""
        address = self.get_object()
        request.user.default_address = address
        request.user.save()
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)


 





