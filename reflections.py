from config import Config
from app import create_app, db
# from app.main.models (import models here)
import sqlalchemy as sqla 
import sqlalchemy.orm as sqlo 

app = create_app(Config)

@app.shell_context_processor
def make_shell_context():
    return {'sqla': sqla, 'sqlo': sqlo, 'db': db}
    
@app.before_request
def initDB(*args, **kwargs):
    # initialize db here
    pass 