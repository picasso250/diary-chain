// Production configuration: Arbitrum One. Ethereum history is available in Git.
export const CONTRACT_ADDRESS = import.meta.env.VITE_CONTRACT_ADDRESS;
export const TARGET_CHAIN_ID = import.meta.env.VITE_CHAIN_ID;
export const BLOCK_EXPLORER = import.meta.env.VITE_BLOCK_EXPLORER;
export const NETWORK_NAME = import.meta.env.VITE_NETWORK_NAME;
export const SUBGRAPH_URL = import.meta.env.VITE_SUBGRAPH_URL;
export const START_BLOCK = Number(import.meta.env.VITE_START_BLOCK || 0);

export const CONTRACT_ABI = [
  "event EntryCreated(address indexed user, uint256 timestamp, string content)",
  "function writeEntry(string _content)"
];
