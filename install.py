#!/usr/bin/env python3
"""
Installation script for trading-backend with custom CCXT support.
This ensures the correct CCXT package is installed for weex exchange support.
"""
import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(cmd, check=True, shell=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.returncode}")
        print(f"Output: {e.stdout}")
        print(f"Error Output: {e.stderr}")
        return False

def main():
    print("=" * 60)
    print("Trading-Backend Installation Script")
    print("This will install trading-backend with weex exchange support")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found. Please run this script from the trading-backend directory.")
        sys.exit(1)
    
    # Step 1: Upgrade pip
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        sys.exit(1)
    
    # Step 2: Install requirements (including custom CCXT)
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", 
                      "Installing requirements with custom CCXT"):
        sys.exit(1)
    
    # Step 3: Install trading-backend in development mode
    if not run_command(f"{sys.executable} -m pip install -e .", 
                      "Installing trading-backend in development mode"):
        sys.exit(1)
    
    # Step 4: Verify installation
    print("\n" + "=" * 40)
    print("Verifying installation...")
    print("=" * 40)
    
    try:
        # Test imports
        import trading_backend
        print("✓ trading_backend imported successfully")
        
        import trading_backend.exchanges
        print("✓ exchanges module imported successfully")
        
        # Check if weex is available
        if hasattr(trading_backend.exchanges, 'Weex'):
            weex_class = trading_backend.exchanges.Weex
            print(f"✓ Weex exchange available (name: {weex_class.get_name()}, sponsoring: {weex_class.is_sponsoring()})")
        else:
            print("❌ Weex exchange not found")
            
        # Check CCXT
        import ccxt
        print(f"✓ CCXT version: {ccxt.__version__}")
        
        print("\n" + "=" * 60)
        print("🎉 Installation completed successfully!")
        print("Trading-backend is ready to use with weex exchange support.")
        print("=" * 60)
        
    except ImportError as e:
        print(f"❌ Import error during verification: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
