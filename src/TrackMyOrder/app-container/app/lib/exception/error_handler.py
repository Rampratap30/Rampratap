from flask import render_template, request


class ErrorHandler:
    def __init__(self, flask_app, log) -> None:
        @flask_app.errorhandler(Exception)
        def app_exception_handling(err):
            if str(err):
                log.write_log(request.path)
                log.write_log(str(err))
            return render_template(
                "error_page.html",
                errors=[type(err).__name__, str(err)],
                error_reason="APP - Kindly check log for furhter analysis",
            )
