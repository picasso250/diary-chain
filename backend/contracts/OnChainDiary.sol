// SPDX-License-Identifier: MIT
pragma solidity 0.8.30;

/**
 * @title OnChainDiary
 * @dev 反修正主义内容网络。
 *      没有“删除键”，没有“修改键”，只有不可篡改的历史。
 */
contract OnChainDiary {
    uint256 public diaryFee = 0.000006 ether;
    address public owner;

    event EntryCreated(
        address indexed user, 
        uint256 timestamp, 
        string content
    );

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }

    function writeEntry(string memory _content) public payable {
        require(msg.value >= diaryFee, "Please pay the diary fee");
        emit EntryCreated(msg.sender, block.timestamp, _content);
    }

    function setDiaryFee(uint256 _newFee) public onlyOwner {
        diaryFee = _newFee;
    }

    function withdraw() public onlyOwner {
        payable(owner).transfer(address(this).balance);
    }

    receive() external payable {}
}
