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
- **The Graph Subgraph** — Ethereum 链上日记事件索引（`diary-chain-subgraph/`），免费额度（Subgraph Studio 每月约 10 万次查询）

### 事件读取（重要）

前端读取日记默认使用 **The Graph Subgraph**（GraphQL，无 `eth_getLogs` 区块范围限制）。
未配置 `VITE_SUBGRAPH_URL` 时自动回退到 **分批 eth_getLogs**（自适应窗口：10 万块起，被 RPC 拒绝时减半至 500 块，并用 `localStorage` 记录已扫描区块断点续扫）。

- 各链起始扫描区块见 `frontend/.env.{chain}` 中的 `VITE_START_BLOCK`。
- 配置好 `VITE_SUBGRAPH_URL` 后，前端查询完全走 GraphQL，不再依赖钱包 RPC 拉日志。

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

## Subgraph 部署（The Graph Studio，Ethereum 主网）

**已部署**（2026-09-24）：

- Studio 页面：https://thegraph.com/studio/subgraph/diary
- 查询地址：`https://api.studio.thegraph.com/query/1723159/diary/version/latest`
- 当前版本：v0.0.1

后续重新部署：

```bash
cd diary-chain-subgraph
npm install

# 1. 在 The Graph Studio 新建 subgraph，slug 填 diary（已建好，Draft 状态）
# 2. 在 Studio 页面复制 Deploy Key，然后：
npx graph auth <YOUR_DEPLOY_KEY>

# 3. 部署（slug 与 Studio 中创建的一致：diary）
npm run deploy
```

部署完成后，把查询地址填入 `frontend/.env.ethereum`（当前已填好）：

```
VITE_SUBGRAPH_URL=https://api.studio.thegraph.com/query/<DEPLOYMENT_ID>/diary/version/latest
```

然后重新构建前端：

```bash
cd frontend
npm run build:ethereum
```

## 已知事项（暂缓处理）

1. **线上合约与仓库源码不一致**：线上主网合约（`0xc316…E5593`）的 `writeEntry` 不要求 `msg.value > 0`（8 笔历史交易均为 0 值成功），但仓库 `backend/contracts/OnChainDiary.sol` 仍保留了 `require(msg.value > 0)`。这是已知差异（曾计划移除费用要求），重新部署合约前需统一源码。
2. **Arbitrum/Sepolia 构建**：这两条链暂未配置 subgraph 与 `VITE_START_BLOCK`，前端走 RPC 回退时会从区块 0 扫描（不现实）。旧版本同样存在该问题，非本次回归；待主网稳定后再处理。

> subgraph 起始区块 `24567600`（`subgraph.yaml` / `networks.json`）：合约部署于区块 `24567728`（`0x176dfb0`），取前 128 块余量；首个 `EntryCreated` 事件在区块 `24567860`。
> 若之后要调整 subgraph（例如增加字段），改完重新 `npm run codegen && npm run build` 后再 `npm run deploy`。
