from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from http import HTTPStatus
import jwt
from datetime import datetime, timedelta
from logging import getLogger

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
  email = data['email']
  password = data['password']
  nip = data['nip']
  city = data['city']
  postalCode = data['postalCode']
  buildingNumber = data['buildingNumber']
  street = data['street']
  firstname = data['firstname']
  surname = data['surname']
  phone = data['phone']

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
        customer_postal_code=postalCode,
        customer_street=street,
        customer_building_number=buildingNumber,
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

    return jsonify({'access_token': token})
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

    payload = {
      'user_id': user_id,
      'email': email,
      'exp': datetime.utcnow() + timedelta(minutes=60), # Valid for 60 mins
      'iat': datetime.utcnow(),
      'sub': user_id
    }

    token = create_access_token(payload)

    return jsonify({'access_token': token})
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
