from brownie import network, accounts, config, interface

NON_FORKED_LOCAL_CHAIN = ["development", "ganache-dadaia"]
FORKED_LOCAL_CHAIN = ["mainnet-fork"]
LOCAL_CHAIN_ENV = NON_FORKED_LOCAL_CHAIN + FORKED_LOCAL_CHAIN


def get_account(**kwargs):
    is_local = network.show_active() in LOCAL_CHAIN_ENV
    if is_local and kwargs.get('index'): return accounts[kwargs["index"]]
    elif is_local and not kwargs.get('index'): return accounts[0]
    elif not is_local and kwargs.get("id"): return accounts.load(kwargs["id"])
    else: return accounts.add(config["wallets"]["from_key"])


def get_eth_price():
    pricefeed_eth_uds_address = config["networks"][network.show_active()][f'eth_usd']
    oracle_eth_usd = interface.IV3AggregatorInterface(pricefeed_eth_uds_address)
    price_eth_usd = oracle_eth_usd.latestRoundData()[1] / 10**oracle_eth_usd.decimals()
    return price_eth_usd


def get_user_data(lending_pool, account):
    user_data = lending_pool.getUserAccountData(account.address)
    total_collateral_eth, total_debt_eth, available_borrow_eth = user_data[:3] 
    eth_price = get_eth_price()
    user_data = (
        (total_collateral_eth * eth_price), 
        (total_debt_eth * eth_price), 
        (available_borrow_eth * eth_price),
        user_data[3],
        user_data[4],
        user_data[5],
    )

    user_info = {
    'total_collateral_eth': user_data[0],
    'total_debt_eth': user_data[1],
    'available_borrow_eth': user_data[2],
    'current_liquidation_threshold': user_data[3],
    'locked_total_value': user_data[4],
    'health_factor': user_data[5],
    }
    available_borrow_eth = user_info['available_borrow_eth']
    total_collateral_eth = user_info['total_collateral_eth']
    total_debt_eth = user_info['total_debt_eth']
    return user_info