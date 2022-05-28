from flask import Blueprint, request
from folder.database import devotion_types


devotion_types_bp = Blueprint('devotion_types', __name__, url_prefix="/api/haggai/dev_types")

@devotion_types_bp.route('/', methods=['GET'])
def fetch_devotion_types():
  try:
      types = []
      for type in devotion_types.find():
        type['_id'] = str(type['_id'])
        types.append(type)
      return ({ 'status': 'success', 'message': 'Devotion types', 'devotion_types': types})
  except Exception as e:
      print('Error creating devotion type')
      return ({ 'status': 'error', 'message': str(e)})

@devotion_types_bp.route('/', methods=['POST'])
def create_devotion_type():
  try:
      req_json = request.json
      insert_result = devotion_types.insert_one({
        '_id':req_json.get('_id'),
        'description': req_json.get('description'),
        'name': req_json.get('name'),
        'image_url': req_json.get('image_url')
      })
      return ({ 'status': 'success', 'message': 'Created devotion type'})
  except Exception as e:
      print('Error creating devotion type')
      return ({ 'status': 'error', 'message': str(e)})