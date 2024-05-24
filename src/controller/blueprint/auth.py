from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from http import HTTPStatus
import jwt
from datetime import datetime, timedelta
from logging import getLogger

from src.model.views.user_view import UserView
from src.utils.utils import db
from src.model.views.customer_view import CustomerView
from src.controller.types.response import Response
from src.controller.enums.database_response_status import DatabaseResponseStatus
from src.utils.utils import sqlalchemy_error_to_dict
from src.env import JWT_SECRET_KEY

auth = Blueprint('auth', __name__, url_prefix='/api')
logger = getLogger(__name__)


@auth.route('auth/sign-up', methods=['POST'])
def signUp():
  data = request.get_json()
  email = data['customer_email']
  password = data['customer_password']
  nip = data['customer_nip_number']
  city = data['customer_city']
  postal_code = data['customer_postal_code']
  building_number = data['customer_building_number']
  street = data['customer_street']
  firstname = data['customer_firstname']
  surname = data['customer_surname']
  phone = data['customer_phone']

  try:
    new_user_id = db.session.query(
      func.insert_user_account(email, password, None)
    ).scalar()

    new_customer = CustomerView(
        customer_id=new_user_id,
        customer_nip_number=nip,
        customer_name=firstname,
        customer_surname=surname,
        customer_email=email,
        customer_phone=phone,
        customer_city=city,
        customer_postal_code=postal_code,
        customer_street=street,
        customer_building_number=building_number,
        customer_last_modified_by=None,
        customer_last_modified_at=None
    )
    db.session.add(new_customer)
    db.session.commit()

    payload = {
      'user_id': new_user_id,
      'email': email,
      'exp': datetime.now() + timedelta(minutes=60), # Valid for 60 mins
      'iat': datetime.now()
    }

    token = create_access_token(payload)

    return jsonify({
      'auth_schema': 'Bearer',
      'access_token': token,
      'user_id': new_user_id,
      'email': email,
      'is_admin': False # Przy rejestracji jest to normalny użytkownik (żaden recepcjonista czy admin)
    })
  except SQLAlchemyError as e:
    db.session.rollback()
    json_data_error = sqlalchemy_error_to_dict(e)
    logger.error(json_data_error)
    return Response.create(
      DatabaseResponseStatus.DATABASE_ERROR.get_value(),
      [],
      json_data_error.json
    ), HTTPStatus.INTERNAL_SERVER_ERROR


@auth.route('auth/sign-in', methods=['POST'])
def signIn():
  data = request.get_json()
  email = data.get('email', None)
  password = data.get('password', None)

  try:
    user_id = db.session.query(
      func.authenticate_user_account(email, password)
    ).scalar()

    user = db.session.query(UserView).filter(user_id == user_id).first()

    payload = {
      'user_id': user_id,
      'email': email,
      'exp': datetime.utcnow() + timedelta(minutes=60), # Valid for 60 mins
      'iat': datetime.utcnow(),
      'sub': user_id
    }

    token = create_access_token(payload)
    return jsonify({
      'auth_schema': 'Bearer',
      'access_token': token,
      'user_id': user_id,
      'email': email,
      'is_admin': user.user_is_admin
    })
  except SQLAlchemyError as e:
    json_data_error = sqlalchemy_error_to_dict(e)
    logger.error(json_data_error)
    return Response.create(
      DatabaseResponseStatus.DATABASE_ERROR.get_value(),
      [],
      json_data_error.json
    ), HTTPStatus.NOT_FOUND


# Endpoint jest przykładowy w celach poglądowych jak zabezpieczać
# nieautoryzowane żądania
@auth.route('auth/secured', methods=['POST'])
@jwt_required()
def secured():
  return jsonify(True)


def create_access_token(payload: dict[str, any]) -> str:
  return jwt.encode(payload, JWT_SECRET_KEY)
