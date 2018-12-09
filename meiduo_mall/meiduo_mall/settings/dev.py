"""
Django settings for meiduo_mall project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hf354&@8#s)2$c38_oj0bd!5^gxa=9!*7v*(-d*ma*&70ufy++'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 指定可以通过哪些主机(ip,域名)访问后台服务器(django应用，django视图)
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'api.meiduo.site']


# 添加导包路径
# import sys
# sys.path.append('/home/python/code/gz07/meiduo/meiduo_mall/meiduo_mall/apps')
import sys
sys.path.insert(0,os.path.join(BASE_DIR,'apps')) # 添加导包路径，添加到列表的第一位


# 注册应用
INSTALLED_APPS = [
    'django.contrib.admin', # 后台管理模块
    'django.contrib.auth', # 用户认证模块
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    # 'meiduo_mall.apps.users.apps.UsersConfig',
    'users', # 添加了导包路径后，只需要写user
    'rest_framework', # 注册 django rest framwork 框架应用
    'oauth',  #
    'areas',   # 地区
    'goods',   # 商品
    'contents', # 广告内容应用
    'ckeditor',  # 富文本编辑器
    'ckeditor_uploader',  # 富文本编辑器上传图片模块
    'django_crontab', # 定时任务
    'django_filters', # 商品列表数据的过滤
    'haystack', # Haystack千草堆
]


# 中建键
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'meiduo_mall.urls'


# 模板
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'meiduo_mall.wsgi.application'


# 数据库配置
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '127.0.0.1',
            'PORT': 3306,
            'USER': 'root',
            'PASSWORD': 'mysql',
            'NAME': 'meiduo_mall'
        }

}


# 密码验证
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'zh-hans' # 设置中文

TIME_ZONE = 'Asia/Shanghai' # 设置时区

USE_I18N = True

USE_L10N = True

USE_TZ = True


# 静态资源访问路径
STATIC_URL = '/static/'

#　指定静态文件保存在哪个目录下
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_files')
]


# caches缓存，配置使用redis数据库
CACHES = {
    # 接口数据缓存: 省份城市数据
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 保存短信验证码
    "sms_codes":{
        "BACKEND":"django_redis.cache.RedisCache",
        "LOCATION":"redis://127.0.0.1:6379/2",
        "OPTIONS":{
            "CLIENT_CLASS":"django_redis.client.DefaultClient",
        }
    }
}

# 保存session数据到Redis中，主要是为了给Admin站点使用
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"


# 日志文件配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {                      # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {      # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {          # 日志处理方法
        'console': {      # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {          # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志文件的位置
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/meiduo.log"),
            'maxBytes': 300 * 1024 * 1024,   # 日志文件的最大容量
            'backupCount': 10,   # 300M * 10
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {      # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],      # 可以同时向终端与文件中输出日志
            'level': 'INFO',                      # 日志器接收的最低日志级别
        },
    }
}


# DRFkj相关配置 # 建议：项目开发完成再添加进来
REST_FRAMEWORK = {
     # 异常处理
     # 'EXCEPTION_HANDLER': 'meiduo_mall.meiduo_mall.utils.exceptions.custom_exception_handler',
        'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',# jwt认证
        'rest_framework.authentication.SessionAuthentication',# 管理后台使用
        'rest_framework.authentication.BasicAuthentication',
    ),
        'DEFAULT_PAGINATION_CLASS':'meiduo_mall.utils.paginations.MyPageNumberPagination', # 分页设置
}


# jwt认证配置
import datetime
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),# jwt有效时间

    # 修改登录成功接口返回的响应参数， 新增 user_id 和 username两个字段(设置之后就不再用源码里的默认返回,而是用这里的)
    'JWT_RESPONSE_PAYLOAD_HANDLER':'users.utils.jwt_response_payload_handler',
}


# 在项目配置文件中，指定使用自定义的用户模型类
# AUTH_USER_MODEL = 'users.modeles.User' # 错误的写法
AUTH_USER_MODEL = 'users.User'


# 允许跨域访问
CORS_ORIGIN_WHITELIST = (
    '127.0.0.1:8080',
    'localhost:8080',
    'www.meiduo.site:8080',
    'api.meiduo.site:8000'
)
# 指定在跨域访问中，后台是否支持cookie操作
CORS_ALLOW_CREDENTIALS = True


# 扩展登录接口: 手机号也可以登陆, 配置之后就不在使用源码里的默认的只能用户名登陆的方式了
AUTHENTICATION_BACKENDS = [
    'users.utils.UsernameMobileAuthBackend',
]

# 已经审核通过的应用参数， 配置到setting文件中
QQ_CLIENT_ID = '101474184'									# APP ID
QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'		# APP Key
QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html' # 登录成功的回调地址


# 发送邮件的配置项
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com' # 指定邮箱服务器
EMAIL_PORT = 25 # 默认端口
EMAIL_HOST_USER = 'yls_lm@163.com' #发送邮件的邮箱
EMAIL_HOST_PASSWORD = 'lm272049690' #在邮箱中设置的客户端授权密码
EMAIL_FROM = '美多官方邮箱<yls_lm@163.com>' #收件人看到的发件人


# drf扩展: 缓存配置, 获取省份和区县接口使用到
REST_FRAMEWORK_EXTENSIONS = {
    # 缓存时间(1小时)
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 60,
    # 缓存到哪里 (caches中配置的default)
    'DEFAULT_USE_CACHE': 'default',
}

# 指定使用自定义的文件存储类
DEFAULT_FILE_STORAGE = 'meiduo_mall.utils.fastdfs.storage.FdfsStorage'


# 富文本编辑器ckeditor配置
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',  # 工具条功能
        'height': 300,  # 编辑器高度
        # 'width': 300,  # 编辑器宽
    },
}
CKEDITOR_UPLOAD_PATH = ''  # 上传图片保存路径，使用了FastDFS，所以此处设为''


# FastDFS 客户端配置文件相对路径
FDFS_CLIENT_CONF = 'meiduo_mall/utils/fastdfs/client.conf'
# FastDFS服务器图片地址
FDFS_URL = 'http://image.meiduo.site:8888/'


# 生成的静态html文件保存的目录
GENERATED_STATIC_HTML_FILES_DIR = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'front_end_pc')


# 配置定时任务
CRONJOBS = [
    ('*/1 * * * *', 'contents.crons.generate_static_index_html','>> /home/python/PycharmProjects/meiduo/meiduo_mall/meiduo_mall/logs/crontab.log'),
# 参数1：定时时间设置，表示每隔3分钟执行一次
# 参数2：要定义执行的函数
# 说明：日志文本使用绝对路径，会自动创建
]


# 配置haystack全文检索框架
HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            # 此处为elasticsearch运行的服务器ip地址，端口号默认为9200
            'URL': 'http://192.168.234.140:9200/',
            # 指定elasticsearch建立的索引库的名称
            'INDEX_NAME': 'meiduo',
        },
    }
# 当添加、修改、删除数据时，自动更新索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'