from .setup import db

class Database:
    """
    Wrapper around Cloud Firestore to send and receive upmed-specific data.
    TODO: Add all getters and setters.
    """

    def __init__(self):
        self.db = db

