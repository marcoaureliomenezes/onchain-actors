// SPDX-License-Identifier: MIT

pragma solidity >=0.5.0;


interface IUniswapV3DMTransact {

    
    function swapExactInputSingle(uint256 amountIn, uint amountOutMin, address tokenIn, address tokenOut, uint24 poolFee) external returns (uint256 amountOut);

    function swapExactOutputSingle(uint256 amountOut, uint256 amountInMax, address tokenIn, address tokenOut, uint24 poolFee) external returns (uint256 amountIn);

}
