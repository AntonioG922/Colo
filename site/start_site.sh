#!/bin/bash

# Set up Flask to host site
export FLASK_APP=colosite-test.py
export FLASK_DEBUG=1
export FLASK_ENV=development

# Start site
cd ~/Desktop/Colo/site
flask run