from flask import Flask, render_template
from controller.car_controller import car_blueprint
from controller.customer_controller import customer_blueprint
from controller.employee_controller import employee_blueprint
from controller.order_controller import order_blueprint
from database_neo4j import close_db

app = Flask(__name__)

app.register_blueprint(car_blueprint, url_prefix='/cars')
app.register_blueprint(customer_blueprint, url_prefix='/customers')
app.register_blueprint(employee_blueprint, url_prefix='/employees')
app.register_blueprint(order_blueprint, url_prefix='/orders')

@app.route('/')
def home():
    return render_template('index.html')

@app.teardown_appcontext
def shutdown_session(exception=None):
    close_db()

if __name__ == '__main__':
    app.run(debug=True)




# Output ved kjøring av app.py:
# * Serving Flask app 'app'
# * Debug mode: on
# WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
# * Running on http://127.0.0.1:5000
# Press CTRL+C to quit
# * Restarting with stat
# * Debugger is active!
# * Debugger PIN: 126-354-847
