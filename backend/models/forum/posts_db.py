from models.imp import db
from sqlalchemy.orm import relationship

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    # Связь с пользователем - убрал backref чтобы избежать конфликтов
    user = relationship('User')

    def __repr__(self):
        return f"<Post id={self.id} user_id={self.user_id} title={self.title}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
            'timestamp': self.timestamp
        }