# Onchain Actors

In a quick resume, this repo was created with the intent to demonstrate in a case presented to become an Data Engineer Expert. how can Data Engineering and blockchain technologies can work together to a end application to the presentatioIt brings a example of a final application created to interact with 2 DEFI protocols: 

* AAVE protocol for borrowing and lending crypto assets and do flashloans and liquidations.

* Uniswap protocol for exchange tokens and do arbitrage.

how can Data Engineering and blockchain technologies can work together to a end application to the presentatio

How to execute swap using uniswap protocol and these APIs.



### Swap an exact amount of ether per a desired token
brownie run scripts/uniswap_api_v2.py swap_exact_eth_amount_for_token "amount_in" "token_address_out" --network "network"

Example:
    SWAP 1 ETHER (10**18 WEI) PER UNI TOKEN (0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984)
    $ brownie run scripts/uniswap_api_v2.py swap_exact_eth_amount_for_token 1000000000000000000 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984 --network goerli


### Swap an exact amount of desired token per ether




### Swap an exact amount of a token per another token

brownie run scripts/uniswap_api_v2.py swap_exact_eth_amount_for_token "amount_in" "token_address_in" "token_address_out" --network "network"

Example:
brownie run scripts/uniswap_api_v2.py swap_exact_token_amount_for_token 1365719243988211854 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984 0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6 --network goerli







## Uniswap V3 interaction

Uniswap swaps are only available from ERC20 to ERC20 tokens. However, it's possible wrap the native token of a network and swap its ERC20 version unwrapped. To do that, call
### Swap an exact amount of token for another token (swap_exact_input_single)

brownie run scripts/uniswap_api_v3.py swap_exact_input_single "amount_in" "address_token_in" "address_token_out" "pool_fee" --network "network"

Example: Swaping 1 WETH per as many UNI Tokens as possible:

    brownie run scripts/uniswap_api_v3.py swap_exact_input_single 1000000000000000000 0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984 3000 --network goerli


### Swap an exact amount of token for another token (swap_exact_input_single)

brownie run scripts/uniswap_api_v3.py swap_exact_input_single "amount_in" "address_token_in" "address_token_out" "amount_in_max" "pool_fee" --network "network"

Example: Swaping AMOUNT of WETH to get 1000000000000000000 UNI Tokens. The Amount_in_max parameter is used to secure that because of slippage the transaction will fail if a high input is required to return that amount of tokens.

    brownie run scripts/uniswap_api_v3.py swap_exact_output_single 1000000000000000000  0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984 1000000000000000000 3000 --network goerli

## Aave 