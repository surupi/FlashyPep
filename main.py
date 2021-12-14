from FlashyPep import create_app

if __name__ == "__main__":
    app, api = create_app()
    
    app.run(host = "0.0.0.0", port = 5432, debug=True)