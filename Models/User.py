from datetime import datetime
class User:
    def __init__(self, apiobj, login_code):
        self.creation_time = datetime.now()
        self.login_type = apiobj["login_type"]
        # this here will be assigned by google,facebook etc.
        self.login_code = login_code
        self.user_name =apiobj[ "user_name"]
        self.email_address = apiobj["email"]
    
    
        
    

