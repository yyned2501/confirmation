from app import init_app

app = init_app()

if __name__ == '__main__':
    app.run("0.0.0.0", 5002, debug=True)
