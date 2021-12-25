# sarans-restaurant-api

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

This is a sample project to get started with python-flask

## Features

- Get the details(name, price, ratings, number of reviews) of dishes served in sarans restaurant
- Register as a user
- Login as a user (Get jwt)
- Customer - Submit ratings for dishes
- Users can add new dishes to the restaurant

## Tech
This repo uses a number of open source projects to work properly:

- Python 3
- Flask
- SQLite

## Installation

This repo requires python 3 to run.

Install the dependencies and devDependencies and start the server.

```sh
git clone git@github.com:saran1992/sarans-restaurant-api.git
cd sarans-restaurant-api
pipenv install
pipenv shell
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

## Postman collection: 
https://www.getpostman.com/collections/4be7d05dd725304b6a28
