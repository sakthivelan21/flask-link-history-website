# Link History Saving Website in Flask

## A minimal flask application to perform CRUD operations and authenticate the users

### website capabilities

❖ Session handling and authenticating the users.   
❖ Dark Mode and Light Mode is provided with css as per user browser theme.   
❖ Allowing user to save their youtube video links and update them for future.   
❖ can also play youtube videos in the website with iframe but the url should be in format like this https://youtu.be/WJbu2Ib3ozE   

## Steps to start the Application

```
git clone https://github.com/sakthivelan21/flask-link-history-website.git
```

**Creating and Activating Virtual Environment**

```
pip install virtualenv

# or

pip install venv
```

**Setup Virtual Environment**

```
python -m venv env
```

**Activate Virtual Environment**

```
# activate env (windows)

.\env\scripts\activate

# activate env (Linux/Mac)

source env/bin/activate
```

**Installing Dependencies**

```
pip install -r requirements.txt
```

**Creating database DB (SQLite)**

```
python3	# to enter the python shell for linux

python or py # to enter the python shell for windows

from app import db

db.create_all()

exit()
```

**Starting Application**

```
python3 app.py  -- linux

py app.py -- windows
```

**Deactivating Virtual Environment**

```
deactivate env
```

Visit http://localhost:5000 or http://0.0.0.0:5000 or http://yourIp:5000   


## Dependencies

click==8.0.3
Flask==2.0.2
Flask-SQLAlchemy==2.5.1
greenlet==1.1.2
itsdangerous==2.0.1
Jinja2==3.0.3
MarkupSafe==2.0.1
SQLAlchemy==1.4.29
Werkzeug==2.0.2


