import bcrypt

class EncryptionService:
    def encryptData(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def isEqual(self, inComingPassword, database_password):
        return bcrypt.checkpw(inComingPassword.encode('utf-8'), database_password.encode('utf-8'))
