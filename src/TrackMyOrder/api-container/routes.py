# ------------------------------------------------------------------------------#
# Type                  : Python												#
# File Name             : main.py                                               #
# Purpose               : Declare all the API details                           #
# Created By			: Rampratap.kushwah@ricoh-usa.com                       #
# Last Updated By       :                                                       #
#                                                                               #
# Author   	   Date       	 Ver   		Description                             #
# ---------    -----------   ------   	----------------------------------------#
# Hexaware	   20-Jan-2025   210.00		CHG0093323 - Created                    #
# ------------------------------------------------------------------------------#
from datetime import datetime
from initialize import initialize_app

app = initialize_app()

@app.route("/status")
@app.route("/")
def server_up():
    return "Server is running! Current Server Time : {}".format(datetime.now())
