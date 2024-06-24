
class Users:
    def __init__(self, id_for_full_cleanup=None, id_for_secondary_cleaning=None, temp_mess_id=0, temp_user_id=0, profile_id=0, phone_number="+380", temp=''):
        if id_for_full_cleanup is None:
            id_for_full_cleanup = []
        self.id_for_full_cleanup = id_for_full_cleanup

        if id_for_secondary_cleaning is None:
            id_for_secondary_cleaning = []
        self.id_for_secondary_cleaning = id_for_secondary_cleaning

        self.temp_mess_id = temp_mess_id
        self.temp_user_id = temp_user_id
        self.profile_id = profile_id
        self.phone_number = phone_number

        self.temp = temp

