from .extensions import db


class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(15), nullable=False, unique=True)
    os_type = db.Column(db.String(20))

    def to_dict(self):
        return {
            "id": self.id,
            "hostname": self.hostname,
            "ip_address": self.ip_address,
            "os_type": self.os_type,
        }
