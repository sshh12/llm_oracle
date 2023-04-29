from server.app import app, db


if __name__ == "__main__":
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    app.run(port=5000)
