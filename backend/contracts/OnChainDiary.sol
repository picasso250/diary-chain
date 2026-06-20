// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title OnChainDiary
 * @dev 反修正主义内容网络。
 *      没有“删除键”，没有“修改键”，只有不可篡改的历史。
 */
contract OnChainDiary {
    // 记录合约的拥有者（部署者），用于后续提现
    // 虽名 owner，实则 begger
    address public owner;

    // 每一条记录都是一个永久的事件日志
    // 删除了 timestamp，因为区块本身自带时间戳
    event EntryCreated(
        address indexed user, 
        string content
    );

    // 部署时自动将调用者设为 owner
    constructor() {
        owner = msg.sender;
    }

    /**
     * @dev 写入一条不可篡改的公开内容
     * @param _content 明文内容
     * 保持 payable 以支持打赏，且比 non-payable 更省 Gas（少了一次 msg.value == 0 的检查）
     */
    function writeEntry(string memory _content) public payable {
        // 删除了 msg.value > 0 的强制要求，变为自愿打赏
        emit EntryCreated(msg.sender, _content);
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
