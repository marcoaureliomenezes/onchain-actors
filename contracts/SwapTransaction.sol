// SPDX-License-Identifier: MIT

pragma solidity 0.6.6;


import "../interfaces/ILiquidityValueCalculator.sol";
import "./uniswap_v2/libraries/UniswapV2Library.sol";
import '@uniswap_core_v2/contracts/interfaces/IUniswapV2Pair.sol';

contract SwapTransaction {


    address public factory;
    
    constructor(address factory_) public {
        factory = factory_;
    }


}