import os

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    
    # Use PORT from environment (Render sets it automatically)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
