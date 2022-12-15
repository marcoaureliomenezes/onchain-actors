from scripts.utils import LOCAL_CHAIN_ENV, get_account, get_chainlink_price
from scripts.deploy import deploy_uniswap_v2_actor
from brownie import network, exceptions, config, UniswapV2DMTransact
from web3 import Web3
import pytest, logging

logging.basicConfig(level='INFO')

@pytest.fixture
def uniswap_watcher():
    if network.show_active() != "mainnet-fork": pytest.skip("only for forked-networks")
    owner = get_account()
    router02 = config['networks'][network.show_active()]['uniswapV2Router02']
    return deploy_uniswap_v2_actor(owner, router02)


def test_is_factory_right(uniswap_watcher):
    if network.show_active() != "mainnet-fork": pytest.skip("only for forked-networks")
    uniswap_v2_factory = config['networks'][network.show_active()]['uniswapV2Factory']
    assert UniswapV2DMTransact[-1].getFactory() == uniswap_v2_factory


# tests if actual price of UNI-WETH given 1 UNI.
def test_can_calculate_amounts_in(uniswap_watcher):
    if network.show_active() != "mainnet-fork": pytest.skip("only for forked-networks")
    uni_token = config['networks'][network.show_active()]['uni_token']
    weth_token = config['networks'][network.show_active()]['weth_token']
    uni_eth_oracle_price = get_chainlink_price().latestRoundData()[1] / 10**18
    uni_eth_swap_price_path = UniswapV2DMTransact[-1].getAmountIn(10**18, uni_token, weth_token)
    uni_eth_swap_price = uni_eth_swap_price_path[1] / uni_eth_swap_price_path[0]
    assert uni_eth_oracle_price / uni_eth_swap_price > 0.9
    assert uni_eth_oracle_price / uni_eth_swap_price < 1.01


# tests if actual price of UNI-WETH given 1 UNI.
def test_can_calculate_amounts_out(uniswap_watcher):
    if network.show_active() != "mainnet-fork": pytest.skip("only for forked-networks")
    uni_token = config['networks'][network.show_active()]['uni_token']
    weth_token = config['networks'][network.show_active()]['weth_token']
    uni_eth_oracle_price = get_chainlink_price().latestRoundData()[1] / 10**18
    uni_eth_swap_price_path = UniswapV2DMTransact[-1].getAmountOut(10**18, uni_token, weth_token)
    uni_eth_swap_price = uni_eth_swap_price_path[1] / uni_eth_swap_price_path[0]
    assert uni_eth_oracle_price / uni_eth_swap_price > 0.9
    assert uni_eth_oracle_price / uni_eth_swap_price < 1.01



