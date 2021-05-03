# CK Mart

Online platform that sells products that are inspired by Chinese and Korean dramas for CK drama lovers. The application is still under development and will be released in Phases.Phase 1 has been released on Heroku and a staging platform.

## Phase 1
### Account Component 
* registration
* login
* profile edit

### Store Component 
* view products
* add product to cart
* checkout
* pay using paypay - sandbox accoun at the moment
* view orders


## Phase 2
### Account Component
* password reset
* crud shipping addresses

### Store Component 
* delete orders
* intergrate payU - sandbox
* link payment to user account

## [View Site here](https://ckmart.herokuapp.com)


## Setup
* clone the repo to your local
* copy .env.example to /ckmart/.env
* activate venv
* make and run migrations by the running these commands

```python
python manage.py makemigrations
python manage.py migrate
```

* run the server using the below command
 ```python
 python manage.py runserver
 ```
* #### congratulations #### Youe app is running at localhost:8000/store
