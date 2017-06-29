# Deploy EC2

## requirements

**Python**  
3.6.1

**pip**

```
pip install -r requirements.txt
```

## Create secret config file

### Proeject structure

```
project_folder/
	.conf_secret/
		settings_common.json
		settings_degub.json
		settings_deploy.json
	.django_app/
	...
	...
```

### settings_common.json example

```
{
	"django": {
		"secret_key": "Django project secret key"
	}
}
```

### settings_debug.json example

```
{
	"allowed_hosts": [
		"*"
	]
}
```

### settings_deploy.json example

```
{
	"allowed_hosts": [
		"*"
	]
}
```

### runserver

```
# local developement
python3 manage.py runserver --settings=config.settings.debug
```