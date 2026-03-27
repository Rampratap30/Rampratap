#!/bin/bash
ENV=prod

# copy environment ({ENV}.env) file into root folder
cp /tech-master/app-container/config/environments/$ENV.env .env
