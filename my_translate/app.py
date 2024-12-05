from chalice import Chalice
from chalicelib.views.routs import extra_routes_translate

app = Chalice(app_name='my_translate')
app.register_blueprint(extra_routes_translate)

