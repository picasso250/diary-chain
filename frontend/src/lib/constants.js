export const CONTRACT_ADDRESS = import.meta.env.VITE_CONTRACT_ADDRESS;
export const TARGET_CHAIN_ID = import.meta.env.VITE_CHAIN_ID;
export const BLOCK_EXPLORER = import.meta.env.VITE_BLOCK_EXPLORER;
export const NETWORK_NAME = import.meta.env.VITE_NETWORK_NAME;

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
        "internalType": "uint256",
        "name": "timestamp",
        "type": "uint256"
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
    "stateMutability": "nonpayable",
    "type": "function"
  }
];
