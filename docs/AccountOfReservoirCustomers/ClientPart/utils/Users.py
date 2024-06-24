
class Users:
    def __init__(self, phone_number="+380", text="", time="", confirmation_code=0, temp_mess_id=0,
                 mess_id_for_clean=None):
        if mess_id_for_clean is None:
            mess_id_for_clean = []
        self.phone_number = phone_number
        self.text = text
        self.confirmation_code = confirmation_code
        self.temp_mess_id = temp_mess_id
        self.time = time
        self.mess_id_for_clean = mess_id_for_clean

