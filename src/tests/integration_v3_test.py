from scripts.utils import LOCAL_CHAIN_ENV, get_account
from brownie import network, config, UniswapV3DMTransact, interface
from scripts.uniswap_api_v2 import *
import pytest, logging
from scripts.deploy import deploy_uniswap_v3_actor

logging.basicConfig(level='INFO')


# def test_can_wrap_and_unwrap_ether():
#     if network.show_active() not in ["goerli", "mainnet-fork"]: pytest.skip("only for test-networks")
#     PERSON = get_account()
#     WETH_ADDRESS = config['networks'][network.show_active()]['weth_token']
#     AMOUNT_IN_ETH = 10**18
#     weth_contract = interface.IERC20(WETH_ADDRESS)
#     eth_balance_before = PERSON.balance()
#     weth_balance_before = weth_contract.balanceOf(PERSON)
#     interface.IERC20(WETH_ADDRESS).deposit({"from": PERSON, "value": AMOUNT_IN_ETH})
#     eth_balance_after = PERSON.balance()
#     weth_balance_after = weth_contract.balanceOf(PERSON)
#     assert weth_balance_before == 0 
#     assert eth_balance_before == eth_balance_after + weth_balance_after
    
    
# def test_can_swap_and_unswap_tokens():
#     if network.show_active() not in ["goerli"]: pytest.skip("only for test-networks")
#     ROUTER03 = config['networks'][network.show_active()]['uniswapV3Router']
#     WETH_ADDRESS = config['networks'][network.show_active()]['weth_token']
#     UNI_ADDRESS  = config['networks'][network.show_active()]['uni_token']
#     AMOUNT_IN_ETH = 10**18
#     FEE = 3000
#     PERSON = get_account()
#     weth_contract = interface.IERC20(WETH_ADDRESS)
#     uni_contract = interface.IERC20(UNI_ADDRESS)

#     # SWAP ETH FOR WETH
#     print(f"Balance of ETH Before deposit ETH to get WETH: {PERSON.balance()}")
#     print(f"Balance of WETH Before deposit ETH to get WETH: {weth_contract.balanceOf(PERSON)}")
#     print(f"Balance of UNI Before deposit ETH to get WETH: {uni_contract.balanceOf(PERSON)}")
#     interface.IERC20(WETH_ADDRESS).deposit({"from": PERSON, "value": AMOUNT_IN_ETH})
    
#     print(f"Balance of ETH before 1º SWAP: {PERSON.balance()}")
#     print(f"Balance of WETH before 1º SWAP: {weth_contract.balanceOf(PERSON)}")
#     print(f"Balance of UNI before 1º SWAP: {uni_contract.balanceOf(PERSON)}")
#     swap_v3_1(PERSON, WETH_ADDRESS, UNI_ADDRESS, AMOUNT_IN_ETH, FEE)





