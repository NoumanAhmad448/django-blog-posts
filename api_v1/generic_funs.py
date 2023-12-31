class ApiResponse:
    def __init__(self):
        self.is_success = ""
        self.data = ""
        self.message = ""
        self.IS_SUCCESS = "is_success"
        self.DATA = "data"
        self.MESSAGE = "message"
        self.DEBUG = "debug"
        self.debug = {}

    def send_response(self):
        return {
            self.IS_SUCCESS: self.is_success,
            self.DATA: self.data,
            self.MESSAGE: self.message,
            self.DEBUG: self.debug
        }

def is_user_not_authenticated(req):
    return not req.user.is_authenticated