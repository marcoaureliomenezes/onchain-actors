// SPDX-License-Identifier: MIT

pragma solidity 0.6.6;


import "../interfaces/IUniswapWatcher.sol";
import "./uniswap_v2/libraries/UniswapV2Library.sol";
import '@uniswap_core_v2/contracts/interfaces/IUniswapV2Pair.sol';

contract UniswapWatcher is IUniswapWatcher {

    address public factory;

    constructor(address factory_) public {
        factory = factory_;
    }

    function pairInfo(address tokenA, address tokenB) external view returns (uint reserveA, uint reserveB, uint totalSupply) {
        IUniswapV2Pair pair = IUniswapV2Pair(UniswapV2Library.pairFor(factory, tokenA, tokenB));
        totalSupply = pair.totalSupply();
        (uint reserves0, uint reserves1,) = pair.getReserves();
        (reserveA, reserveB) = tokenA == pair.token0() ? (reserves0, reserves1) : (reserves1, reserves0);
        return (reserveA, reserveB, totalSupply);
    }
    
    function computeLiquidityShareValue(uint liquidity, address tokenA, address tokenB)
                                            external override returns (uint tokenAAmount, uint tokenBAmount) {
    (uint reserveA, uint reserveB, ) = this.pairInfo(tokenA, tokenB);
    tokenAAmount = reserveA + liquidity;
    tokenBAmount = reserveB + liquidity;
    return (tokenAAmount, tokenAAmount);
    }

    function quotePair(uint256 amountIn, address tokenA, address tokenB) public view returns (uint256 amountOut) {
        (uint reserveA, uint reserveB, ) = this.pairInfo(tokenA, tokenB);
        amountOut = UniswapV2Library.quote(amountIn, reserveA, reserveB);
        return amountOut;
    }

    function getPairAddress(address tokenA, address tokenB) public view returns (address poolAddress){
        poolAddress = UniswapV2Library.pairFor(factory, tokenA, tokenB);
        return poolAddress;
    }
}