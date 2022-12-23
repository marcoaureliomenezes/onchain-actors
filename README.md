# Onchain Actors

In a quick resume, this repo was created with the intent to demonstrate in a case presented to become an Data Engineer Expert. In a study about how can Data Engineering and blockchain technologies work together to create a profitable tech product.

The concepts that unified both fields are:

* Anyone can read data from blockchain.
* There are in the defi world many opportunities to realize profit only with software resources.

Anyone that has needed resources can read data from the blockchain and defi protocols and find insights and opportunities to make money and contribute to the defi ecossystem. How this profit happens? Keepers or liquidators and arbitrage opportunities unified with flashloans and flashswaps are the key. To execute transactions and make money from these opportunities a onchain executor is needed.

In this case, a final application was created to interact with 2 DEFI protocols and make transactions. because of its nature, receive messages from Apache Kafka and do transactions using DEFI protocols on top of different blockchain networks EVM compatible, it was called Onchain Actors.

The application only executes required transactions it receives from a Apache Kafka Topic.

Onchain-Actors can do transactions on the following protocols: 

* AAVE protocol for borrowing and lending crypto assets and do flashloans and liquidations.

* Uniswap protocol for swapping tokens and do arbitrage.


## 1 - AAVE Protocol

This application was designed to interact with:

* AAVE V2 protocol on Ethereum mainnet, Polygon mainnet, Goerli and Mumbai testnets.
* AAVE V3 protocol on Polygon mainnet and Mumbai testnet.

Using Aave protocol the following transactions can be made:

### 1.1 - Supplying and Removing liquidity to the protocol and earning interest

Any user can provide liquidity to the lending and borrow using the accepted ERC20 tokens and earn interest.

Example: Supplying 1 WETH to Aave V2 protocol on goerli testnet.

    brownie run scripts/aave_api_v2.py supply_asset 0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6 1000000000000000000 --network goerli

Of course, if a user can supply liquidity, he can also remove the liquidity he supplied.

Example: Withdrawing 1 WETH from the Aave V2 protocol on goerli testnet.

    brownie run scripts/aave_api_v2.py withdraw_asset 0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6 1000000000000000000 --network goerli

### 1.2 - Borrowing and repaying borrowed tokens

Any user can make a traditional loan on Aave. However, in order to borrow ERC20 tokens, it's needed to have some collateral. To be precise, to borrow X amount of tokens a user need to be overcollaterized with a 150% ratio. And of course there are interests.

Example: Borrowing 10000 DAI from Aave V2 protocol on goerli testnet.

    brownie run scripts/aave_api_v2.py borrow_asset 0x75Ab5AB1Eef154C0352Fc31D2428Cef80C7F8B33 1000000000000000000 --network goerli

Of course, if a user can make a loan, he can also repay the debts.

Example: Repaying a debt of 10000 DAI on Aave V2 protocol on goerli testnet.

    brownie run scripts/aave_api_v2.py repay_asset 0x75Ab5AB1Eef154C0352Fc31D2428Cef80C7F8B33 1000000000000000000 --network goerli

### 1.3 - Advanced Financial operations such as leverage and short selling.

### 1.4 - Keepers and liquidations

### 1.5 - Flashloans and its opportunities


## UNISWAP Decentrilized Exchange Protocol


### 1.1 Swap an exact amount of ether per a desired token
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