// SPDX-License-Identifier: MIT

pragma solidity 0.6.6;


interface IUniswapWatcher {
    function computeLiquidityShareValue(
        uint liquidity, 
        address tokenA, 
        address tokenB) external returns (uint tokenAAmount, uint tokenBAmount);

    function quotePair(uint256 amountIn, address tokenA, address tokenB) external view returns (uint256 amountOut);

}