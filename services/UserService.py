from UserGlobalVariables import *
from services.EncryptionService import EncryptionService


class UserService():

    def register_user(self, user, db):
        from app import UserDBModel as User
        # Check if the user already exists
        existing_user = db.session.query(User).filter_by(name=user.name).first()
        if existing_user:
            return USER_REGISTERED

        # make a variable of type encryptionService
        encryptionService = EncryptionService()
        # Hash the password before saving
        user.password = encryptionService.encryptData(user.password)

        try:
            db.session.add(user)
            db.session.commit()
            # debug
            db.session.refresh(user)
            print(user)
            return REGISTER_SUCCESS
        except:
            db.session.rollback()
            return REGISTER_FAIL

    def login_user(self, user, db):
        from app import UserDBModel as User
        # Fetch the user from the database
        registered_user = db.session.query(User).filter_by(name=user.name).first()

        if not registered_user:
            return USER_NOT_FOUND

        # Compare the stored password hash with the entered password
        encryptionService = EncryptionService()
        if encryptionService.isEqual(user.password, registered_user.password):
            return LOGIN_SUCCES
        else:
            return LOGIN_FAIL
