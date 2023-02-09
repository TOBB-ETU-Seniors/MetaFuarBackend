from datetime import datetime
class User:
    def __init__(self, apiobj):
        self.creation_time = datetime.now()
        self.login_type = apiobj["login_type"]
        # this here will be assigned by google,facebook etc.
        self.login_id = apiobj["login_id"]
        self.user_name =apiobj[ "user_name"]
        self.email_address = apiobj["email_address"]
    
    
        
    

