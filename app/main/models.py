from datetime import datetime, timezone
from typing import Optional 

from app import db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import Table, Column, Integer, ForeignKey

class User(db.Model, UserMixin):
    __tablename__='user'
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    username: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50), unique = True)
    name: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(132))
    password_hash: sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.String(256))
    user_type: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(25))
    
    __mapper_args__ = {
        'polymorphic_identity': 'User',
        'polymorphic_on': user_type
    }
    
    # relationships
    posts : sqlo.WriteOnlyMapped['Post'] = sqlo.relationship(back_populates='writer', passive_deletes=True, cascade='all, delete-orphan')
    
    def get_posts(self):
        query = self.posts.select()
        return db.session.scalars(query).all()
    
    def __repr__(self):
        return '<User - {} - {} - {} is a {}>'.format(self.id, self.username, self.name, self.user_type)
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(str(self.password_hash), password)
        
    def get_name(self):
        return self.name
        
    def get_username(self):
        return self.username
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
class Admin(User):
    __tablename__='admin'
    id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(User.id), primary_key=True)
    
    __mapper_args__= {
        'polymorphic_identity': 'Admin'
    }
    
class Post(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key = True)
    name : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(132))
    date : sqlo.Mapped[datetime]  = sqlo.mapped_column(sqla.DateTime, default=datetime.utcnow())
    body : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(2048))
    writer_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(User.id, ondelete='CASCADE'), index = True)
    
    writer : sqlo.Mapped[User] = sqlo.relationship(back_populates='posts', passive_deletes = True) 
    
    def get_name(self):
        return self.name
        
    def get_writer(self):
        writer = db.session.scalars(sqla.select(User).where(User.id == self.writer_id)).first()
        return writer
        
    
    
        
    

    