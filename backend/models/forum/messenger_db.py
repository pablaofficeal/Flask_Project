from models.imp import db

class MessengerDB(db.Model):
    __tablename__ = 'messenger'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<MessengerDB id={self.id} user_id={self.user_id}>"