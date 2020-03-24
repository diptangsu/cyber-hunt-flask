from os.path import join, dirname, realpath


SECRET_KEY = '$%^uke45f78v4ei#$%^&ydfg12734vgn35y65o2!@#$&^'
DATABASE_FILE = 'data.db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_FILE
SQLALCHEMY_TRACK_MODIFICATIONS = False
FLASK_ADMIN_SWATCH = 'yeti'

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'uploads/media')
ALLOWED_EXTENSIONS = ['jpg', 'png', 'jpeg', 'class', 'java', 'c', 'cpp', 'py', 'out']
MAX_CONTENT_LENGTH = 1000 * 1024 * 1024  # 1000mb
