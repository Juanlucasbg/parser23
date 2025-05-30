from app import app

# Import enhanced routes
try:
    import enhanced_routes
    print("✅ Enhanced routes loaded successfully")
except Exception as e:
    print(f"⚠️ Enhanced routes not loaded: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)