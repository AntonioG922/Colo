#!/bin/bash

# Set up Flask to host site
export FLASK_APP=machine-test.py
export FLASK_DEBUG=1
export FLASK_ENV=development

# Start site
cd ~/Desktop/Colo/site
flask run