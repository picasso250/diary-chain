// SPDX-License-Identifier: MIT
pragma solidity 0.8.30;

/**
 * @title OnChainDiary
 * @dev 反修正主义内容网络。
 *      没有“删除键”，没有“修改键”，只有不可篡改的历史。
 */
contract OnChainDiary {
    // 记录合约的拥有者（部署者），用于后续提现
    address public owner;

    // 每一条记录都是一个永久的事件日志
    event EntryCreated(
        address indexed user, 
        uint256 timestamp, 
        string content
    );

    // 部署时自动将调用者设为 owner
    constructor() {
        owner = msg.sender;
    }

    /**
     * @dev 写入一条不可篡改的公开内容
     * @param _content 明文内容
     * 注意：加上了 payable，并要求必须附带大于 0 的金额
     */
    function writeEntry(string memory _content) public payable {
        // 核心修改：极其省 Gas 的检查方式。金额随意，但不能为 0
        require(msg.value > 0, "Must pay something to write");

        emit EntryCreated(msg.sender, block.timestamp, _content);
    }

    /**
     * @dev 提现函数，把合约里收到的“日记费”提取到你的钱包
     */
    function withdraw() public {
        require(msg.sender == owner, "Only owner can withdraw");
        
        // 获取合约当前的所有余额
        uint256 balance = address(this).balance;
        require(balance > 0, "No funds to withdraw");
        
        // 安全提现方式
        (bool success, ) = payable(owner).call{value: balance}("");
        require(success, "Transfer failed");
    }
}