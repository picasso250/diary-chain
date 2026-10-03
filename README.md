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

## 经济模型

Diary Chain 采用极简的“打赏（乞讨）模式”：

- **Begger (Owner)**：合约部署者即为收款人。虽然在合约中称为 `owner`，但其唯一特权是提取合约中收到的打赏。
- **Voluntary Tipping**：写入日记是免费的（除了必要的 Gas 费）。用户在 `writeEntry` 时可以自愿附带任意金额的 ETH 作为对平台的打赏。
- **Zero Enforcement**：合约不强制要求付费。这种模式旨在通过“用完即走、随心打赏”的经济行为，支持去中心化基础设施的运行。

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
| Ethereum | `0x493e084c3959d2728a3277c18ee47ffcc41eff24` |
| Arbitrum One | `0x09e8c43372CB00eC109D029e321dC7FFf0bb1e28` |
| Sepolia | `0x3E249b0da8F0a112Ad9b0a9b7cf907712C213021` |

各链的合约实例及对应前端 env 配置位于 `frontend/.env.{chain}`。

### 历史合约与取回日记数据

以下地址永久保留在文档中，供老用户查找和自行读取历史记录。更换前端、索引或合约不会删除这些合约中已经写入的日记。

| 链 | 历史合约地址（点击查看区块浏览器） | 说明 |
|---|---|---|
| Ethereum 主网（chain ID `1`） | [0xc316f67824A3508eD4a568391ABc47a4318E5593](https://etherscan.io/address/0xc316f67824A3508eD4a568391ABc47a4318E5593) | 2026-10-03 切换前使用的旧合约；部署区块 `24567728` |
| Arbitrum One（chain ID `42161`） | [0x09e8c43372CB00eC109D029e321dC7FFf0bb1e28](https://arbiscan.io/address/0x09e8c43372CB00eC109D029e321dC7FFf0bb1e28) | 原 Arbitrum 合约，尚未迁移到新事件格式 |
| Sepolia（chain ID `11155111`） | [0x3E249b0da8F0a112Ad9b0a9b7cf907712C213021](https://sepolia.etherscan.io/address/0x3E249b0da8F0a112Ad9b0a9b7cf907712C213021) | 原测试网合约 |

日记存储在交易的 **事件日志** 中，不是合约的可枚举存储变量。读取公开日志不需要连接钱包、提供私钥或发送付费交易，也不依赖本项目网站或 Subgraph。

取回自己的历史记录：

1. 在对应链的区块浏览器打开上述合约，找到自己地址发送的写入交易，查看交易的 Logs；批量导出可使用该链 RPC 的 `eth_getLogs`。
2. 旧合约使用以下事件 ABI，`user` 是索引字段。批量查询时指定旧合约地址，并按自己的钱包地址过滤 `user`；不要使用新合约的两参数事件 ABI。

   ```solidity
   event EntryCreated(address indexed user, uint256 timestamp, string content);
   ```

3. 按区块范围分批读取并保存 `user`、`timestamp`、`content`、区块号、交易哈希和日志索引。Ethereum 旧合约可从区块 `24567728` 开始；Arbitrum/Sepolia 可先在区块浏览器找到合约创建交易的区块，再从该区块开始扫描。RPC 历史日志范围受限时，缩小查询窗口或使用支持历史日志的 RPC。
4. 明文日记可直接读取。以 `AES:` 开头的内容需要原先设置的加密密码，按原前端方式 `CryptoJS.AES.decrypt(content.slice(4), password).toString(CryptoJS.enc.Utf8)` 解密；钱包私钥不能替代该密码。

当前 Ethereum 网站和 Subgraph v0.0.2 只读取新合约，旧日记不会自动出现在新时间线中。上述历史地址及事件格式用于独立取回数据。

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

**已部署**（2026-10-03）：

- Studio 页面：https://thegraph.com/studio/subgraph/diary
- 查询地址：`https://api.studio.thegraph.com/query/1723159/diary/v0.0.2`
- 当前版本：v0.0.2

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
VITE_SUBGRAPH_URL=https://api.studio.thegraph.com/query/<DEPLOYMENT_ID>/diary/v0.0.2
```

然后重新构建前端：

```bash
cd frontend
npm run build:ethereum
```

## 已知事项（暂缓处理）

1. **Ethereum 新合约已部署**：2026-10-03 部署，区块 `26108868`，支持零金额写入和自愿打赏。`EntryCreated(address,string)` 的时间戳从区块获取；前端与 Subgraph v0.0.2 已指向新合约。旧合约中的记录仍保留在链上，新版本时间线只读取新合约。Arbitrum/Sepolia 尚未迁移，当前源码的新事件 ABI 不适用于其旧合约。
2. **Arbitrum/Sepolia 构建**：这两条链暂未配置 subgraph 与 `VITE_START_BLOCK`，前端走 RPC 回退时会从区块 0 扫描（不现实）。旧版本同样存在该问题，非本次回归；待主网稳定后再处理。

> subgraph 起始区块 `26108868`（`subgraph.yaml` / `networks.json`），等于新合约部署区块。
> 若之后要调整 subgraph（例如增加字段），改完重新 `npm run codegen && npm run build` 后再 `npm run deploy`。
