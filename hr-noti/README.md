My simple rest-api & celery cron/background task

0. Check your OS version ?
If Windows, please install **"Microsoft Visual C++ Build Tools**
```
https://go.microsoft.com/fwlink/?LinkId=691126
```
or
```
https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

after install this, you can install cffi, bcrypt, jwt,...libs

(free space from 4GB to 9GB :(( )

1. Install requirement


```
pip install -r requirements.txt
```

Install redis & start it before start app

2. Start API application

```
python manage.py runserver
```

3. Connect to web-route:

http://127.0.0.1:5001/myApi/hello


4. Connect to healtCheck API

http://127.0.0.1:5001/myApi/healthCheck/


5. Connect to swagger

http://127.0.0.1:5001/myApi/

6. Start background-task

**\*nix:**

celery -A app.task worker -E --loglevel=info -f \logs\celery.log

**windows:**

install eventlet lib for debug in windows
```
pip install eventlet
```

celery -A app.task worker -E --loglevel=info -P eventlet -f \logs\celery.log

