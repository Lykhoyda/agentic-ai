#!/usr/bin/env python3

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import accounts
from accounts import Account

class TestGetSharePrice(unittest.TestCase):
    def test_get_share_price_known_symbol(self):
        """Test get_share_price returns correct price for known symbols"""
        self.assertEqual(accounts.get_share_price('AAPL'), 150.0)
        self.assertEqual(accounts.get_share_price('TSLA'), 800.0)
        self.assertEqual(accounts.get_share_price('GOOGL'), 2800.0)

    def test_get_share_price_unknown_symbol(self):
        """Test get_share_price returns 0.0 for unknown symbols"""
        self.assertEqual(accounts.get_share_price('UNKNOWN'), 0.0)
        self.assertEqual(accounts.get_share_price(''), 0.0)

class TestAccount(unittest.TestCase):
    def setUp(self):
        """Set up a test account for each test"""
        self.account = Account("test_user")
    
    def test_init(self):
        """Test account initialization"""
        self.assertEqual(self.account.user_id, "test_user")
        self.assertEqual(self.account.balance, 0.0)
        self.assertEqual(self.account.initial_deposit, 0.0)
        self.assertEqual(self.account.portfolio, {})
        self.assertEqual(len(self.account.transactions), 0)
        self.assertIsInstance(self.account.created_at, datetime)
    
    def test_create_account(self):
        """Test create_account resets account state"""
        # First modify the account
        self.account.balance = 1000.0
        self.account.initial_deposit = 1000.0
        self.account.portfolio = {'AAPL': 10}
        self.account.transactions = [{'type': 'DEPOSIT'}]
        
        # Now call create_account and verify it resets everything
        self.account.create_account()
        self.assertEqual(self.account.balance, 0.0)
        self.assertEqual(self.account.initial_deposit, 0.0)
        self.assertEqual(self.account.portfolio, {})
        self.assertEqual(len(self.account.transactions), 0)
        self.assertIsInstance(self.account.created_at, datetime)
    
    def test_deposit_funds_positive(self):
        """Test depositing a positive amount of funds"""
        result = self.account.deposit_funds(1000.0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(self.account.initial_deposit, 1000.0)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0]['type'], 'DEPOSIT')
        self.assertEqual(self.account.transactions[0]['amount'], 1000.0)
        self.assertEqual(self.account.transactions[0]['balance_after'], 1000.0)
    
    def test_deposit_funds_negative(self):
        """Test depositing a negative amount of funds"""
        result = self.account.deposit_funds(-100.0)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 0.0)
        self.assertEqual(len(self.account.transactions), 0)
    
    def test_deposit_funds_zero(self):
        """Test depositing zero funds"""
        result = self.account.deposit_funds(0.0)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 0.0)
        self.assertEqual(len(self.account.transactions), 0)
    
    def test_withdraw_funds_valid(self):
        """Test withdrawing a valid amount of funds"""
        self.account.deposit_funds(1000.0)
        result = self.account.withdraw_funds(500.0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 500.0)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[1]['type'], 'WITHDRAWAL')
        self.assertEqual(self.account.transactions[1]['amount'], 500.0)
        self.assertEqual(self.account.transactions[1]['balance_after'], 500.0)
    
    def test_withdraw_funds_negative(self):
        """Test withdrawing a negative amount of funds"""
        self.account.deposit_funds(1000.0)
        result = self.account.withdraw_funds(-100.0)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(len(self.account.transactions), 1)
    
    def test_withdraw_funds_zero(self):
        """Test withdrawing zero funds"""
        self.account.deposit_funds(1000.0)
        result = self.account.withdraw_funds(0.0)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(len(self.account.transactions), 1)
    
    def test_withdraw_funds_insufficient_balance(self):
        """Test withdrawing more than the available balance"""
        self.account.deposit_funds(1000.0)
        result = self.account.withdraw_funds(1500.0)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(len(self.account.transactions), 1)
    
    def test_buy_shares_valid(self):
        """Test buying shares with sufficient funds"""
        self.account.deposit_funds(10000.0)
        result = self.account.buy_shares('AAPL', 10)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 8500.0)  # 10000 - (150 * 10)
        self.assertEqual(self.account.portfolio['AAPL'], 10)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[1]['type'], 'BUY')
        self.assertEqual(self.account.transactions[1]['symbol'], 'AAPL')
        self.assertEqual(self.account.transactions[1]['quantity'], 10)
        self.assertEqual(self.account.transactions[1]['price'], 150.0)
        self.assertEqual(self.account.transactions[1]['total'], 1500.0)
    
    def test_buy_shares_insufficient_funds(self):
        """Test buying shares with insufficient funds"""
        self.account.deposit_funds(1000.0)
        result = self.account.buy_shares('TSLA', 10)  # TSLA is 800 per share
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(self.account.portfolio, {})
        self.assertEqual(len(self.account.transactions), 1)
    
    def test_buy_shares_invalid_symbol(self):
        """Test buying shares with an invalid symbol"""
        self.account.deposit_funds(10000.0)
        result = self.account.buy_shares('INVALID', 10)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 10000.0)
        self.assertEqual(self.account.portfolio, {})
        self.assertEqual(len(self.account.transactions), 1)
    
    def test_buy_shares_negative_quantity(self):
        """Test buying a negative quantity of shares"""
        self.account.deposit_funds(10000.0)
        result = self.account.buy_shares('AAPL', -10)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 10000.0)
        self.assertEqual(self.account.portfolio, {})
        self.assertEqual(len(self.account.transactions), 1)
    
    def test_buy_shares_zero_quantity(self):
        """Test buying zero shares"""
        self.account.deposit_funds(10000.0)
        result = self.account.buy_shares('AAPL', 0)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 10000.0)
        self.assertEqual(self.account.portfolio, {})
        self.assertEqual(len(self.account.transactions), 1)
    
    def test_sell_shares_valid(self):
        """Test selling shares that are in the portfolio"""
        self.account.deposit_funds(10000.0)
        self.account.buy_shares('AAPL', 10)
        result = self.account.sell_shares('AAPL', 5)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 9250.0)  # 8500 + (150 * 5)
        self.assertEqual(self.account.portfolio['AAPL'], 5)
        self.assertEqual(len(self.account.transactions), 3)
        self.assertEqual(self.account.transactions[2]['type'], 'SELL')
        self.assertEqual(self.account.transactions[2]['symbol'], 'AAPL')
        self.assertEqual(self.account.transactions[2]['quantity'], 5)
        self.assertEqual(self.account.transactions[2]['price'], 150.0)
        self.assertEqual(self.account.transactions[2]['total'], 750.0)
    
    def test_sell_shares_all(self):
        """Test selling all shares of a symbol, which should remove it from portfolio"""
        self.account.deposit_funds(10000.0)
        self.account.buy_shares('AAPL', 10)
        result = self.account.sell_shares('AAPL', 10)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 10000.0)
        self.assertNotIn('AAPL', self.account.portfolio)
        self.assertEqual(len(self.account.transactions), 3)
    
    def test_sell_shares_insufficient_shares(self):
        """Test selling more shares than are in the portfolio"""
        self.account.deposit_funds(10000.0)
        self.account.buy_shares('AAPL', 10)
        result = self.account.sell_shares('AAPL', 15)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 8500.0)
        self.assertEqual(self.account.portfolio['AAPL'], 10)
        self.assertEqual(len(self.account.transactions), 2)
    
    def test_sell_shares_not_in_portfolio(self):
        """Test selling shares that are not in the portfolio"""
        self.account.deposit_funds(10000.0)
        result = self.account.sell_shares('AAPL', 5)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 10000.0)
        self.assertEqual(self.account.portfolio, {})
        self.assertEqual(len(self.account.transactions), 1)
    
    def test_sell_shares_negative_quantity(self):
        """Test selling a negative quantity of shares"""
        self.account.deposit_funds(10000.0)
        self.account.buy_shares('AAPL', 10)
        result = self.account.sell_shares('AAPL', -5)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 8500.0)
        self.assertEqual(self.account.portfolio['AAPL'], 10)
        self.assertEqual(len(self.account.transactions), 2)
    
    def test_sell_shares_zero_quantity(self):
        """Test selling zero shares"""
        self.account.deposit_funds(10000.0)
        self.account.buy_shares('AAPL', 10)
        result = self.account.sell_shares('AAPL', 0)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 8500.0)
        self.assertEqual(self.account.portfolio['AAPL'], 10)
        self.assertEqual(len(self.account.transactions), 2)
    
    def test_calculate_portfolio_value(self):
        """Test calculating the portfolio value with various stocks"""
        self.account.deposit_funds(10000.0)
        self.account.buy_shares('AAPL', 10)
        self.account.buy_shares('TSLA', 5)
        
        # Portfolio value should be: (10 * 150) + (5 * 800) = 1500 + 4000 = 5500
        portfolio_value = self.account.calculate_portfolio_value()
        self.assertEqual(portfolio_value, 5500.0)
    
    def test_calculate_portfolio_value_empty(self):
        """Test calculating the portfolio value with an empty portfolio"""
        portfolio_value = self.account.calculate_portfolio_value()
        self.assertEqual(portfolio_value, 0.0)
    
    def test_calculate_profit_loss(self):
        """Test calculating profit/loss with various transactions"""
        self.account.deposit_funds(10000.0)
        self.account.buy_shares('AAPL', 10)  # Cost: 1500
        
        # Initial deposit: 10000, Current assets: 8500 (balance) + 1500 (portfolio) = 10000
        profit_loss = self.account.calculate_profit_loss()
        self.assertEqual(profit_loss, 0.0)
        
        # Now let's simulate a price increase (we'll need to mock get_share_price)
        with patch('accounts.get_share_price', return_value=200.0):
            # Portfolio is now worth 10 * 200 = 2000, giving a profit of 500
            profit_loss = self.account.calculate_profit_loss()
            self.assertEqual(profit_loss, 500.0)
    
    def test_get_holdings(self):
        """Test getting holdings information"""
        self.account.deposit_funds(10000.0)
        self.account.buy_shares('AAPL', 10)
        
        holdings = self.account.get_holdings()
        self.assertIn('AAPL', holdings)
        self.assertEqual(holdings['AAPL']['quantity'], 10)
        self.assertEqual(holdings['AAPL']['price'], 150.0)
        self.assertEqual(holdings['AAPL']['value'], 1500.0)
    
    def test_get_holdings_empty(self):
        """Test getting holdings with an empty portfolio"""
        holdings = self.account.get_holdings()
        self.assertEqual(holdings, {})
    
    def test_get_transaction_history(self):
        """Test getting transaction history"""
        self.account.deposit_funds(10000.0)
        self.account.buy_shares('AAPL', 10)
        self.account.sell_shares('AAPL', 5)
        
        transactions = self.account.get_transaction_history()
        self.assertEqual(len(transactions), 3)
        self.assertEqual(transactions[0]['type'], 'DEPOSIT')
        self.assertEqual(transactions[1]['type'], 'BUY')
        self.assertEqual(transactions[2]['type'], 'SELL')
    
    def test_get_transaction_history_empty(self):
        """Test getting transaction history with no transactions"""
        transactions = self.account.get_transaction_history()
        self.assertEqual(transactions, [])
    
    def test_get_profit_loss_report(self):
        """Test getting a detailed profit/loss report"""
        self.account.deposit_funds(10000.0)
        self.account.buy_shares('AAPL', 10)