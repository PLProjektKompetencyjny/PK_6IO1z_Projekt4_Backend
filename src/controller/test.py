from flask import Blueprint, jsonify

from src.model.views.room_view import RoomView
from src.model.views.invoice_view import InvoiceView
from src.model.views.reservation_view import ReservationView
from src.utils.utils import db


from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db.session.query(RoomView.room_id).all()

# engine = create_engine(connectionString)
# Session = sessionmaker(bind=engine)