# -------------------------------------------------------------------------------#
# Type                  : Python												#
# File Name             : main.py                                               #
# Purpose               : Declare all the API details                           #
# Created By			: Sathish.Shanmugam@ricoh-usa.com                       #
# Last Updated By       :                                                       #
# #
# Author   	   Date       	 Ver   		Description                             #
# ---------    -----------   ------   	----------------------------------------#
# Hexaware	   26-Jun-2023   210.00		CHG0082320 - Created                    #
# -------------------------------------------------------------------------------#
from datetime import datetime

from initialize import initialize_app

app, api = initialize_app()


@app.route("/status")
@app.route("/")
def server_up():
    return "Server is running! Current Server Time : {}".format(datetime.now())
