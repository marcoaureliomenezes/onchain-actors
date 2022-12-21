from scripts.utils import LOCAL_CHAIN_ENV, get_account
from scripts.deploy import deploy_uniswap_v2_actor
from brownie import network, interface, config, UniswapV2DMTransact
import time





def swap_exact_eth_amount_for_token(amount_in, token_out):
    """ METHOD: swap_exact_eth_amount_for_token
    PARM 1: certain amount of ether user will spend to perform the swap.
    PARM 2: token address which user will receive after swap.
    The swap occurs.
    """
    user_account = get_account()
    amount_out_min = 1
    tx = UniswapV2DMTransact[-1].swapExactETHForTokens(token_out, amount_out_min, {"from": user_account, "value": amount_in})


def swap_exact_token_amount_for_eth(amount_in, token_in):
    """ METHOD: swap_exact_token_amount_for_eth
    PARM 1: certain amount of ether user will spend to perform the swap.
    PARM 2: token address which user will receive after swap.
    Approve to spend the amount of ERC20 TokenIn to be spend.
    The swap occurs.
    """
    user_account = get_account()
    amount_out_min = 1
    interface.IERC20(token_in).approve(UniswapV2DMTransact[-1].address, amount_in, {"from": user_account})
    tx = UniswapV2DMTransact[-1].swapExactTokensForETH(amount_in, amount_out_min, token_in, {"from": user_account})


def swap_eth_for_exact_token_amount(amount_out, token_out):
    """ METHOD: swap_eth_for_exact_token_amount
    PARM 1: certain amount of ether user will receive after perform the swap.
    PARM 2: token address which user will receive after swap.
    Calculates the swap amounts.
    The swap occurs.
    """
    user_account = get_account()
    weth_token = config['networks'][network.show_active()]['weth_token']
    amount_in, expected_amount_out = UniswapV2DMTransact[-1].getAmountIn(amount_out, weth_token, token_out)
    tx = UniswapV2DMTransact[-1].swapETHForExactTokens(amount_out, token_out, {"from": user_account, "value": amount_in})


def swap_token_for_exact_eth_amount(amount_out, token_in):
    """ METHOD: swap_token_for_exact_eth_amount
    PARM 1: certain amount of ether user will receive after perform the swap.
    PARM 2: token address which user will spend to make the swap.
    Calculates the swap amounts.
    Approve to spend the amount of ERC20 TokenIn to be spend.
    The swap occurs.
    """
    user_account = get_account()
    weth_token = config['networks'][network.show_active()]['weth_token']
    amount_in, amount_out = UniswapV2DMTransact[-1].getAmountIn(amount_out, token_in, weth_token)
    amount_in_max = 10**21
    interface.IERC20(token_in).approve(UniswapV2DMTransact[-1].address, amount_in, {"from": user_account})
    tx = UniswapV2DMTransact[-1].swapTokensForExactETH(amount_in, amount_in_max, amount_out, token_in, {"from": user_account})


def swap_exact_token_amount_for_token(amount_in, token_in, token_out):
    """ METHOD: swap_exact_token_amount_for_token
    PARM 1: certain amount of ether user will spend to perform the swap.
    PARM 2: token address which user will spend to make the swap.
    PARM 3: token address which user will receive after swap.
    Approve to spend the amount of ERC20 TokenIn to be spend.
    The swap occurs.
    """
    user_account = get_account()
    amount_out_min = 1
    interface.IERC20(token_in).approve(UniswapV2DMTransact[-1].address, amount_in, {"from": user_account})
    tx = UniswapV2DMTransact[-1].swapExactTokensForTokens(amount_in, amount_out_min, token_in, token_out, {"from": user_account})


def swap_token_for_exact_token_amount(amount_out, token_in, token_out):
    """ METHOD: swap_token_for_exact_token_amount
    PARM 1: certain amount of ether user will receive after perform the swap.
    PARM 2: token address which user will spend to make the swap.
    PARM 3: token address which user will receive after swap.
    Calculates the swap amounts.
    Approve to spend the amount of ERC20 TokenIn to be spend.
    The swap occurs.
    """
    user_account = get_account()
    amount_in_max = 10**21
    amount_in, amount_out = UniswapV2DMTransact[-1].getAmountIn(amount_out, token_in,  token_out)
    interface.IERC20(token_in).approve(UniswapV2DMTransact[-1].address, amount_in, {"from": user_account})
    tx = UniswapV2DMTransact[-1].swapTokensForExactTokens(amount_in, amount_in_max, amount_out, token_in, token_out, {"from": user_account})


def main():
    owner = get_account()


    WETH_ADDRESS = config['networks'][network.show_active()]['weth_token']
    print(interface.IERC20(WETH_ADDRESS).balanceOf(owner))

