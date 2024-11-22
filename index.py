from app import app
from flask import  render_template

@app.route("/")
def index():
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True) #Lên pythonanywhere nhớ để Falsse