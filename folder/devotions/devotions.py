

from flask import Blueprint
from ..database import devotions as devotion_collection


devotions_bp = Blueprint('devotions', __name__)

@devotions_bp.route('/', methods=["GET"])
def fetch_devotions():
  try:
    devotions = []
    for devotion in devotion_collection.find():
      devotion['_id'] = str(devotion['_id'])
      devotions.append(devotion)
    return ({ 'status': 'success', 'message': 'Devotions', 'devotions': devotions })
  except Exception as e:
    print('Error getting devotions')
    return ({ 'status': 'error', 'message': str(e)})



@devotions_bp.route("/", methods=["POST"])
def create_devotion():
  pass