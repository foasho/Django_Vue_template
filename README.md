#Django＋Vue.jsでWEBアプリケーションを作るメモ

##システム構成
・Django
・Vue.js
・MySQL

```commandline
django-admin startproject config .
python manage.py startapp accounts
```


##最初の設定

###APPSに追加
```python:config/setting.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    "accounts.apps.AccountsConfig",
]
```

###言語とタイムゾーンを日本仕様にする

```python:config/setting.py
LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'
```

###DjangoのデータベースにMySQLを設定する

```commandline
pip install pymysql
pip install python-dotenv
```

manage.pyの編集(MySQLの追加)
```python:manage.py
import pymysql
pymysql.install_as_MySQLdb()
```

configの中に.envファイルの作成
```editorconfig:config/.env
DB_NAME = XXXXX
DB_PWD = XXXXX
DB_USER = XXXXX
DB_HOST = XXXXX
```

setting.pyの編集
```python:config/setting.py
from os.path import join, dirname
from dotenv import load_dotenv
```

```python:config/setting.py
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
DB_NAME = os.environ.get("DB_NAME")
DB_PWD = os.environ.get("DB_PWD")
DB_USER = os.environ.get("DB_USER")
DB_HOST = os.environ.get("DB_HOST")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,#データベース名
        'USER': DB_USER,#ユーザー名
        'PASSWORD': DB_PWD,#パスワード
        'HOST': DB_HOST,#ローカルホスト等
        'PORT': '3306',#接続ポート
    }
}
```

###ロガーの設定をする
```python:config/settings.py
#ロギング設定
LOGGING = {
    "version": 1,
    "disavle_existing_loggers": False,
    
    #ロガーの設定
    "logger":{
        "django": {
            "handlers": ["console"],
            "lebel": "INFO",
        }
    },
    #accountsのアプリ利用するロガー
    "diary": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
    #ハンドラの設定
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "dev"
        },
    },
    #フォーマッターの設定
    "formatters": {
        "dev": {
            "format": "\t".join([
                "%(asctime)s",
                "[%(levelname)s]",
                "%(pathname)s(Line:%(lineno)d)",
                "%(message)s"
            ])
        },
    },
}
```

###ルーティングの設定し、index.htmlへアクセスさせる
```python:config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("accounts.urls"))
]
```

新規ファイル作成：accounts/urls.py
```python:accounts/urls.py
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index")
]
```

新しいディレクトリ『templates』を作成
accounts/templatesに作成

新規ファイルindex.htmlを作成
```html:accouts/templates/index.html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>トップページ</title>
</head>
<body>
    <h1>Hello World</h1>
</body>
</html>
```

確認
```commandline
python manage.py runserver
```

##Bootstrapテンプレートを反映させる
###staticフォルダの追加

