// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity =0.7.6;
pragma abicoder v2;


import "../interfaces/IUniswapV3DMTransact.sol";
import "../interfaces/IERC20.sol";
import '../interfaces/UniswapV3/ISwapRouter.sol';
import './libraries/TransferHelper.sol';
import '../interfaces/UniswapV3/IPeripheryImmutableState.sol';


contract UniswapV3DMTransact {

    uint24 public poolFee;
    address public WETH9;
    address public factory;

    ISwapRouter public immutable swapRouter;

    constructor(address _swapRouter) {
        swapRouter = ISwapRouter(_swapRouter);
        WETH9 = IPeripheryImmutableState(_swapRouter).WETH9();
        factory = IPeripheryImmutableState(_swapRouter).factory();
    }

    function getFactory() public view returns (address factory) {
        return address(swapRouter);
    }

    function swapExactInputSingle(uint256 amountIn, uint amountOutMin, address tokenIn, address tokenOut, uint24 poolFee) external returns (uint256 amountOut) {
        TransferHelper.safeTransferFrom(tokenIn, msg.sender, address(this), amountIn);
        TransferHelper.safeApprove(tokenIn, address(swapRouter), amountIn);

        ISwapRouter.ExactInputSingleParams memory params =
            ISwapRouter.ExactInputSingleParams({
                tokenIn: tokenIn,
                tokenOut: tokenOut,
                fee: poolFee,
                recipient: msg.sender,
                deadline: block.timestamp,
                amountIn: amountIn,
                amountOutMinimum: amountOutMin,
                sqrtPriceLimitX96: 0
            });
        amountOut = swapRouter.exactInputSingle(params);
    }

    function swapExactOutputSingle(uint256 amountOut, uint256 amountInMax, address tokenIn, address tokenOut, uint24 poolFee) 
                                                                                    external returns (uint256 amountIn) {
        TransferHelper.safeTransferFrom(tokenIn, msg.sender, address(this), amountInMax);
        TransferHelper.safeApprove(tokenIn, address(swapRouter), amountInMax);

        ISwapRouter.ExactOutputSingleParams memory params =
            ISwapRouter.ExactOutputSingleParams({
                tokenIn: tokenIn,
                tokenOut: tokenOut,
                fee: poolFee,
                recipient: msg.sender,
                deadline: block.timestamp,
                amountOut: amountOut,
                amountInMaximum: amountInMax,
                sqrtPriceLimitX96: 0
            });
        amountIn = swapRouter.exactOutputSingle(params);
          if (amountIn < amountInMax) {
            TransferHelper.safeApprove(tokenIn, address(swapRouter), 0);
            TransferHelper.safeTransfer(tokenIn, msg.sender, amountInMax - amountIn);
        }
    }
}