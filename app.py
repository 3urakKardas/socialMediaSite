from flaskManager import *

def main():

    myServer = Server(__name__)

    myServer.app.run(debug=False) #when debug true starting script executed twice

if __name__ == "__main__":

    main()

    """db = SQLAlchemy(main())


    class account(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        userName = db.Column(db.String(20), nullable=False)
        userPassword = db.Column(db.String(20), nullable=False)"""
