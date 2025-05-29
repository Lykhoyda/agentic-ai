#!/usr/bin/env python3

from datetime import datetime
from typing import Dict, List, Optional, Union

def get_share_price(symbol: str) -> float:
    """
    Returns the current price of a share for the given symbol.
    This is a test implementation that returns fixed prices.
    
    Args:
        symbol: The stock symbol to get the price for.
        
    Returns:
        The current price of the share.
    """
    prices = {
        'AAPL': 150.0,
        'TSLA': 800.0,
        'GOOGL': 2800.0
    }
    return prices.get(symbol, 0.0)

class Account:
    """
    Represents a user's account in the trading simulation platform.
    Manages user funds, share transactions, and calculations related to
    portfolio and profit/loss.
    """
    
    def __init__(self, user_id: str):
        """
        Initialize an account for a user with a unique identifier.
        
        Args:
            user_id: A unique string identifier for the user.
        """
        self.user_id = user_id
        self.balance = 0.0
        self.initial_deposit = 0.0
        self.portfolio = {}  # symbol -> quantity
        self.transactions = []
        self.created_at = datetime.now()
    
    def create_account(self) -> None:
        """
        Prepares the account for use, initializing balance and portfolio.
        """
        self.balance = 0.0
        self.initial_deposit = 0.0
        self.portfolio = {}
        self.transactions = []
        self.created_at = datetime.now()
    
    def deposit_funds(self, amount: float) -> bool:
        """
        Deposits an amount into the account balance.
        
        Args:
            amount: The amount of money to deposit. Must be positive.
            
        Returns:
            True if the deposit was successful, False otherwise.
        """
        if amount <= 0:
            return False
        
        self.balance += amount
        self.initial_deposit += amount
        
        transaction = {
            'type': 'DEPOSIT',
            'amount': amount,
            'timestamp': datetime.now(),
            'balance_after': self.balance
        }
        self.transactions.append(transaction)
        
        return True
    
    def withdraw_funds(self, amount: float) -> bool:
        """
        Withdraws funds from the account if the balance is sufficient.
        
        Args:
            amount: The amount of money to withdraw.
            
        Returns:
            True if the withdrawal was successful, False otherwise.
        """
        if amount <= 0 or amount > self.balance:
            return False
        
        self.balance -= amount
        
        transaction = {
            'type': 'WITHDRAWAL',
            'amount': amount,
            'timestamp': datetime.now(),
            'balance_after': self.balance
        }
        self.transactions.append(transaction)
        
        return True
    
    def buy_shares(self, symbol: str, quantity: int) -> bool:
        """
        Buys a specified quantity of shares if funds are sufficient.
        
        Args:
            symbol: The stock symbol to buy.
            quantity: The number of shares to buy.
            
        Returns:
            True if the purchase was successful, False otherwise.
        """
        if quantity <= 0:
            return False
        
        price = get_share_price(symbol)
        if price == 0.0:  # Symbol not found
            return False
        
        total_cost = price * quantity
        
        if total_cost > self.balance:
            return False
        
        self.balance -= total_cost
        
        # Update portfolio
        if symbol in self.portfolio:
            self.portfolio[symbol] += quantity
        else:
            self.portfolio[symbol] = quantity
        
        transaction = {
            'type': 'BUY',
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'total': total_cost,
            'timestamp': datetime.now(),
            'balance_after': self.balance
        }
        self.transactions.append(transaction)
        
        return True
    
    def sell_shares(self, symbol: str, quantity: int) -> bool:
        """
        Sells a specified quantity of shares if available in the portfolio.
        
        Args:
            symbol: The stock symbol to sell.
            quantity: The number of shares to sell.
            
        Returns:
            True if the sale was successful, False otherwise.
        """
        if quantity <= 0:
            return False
        
        if symbol not in self.portfolio or self.portfolio[symbol] < quantity:
            return False
        
        price = get_share_price(symbol)
        if price == 0.0:  # Symbol not found
            return False
        
        total_value = price * quantity
        
        self.balance += total_value
        self.portfolio[symbol] -= quantity
        
        # Remove the symbol from the portfolio if quantity becomes 0
        if self.portfolio[symbol] == 0:
            del self.portfolio[symbol]
        
        transaction = {
            'type': 'SELL',
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'total': total_value,
            'timestamp': datetime.now(),
            'balance_after': self.balance
        }
        self.transactions.append(transaction)
        
        return True
    
    def calculate_portfolio_value(self) -> float:
        """
        Calculates and returns the current total value of the user's portfolio.
        
        Returns:
            The current total value of the portfolio.
        """
        total_value = 0.0
        
        for symbol, quantity in self.portfolio.items():
            price = get_share_price(symbol)
            total_value += price * quantity
        
        return total_value
    
    def calculate_profit_loss(self) -> float:
        """
        Calculates and returns the profit or loss based on the initial deposits.
        
        Returns:
            The profit or loss as a float value.
        """
        portfolio_value = self.calculate_portfolio_value()
        total_assets = portfolio_value + self.balance
        
        return total_assets - self.initial_deposit
    
    def get_holdings(self) -> Dict[str, Dict[str, Union[int, float]]]:
        """
        Returns a dictionary representing the user's current holdings.
        
        Returns:
            Dictionary where keys are stock symbols and values are dictionaries
            containing quantity and current value.
        """
        holdings = {}
        
        for symbol, quantity in self.portfolio.items():
            price = get_share_price(symbol)
            value = price * quantity
            holdings[symbol] = {
                'quantity': quantity,
                'price': price,
                'value': value
            }
        
        return holdings
    
    def get_transaction_history(self) -> List[Dict]:
        """
        Returns a list of all the transactions made by the user.
        
        Returns:
            List of dictionaries containing transaction details.
        """
        return self.transactions
    
    def get_profit_loss_report(self) -> Dict:
        """
        Provides a detailed report of the user's profit or loss.
        
        Returns:
            A dictionary with detailed profit/loss calculation.
        """
        portfolio_value = self.calculate_portfolio_value()
        profit_loss = self.calculate_profit_loss()
        
        report = {
            'initial_deposit': self.initial_deposit,
            'current_balance': self.balance,
            'portfolio_value': portfolio_value,
            'total_assets': portfolio_value + self.balance,
            'profit_loss': profit_loss,
            'profit_loss_percentage': (profit_loss / self.initial_deposit) * 100 if self.initial_deposit > 0 else 0.0,
            'holdings': self.get_holdings()
        }
        
        return report

if __name__ == "__main__":
    # Example usage
    account = Account("user123")
    account.create_account()
    account.deposit_funds(10000.0)
    account.buy_shares("AAPL", 10)
    account.buy_shares("TSLA", 5)
    account.sell_shares("AAPL", 5)
    
    print(f"Current balance: ${account.balance:.2f}")
    print(f"Portfolio value: ${account.calculate_portfolio_value():.2f}")
    print(f"Profit/Loss: ${account.calculate_profit_loss():.2f}")
    print(f"Holdings: {account.get_holdings()}")
    print(f"Transaction history: {account.get_transaction_history()}")
    print(f"Profit/Loss report: {account.get_profit_loss_report()}")