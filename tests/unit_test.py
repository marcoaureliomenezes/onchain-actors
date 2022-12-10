from scripts.utils import LOCAL_CHAIN_ENV, get_account, get_chainlink_price
from scripts.deploy import deploy_dm_actor
from brownie import network, exceptions, interface, config, UniswapWatcher
from web3 import Web3
import pytest, logging

logging.basicConfig(level='INFO')

@pytest.fixture
def uniswap_watcher():
    owner = get_account()
    factory = config['networks'][network.show_active()]['uniswapV2Factory']
    return deploy_dm_actor(owner, factory)


def test_is_factory_right():
    assert config['networks'][network.show_active()]['uniswapV2Factory'] == UniswapWatcher[-1].factory()


def test_is_getting_uniswap_pair_address(uniswap_watcher):
    uni_token = config['networks'][network.show_active()]['uni_token']
    weth_token = config['networks'][network.show_active()]['weth_token']
    address_uniswap_pair = UniswapWatcher[-1].getPairAddress(uni_token, weth_token)
    uniswap_pair_contract = interface.IUniswapV2Pair(address_uniswap_pair)
    assert uniswap_pair_contract.symbol() == 'UNI-V2'
     

def test_is_exceptions_right_getting_uniswap_pair_address_wrongly(uniswap_watcher):
    uni_token = config['networks'][network.show_active()]['uni_token']
    with pytest.raises(exceptions.VirtualMachineError):
        _ = UniswapWatcher[-1].getPairAddress(uni_token, uni_token)


def test_can_quote_token_exchange(uniswap_watcher):
    uni_token = config['networks'][network.show_active()]['uni_token']
    weth_token = config['networks'][network.show_active()]['weth_token']
    uni_eth_price = get_chainlink_price().latestRoundData()[1] / 10**18
    uniswap_price = UniswapWatcher[-1].quotePair(10**18, uni_token, weth_token) / 10 ** 18
    assert uniswap_price / uni_eth_price > 0.9
    assert uniswap_price / uni_eth_price < 1.1


def test_can_quote_token_exchange2(uniswap_watcher):
    uni_token = config['networks'][network.show_active()]['uni_token']
    weth_token = config['networks'][network.show_active()]['weth_token']
    uni_eth_price = get_chainlink_price().latestRoundData()[1] / 10**18
    eth_uni_uniswap_price = UniswapWatcher[-1].quotePair(10**18, weth_token, uni_token) / 10 ** 18
    assert (1 / eth_uni_uniswap_price) / uni_eth_price > 0.9
    assert (1 / eth_uni_uniswap_price) / uni_eth_price < 1.1
