from src import db

class Anime(db.Model):
    __tablename__ = 'anime'

    anime_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)

    def __init__(self, anime_id, title):
        self.anime_id = anime_id
        self.title = title

    def __repr__(self):
        return str(self.title)
