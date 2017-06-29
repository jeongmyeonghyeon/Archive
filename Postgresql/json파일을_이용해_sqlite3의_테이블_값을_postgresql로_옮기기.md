### `.json`을 이용해 sqlite3 의 테이블 값을 postgresql로 옮기기

```
1. 기존 데이터베이스 값을 포함한 .json파일 생성
	1-1. table을 생략하면 전체 데이터베이스 값을 포함한 .json파일이 생성됨
	1-2. '>'(꺽쇠 괄호)는 앞의 명령어를 통해 생성된 내용을 뒤에 지정한 파일에 담겠다는 의미
	
>>> ./manage.py dumpdata [table, table, ...] > filename.json

2. settings.py의 DATABASES 설정 변경

# 기존 설정 (sqlite3)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

# 변경한 설정 (postgresql)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'instagram',
        'USER': 'instagram',
        'PASSWORD': 'dlgksdud',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

3. 마이그레이트
>>> ./manage.py migrate

4. .json 파일을 로드해 postgresql에 담기
>>> ./manage.py loaddata filename.dump
```
