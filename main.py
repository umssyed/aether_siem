from flask import Flask, render_template
from app.routes import routes
from app.database import Base, engine

app = Flask(__name__, template_folder="app/templates")
app.register_blueprint(routes)
Base.metadata.create_all(bind=engine)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)