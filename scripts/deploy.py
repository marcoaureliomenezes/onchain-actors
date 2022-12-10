from brownie import UniswapWatcher, config, network
from scripts.utils import get_account

import logging
from web3 import Web3

logging.basicConfig(level='INFO')


def deploy_dm_actor(owner, uniswap_v2_factory):
    is_verified = config["networks"][network.show_active()].get("verify")
    dm_actor_contract = UniswapWatcher.deploy(uniswap_v2_factory, {'from': owner}, publish_source=is_verified)
    return dm_actor_contract


def main():
    owner = get_account()
    factory = config['networks'][network.show_active()]['uniswapV2Factory']
    deploy_dm_actor(owner, factory)