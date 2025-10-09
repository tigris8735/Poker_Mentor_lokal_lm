print("Testing basic Python...")
try:
    import sys
    print(f"Python path: {sys.executable}")
    print("✅ Python works!")
except Exception as e:
    print(f"❌ Python error: {e}")