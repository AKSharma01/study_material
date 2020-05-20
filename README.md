# Online Study Material

[![N|Study Material](https://blog-digital.aakash.ac.in/wp-content/uploads/2018/10/online-education.png)](https://github.com/AKSharma01/study_material)

[![Nodejs version](https://img.shields.io/badge/python-3.7.6-blue.svg)](https://docs.python.org/3/) [![pip](https://img.shields.io/badge/pip-20.1-skyblue.svg)](https://pip.pypa.io/en/stable/) [![Flask](https://img.shields.io/badge/Flask-1.1.1-%23ff3300.svg)](https://flask.palletsprojects.com/en/1.1.x/) [![Postgres](https://img.shields.io/badge/postgres-12.3-green.svg)](https://www.postgresql.org/docs/12/index.html)  [![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.3.13-%23990099.svg)](https://docs.sqlalchemy.org/en/13/index.html)  [![psycopg2-binary](https://img.shields.io/badge/psycopg2--binary-4.17.1-green.svg)](https://pypi.org/project/psycopg2-binary/) 


__Table of content__
    
- [Install](#install)
- [Configure and Run](#configure-and-run)
- [Authors](#authors)


# Install
> Pre-requirement
**python3**, **pip**, **virtualenv**, **postgres**

#### Install The virtualenv
```sh
 >>> pip install virtualenv
 >>> virtualenv --version
 v16.7.9
```

#### Install latest version of [Postgres](http://www.postgresqltutorial.com/)
```sh
 >>> brew install postgresql
 >>> postgres --version
 postgres (PostgreSQL) 12.3
```

## Configure and Run
```sh
 >>> sudo git clone https://github.com/AKSharma01/study_material.git
 >>> cd study_material
 >>> virtualenv venv -p python3 (create local enviroment)
 >>> source venv/bin/activate
 >>> pip install -r requirement.txt (to install project dependencies)
 >>> touch .env (save the project env in .env file)
 >>> python manager.py db init
 >>> python manager.py db migrate
 >>> python manager.py db upgrade
 >>> python server.py
* Serving Flask app "server" (lazy loading)
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 765-751-285
```

## Postman
```
 >>> set postman env 
 domain : http://localhost:5000
 >>> import link 
 https://www.getpostman.com/collections/b5f49e8ee6fdc7fa80f2
```

## APIs
```
 >>> solution_api =>  method["post"] => url[http://localhost:5000/search/v1.0/solution]
 (to get list of videos and similar questions)
 >>> visited videos => method["post"] => url[http://localhost:5000/search/v1.0/solution/video]
 (api that to notify that video has been watched)
```

# Authors
- Akash Kumar Sharma ([github.com/AKSharma01](https://github.com/AKSharma01))
