"""
Database models for Fonteyn Customer API
Uses SQLAlchemy ORM with MSSQL
"""
from extensions import db

class Account(db.Model):
    """User account model - maps to dbo.accounts table"""
    __tablename__ = 'accounts'
    
    UID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    UPass = db.Column(db.String(255), nullable=False)
    UEmail = db.Column(db.String(100), nullable=False, unique=True)
    URole = db.Column(db.String(20), default='user')
    UDoB = db.Column(db.Date)
    
    def to_dict(self):
        """Convert model to dictionary (for JSON responses)"""
        return {
            'uid': self.UID,
            'firstName': self.FirstName,
            'lastName': self.LastName,
            'email': self.UEmail,
            'role': self.URole,
            'dateOfBirth': self.UDoB.isoformat() if self.UDoB else None
        }
    
    def __repr__(self):
        return f'<Account {self.UEmail}>'


class Ticket(db.Model):
    __tablename__ = 'tickets'

    TID = db.Column(db.Integer, primary_key=True)
    UID = db.Column(db.Integer, db.ForeignKey('accounts.UID'), nullable=False)
    TAmount = db.Column(db.Integer)
    TStart = db.Column(db.Date)
    TEnd = db.Column(db.Date)
    Timestamp = db.Column(db.DateTime, nullable=False, server_default=db.text('GETDATE()'), default=db.func.now())
    TType = db.Column(db.String(50))
    TPark = db.Column(db.String(100))
    RoomID = db.Column(db.Integer)
    PaymentAmount = db.Column(db.Numeric(10, 2))

    def to_dict(self):
        return {
            'id': self.TID,
            'uid': self.UID,
            'amount': self.TAmount,
            'startDate': self.TStart.isoformat() if self.TStart else None,
            'endDate': self.TEnd.isoformat() if self.TEnd else None,
            'timestamp': self.Timestamp.isoformat() if self.Timestamp else None,
            'type': self.TType,
            'park': self.TPark,
            'roomId': self.RoomID,
            'paymentAmount': float(self.PaymentAmount) if self.PaymentAmount is not None else None,
        }
    
    def __repr__(self):
        return f'<Ticket {self.TID}>'

class LoginAttempt(db.Model):
    """Audit log for login attempts"""
    __tablename__ = 'login_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    ip_address = db.Column(db.String(50))
    success = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, default=db.func.now())
