How to execute swap using uniswap protocol and these APIs.



### Swap an exact amount of ether per a desired token
brownie run scripts/uniswap_api_v2.py swap_exact_eth_amount_for_token "amount_in" "token_address_out" --network "network"

Example:
    SWAP 1 ETHER (10**18 WEI) PER UNI TOKEN (0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984)
    $ brownie run scripts/uniswap_api_v2.py swap_exact_eth_amount_for_token 1000000000000000000 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984 --network goerli


### Swap an exact amount of desired token per ether




### Swap an exact amount of a token per another token

brownie run scripts/uniswap_api_v2.py swap_exact_eth_amount_for_token "amount_in" "token_address_in" "token_address_out" --network "network"

Example
brownie run scripts/uniswap_api_v2.py swap_exact_token_amount_for_token 1365719243988211854 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984 0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6 --network goerli



