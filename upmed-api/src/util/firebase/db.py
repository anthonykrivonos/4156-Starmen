from .setup import db


class Database:
    """
    Wrapper around Cloud Firestore to send and receive
    upmed-specific data.
    """

    def getPatients(self):
        return self.db.collection('patients')

    def getHCP(self):
        return self.db.collection('hcp')

    def getAppointments(self):
        return self.db.collection('appointments')

    def __init__(self):
        self.db = db
