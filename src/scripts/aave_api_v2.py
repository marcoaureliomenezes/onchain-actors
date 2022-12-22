from brownie import network, config, interface
from scripts.utils import get_account, get_user_data
from web3 import Web3
import logging


ACTIVE_NETWORK = config["networks"][network.show_active()]
logging.basicConfig(level='INFO')


def approve_erc20(amount, spender, erc20_address, account):
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {'from': account})
    return tx


def get_aave_pool_contract():
    aave_pool_address_provider_address = config['networks'][network.show_active()]['lendingPoolAddressProvider']
    provider_contract = interface.ILendingPoolAddressesProvider(aave_pool_address_provider_address)
    aave_contract_address = provider_contract.getLendingPool()
    aave_contract = interface.ILendingPool(aave_contract_address)
    return aave_contract


def supply_asset(token, amount):
    user_account = get_account()
    aave_contract = get_aave_pool_contract()
    approve_erc20(amount, aave_contract.address, token, user_account)
    tx = aave_contract.deposit(token, amount, user_account.address, 0, {'from': user_account})
    return tx


def withdraw_asset(token, amount):
    user_account = get_account()
    aave_contract = get_aave_pool_contract()
    approve_erc20(amount, aave_contract.address, token, user_account)
    tx = aave_contract.withdraw(token, amount, user_account.address, {'from': user_account})
    return tx


def borrow_asset(token, amount):
    user_account = get_account()
    aave_contract = get_aave_pool_contract()
    tx = aave_contract.borrow(token, amount, 1, 0, user_account.address, {'from': user_account})
    return


def repay_asset(token, amount):
    user_account = get_account()
    aave_contract = get_aave_pool_contract()
    approve_erc20(amount,aave_contract, token, user_account)
    tx = aave_contract.repay(token, amount, 1, user_account, {'from': user_account})


def get_user_data_farm():
    user_account = get_account()
    aave_contract = get_aave_pool_contract()

    return get_user_data(aave_contract, user_account)

def main():

    #tx = supply_asset("0xCCa7d1416518D095E729904aAeA087dBA749A4dC", 100000000000000000)
    #tx = withdraw_asset("0xCCa7d1416518D095E729904aAeA087dBA749A4dC", 2100000000000000000)
    # para pegar emprestado ver o quanto é possivel e o quanto tem disponivel
    #amount_stable_coins_to_borrow = int(get_user_data_farm()['available_borrow_eth'])
    #tx = borrow_asset("0x75Ab5AB1Eef154C0352Fc31D2428Cef80C7F8B33", 238000000000000000000)

    # para pegar emprestado ver o quanto é possivel e o quanto tem disponivel
    amount_stable_coins_to_pay = int(get_user_data_farm()['total_debt_eth'])
    tx = repay_asset("0x75Ab5AB1Eef154C0352Fc31D2428Cef80C7F8B33", amount_stable_coins_to_pay)
    #print(tx)