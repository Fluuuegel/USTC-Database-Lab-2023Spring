# memo

## Virtual environment

> Tip: if using windows, change 'python' with 'py'

Create: 

`python -m venv vename`

Activate:

 `source vename/bin/activate`

Exit: 

`Ctrl + D`

## Django 

Update:

`python manage.py makemigrations members` 

`python manage.py migrate`

Run: 

`python manage.py runserver`

## Django Admin

Create: 

`py manage.py createsuperuser`

Login:

```bash
Username: fluegelcat

Password: jiuguaiwanfang
```

## Data Operation


### Insert Data With .CSV

`pip install django_extension`

`python manage.py runscript insert`

### Display Data

`python manage.py shell`

```python
>>> from api.models import Client
>>> Client.objects.all()
>>> Client.objects.all().values()
```

### Vue

Init: 

`npm init vue@latest`

Run:

`cd vue-project` `npm install` ` npm run dev`

### Plugins

`npm install element-plus --save`

`npm install vue-router`

