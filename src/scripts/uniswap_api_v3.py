from scripts.utils import LOCAL_CHAIN_ENV, get_account
from scripts.deploy import deploy_uniswap_v3_actor
from brownie import network, interface, config, UniswapV3DMTransact


def wrap_native_token(amount):
    customer = get_account()
    WETH_ADDRESS = UniswapV3DMTransact[-1].WETH9()
    weth_contract = interface.IERC20(WETH_ADDRESS)
    weth_contract.deposit({"from": customer, "value": amount})

   
def unwrap_native_token(amount):
    customer = get_account()
    WETH_ADDRESS = UniswapV3DMTransact[-1].WETH9()
    weth_contract = interface.IERC20(WETH_ADDRESS)
    weth_contract.withdraw(amount, {"from": customer})


def swap_exact_input_single(amount_in, token_in, token_out, fee):
    customer = get_account()
    interface.IERC20(token_in).approve(UniswapV3DMTransact[-1].address, amount_in, {"from": customer})
    tx = UniswapV3DMTransact[-1].swapExactInputSingle(amount_in, token_in, token_out, fee, {"from": customer})


def swap_exact_output_single(amount_out, token_in, token_out, amount_in_max, fee):
    customer = get_account()
    interface.IERC20(token_in).approve(UniswapV3DMTransact[-1].address, amount_in_max, {"from": customer})
    tx = UniswapV3DMTransact[-1].swapExactOutputSingle(amount_out, amount_in_max, token_in, token_out, fee, {"from": customer})


def deploy_uniswap_v3_interaction():
    person = get_account()
    router03 = config['networks'][network.show_active()]['uniswapV3Router']
    deploy_uniswap_v3_actor(person, router03)


def main():
    pass