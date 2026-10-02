export const CONTRACT_ADDRESS = import.meta.env.VITE_CONTRACT_ADDRESS;
export const TARGET_CHAIN_ID = import.meta.env.VITE_CHAIN_ID;
export const BLOCK_EXPLORER = import.meta.env.VITE_BLOCK_EXPLORER;
export const NETWORK_NAME = import.meta.env.VITE_NETWORK_NAME;
// The Graph Subgraph 查询地址；未配置时回退到分批 eth_getLogs
export const SUBGRAPH_URL = import.meta.env.VITE_SUBGRAPH_URL;
// 链上日志扫描起始区块（低于合约首个事件的区块，避免全链扫描被 RPC 拒绝）
export const START_BLOCK = Number(import.meta.env.VITE_START_BLOCK || 0);

export const CONTRACT_ABI = [
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "user",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "string",
        "name": "content",
        "type": "string"
      }
    ],
    "name": "EntryCreated",
    "type": "event"
  },
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "_content",
        "type": "string"
      }
    ],
    "name": "writeEntry",
    "outputs": [],
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "withdraw",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "owner",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  }
];
