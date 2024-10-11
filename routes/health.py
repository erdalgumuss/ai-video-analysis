from flask import Blueprint
from controllers.healthController import health_check

health_bp = Blueprint('health', __name__)

# Sağlık kontrolü rotası
@health_bp.route('/api/health', methods=['GET'])
def health():
    return health_check()
