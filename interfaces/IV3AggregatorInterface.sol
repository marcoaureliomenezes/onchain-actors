// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;


interface IV3AggregatorInterface {



  function getRoundData(uint80 _roundId) external view 
    returns (
      uint80 roundId,
      int256 answer,
      uint256 startedAt,
      uint256 updatedAt,
      uint80 answeredInRound
    );

  function latestRoundData() external view  returns (
      uint80 roundId,
      int256 answer,
      uint256 startedAt,
      uint256 updatedAt,
      uint80 answeredInRound
    );

  function description() external view  returns (string memory);

}

// MockOracle
// Function signatures, event signatures, log topics