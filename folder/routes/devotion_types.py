from crypt import methods
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


@devotion_types_bp.route("/", methods=["PUT"])
def update_devotion_types():
  try:
      #req_json = request.json

      info = request.json
      id  = info.get("_id")

      keys = [i for i in info.keys()]

      data = {}

      for i in keys:
            data[i] = info.get(i)
        
      for key in keys:
            if data[key] == "":
                data.pop(key)
                
      data.pop("_id")

      insert_result = devotion_types.find_one_and_update({'_id':id}, {"$set":data}  )
      return ({ 'status': 'success', 'message': 'Updated devotion type'})
  except Exception as e:
      print('Error updating devotion type')
      return ({ 'status': 'error', 'message': str(e)})
    
@devotion_types_bp.route("/", methods=["DELETE"])
def delete_devotion_type():
  try:
    id = request.args.get("_id")
    devotion_types.find_one_and_delete({"_id":id})
    return {"message":"devotion type deleted", "status":"success"}
  except Exception as e:
    print("Error deleting devotion type")
    return {"status":"error", "message":str(e)}