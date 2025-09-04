# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## About This Project

This is `trading-backend`, a Python library for cryptocurrency exchange integrations built by Drakkar-Software. It provides a unified backend abstraction layer over CCXT exchanges with enhanced error handling, API key validation, and exchange-specific customizations.

**Key Details:**
- Python 3.8+ requirement
- Primary dependency on custom CCXT library for exchange connections (includes weex exchange support)
- LGPL-3.0 licensed
- Version 1.2.41 (as of last update)
- Uses custom CCXT from: https://github.com/Danijel-Enoch/ccxt

## Development Commands

### Environment Setup
```bash
# Recommended: Use the installation script
python3 install.py

# OR Manual installation:
# 1. Install custom CCXT and dependencies first
python3 -m pip install -r requirements.txt

# 2. Install the library in development mode
python3 -m pip install -e .

# Install development dependencies
python3 -m pip install -r dev_requirements.txt
```

### Testing
```bash
# Run all tests
python3 -m pytest

# Run tests with coverage
python3 -m pytest --cov=trading_backend --cov-report=html

# Run tests with verbose output
python3 -m pytest -v

# Run a specific test file
python3 -m pytest tests/test_exchanges_factory.py

# Run tests in parallel
python3 -m pytest -n auto
```

### Code Quality
```bash
# Run pylint with project configuration
pylint --rcfile=standard.rc trading_backend/

# Check PEP8 compliance (via pytest-pep8)
python3 -m pytest --pep8

# Run coverage report
coverage run -m pytest
coverage report
coverage html
```

### Build and Distribution
```bash
# Build distribution packages
python3 setup.py sdist bdist_wheel

# Upload to PyPI (requires authentication)
twine upload dist/*

# Check package integrity before upload
twine check dist/*
```

## Code Architecture

### Core Components

**Exchange Factory Pattern (`exchange_factory.py`)**
- `create_exchange_backend()`: Main factory function that instantiates appropriate exchange backend based on CCXT exchange ID
- `is_sponsoring()`: Checks if an exchange provides broker rebates
- Dynamic discovery of exchange implementations using class introspection

**Base Exchange Class (`exchanges/exchange.py`)**
- Abstract base providing common functionality for all exchange backends
- API key validation and rights checking (`_get_api_key_rights()`, `_ensure_api_key_rights()`)
- Error handling and transformation (`error_describer()` context manager)
- Account validation workflow (`is_valid_account()`)
- Broker/sponsoring integration hooks

**Exchange Implementations (`exchanges/`)**
Each exchange inherits from base `Exchange` class and provides:
- Exchange-specific API key permission checking
- Custom error handling for exchange-specific edge cases  
- Broker ID configuration for sponsored exchanges
- Trading type support (spot, margin, futures)

**Supported Exchanges:**
- Binance, BinanceUS, Bybit, OKX, Coinbase
- KuCoin, KuCoin Futures, MEXC, Bitget, Phemex
- Gate.io, HTX, Huobi, Crypto.com, Ascendex
- Bingx, Coinex, Bitmart, HollaEx, Weex

### Error Handling System

**Custom Exception Hierarchy:**
```
UnexpectedError (RuntimeError)
├── TimeSyncError - Clock sync issues
└── NetworkError - Connection problems

ExchangeAuthError (RuntimeError)
├── APIKeyIPWhitelistError - IP restriction violations
└── APIKeyPermissionsError - Insufficient API key rights
```

**Key Features:**
- Proxy error detection and transformation
- CCXT error mapping to domain-specific exceptions
- Automatic retry logic for transient issues

### API Key Rights System

**Rights Enum (`enums.py`):**
- `READING` - Market data access
- `SPOT_TRADING` - Spot market trading
- `MARGIN_TRADING` - Margin trading capabilities
- `FUTURES_TRADING` - Derivatives trading
- `WITHDRAWALS` - Funds withdrawal (restricted by default)

**Validation Flow:**
1. Attempt dummy order cancellation to test trading permissions
2. Parse exchange-specific error responses
3. Map to appropriate rights based on error type
4. Validate against required permissions for trading mode
5. Block withdrawal rights unless explicitly allowed via `ALLOW_WITHDRAWAL_KEYS` env var

## Development Patterns

### Adding New Exchange Support
1. Create new file in `exchanges/` directory named after exchange
2. Inherit from `exchanges.Exchange` base class
3. Override `get_name()` to return CCXT exchange ID
4. Implement `_get_api_key_rights()` for exchange-specific validation
5. Add import/export to `exchanges/__init__.py`
6. Set `IS_SPONSORING = True` if broker rebates available

### Error Handling Best Practices
- Always use `error_describer()` context manager for CCXT operations
- Call `raise_accurate_auth_error_if_any()` for authentication errors  
- Transform generic CCXT exceptions to specific trading_backend errors
- Log errors appropriately using octobot_commons.logging when available

### Testing Considerations
- Mock exchange instances using test fixtures in `tests/`
- Test both success and failure scenarios for API key validation
- Verify exchange factory correctly instantiates specific backends
- Coverage configured to exclude tests and setup files

## Environment Variables

- `ALLOW_WITHDRAWAL_KEYS`: Set to "False" to block API keys with withdrawal permissions (default: "True")
