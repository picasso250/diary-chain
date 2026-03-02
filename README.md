# Diary Chain

[![Netlify Status](https://api.netlify.com/api/v1/badges/474a177d-1f29-4159-8de4-a071d637b237/deploy-status)](https://app.netlify.com/projects/diary-chain/deploys)

GitHub: [picasso250/diary-chain](https://github.com/picasso250/diary-chain)

Diary Chain is an on-chain diary application designed for the Arbitrum network. It leverages the security and immutability of the Ethereum ecosystem while utilizing Arbitrum's low gas fees for high-frequency interactions like writing diary entries.

## Project Structure

This repository is structured into two main directories:

- `/backend`: Smart contracts for the Diary Chain application.
- `/frontend`: The web application built to interact with the smart contracts.

## Tech Stack

### Frontend
- **Framework:** Svelte 5
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **Web3 Integration:** ethers.js
- **Deployment:** Netlify (configured via root `netlify.toml`)

### Backend
- **Framework:** Hardhat
- **Language:** Solidity
- **Network:** Arbitrum (optimized for low gas fees using event logs for data storage)

## Getting Started

### Prerequisites
- Node.js
- npm or yarn

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. Build for production:
   ```bash
   npm run build
   ```

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run tests:
   ```bash
   npx hardhat test
   ```

## License

This project embraces the decentralized, on-chain nature of Web3.

Open-source under the **ISC License**. No rights reserved.
