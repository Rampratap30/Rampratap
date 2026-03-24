#!/bin/bash
ENV=prod
# copy environment ({ENV}.env) file into root folder
cp /track-my-order/api-container/config/environments/$ENV.env .env