from app import db


class Details(db.Model):
    __tablename__ = "details"  # Define nama table

    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    document    = db.Column(db.String, nullable=False)
    label       = db.Column(db.Integer, nullable=False)
    score       = db.Column(db.Float, nullable=False)
    judul       = db.Column(db.String, nullable=False)
    dosen_id    = db.Column(db.String, nullable=False)
    dosen       = db.Column(db.String, nullable=False)
    dosen_judul_id       = db.Column(db.String, nullable=False)
    query_id    = db.Column(db.Integer, db.ForeignKey("queries.id"))

    def __init__(self, data):
        document, label, score, judul, dosen, dosen_id, dosen_judul_id = data
        self.document       = document
        self.label          = label
        self.score          = score
        self.judul          = judul
        self.dosen          = dosen
        self.dosen_id       = dosen_id
        self.dosen_judul_id = dosen_judul_id
        

    def __repr__(self):
        return "<judul: {}>".format(self.judul)

    @staticmethod
    def getAll(queryId):
        details = Details.query.filter_by(query_id=queryId).order_by(Details.score.desc()).limit(5).all()
        result = list()
        for data in details:
            obj = {
                "id": data.id,
                "document": data.document,
                "label": data.label,
                "score": data.score,
                "dosen": data.dosen,
                "dosen_id": data.dosen_id,
                "dosen_judul_id": data.dosen_judul_id,
                "judul": data.judul
            }
            result.append(obj)
        return result
