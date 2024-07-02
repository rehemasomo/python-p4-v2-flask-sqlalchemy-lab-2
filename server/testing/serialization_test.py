from app import app, db
from server.models import Customer, Item, Review


class TestSerialization:
    '''models in models.py'''


    def test_customer_is_serializable(self):
        '''customer is serializable'''
        with app.app_context():
            c = Customer(name='Phil')
            db.session.add(c)
            db.session.commit()
            r = Review(comment='great!', customer=c)
            db.session.add(r)
            db.session.commit()
            customer_dict = c.to_dict()

            assert customer_dict['id']
            assert customer_dict['name'] == 'Phil'
            assert 'reviews' in customer_dict
            assert 'customer' not in customer_dict['reviews']

    def test_item_is_serializable(self):
        '''item is serializable'''
        with app.app_context():
            i = Item(name='Insulated Mug', price=9.99)
            db.session.add(i)
            db.session.commit()
            r = Review(comment='great!', item=i)
            db.session.add(r)
            db.session.commit()

            item_dict = i.to_dict()
            assert item_dict['id']
            assert item_dict['name'] == 'Insulated Mug'
            assert item_dict['price'] == 9.99
            assert 'reviews' in item_dict
            assert 'item' not in item_dict['reviews']

    def test_review_is_serializable(self):
        '''review is serializable'''
        with app.app_context():
            c = Customer()
            i = Item(name='Test Item', price=10.0)  
            db.session.add_all([c, i])
            db.session.commit()

            r = Review(comment='great!', customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            review_dict = r.to_dict()

            assert review_dict['id']
            assert review_dict['item']