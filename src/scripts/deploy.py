from brownie import UniswapV2DMTransact, UniswapV3DMTransact, config, network
from scripts.utils import get_account

import logging
from web3 import Web3

logging.basicConfig(level='INFO')


def deploy_uniswap_v2_actor(owner, uniswap_v2_router):
    is_verified = config["networks"][network.show_active()].get("verify")
    dm_actor_contract = UniswapV2DMTransact.deploy(uniswap_v2_router, {'from': owner}, publish_source=is_verified)
    return dm_actor_contract


def deploy_uniswap_v3_actor(owner, uniswap_v3_router):
    is_verified = config["networks"][network.show_active()].get("verify")
    dm_actor_contract = UniswapV3DMTransact.deploy(uniswap_v3_router, {'from': owner}, publish_source=is_verified)
    return dm_actor_contract


def main():
    owner = get_account()
    router02 = config['networks'][network.show_active()]['uniswapV2Router02']
    router03 = config['networks'][network.show_active()]['uniswapV3Router']

    deploy_uniswap_v3_actor(owner, router03)