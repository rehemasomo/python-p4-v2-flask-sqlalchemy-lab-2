# server/models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


customer_items = Table('customer_items', metadata,
                       db.Column('customer_id', db.Integer, db.ForeignKey('customers.id')),
                       db.Column('item_id', db.Integer, db.ForeignKey('items.id'))
                       )

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    items = relationship('Item', secondary=customer_items, backref='customers')

    reviews = relationship('Review', back_populates='customer')

    serialize_only = ('id', 'name', 'items')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'items': [item.to_dict() for item in self.items],
            'reviews': [{'id': review.id, 'comment': review.comment} for review in self.reviews]
        }

class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    reviews = relationship('Review', back_populates='item')

    serialize_only = ('id', 'name', 'price')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': float(self.price), 
            'reviews': [{'id': review.id, 'comment': review.comment} for review in self.reviews]
        }


class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    customer = relationship('Customer', back_populates='reviews')
    item = relationship('Item', back_populates='reviews')

    serialize_only = ('id', 'comment', 'customer_id', 'item_id', 'customer')  

    def to_dict(self):
        return {
            'id': self.id,
            'comment': self.comment,
            'customer_id': self.customer_id,
            'item_id': self.item_id,
            'customer': self.customer.to_dict(),
            'item': self.item.to_dict() 
        }
