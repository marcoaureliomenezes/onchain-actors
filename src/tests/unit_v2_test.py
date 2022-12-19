from scripts.utils import LOCAL_CHAIN_ENV, get_account
from scripts.deploy import deploy_uniswap_v2_actor
from brownie import network, interface, config, UniswapV2DMTransact
import pytest, logging

logging.basicConfig(level='INFO')

@pytest.fixture
def uniswap_watcher():
    if network.show_active() != "mainnet-fork": pytest.skip("only for forked-networks")
    owner = get_account()
    router02 = config['networks'][network.show_active()]['uniswapV2Router02']
    return deploy_uniswap_v2_actor(owner, router02)


@pytest.fixture
def init_config():
    UNI_TOKEN = config['networks'][network.show_active()]['uni_token']
    WETH_TOKEN = config['networks'][network.show_active()]['weth_token']
    UNI_ETH_ORACLE_ADDRESS = config['networks'][network.show_active()]['uni_eth_price']
    AMOUNT_IN = 10**18
    UNI_ETH_PRICE = interface.IV3AggregatorInterface(UNI_ETH_ORACLE_ADDRESS).latestRoundData()[1]
    return UNI_TOKEN, WETH_TOKEN, UNI_ETH_PRICE, AMOUNT_IN

@pytest.fixture
def init_balance():
    PERSON = get_account()
    UNI_TOKEN = config['networks'][network.show_active()]['uni_token']
    WETH_TOKEN = config['networks'][network.show_active()]['weth_token']
    BALANCE_ETH = PERSON.balance()
    BALANCE_WETH = interface.IERC20(WETH_TOKEN).balanceOf(PERSON)
    BALANCE_UNI = interface.IERC20(UNI_TOKEN).balanceOf(PERSON)
    return PERSON, BALANCE_ETH, BALANCE_WETH, BALANCE_UNI


@pytest.fixture
def get_some_uni():
    PERSON = get_account()
    UNI_TOKEN = config['networks'][network.show_active()]['uni_token']
    AMOUNT_OUT_MIN = 1
    tx = UniswapV2DMTransact[-1].swapExactETHForTokens(UNI_TOKEN, AMOUNT_OUT_MIN, {"from": PERSON, "value": 10**18})
    uni_balance = interface.IERC20(UNI_TOKEN).balanceOf(PERSON)
    interface.IERC20(UNI_TOKEN).approve(UniswapV2DMTransact[-1].address, uni_balance, {"from": PERSON})
    return uni_balance, PERSON



def test_is_factory_right(uniswap_watcher):
    if network.show_active() != "mainnet-fork": pytest.skip("only for forked-networks")
    uniswap_v2_factory = config['networks'][network.show_active()]['uniswapV2Factory']
    assert uniswap_watcher.getFactory() == uniswap_v2_factory


# tests if actual price of UNI-WETH given 1 UNI.
def test_can_calculate_amounts_in(uniswap_watcher, init_config):
    if network.show_active() != "mainnet-fork": pytest.skip("only for forked-networks")
    UNI_TOKEN, WETH_TOKEN, UNI_ETH_PRICE, AMOUNT_IN = init_config
    uni_eth_swap_price_path = uniswap_watcher.getAmountIn(AMOUNT_IN, UNI_TOKEN, WETH_TOKEN)
    uni_eth_swap_price = (uni_eth_swap_price_path[1] / uni_eth_swap_price_path[0]) * 10 ** 18
    assert UNI_ETH_PRICE / uni_eth_swap_price > 0.98
    assert UNI_ETH_PRICE / uni_eth_swap_price < 1.02


# tests if actual price of UNI-WETH given 1 UNI.
def test_can_calculate_amounts_out(uniswap_watcher, init_config):
    if network.show_active() != "mainnet-fork": pytest.skip("only for forked-networks")
    UNI_TOKEN, WETH_TOKEN, UNI_ETH_PRICE, AMOUNT_IN = init_config
    uni_eth_swap_price_path = uniswap_watcher.getAmountOut(AMOUNT_IN, UNI_TOKEN, WETH_TOKEN)
    uni_eth_swap_price = uni_eth_swap_price_path[1]
    assert UNI_ETH_PRICE / uni_eth_swap_price > 0.98
    assert UNI_ETH_PRICE / uni_eth_swap_price < 1.02


# test can swap exact amount of ther per token successfully.
def test_can_swap_exact_eth_amount_for_token(uniswap_watcher, init_config, init_balance):
    if network.show_active() not in ["mainnet-fork"]: pytest.skip("only for test-networks")
    UNI_TOKEN, _, UNI_ETH_PRICE, AMOUNT_IN = init_config
    PERSON, INIT_BALANCE_ETH, _, INIT_BALANCE_UNI = init_balance
    AMOUNT_OUT_MIN = 1
    # Executing the swap
    tx = uniswap_watcher.swapExactETHForTokens(UNI_TOKEN, AMOUNT_OUT_MIN, {"from": PERSON, "value": AMOUNT_IN})
    balance_uni_after_swap = interface.IERC20(UNI_TOKEN).balanceOf(PERSON)
    oracle_price_1_eth_uni = 1 / UNI_ETH_PRICE
    assert INIT_BALANCE_UNI == 0
    assert PERSON.balance() == INIT_BALANCE_ETH - AMOUNT_IN
    assert balance_uni_after_swap > (1 - 0.01) * oracle_price_1_eth_uni


