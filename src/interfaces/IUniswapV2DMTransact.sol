// SPDX-License-Identifier: MIT

pragma solidity >=0.5.0;


interface IUniswapV2DMTransact {

    
    function getFactory() external view returns (address factory);
    function getAmountIn(uint amountOut, address tokenIn, address tokenOut) external view returns (uint[] memory amountIn);
    function getAmountOut(uint amountIn, address tokenIn, address tokenOut) external view returns (uint[] memory amountOut);
    function swapETHForExactTokens(uint amountOut, address tokenOut) external payable returns (uint[] memory amounts);
    function swapExactETHForTokens(address tokenOut, uint amountOutMin) external payable returns (uint[] memory amounts);
    function swapExactTokensForETH(uint amountIn, uint amountOutMin, address tokenIn) external returns (uint[] memory amounts);
    function swapTokensForExactETH(uint amountIn, uint amountInMax, uint amountOut, address tokenIn) external returns (uint[] memory amounts);
    function swapExactTokensForTokens(uint amountIn, uint amountOutMin, address tokenIn, address tokenOut) external returns (uint[] memory amounts);
    function swapTokensForExactTokens(uint amountIn, uint amountInMax, uint amountOut, address tokenIn, address tokenOut) external returns (uint[] memory amounts);

}
