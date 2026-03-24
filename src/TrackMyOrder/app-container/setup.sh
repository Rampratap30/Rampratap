#!/bin/bash
ENV=prod

# copy environment ({ENV}.env) file into root folder
cp /track-my-order/app-container/config/environments/$ENV.env .env