def test_can_swap_eth_for_exact_token_amount(uniswap_watcher, init_config, init_balance): 
    if network.show_active() not in ["mainnet-fork"]: pytest.skip("only for test-networks")
    PERSON, INIT_BALANCE_ETH, _, INIT_BALANCE_UNI = init_balance
    UNI_TOKEN, WETH_TOKEN, UNI_ETH_PRICE, AMOUNT_IN = init_config
    uni_eth_swap_price_pair = uniswap_watcher.getAmountOut(AMOUNT_IN, WETH_TOKEN, UNI_TOKEN)
    # Executing the swap
    tx = uniswap_watcher.swapETHForExactTokens(uni_eth_swap_price_pair[1], UNI_TOKEN, {"from": PERSON, "value": AMOUNT_IN})
    oracle_price_1_eth_uni = 1 / UNI_ETH_PRICE
    balance_uni_after_swap = interface.IERC20(UNI_TOKEN).balanceOf(PERSON)
    assert INIT_BALANCE_UNI == 0
    assert PERSON.balance() == INIT_BALANCE_ETH - AMOUNT_IN
    assert balance_uni_after_swap > (1 - 0.01) * oracle_price_1_eth_uni


def test_can_swap_exact_token_amount_for_eth(uniswap_watcher, init_config, get_some_uni):
    if network.show_active() not in["mainnet-fork"]: pytest.skip("only for test-networks")
    UNI_TOKEN, _, UNI_ETH_PRICE, _ = init_config
    uni_balance_before, PERSON = get_some_uni
    eth_balance_before = PERSON.balance()
    tx = uniswap_watcher.swapExactTokensForETH(uni_balance_before, 1, UNI_TOKEN, {"from": PERSON})
    uni_balance_after = interface.IERC20(UNI_TOKEN).balanceOf(PERSON)
    eth_balance_after = PERSON.balance()
    assert uni_balance_after == 0
    assert eth_balance_after - eth_balance_before > 0.99 * UNI_ETH_PRICE * uni_balance_before / 10**18



def test_can_swap_token_for_exact_amount_eth(uniswap_watcher, init_config, get_some_uni):
    if network.show_active() not in["mainnet-fork"]: pytest.skip("only for test-networks")
    UNI_TOKEN, WETH_TOKEN, UNI_ETH_PRICE, AMOUNT_IN = init_config
    uni_balance_before, PERSON = get_some_uni
    eth_balance_before = PERSON.balance()
    amount_out, new_amount_in = uniswap_watcher.getAmountIn(uni_balance_before, WETH_TOKEN, UNI_TOKEN)
    tx = uniswap_watcher.swapTokensForExactETH(uni_balance_before, 0.99 * amount_out, UNI_TOKEN, {"from": PERSON})
    uni_balance_after = interface.IERC20(UNI_TOKEN).balanceOf(PERSON)
    eth_balance_after = PERSON.balance()
    assert uni_balance_after == 0
    assert eth_balance_after - eth_balance_before > 0.99 * UNI_ETH_PRICE * uni_balance_before / 10**18


def test_can_swap_exact_token_for_token(uniswap_watcher, init_config, get_some_uni):
    if network.show_active() not in["mainnet-fork"]: pytest.skip("only for test-networks")
    UNI_TOKEN, WETH_TOKEN, UNI_ETH_PRICE, _ = init_config
    uni_balance_before, PERSON = get_some_uni
    amount_out_min = 10*22
    uni_balance_before = interface.IERC20(UNI_TOKEN).balanceOf(PERSON)
    weth_balance_before = interface.IERC20(WETH_TOKEN).balanceOf(PERSON)
    tx = uniswap_watcher.swapExactTokensForTokens(uni_balance_before, amount_out_min, UNI_TOKEN, WETH_TOKEN, {"from": PERSON})
    uni_balance_after = interface.IERC20(UNI_TOKEN).balanceOf(PERSON)
    weth_balance_after = interface.IERC20(WETH_TOKEN).balanceOf(PERSON)
    assert uni_balance_after == 0
    assert weth_balance_after - weth_balance_before > 0.99 * UNI_ETH_PRICE * uni_balance_before / 10**18


def test_can_swap_token_for_exact_token(uniswap_watcher, init_config, get_some_uni):
    if network.show_active() not in["mainnet-fork"]: pytest.skip("only for test-networks")
    UNI_TOKEN, WETH_TOKEN, UNI_ETH_PRICE, _ = init_config
    uni_balance_before, PERSON = get_some_uni
    uni_balance_before = interface.IERC20(UNI_TOKEN).balanceOf(PERSON)
    weth_balance_before = interface.IERC20(WETH_TOKEN).balanceOf(PERSON)
    new_amount_in, amount_out = UniswapV2DMTransact[-1].getAmountOut(uni_balance_before, UNI_TOKEN,  WETH_TOKEN)
    tx = uniswap_watcher.swapTokensForExactTokens(1 * new_amount_in, new_amount_in, 1 * amount_out, UNI_TOKEN, WETH_TOKEN, {"from": PERSON})
    uni_balance_after = interface.IERC20(UNI_TOKEN).balanceOf(PERSON)
    weth_balance_after = interface.IERC20(WETH_TOKEN).balanceOf(PERSON)
    assert uni_balance_after == 0
    assert weth_balance_after - weth_balance_before > 0.99 * UNI_ETH_PRICE * uni_balance_before / 10**18