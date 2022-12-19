from scripts.utils import LOCAL_CHAIN_ENV, get_account
from brownie import network, config, UniswapV2DMTransact, interface
from web3 import Web3
import pytest, logging
from scripts.deploy import deploy_uniswap_v2_actor
import subprocess
logging.basicConfig(level='INFO')