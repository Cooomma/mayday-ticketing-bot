import unittest

import pytest
from sqlalchemy import MetaData, create_engine

from mayday.helpers.query_helper import QueryHelper
from mayday.objects.query import Query
from mayday.objects.ticket import Ticket
from mayday.db.tables.users import UsersModel

USER_ID = 123456789
USERNAME = 'pytest'


@pytest.mark.usefixtures()
class Test(unittest.TestCase):

    @pytest.fixture(autouse=True, scope='function')
    def before_all(self):
        engine = create_engine('sqlite://')
        metadata = MetaData(bind=engine)
        self.db = UsersModel(engine, metadata)

        # Create Table
        self.db.metadata.drop_all()
        self.db.metadata.create_all()
        self.db.role = 'writer'

        self.helper = QueryHelper(self.db)
    '''
    def test_save_and_load_quick_search_query(self):
        query = Query(user_id=USER_ID, username=USERNAME, category_id=1)
        query.update_field('dates', 503)
        query.update_field('dates', 504)
        query.update_field('prices', 1)

        assert self.helper.save_quick_search(query)

        quick_search_queries = self.mongo.load(
            db_name=self.helper.QUICK_SEARCH_QUERY_DB_NAME, collection_name=self.helper.QUICK_SEARCH_COLLECTION_NAME,
            query=dict(user_id=USER_ID, username=USERNAME))

        assert bool(quick_search_queries)
        quick_search_query = quick_search_queries[0]
        assert quick_search_query['dates'] == query.dates
        assert quick_search_query['prices'] == query.prices

        quick_search_query = self.helper.load_quick_search(USER_ID)
        assert quick_search_query.dates == query.dates
        assert quick_search_query.prices == query.prices


    def test_search_by_conditions(self):
        query = Query(user_id=USER_ID, username=USERNAME, category_id=1)
        query.update_field('dates', 503)
        query.update_field('dates', 504)
        query.update_field('prices', 1)

        ticket = Ticket(username=USERNAME, user_id=USER_ID)
        ticket.category = 1
        ticket.date = 503
        ticket.price_id = 1
        ticket.quantity = 2
        ticket.status = 1
        ticket.section = 'D3'
        assert ticket.validate()['status']
        self.mongo.save(
            db_name=self.helper.TICKET_DB_NAME, collection_name=self.helper.TICKET_COLLECTION_NAME,
            content=ticket.to_dict())

        # By one query
        result = self.helper.search_by_query(query)[0]
        assert result.category == ticket.category
        assert result.date == ticket.date
        assert result.price == ticket.price_id
        assert result.quantity == ticket.quantity
        assert result.status == ticket.status

        # By Section
        result = self.helper.search_by_section('D3')[0]
        assert result['section'] == ticket.section
        assert result['category'] == ticket.category
        assert result['date'] == ticket.date
        assert result['price'] == ticket.price_id
        assert result['quantity'] == ticket.quantity
        assert result['status'] == ticket.status

        # By Date
        result = self.helper.search_by_date(503)[0]
        assert result['section'] == ticket.section
        assert result['category'] == ticket.category
        assert result['date'] == ticket.date
        assert result['price'] == ticket.price_id
        assert result['quantity'] == ticket.quantity
        assert result['status'] == ticket.status
        '''

    def test_split_tickets_traits(self):
        ticket = Ticket()
        tickets = list()
        for i in range(0, 9):
            tickets.append(ticket)

        traits = QueryHelper.split_tickets_traits(tickets)
        assert len(traits) == 2
        assert len(traits[0]) == 5
        assert len(traits[1]) == 4
