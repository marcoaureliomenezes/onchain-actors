from scripts.utils import LOCAL_CHAIN_ENV, get_account
from scripts.deploy import deploy_uniswap_v3_actor
from brownie import network, interface, config, UniswapV3DMTransact
import time




def swap_exact_input_single(user_account, token_in, token_out, amount_in, fee):
    interface.IERC20(token_in).approve(UniswapV3DMTransact[-1].address, amount_in, {"from": user_account})
    tx = UniswapV3DMTransact[-1].swapExactInputSingle(amount_in, token_in, token_out, fee, {"from": user_account})


def swap_exact_input_single(user_account, token_in, token_out, amount_out, amount_in_max, fee):
    interface.IERC20(token_in).approve(UniswapV3DMTransact[-1].address, amount_in, {"from": user_account})
    tx = UniswapV3DMTransact[-1].swapExactOutputSingle(amount_out, amount_in_max, token_in, token_out, fee, {"from": user_account})

def main():
    WETH_ADDRESS = config['networks'][network.show_active()]['weth_token']
    UNI_ADDRESS  = config['networks'][network.show_active()]['uni_token']
    weth_contract = interface.IERC20(WETH_ADDRESS)
    uni_contract = interface.IERC20(UNI_ADDRESS)
    AMOUNT_IN_ETH = 10**18
    FEE = 3000
    PERSON = get_account()
    ROUTER03 = config['networks'][network.show_active()]['uniswapV3Router']
    deploy_uniswap_v3_actor(PERSON, ROUTER03)

    # SWAP ETH FOR WETH
    print(f"Balance of ETH Before deposit ETH to get WETH: {PERSON.balance()}")
    print(f"Balance of WETH Before deposit ETH to get WETH: {weth_contract.balanceOf(PERSON)}")
    print(f"Balance of UNI Before deposit ETH to get WETH: {uni_contract.balanceOf(PERSON)}")
    interface.IERC20(WETH_ADDRESS).deposit({"from": PERSON, "value": AMOUNT_IN_ETH})
    
    print(f"Balance of ETH before 1º SWAP: {PERSON.balance()}")
    print(f"Balance of WETH before 1º SWAP: {weth_contract.balanceOf(PERSON)}")
    print(f"Balance of UNI before 1º SWAP: {uni_contract.balanceOf(PERSON)}")
    swap_exact_input_single(PERSON, WETH_ADDRESS, UNI_ADDRESS, AMOUNT_IN_ETH, FEE)

    print(f"Balance of ETH after 1º SWAP: {PERSON.balance()}")
    print(f"Balance of WETH after 1º SWAP: {weth_contract.balanceOf(PERSON)}")
    print(f"Balance of UNI after 1º SWAP: {uni_contract.balanceOf(PERSON)}")

    swap_exact_input_single(PERSON, UNI_ADDRESS, WETH_ADDRESS, uni_contract.balanceOf(PERSON), FEE)
    interface.IERC20(WETH_ADDRESS).withdraw(weth_contract.balanceOf(PERSON), {"from": PERSON})

    print(f"Balance of ETH after 2º SWAP: {PERSON.balance()}")
    print(f"Balance of WETH after 2º SWAP: {weth_contract.balanceOf(PERSON)}")
    print(f"Balance of UNI after 2º SWAP: {uni_contract.balanceOf(PERSON)}")