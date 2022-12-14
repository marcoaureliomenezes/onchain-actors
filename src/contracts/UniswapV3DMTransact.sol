// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity =0.7.6;
pragma abicoder v2;


import "../interfaces/IUniswapV3DMTransact.sol";
import "../interfaces/IERC20.sol";
import '../interfaces/ISwapRouter.sol';
import './libraries/TransferHelper.sol';

contract UniswapV3DMTransact {

    uint24 public poolFee;
    ISwapRouter public immutable swapRouter;

    constructor(address _swapRouter, uint24 _poolFee) {
        swapRouter = ISwapRouter(_swapRouter);
        poolFee = _poolFee;
    }

    function getFactory() public view returns (address factory) {

        return address(swapRouter);
    }

    function swapExactInputSingle(uint256 amountIn, address tokenIn, address tokenOut) external returns (uint256 amountOut) {
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
                amountOutMinimum: 0,
                sqrtPriceLimitX96: 0
            });
        amountOut = swapRouter.exactInputSingle(params);
    }

    function swapExactOutputSingle(uint256 amountOut, uint256 amountInMaximum, address tokenIn, address tokenOut) 
                                                                                    external returns (uint256 amountIn) {
        TransferHelper.safeTransferFrom(tokenIn, msg.sender, address(this), amountInMaximum);
        TransferHelper.safeApprove(tokenIn, address(swapRouter), amountInMaximum);

        ISwapRouter.ExactOutputSingleParams memory params =
            ISwapRouter.ExactOutputSingleParams({
                tokenIn: tokenIn,
                tokenOut: tokenOut,
                fee: poolFee,
                recipient: msg.sender,
                deadline: block.timestamp,
                amountOut: amountOut,
                amountInMaximum: amountInMaximum,
                sqrtPriceLimitX96: 0
            });

        amountIn = swapRouter.exactOutputSingle(params);

          if (amountIn < amountInMaximum) {
            TransferHelper.safeApprove(tokenIn, address(swapRouter), 0);
            TransferHelper.safeTransfer(tokenIn, msg.sender, amountInMaximum - amountIn);
        }
    }
}