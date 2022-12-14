// SPDX-License-Identifier: MIT

pragma solidity >=0.5.0;

import "../interfaces/IUniswapV2DMTransact.sol";
import "../interfaces/IUniswapV2Router02.sol";
import "../interfaces/IUniswapV2Pair.sol";
import "../interfaces/IERC20.sol";


contract UniswapV2DMTransact is IUniswapV2DMTransact {

    IUniswapV2Router02 public immutable router02;

    constructor(address _router02) public {
        router02 = IUniswapV2Router02(_router02);
    }

    function getFactory() external view override returns (address factory) {
        factory = router02.factory();
        return factory;
    }

    function getAmountIn(uint amountOut, address tokenIn, address tokenOut) public view returns (uint[] memory amountIn) {
        address[] memory path = new address[](2);
        path[0] = tokenIn;
        path[1] = tokenOut;
        amountIn = router02.getAmountsIn(amountOut, path);
        return amountIn;
    }
    

    function getAmountOut(uint amountIn, address tokenIn, address tokenOut) public view returns (uint[] memory amountOut) {
        address[] memory path = new address[](2);
        path[0] = tokenIn;
        path[1] = tokenOut;
        amountOut = router02.getAmountsOut(amountIn, path);
        return amountOut;
    }

    function swapETHForExactTokens(uint amountOut, address tokenOut) external payable returns (uint[] memory amounts) {
        
        address[] memory path = new address[](2);
        path[0] = router02.WETH();
        path[1] = tokenOut;
        amounts = router02.swapETHForExactTokens{value: msg.value}(amountOut, path, msg.sender, block.timestamp);
        return amounts;
      
    }

    function swapExactETHForTokens(address tokenOut) external payable returns (uint[] memory amounts) {
        
        address[] memory path = new address[](2);
        path[0] = router02.WETH();
        path[1] = tokenOut;
        uint amountOutMin = 1;
        amounts = router02.swapExactETHForTokens{value: msg.value}(amountOutMin, path, msg.sender, block.timestamp);
        return amounts;
      
    }

    function swapExactTokensForETH(uint amountIn, address tokenIn) public returns (uint[] memory amounts) {
        IERC20 ERC20 = IERC20(tokenIn);
        require(ERC20.transferFrom(msg.sender, address(this), amountIn), 'transferFrom failed.');
        require(ERC20.approve(address(router02), amountIn), 'approve failed.');
        address[] memory path = new address[](2);
        path[0] = tokenIn;
        path[1] = router02.WETH();
        uint amountOutMin = 1;
        amounts = router02.swapExactTokensForETH(amountIn, amountOutMin, path, msg.sender, block.timestamp);
        return amounts;
    }

    function swapTokensForExactETH(uint amountIn, uint amountOut, address tokenIn) public returns (uint[] memory amounts) {
        IERC20 ERC20 = IERC20(tokenIn);
        require(ERC20.transferFrom(msg.sender, address(this), amountIn), 'transferFrom failed.');
        require(ERC20.approve(address(router02), amountIn), 'approve failed.');
        address[] memory path = new address[](2);
        path[0] = tokenIn;
        path[1] = router02.WETH();
        uint amountInMax = 10**21;
        amounts = router02.swapTokensForExactETH(amountOut, amountInMax, path, msg.sender, block.timestamp);
        return amounts;
    }

    function swapExactTokensForTokens(uint amountIn, address tokenIn, address tokenOut) public returns (uint[] memory amounts) {
        IERC20 ERC20 = IERC20(tokenIn);
        require(ERC20.transferFrom(msg.sender, address(this), amountIn), 'transferFrom failed.');
        require(ERC20.approve(address(router02), amountIn), 'approve failed.');
        address[] memory path = new address[](2);
        path[0] = tokenIn;
        path[1] = tokenOut;
        uint amountOutMin = 1;
        amounts = router02.swapExactTokensForTokens(amountIn, amountOutMin, path, msg.sender, block.timestamp);
        return amounts;
    }

    function swapTokensForExactTokens(uint amountIn, uint amountOut, address tokenIn, address tokenOut) public returns (uint[] memory amounts) {
        IERC20 ERC20 = IERC20(tokenIn);
        require(ERC20.transferFrom(msg.sender, address(this), amountIn), 'transferFrom failed.');
        require(ERC20.approve(address(router02), amountIn), 'approve failed.');
        address[] memory path = new address[](2);
        path[0] = tokenIn;
        path[1] = tokenOut;
        uint amountInMax = 10**21;
        amounts = router02.swapTokensForExactTokens(amountOut, amountInMax, path, msg.sender, block.timestamp);
        return amounts;
    }


}