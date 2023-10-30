from flo import create_app, db, migrate, mail

app = create_app()

# db.init_app(app)
# migrate.init_app(app, db)
#
# mail.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)