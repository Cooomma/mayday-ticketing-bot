import unittest

import pytest
from sqlalchemy import create_engine, MetaData
from mayday.db.tables.tickets import TicketsModel
from mayday.helpers.ticket_helper import TicketHelper
from mayday.objects.ticket import Ticket


USER_ID = 123456789
USERNAME = 'pytest'


@pytest.mark.usefixtures()
class Test(unittest.TestCase):

    @pytest.fixture(autouse=True, scope='function')
    def before_all(self):
        engine = create_engine('sqlite://')
        metadata = MetaData(bind=engine)
        self.db = TicketsModel(engine, metadata)

        # Create Table
        self.db.metadata.drop_all()
        self.db.metadata.create_all()
        self.db.role = 'writer'

        self.helper = TicketHelper(self.db)

    def test_save_formal_ticket(self):
        ticket = Ticket(user_id=USER_ID, username=USERNAME)
        assert self.helper.save_ticket(ticket)

        tickets_in_db = self.db.get_tickets_by_user_id(USER_ID)
        assert tickets_in_db

        ticket_in_db = tickets_in_db[0]

        assert ticket.category == ticket_in_db.category
        assert ticket.date == ticket_in_db.date
        assert ticket.price_id == ticket_in_db.price_id
        assert ticket.quantity == ticket_in_db.quantity
        assert ticket.section == ticket_in_db.section
        assert ticket.row == ticket_in_db.row
        assert ticket.seat == ticket_in_db.seat
        assert ticket.status == ticket_in_db.status
        assert ticket.remarks == ticket_in_db.remarks
        assert ticket.wish_dates == ticket_in_db.wish_dates
        assert ticket.wish_price_ids == ticket_in_db.wish_price_ids
        assert ticket.wish_quantities == ticket_in_db.wish_quantities
        assert ticket.user_id == ticket_in_db.user_id
        assert ticket.username
        assert ticket.username == ticket_in_db.username
        assert ticket_in_db.id  # can not know the ticket if before insert
        assert ticket_in_db.created_at  # can not know the created ts before create
        assert ticket_in_db.updated_at  # always change
