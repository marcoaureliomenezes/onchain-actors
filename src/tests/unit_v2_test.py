from scripts.utils import LOCAL_CHAIN_ENV, get_account
from scripts.deploy import deploy_uniswap_v2_actor
from brownie import network, interface, config, UniswapV2DMTransact
import pytest, logging

logging.basicConfig(level='INFO')

@pytest.fixture(scope="module")
def uniswap_watcher():
    if network.show_active() != "mainnet-fork": pytest.skip("only for forked-networks")
    owner = get_account()
    router02 = config['networks'][network.show_active()]['uniswapV2Router02']
    return deploy_uniswap_v2_actor(owner, router02)


@pytest.fixture()
def init_config():
    uni_address = config['networks'][network.show_active()]['uni_token']
    weth_address = config['networks'][network.show_active()]['weth_token']
    uni_eth_price = config['networks'][network.show_active()]['uni_eth_price']
    amount_in = 10**18
    duni_eth_price = interface.IV3AggregatorInterface(uni_eth_price).latestRoundData()[1]
    return uni_address, weth_address, duni_eth_price, amount_in

@pytest.fixture()
def init_balance():
    customer = get_account()
    uni_address = config['networks'][network.show_active()]['uni_token']
    weth_address = config['networks'][network.show_active()]['weth_token']
    balance_eth = customer.balance()
    balance = interface.IERC20(weth_address).balanceOf(customer)
    balance_uni = interface.IERC20(uni_address).balanceOf(customer)
    return customer, balance_eth, balance, balance_uni


@pytest.fixture()
def get_some_uni():
    customer = get_account()
    uni_address = config['networks'][network.show_active()]['uni_token']
    amount_out_min = 1
    _ = UniswapV2DMTransact[-1].swapExactETHForTokens(uni_address, amount_out_min, {"from": customer, "value": 10**18})
    uni_balance = interface.IERC20(uni_address).balanceOf(customer)
    interface.IERC20(uni_address).approve(UniswapV2DMTransact[-1].address, uni_balance, {"from": customer})
    return uni_balance, customer

@pytest.mark.require_network("mainnet-fork")
def test_is_factory_right(uniswap_watcher):
    uniswap_v2_factory = config['networks'][network.show_active()]['uniswapV2Factory']
    assert uniswap_watcher.getFactory() == uniswap_v2_factory


@pytest.mark.require_network("mainnet-fork")
def test_can_calculate_amounts_in(uniswap_watcher):
    uni_eth_pricefeed_address = config['networks'][network.show_active()]['uni_eth_price']
    uni_eth_price = interface.IV3AggregatorInterface(uni_eth_pricefeed_address).latestRoundData()[1]
    uni_address = config['networks'][network.show_active()]['uni_token']
    weth_address = config['networks'][network.show_active()]['weth_token']
    amount_in = 10**18
    uni_eth_swap_price_path = uniswap_watcher.getAmountIn(amount_in, uni_address, weth_address)
    uni_eth_swap_price = (uni_eth_swap_price_path[1] / uni_eth_swap_price_path[0]) * 10 ** 18
    assert uni_eth_price / uni_eth_swap_price > 0.98
    assert uni_eth_price / uni_eth_swap_price < 1.02


@pytest.mark.require_network("mainnet-fork")
def test_can_calculate_amounts_out(uniswap_watcher):
    uni_eth_pricefeed_address = config['networks'][network.show_active()]['uni_eth_price']
    uni_eth_price = interface.IV3AggregatorInterface(uni_eth_pricefeed_address).latestRoundData()[1]
    uni_address = config['networks'][network.show_active()]['uni_token']
    weth_address = config['networks'][network.show_active()]['weth_token']
    amount_in = 10**18
    uni_eth_swap_price_path = uniswap_watcher.getAmountOut(amount_in, uni_address, weth_address)
    uni_eth_swap_price = uni_eth_swap_price_path[1]
    assert uni_eth_price / uni_eth_swap_price > 0.98
    assert uni_eth_price / uni_eth_swap_price < 1.02


@pytest.mark.require_network("mainnet-fork")
def test_can_swap_eth_for_exact_token_amount(uniswap_watcher):
    uni_address = config['networks'][network.show_active()]['uni_token']
    weth_address = config['networks'][network.show_active()]['weth_token']
    uni_eth_pricefeed_address = config['networks'][network.show_active()]['uni_eth_price']
    uni_eth_price = interface.IV3AggregatorInterface(uni_eth_pricefeed_address).latestRoundData()[1]
    customer = get_account()
    eth_balance_before = customer.balance()
    amount_in = 10**18
    uni_balance_before = interface.IERC20(uni_address).balanceOf(customer)
    uni_eth_swap_price_pair = uniswap_watcher.getAmountOut(amount_in, weth_address, uni_address)
    # Executing the swap
    _ = uniswap_watcher.swapETHForExactTokens(uni_eth_swap_price_pair[1], uni_address, {"from": customer, "value": amount_in})
    uni_balance_after = interface.IERC20(uni_address).balanceOf(customer)
    eth_balance_after = customer.balance()
    assert uni_balance_before == 0
    assert customer.balance() == eth_balance_before - amount_in
    assert uni_balance_after > 0.99 * uni_eth_price * (eth_balance_after - eth_balance_before) / 10**18


