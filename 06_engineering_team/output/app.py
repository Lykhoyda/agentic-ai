#!/usr/bin/env python3

import gradio as gr
from accounts import Account, get_share_price

# Initialize account for demo
account = Account("demo_user")
account.create_account()

def create_account():
    account.create_account()
    return "Account created successfully!"

def deposit(amount):
    try:
        amount = float(amount)
        if account.deposit_funds(amount):
            return f"Successfully deposited ${amount:.2f}"
        else:
            return "Deposit failed. Amount must be positive."
    except ValueError:
        return "Invalid amount. Please enter a valid number."

def withdraw(amount):
    try:
        amount = float(amount)
        if account.withdraw_funds(amount):
            return f"Successfully withdrew ${amount:.2f}"
        else:
            return "Withdrawal failed. Insufficient funds or invalid amount."
    except ValueError:
        return "Invalid amount. Please enter a valid number."

def buy_shares(symbol, quantity):
    try:
        quantity = int(quantity)
        if account.buy_shares(symbol, quantity):
            return f"Successfully bought {quantity} shares of {symbol}"
        else:
            return "Purchase failed. Check symbol, quantity, or available funds."
    except ValueError:
        return "Invalid quantity. Please enter a valid number."

def sell_shares(symbol, quantity):
    try:
        quantity = int(quantity)
        if account.sell_shares(symbol, quantity):
            return f"Successfully sold {quantity} shares of {symbol}"
        else:
            return "Sale failed. Check symbol or available shares."
    except ValueError:
        return "Invalid quantity. Please enter a valid number."

def get_portfolio_value():
    value = account.calculate_portfolio_value()
    return f"Current portfolio value: ${value:.2f}"

def get_profit_loss():
    profit_loss = account.calculate_profit_loss()
    if profit_loss >= 0:
        return f"Current profit: ${profit_loss:.2f}"
    else:
        return f"Current loss: ${-profit_loss:.2f}"

def get_holdings():
    holdings = account.get_holdings()
    if not holdings:
        return "No holdings found."
    
    result = "Current Holdings:\n"
    for symbol, data in holdings.items():
        result += f"{symbol}: {data['quantity']} shares at ${data['price']:.2f} each = ${data['value']:.2f}\n"
    
    return result

def get_transactions():
    transactions = account.get_transaction_history()
    if not transactions:
        return "No transactions found."
    
    result = "Transaction History:\n"
    for i, tx in enumerate(transactions, 1):
        result += f"{i}. {tx['type']}"
        if tx['type'] == 'DEPOSIT' or tx['type'] == 'WITHDRAWAL':
            result += f": ${tx['amount']:.2f}"
        elif tx['type'] == 'BUY' or tx['type'] == 'SELL':
            result += f": {tx['quantity']} {tx['symbol']} at ${tx['price']:.2f} = ${tx['total']:.2f}"
        result += f" (Balance after: ${tx['balance_after']:.2f})\n"
    
    return result

def get_account_summary():
    if account.initial_deposit == 0:
        return "Account has not been funded yet. Please deposit funds first."
    
    report = account.get_profit_loss_report()
    
    summary = f"""
Account Summary:
----------------
Initial Deposit: ${report['initial_deposit']:.2f}
Current Cash Balance: ${report['current_balance']:.2f}
Portfolio Value: ${report['portfolio_value']:.2f}
Total Assets: ${report['total_assets']:.2f}
"""
    
    if report['profit_loss'] >= 0:
        summary += f"Total Profit: ${report['profit_loss']:.2f} ({report['profit_loss_percentage']:.2f}%)\n"
    else:
        summary += f"Total Loss: ${-report['profit_loss']:.2f} ({-report['profit_loss_percentage']:.2f}%)\n"
    
    summary += "\nHoldings:\n"
    for symbol, data in report['holdings'].items():
        summary += f"- {symbol}: {data['quantity']} shares at ${data['price']:.2f} = ${data['value']:.2f}\n"
    
    return summary

def get_available_stocks():
    stocks = ["AAPL", "TSLA", "GOOGL"]
    prices = [f"{stock}: ${get_share_price(stock):.2f}" for stock in stocks]
    return "\n".join(prices)

with gr.Blocks(title="Trading Simulation Platform") as demo:
    gr.Markdown("# Trading Simulation Platform")
    
    with gr.Tab("Account Management"):
        with gr.Row():
            with gr.Column():
                create_acc_btn = gr.Button("Create New Account")
                create_result = gr.Textbox(label="Result")
                create_acc_btn.click(create_account, inputs=[], outputs=create_result)
                
                gr.Markdown("### Deposit Funds")
                deposit_amount = gr.Textbox(label="Amount")
                deposit_btn = gr.Button("Deposit")
                deposit_result = gr.Textbox(label="Result")
                deposit_btn.click(deposit, inputs=deposit_amount, outputs=deposit_result)
                
                gr.Markdown("### Withdraw Funds")
                withdraw_amount = gr.Textbox(label="Amount")
                withdraw_btn = gr.Button("Withdraw")
                withdraw_result = gr.Textbox(label="Result")
                withdraw_btn.click(withdraw, inputs=withdraw_amount, outputs=withdraw_result)
            
            with gr.Column():
                summary_btn = gr.Button("Get Account Summary")
                summary_result = gr.Textbox(label="Account Summary", lines=15)
                summary_btn.click(get_account_summary, inputs=[], outputs=summary_result)
    
    with gr.Tab("Trading"):
        with gr.Row():
            with gr.Column():
                stocks_info = gr.Textbox(label="Available Stocks", value=get_available_stocks())
                
                gr.Markdown("### Buy Shares")
                buy_symbol = gr.Textbox(label="Symbol")
                buy_quantity = gr.Textbox(label="Quantity")
                buy_btn = gr.Button("Buy")
                buy_result = gr.Textbox(label="Result")
                buy_btn.click(buy_shares, inputs=[buy_symbol, buy_quantity], outputs=buy_result)
                
                gr.Markdown("### Sell Shares")
                sell_symbol = gr.Textbox(label="Symbol")
                sell_quantity = gr.Textbox(label="Quantity")
                sell_btn = gr.Button("Sell")
                sell_result = gr.Textbox(label="Result")
                sell_btn.click(sell_shares, inputs=[sell_symbol, sell_quantity], outputs=sell_result)
            
            with gr.Column():
                portfolio_btn = gr.Button("Get Portfolio Value")
                portfolio_value = gr.Textbox(label="Portfolio Value")
                portfolio_btn.click(get_portfolio_value, inputs=[], outputs=portfolio_value)
                
                profit_btn = gr.Button("Get Profit/Loss")
                profit_value = gr.Textbox(label="Profit/Loss")
                profit_btn.click(get_profit_loss, inputs=[], outputs=profit_value)
                
                holdings_btn = gr.Button("Get Holdings")
                holdings_value = gr.Textbox(label="Holdings", lines=6)
                holdings_btn.click(get_holdings, inputs=[], outputs=holdings_value)
    
    with gr.Tab("Transaction History"):
        transactions_btn = gr.Button("Get Transaction History")
        transactions_value = gr.Textbox(label="Transactions", lines=10)
        transactions_btn.click(get_transactions, inputs=[], outputs=transactions_value)

if __name__ == "__main__":
    demo.launch()