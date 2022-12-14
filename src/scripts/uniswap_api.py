from scripts.utils import LOCAL_CHAIN_ENV, get_account
from scripts.deploy import deploy_dm_actor
from brownie import network, interface, config, UniswapWatcher
import time

def swap_exact_eth_amount_for_token(user_account, token_out, amount_in):
    tx = UniswapWatcher[-1].swapExactETHForTokens(token_out, {"from": user_account, "value": amount_in})


def swap_eth_for_exact_token_amount(user_account, token_out, amount_in):
    weth_token = config['networks'][network.show_active()]['weth_token']
    _, expected_amount_out = UniswapWatcher[-1].getAmountOut(amount_in, weth_token, token_out)
    tx = UniswapWatcher[-1].swapETHForExactTokens(expected_amount_out, token_out, {"from": user_account, "value": amount_in})


def swap_exact_token_amount_for_eth(user_account, token_in, amount_in):
    interface.IERC20(token_in).approve(UniswapWatcher[-1].address, amount_in, {"from": user_account})
    tx = UniswapWatcher[-1].swapExactTokensForETH(amount_in, token_in, {"from": user_account})


def swap_token_for_exact_eth_amount(user_account, token_in, amount_in, slippage):
    weth_token = config['networks'][network.show_active()]['weth_token']
    interface.IERC20(token_in).approve(UniswapWatcher[-1].address, amount_in, {"from": user_account})
    amount_out, new_amount_in = UniswapWatcher[-1].getAmountIn(amount_in, weth_token, token_in)
    tx = UniswapWatcher[-1].swapTokensForExactETH(new_amount_in, slippage * amount_out, token_in, {"from": user_account})


def swap_exact_token_amount_for_token(user_account, token_in, token_out, amount_in):
    interface.IERC20(token_in).approve(UniswapWatcher[-1].address, amount_in, {"from": user_account})
    tx = UniswapWatcher[-1].swapExactTokensForTokens(amount_in, token_in, token_out, {"from": user_account})


def swap_token_for_exact_token_amount(user_account, token_in, token_out, amount_in, slippage):
    interface.IERC20(token_in).approve(UniswapWatcher[-1].address, amount_in, {"from": user_account})
    new_amount_in, amount_out = UniswapWatcher[-1].getAmountOut(amount_in, token_in,  token_out)
    print(new_amount_in / 10**18)
    print(amount_out / 10**18)
    tx = UniswapWatcher[-1].swapTokensForExactTokens(amount_in, slippage * amount_out, token_in, token_out, {"from": user_account})


def main():
    PERSON = get_account()
    UNI_ADDRESS = config['networks'][network.show_active()]['uni_token']
    uni_contract = interface.IERC20(UNI_ADDRESS)
    AMOUNT_IN_ETH = 10**18
    print(UniswapWatcher[-1].address)
    print(f"AMOUNT ETH BEFORE SWAP 1 ETH PER UNI: {PERSON.balance() / 10**18}")
    print(f"AMOUNT UNI BEFORE SWAP 1 ETH PER UNI: {uni_contract.balanceOf(PERSON) / 10**18}")
    swap_exact_eth_amount_for_token(PERSON, UNI_ADDRESS, AMOUNT_IN_ETH)
    time.sleep(2)
    print(f"AMOUNT ETH AFTER SWAP 1 ETH PER UNI: {PERSON.balance() / 10**18}")
    print(f"AMOUNT UNI AFTER SWAP 1 ETH PER UNI: {uni_contract.balanceOf(PERSON) / 10**18}")
    amount_uni_received = uni_contract.balanceOf(PERSON)
    swap_exact_token_amount_for_eth(PERSON, UNI_ADDRESS, amount_uni_received)
    print(f"AMOUNT ETH AFTER SWAP {amount_uni_received} UNI PER ETH: {PERSON.balance() / 10**18}")
    print(f"AMOUNT UNI AFTER SWAP {amount_uni_received} UNI PER ETH: {uni_contract.balanceOf(PERSON) / 10**18}")
