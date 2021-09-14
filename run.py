from simple_login import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="localhost", port=8083)
