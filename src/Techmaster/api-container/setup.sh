#!/bin/bash
ENV=prod

# copy environment ({ENV}.env) file into root folder
cp /tech-master/api-container/config/environments/$ENV.env .env
