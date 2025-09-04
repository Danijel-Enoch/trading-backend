#  Drakkar-Software trading-backend
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import ccxt

import trading_backend.exchanges.exchange as exchange
import trading_backend.enums
import trading_backend.errors


class Weex(exchange.Exchange):
    SPOT_ID = "weex"
    MARGIN_ID = None
    FUTURE_ID = None
    IS_SPONSORING = True

    @classmethod
    def get_name(cls):
        return "weex"

    async def _get_api_key_rights(self) -> list[trading_backend.enums.APIKeyRights]:
        """
        Get API key rights for weex exchange by trying different operations
        Based on weex.llm documentation, API keys can have "Read" and/or "Trade" permissions
        """
        rights = [trading_backend.enums.APIKeyRights.READING]
        
        try:
            with self.error_describer():
                # Try to fetch account assets to confirm reading permissions
                await self._exchange.connector.client.fetch_balance()
                
            # Test trading permissions by attempting to cancel a dummy order
            # This follows the pattern used in other exchanges
            try:
                with self.error_describer():
                    await self._inner_cancel_order()
            except ccxt.AuthenticationError as err:
                if self._is_api_permission_error(err):
                    # No trading permission - keep only reading rights
                    pass
                else:
                    self.raise_accurate_auth_error_if_any(err)
                    raise
            except (ccxt.BadSymbol, ccxt.OperationFailed) as err:
                raise trading_backend.errors.UnexpectedError(err) from err
            except ccxt.ExchangeError as err:
                self.raise_accurate_auth_error_if_any(err)
                if not self._is_api_permission_error(err):
                    # Goal: we are in the expected "order not found" error scenario
                    # => has trading permission
                    rights.append(trading_backend.enums.APIKeyRights.SPOT_TRADING)
                    
        except ccxt.BaseError as err:
            try:
                import octobot_commons.logging as logging
                logging.get_logger(self.__class__.__name__).info(
                    f"Error when checking {self.__class__.__name__} api key rights: {err} ({err.__class__.__name__})"
                )
            except ImportError:
                pass
            raise err
            
        return rights

    def _is_api_permission_error(self, err):
        """
        Check if the error indicates insufficient API permissions
        Based on weex.llm error codes
        """
        error_msg = str(err).lower()
        
        # Common weex permission-related error messages from the documentation
        permission_errors = [
            "invalid permissions",  # Error code 40014
            "api verification failed",  # Error code 40009
            "incorrect api key",  # Error code 40012
            "invalid access_key",  # Error code 40006
            "access denied",
            "permission denied",
            "insufficient permissions",
            "trading not allowed"
        ]
        
        return any(perm_err in error_msg for perm_err in permission_errors)

    def raise_accurate_auth_error_if_any(self, err):
        """
        Transform weex-specific errors to trading_backend errors
        Based on weex.llm error documentation
        """
        error_msg = str(err).lower()
        error_code = getattr(err, 'code', None)
        
        # IP whitelist errors
        if "invalid ip request" in error_msg or error_code == "40018":
            raise trading_backend.errors.APIKeyIPWhitelistError(err) from err
            
        # Authentication errors from weex.llm documentation
        auth_errors = [
            "invalid access_key",  # 40006
            "api verification failed",  # 40009
            "incorrect api key/passphrase",  # 40012
            "header \"access_key\" is required",  # 40001
            "header \"access_sign\" is required",  # 40002
            "header \"access_timestamp\" is required",  # 40003
            "header \"access_passphrase\" is required",  # 40011
            "invalid access_timestamp",  # 40005
            "request timestamp expired",  # 40008
        ]
        
        if any(auth_err in error_msg for auth_err in auth_errors):
            raise ccxt.AuthenticationError(err) from err

    async def _inner_is_valid_account(self) -> (bool, str):
        """
        Check account validity for weex
        Based on weex.llm documentation requirements
        """
        try:
            with self.error_describer():
                # Try to get account assets to verify account is valid
                balance = await self._exchange.connector.client.fetch_balance()
                
                # Check if account has any frozen status
                # Based on weex.llm error code 40013: "Account frozen"
                return True, None
                
        except ccxt.ExchangeError as err:
            error_msg = str(err).lower()
            
            if "account frozen" in error_msg or getattr(err, 'code', None) == "40013":
                return False, "Account is frozen"
            elif "account must be linked" in error_msg:
                return False, "Account must be linked to a mobile number or Google account"
            else:
                # Let the parent method handle other errors
                raise

    def get_headers(self) -> dict:
        """
        Get headers for weex API requests
        Based on weex.llm authentication documentation
        """
        return {
            "Content-Type": "application/json",
            "locale": "en-US"
        }