Bootstrapをダウンロード
(https://startbootstrap.com/themes/one-page-wonder)

プロジェクト直下にstaticフォルダを新規作成

ダウンロードしたBootStrapをstaticフォルダに入れる
```commandline
├── accounts
├── config
├── static
|       ├── css
|       ├── img
|       └── vender
├── manage.py
```

###静的フォルダが配置されている場所を設定する
```python:config/settings.py
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
```

##各ページで共通するbase.htmlを作る
```html:accounts/templates/base.html
{% load static %}

<html lang="ja">

  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>{% block title %}{% endblock %}</title>

    <!-- Bootstrap core CSS -->
    <link href="{% static 'vendor/bootstrap/css/bootstrap.min.css' %}" rel="stylesheet">

    <!-- Custom fonts for this template -->
    <link href="https://fonts.googleapis.com/css?family=Catamaran:100,200,300,400,500,600,700,800,900" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css?family=Lato:100,100i,300,300i,400,400i,700,700i,900,900i" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="{% static 'css/one-page-wonder.min.css' %}" rel="stylesheet">

    <!-- My style -->
    <link rel="stylesheet" type="text/css" href="{% static 'css/mystyle.css' %}">

    <script src="https://cdn.jsdelivr.net/npm/vue"></script>
    <script src="https://unpkg.com/vue"></script>

    {% block head %}{% endblock %}
  </head>

  <body>
	<div id="wrapper">
        <!-- ナビヘッダー -->
        <nav class="navbar navbar-expand-lg navbar-dark navbar-custom fixed-top">
          <div class="container">
            <a class="navbar-brand" href="{% url 'accounts:index' %}">TITLE</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarResponsive">
              <ul class="navbar-nav mr-auto">
                <li class="nav-item {% block active_inquiry %}{% endblock %}">
                  <a class="nav-link" href="#">INQUIRY</a>
                </li>
              </ul>
              <ul class="navbar-nav ml-auto">
                <li class="nav-item">
                  <a class="nav-link" href="#">Sign Up</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="#">Log In</a>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        {% block contents%}{% endblock %}

        <!-- Footer -->
        <footer class="py-5 bg-black">
          <div class="container">
            <p class="m-0 text-center text-white small">&copy;Foa TemplatesCode 2020</p>
          </div>
          <!-- /.container -->
        </footer>

        <!-- Vue.js JavaScript -->
        {% block scripts%}{% endblock %}

        <!-- Bootstrap core JavaScript -->
        <script src="{% static 'vendor/jquery/jquery.min.js' %}"></script>
        <script src="{% static 'vendor/bootstrap/js/bootstrap.bundle.min.js' %}"></script>
  	</div>
  </body>

</html>
```

##合わせてindex.htmlもそれっぽく編集する
```html:accounts/templates/index.html
{% extends 'base.html' %}
{% load static %}

{% block title %}TITLE --Subtitle{% endblock %}

{% block contents %}
<div id="indexapp">
  <header class="masthead text-center text-white">
    <div class="masthead-content">
      <div class="container">
        <h1 class="masthead-heading mb-0">[[ title ]]</h1>
        <h2 class="masthead-subheading mb-0">SubTitle</h2>
        <a href="#" class="btn btn-primary btn-xl rounded-pill mt-5">LOG IN</a>
      </div>
    </div>
    <div class="bg-circle-1 bg-circle"></div>
    <div class="bg-circle-2 bg-circle"></div>
    <div class="bg-circle-3 bg-circle"></div>
    <div class="bg-circle-4 bg-circle"></div>
  </header>
  <div class="py-5 text-white" style="background-image: linear-gradient(to bottom, rgba(0, 0, 0, .75), rgba(0, 0, 0, .75)), url(https://static.pingendo.com/cover-bubble-dark.svg);  background-position: center center, center center;  background-size: cover, cover;  background-repeat: repeat, repeat;">
    <div class="container">
      <div class="row">
        <div class="p-3 col-md-8 col-lg-6 ml-auto text-right text-white">
          <p class="lead">"I throw myself down among the tall grass by the trickling stream; and, as I lie close to the earth, a thousand unknown plants are noticed by me: when I hear the buzz of the little world among the stalks."</p>
          <p><b>Johann Goethe</b><br><small>CEO and founder</small></p>
        </div>
      </div>
    </div>
  </div>
  <div class="py-5" style="background-image: linear-gradient(to left bottom, rgba(189, 195, 199, .75), rgba(44, 62, 80, .75)); background-size: 100%;">
    <div class="container">
      <div class="row">
        <div class="text-center mx-auto col-md-12">
          <h1 class="text-white mb-4">Testimonials</h1>
        </div>
      </div>
      <div class="row">
        <div class="col-lg-4 col-md-6 p-3">
          <div class="card">
            <div class="card-body p-4">
              <div class="row">
                <div class="col-md-4 col-3"> <img class="img-fluid d-block rounded-circle" src="https://static.pingendo.com/img-placeholder-2.svg"> </div>
                <div class="d-flex  col-md-8 flex-column justify-content-center align-items-start col-9">
                  <p class="mb-0 lead"> <b>J. W. Goethe</b> </p>
                  <p class="mb-0">Co-founder</p>
                </div>
              </div>
              <p class="mt-3 mb-0">I throw myself down among the tall grass by the trickling stream; and, as I lie close to the earth, a thousand unknown plants are noticed by me: when I hear the buzz of the little world.</p>
            </div>
          </div>
        </div>
        <div class="col-lg-4 col-md-6 p-3">
          <div class="card">
            <div class="card-body p-4">
              <div class="row">
                <div class="col-md-4 col-3"> <img class="img-fluid d-block rounded-circle" src="https://static.pingendo.com/img-placeholder-1.svg"> </div>
                <div class="d-flex  col-md-8 flex-column justify-content-center align-items-start col-9">
                  <p class="mb-0 lead"> <b>G. W. John</b> </p>
                  <p class="mb-0">CEO &amp; founder</p>
                </div>
              </div>
              <p class="mt-3 mb-0" >I lie close to the earth, a thousand unknown plants are noticed by me: when I hear the buzz of the little world among the stalks, and grow familiar with the countless indescribable forms of the insects and flies.</p>
            </div>
          </div>
        </div>
        <div class="col-lg-4 p-3">
          <div class="card">
            <div class="card-body p-4">
              <div class="row">
                <div class="col-md-4 col-3"> <img class="img-fluid d-block rounded-circle" src="https://static.pingendo.com/img-placeholder-3.svg"> </div>
                <div class="d-flex  col-md-8 flex-column justify-content-center align-items-start col-9">
                  <p class="mb-0 lead"> <b>J. G. Wolf</b> </p>
                  <p class="mb-0">CFO</p>
                </div>
              </div>
              <p class="mt-3 mb-0">Oh, would I could describe these conceptions, could impress upon paper all that is living so full and warm within me, that it might be the mirror of my soul, as my soul is the mirror of the infinite God!</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="py-5 text-center">
    <div class="container">
      <div class="row">
        <div class="mx-auto col-md-8">
          <h1>{{ this.title }}</h1>
          <p class="mb-4"> Oh, would I could describe these conceptions, could impress upon paper all that is living so full and warm within me, that it might be the mirror of my soul, as my soul is the mirror of the infinite God! O my friend -- but it is too much for my strength -- I sink under the weight of the splendour of these visions!</p>
          <div class="row text-muted">
            <div class="col-md-2 col-4 p-2"> <i class="d-block fa fa-angellist fa-3x"></i> </div>
            <div class="col-md-2 col-4 p-2"> <i class="d-block fa fa-cc-visa fa-3x"></i> </div>
            <div class="col-md-2 col-4 p-2"> <i class="d-block fa fa-empire fa-3x"></i> </div>
            <div class="col-md-2 col-4 p-2"> <i class="d-block fa fa-paypal fa-3x"></i> </div>
            <div class="col-md-2 col-4 p-2"> <i class="d-block fa fa-rebel fa-3x"></i> </div>
            <div class="col-md-2 col-4 p-2"> <i class="d-block fa fa-first-order fa-3x"></i> </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
{% endblock %}

{% block scripts %}
<script src="{% static 'js/index_vue.js' %}"></script>
{% endblock %}
```

##Vue.jsを組み込む
###ファイルを作成し、Titleを動的に変化させる
static内に新規フォルダ『js』に作成
js内にindex.jsを作成
Djangoのシステムと混同させないため、
delimiters: ['[[', ']]']が大事
```javascript:static/js/index.js
var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#indexapp',
    data: {
        title: "TestTitle"
    },
})
```

##ログイン画面を作る

ログインフォームを作成
accountsにforms.pyを新規作成
```python

```

url先を作成
```python:accounts/urls.py
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path('login/', views.Login.as_view(), name='login'),
]
```

そのあとは、views.pyを変更
```python:accounts/views.py
from django.contrib.auth import get_user_model

class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'register/login.html'

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url('register:console', pk=self.request.user.pk)
```

