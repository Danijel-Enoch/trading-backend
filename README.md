# trading-backend [1.2.41](https://github.com/Danijel-Enoch/trading-backend/tree/master/CHANGELOG.md)
[![PyPI](https://img.shields.io/pypi/v/trading-backend.svg)](https://pypi.python.org/pypi/trading-backend/)
[![Downloads](https://pepy.tech/badge/trading-backend/month)](https://pepy.tech/project/trading-backend)
[![Github-Action-CI](https://github.com/Drakkar-Software/trading-backend/workflows/trading-backend-CI/badge.svg)](https://github.com/Drakkar-Software/trading-backend/actions)

## Installation

This version of trading-backend includes **weex exchange support** and requires a custom CCXT package.

### Install from GitHub (Recommended)

To get the full functionality including weex exchange support:

``` {.sourceCode .bash}
# Clone the repository
$ git clone https://github.com/Danijel-Enoch/trading-backend.git
$ cd trading-backend

# Install with custom CCXT (includes weex exchange)
$ python3 -m pip install -r requirements.txt
$ python3 -m pip install -e .
```

### Install from PyPI

**Note:** PyPI version may not include the latest weex exchange support.

``` {.sourceCode .bash}
$ python3 -m pip install trading-backend
```

## Features

- **21+ Exchange Support**: Including Binance, Bybit, OKX, Coinbase, KuCoin, and **Weex**
- **Enhanced Error Handling**: Exchange-specific error mapping and handling
- **API Key Validation**: Comprehensive API key rights checking
- **Broker Integration**: Support for exchanges with rebate programs (including Weex)
- **Custom CCXT**: Uses enhanced CCXT library with additional exchange support
