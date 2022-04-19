from oppiamobile.settings import *

DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
DATABASES['default']['NAME'] = os.path.join(BASE_DIR, 'db.sqlite3')
FIXTURES_PATH = os.path.join(BASE_DIR, 'oppia', 'fixtures')
TEST_RESOURCES = os.path.join(BASE_DIR, 'tests', 'resources')
temp_dir = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
MEDIA_ROOT = os.path.join(tempfile.gettempdir(), temp_dir, 'media')
COURSE_UPLOAD_DIR = os.path.join(tempfile.gettempdir(), temp_dir, 'upload')
os.makedirs(MEDIA_ROOT, exist_ok=True)
os.makedirs(COURSE_UPLOAD_DIR, exist_ok=True)
print("Using sqlite3 for test coverage")