@pytest.mark.require_network("mainnet-fork")
def test_can_swap_exact_token_amount_for_eth(uniswap_watcher):
    uni_address = config['networks'][network.show_active()]['uni_token']
    customer = get_account()
    uni_balance = interface.IERC20(uni_address).balanceOf(customer)
    _ = interface.IERC20(uni_address).approve(UniswapV2DMTransact[-1].address, uni_balance, {"from": customer})
    amount_out_min = 1
    uni_eth_pricefeed_address = config['networks'][network.show_active()]['uni_eth_price']
    uni_eth_price = interface.IV3AggregatorInterface(uni_eth_pricefeed_address).latestRoundData()[1]
    eth_balance_before = customer.balance()
    _ = uniswap_watcher.swapExactTokensForETH(uni_balance, amount_out_min, uni_address, {"from": customer})
    uni_balance_after = interface.IERC20(uni_address).balanceOf(customer)
    eth_balance_after = customer.balance()
    assert uni_balance_after == 0
    assert eth_balance_after - eth_balance_before > 0.99 * uni_eth_price * uni_balance/ 10**18


@pytest.mark.require_network("mainnet-fork")
def test_can_swap_exact_eth_amount_for_token(uniswap_watcher):
    uni_address = config['networks'][network.show_active()]['uni_token']
    customer = get_account()
    uni_balance_before = interface.IERC20(uni_address).balanceOf(customer)
    amount_out_min = 1
    amount_in = 10**18
    uni_eth_pricefeed_address = config['networks'][network.show_active()]['uni_eth_price']
    uni_eth_price = interface.IV3AggregatorInterface(uni_eth_pricefeed_address).latestRoundData()[1]
    # Executing the swap
    _ = uniswap_watcher.swapExactETHForTokens(uni_address, amount_out_min, {"from": customer, "value": amount_in})
    balance_uni_after_swap = interface.IERC20(uni_address).balanceOf(customer)
    oracle_price_1_eth_uni = 1 / uni_eth_price
    assert uni_balance_before == 0
    #assert customer.balance() == INIT_balance_eth - amount_in
    #assert balance_uni_after_swap > (1 - 0.01) * oracle_price_1_eth_uni




@pytest.mark.require_network("mainnet-fork")
def test_can_swap_token_for_exact_amount_eth(uniswap_watcher, init_config, get_some_uni):
    uni_address, weth_address, duni_eth_price, amount_in = init_config
    uni_balance_before, customer = get_some_uni
    eth_balance_before = customer.balance()
    amount_out, new_amount_in = uniswap_watcher.getAmountIn(uni_balance_before, weth_address, uni_address)
    _ = uniswap_watcher.swapTokensForExactETH(new_amount_in, 0.99 * amount_out, uni_address, {"from": customer})
    uni_balance_after = interface.IERC20(uni_address).balanceOf(customer)
    eth_balance_after = customer.balance()
    assert uni_balance_after == 0
    assert eth_balance_after - eth_balance_before > 0.99 * duni_eth_price * uni_balance_before / 10**18


def test_can_swap_exact_token_for_token(uniswap_watcher, init_config, get_some_uni):
    if network.show_active() != 'mainnet-fork': pytest.skip("only for test-networks")
    uni_address, weth_address, duni_eth_price, _ = init_config
    uni_balance_before, customer = get_some_uni
    amount_out_min = 10*22
    uni_balance_before = interface.IERC20(uni_address).balanceOf(customer)
    weth_balance_before = interface.IERC20(weth_address).balanceOf(customer)
    _ = uniswap_watcher.swapExactTokensForTokens(uni_balance_before, amount_out_min, uni_address, weth_address, {"from": customer})
    uni_balance_after = interface.IERC20(uni_address).balanceOf(customer)
    weth_balance_after = interface.IERC20(weth_address).balanceOf(customer)
    assert uni_balance_after == 0
    assert weth_balance_after - weth_balance_before > 0.99 * duni_eth_price * uni_balance_before / 10**18


@pytest.mark.require_network("mainnet-fork")
def test_can_swap_token_for_exact_token(uniswap_watcher, init_config, get_some_uni):
    if network.show_active() != 'mainnet-fork': pytest.skip("only for test-networks")
    uni_address, weth_address, duni_eth_price, _ = init_config
    uni_balance_before, customer = get_some_uni
    uni_balance_before = interface.IERC20(uni_address).balanceOf(customer)
    weth_balance_before = interface.IERC20(weth_address).balanceOf(customer)
    new_amount_in, amount_out = UniswapV2DMTransact[-1].getAmountOut(uni_balance_before, uni_address,  weth_address)
    _ = uniswap_watcher.swapTokensForExactTokens(new_amount_in, new_amount_in, amount_out, uni_address, weth_address, {"from": customer})
    uni_balance_after = interface.IERC20(uni_address).balanceOf(customer)
    weth_balance_after = interface.IERC20(weth_address).balanceOf(customer)
    assert uni_balance_after == 0
    assert weth_balance_after - weth_balance_before > 0.99 * duni_eth_price * uni_balance_before / 10**18