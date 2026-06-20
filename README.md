# Diary Chain

[![Netlify Status](https://api.netlify.com/api/v1/badges/474a177d-1f29-4159-8de4-a071d637b237/deploy-status)](https://app.netlify.com/projects/diary-chain/deploys)

每一条记录，都像刻在石碑上。

Diary Chain 是一个不可篡改的个人链上日记。写在链上的每一条记录都无法删除、无法修改——为诚实记录而生。

## 部署拓扑

| 域名 | 平台 | 目标链 | 构建模式 |
|------|------|--------|---------|
| [diary.io99.xyz](https://diary.io99.xyz) | Cloudflare Workers | Ethereum | `npm run build:ethereum` |
| [diary-chain.netlify.app](https://diary-chain.netlify.app) | Netlify | Arbitrum One | `npm run build`（默认） |
| — | 本地开发 | Sepolia（测试） | `npm run dev` |

## Tech Stack

### Frontend
- **Framework:** Svelte 5
- **Build Tool:** Vite 7
- **Styling:** Tailwind CSS v4
- **Wallet Connection:** Reown AppKit (WalletConnect v2)
- **Contract Interaction:** ethers.js v6
- **Encryption:** crypto-js

### Smart Contract
- **Language:** Solidity 0.8.30
- **License:** GPL-3.0

### Infrastructure
- **Cloudflare Workers** — Ethereum 生产部署（`wrangler.toml`）
- **Netlify** — Arbitrum One 生产部署（`netlify.toml`）

## Getting Started

### 前端

```bash
cd frontend
npm install
```

**本地开发**（默认使用 Sepolia 测试网）：

```bash
npm run dev
```

**生产构建**：

| 目标链 | 命令 | 用途 |
|--------|------|------|
| Arbitrum One | `npm run build` | Netlify 默认部署 |
| Ethereum | `npm run build:ethereum` | Cloudflare 部署 |
| Sepolia | `npm run build:sepolia` | 测试构建 |

各构建模式对应的环境变量见 `frontend/.env.*`。

### 合约

```bash
cd backend
npm install
```

编译合约：

```bash
compile.bat
```

部署合约（需设置 `PRIVATE_KEY` 环境变量）：

```powershell
# 先加载密钥（见 env-in.ps1）
.\env-in.ps1
node deploy.js
```

> 注：`deploy.js` 中默认 RPC 指向 Ethereum 主网。部署到其他链时请自行切换 RPC URL。

## 合约地址（已部署）

| 链 | 合约地址 |
|---|---------|
| Ethereum | `0xc316f67824A3508eD4a568391ABc47a4318E5593` |
| Arbitrum One | `0x09e8c43372CB00eC109D029e321dC7FFf0bb1e28` |
| Sepolia | `0x3E249b0da8F0a112Ad9b0a9b7cf907712C213021` |

各链的合约实例及对应前端 env 配置位于 `frontend/.env.{chain}`。

## 部署说明

### Cloudflare Workers（diary.io99.xyz → Ethereum）

```bash
cd frontend
npm run build:ethereum
cd ..
npx wrangler deploy
```

配置见 `wrangler.toml`，Worker 入口为 `frontend/src/worker.js`。

### Netlify（diary-chain.netlify.app → Arbitrum One）

Netlify 自动从 GitHub 仓库部署，配置见 `netlify.toml`。
