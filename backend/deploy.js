const { ethers } = require('ethers');
const fs = require('fs');
const path = require('path');

async function main() {
    const rpcUrl = 'https://ethereum.publicnode.com';
    // const rpcUrl = 'https://ethereum-sepolia.publicnode.com';
    const privateKey = process.env.PRIVATE_KEY;

    if (!privateKey) {
        console.error('请设置 PRIVATE_KEY 环境变量');
        process.exit(1);
    }

    const abi = JSON.parse(fs.readFileSync(path.join(__dirname, 'build/contracts_OnChainDiary_sol_OnChainDiary.abi'), 'utf8'));
    const bytecode = '0x' + fs.readFileSync(path.join(__dirname, 'build/contracts_OnChainDiary_sol_OnChainDiary.bin'), 'utf8');

    const provider = new ethers.JsonRpcProvider(rpcUrl);
    const wallet = new ethers.Wallet(privateKey, provider);

    console.log('部署账户:', wallet.address);

    const balance = await provider.getBalance(wallet.address);
    console.log('账户余额:', ethers.formatEther(balance), 'ETH');

    const factory = new ethers.ContractFactory(abi, bytecode, wallet);
    
    console.log('正在部署合约...');
    const contract = await factory.deploy();
    await contract.waitForDeployment();

    console.log('合约部署成功!');
    console.log('合约地址:', await contract.getAddress());
}

main().catch(console.error);
