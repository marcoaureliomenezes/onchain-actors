from scripts.utils import LOCAL_CHAIN_ENV, get_account, get_chainlink_price
from brownie import network, config, UniswapWatcher, interface
from web3 import Web3
import pytest, logging
from scripts.deploy import deploy_dm_actor

logging.basicConfig(level='INFO')

@pytest.fixture
def uniswap_watcher():
    if network.show_active() != "mainnet-fork": pytest.skip("only for forked-networks")
    owner = get_account()
    router02 = config['networks'][network.show_active()]['uniswapV2Router02']
    return deploy_dm_actor(owner, router02)


def test_can_swap_exact_eth_amount_for_token(uniswap_watcher):
    if network.show_active() not in["goerli", "mainnet-fork"]: pytest.skip("only for test-networks")
    uni_token = config['networks'][network.show_active()]['uni_token']
    PERSON = get_account()
    logging.info(f"Balance of UNI before SWAP: {interface.IERC20(uni_token).balanceOf(PERSON) / 10**18}")
    yx = UniswapWatcher[-1].swapExactETHForTokens(uni_token, {"from": PERSON, "value": 10**18})
    logging.info(f"Balance of UNI after SWAP: {interface.IERC20(uni_token).balanceOf(PERSON) / 10**18}")

    

def test_can_swap_eth_for_exact_token_amount(uniswap_watcher): 
    if network.show_active() not in["goerli", "mainnet-fork"]: pytest.skip("only for test-networks")
    uni_token = config['networks'][network.show_active()]['uni_token']
    weth_token = config['networks'][network.show_active()]['weth_token']
    PERSON = get_account()
    uni_eth_swap_price_path = UniswapWatcher[-1].getAmountOut(10**18, weth_token, uni_token)
    uni_eth_swap_price = uni_eth_swap_price_path[1] / uni_eth_swap_price_path[0]
    logging.info(f"Balance of UNI before SWAP: {interface.IERC20(uni_token).balanceOf(PERSON) / 10**18}")
    tx = UniswapWatcher[-1].swapETHForExactTokens(uni_eth_swap_price_path[1], uni_token, {"from": PERSON, "value": 1*10**18})
    logging.info(f"Balance of UNI after SWAP: {interface.IERC20(uni_token).balanceOf(PERSON) / 10**18}")


def test_can_swap_exact_token_amount_for_eth(uniswap_watcher):
    if network.show_active() not in["goerli", "mainnet-fork"]: pytest.skip("only for test-networks")
    uni_token = config['networks'][network.show_active()]['uni_token']
    PERSON = get_account()
    tx = UniswapWatcher[-1].swapExactETHForTokens(uni_token, {"from": PERSON, "value": 10**18})
    amount_uni_received = interface.IERC20(uni_token).balanceOf(PERSON)
    print(f"Balance of UNI token before swap UNI to ETH: {amount_uni_received / 10**18}")
    tx2 = UniswapWatcher[-1].swapExactTokensForETH(amount_uni_received, uni_token, {"from": PERSON})
    amount_uni_received = interface.IERC20(uni_token).balanceOf(PERSON)
    print(f"Balance of UNI token before swap UNI to ETH: {amount_uni_received / 10**18}")


def test_can_swap4(uniswap_watcher): 
    pass


