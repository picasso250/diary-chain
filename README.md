# Diary Chain — 永久的公共日记

写下即永恒。日记全文作为 Arbitrum One 交易事件写入区块链，公开可读、不可修改、不可删除。

- **全文上链**：日记内容保存在交易事件中，而不是只存哈希。
- **永久公开**：链上明文任何人都能读取；需要私密内容时可自行选择前端的 AES 加密功能。
- **无需平台注册**：使用自己的 EVM 钱包写入。
- **无平台抽成**：旧 Arbitrum 合约写入只需要网络 Gas，不需要额外日记费。
- **当前正式链：Arbitrum One**（chain ID `42161`）。

## 正式服务

| 组件 | 地址 / 说明 |
|---|---|
| 网页 | [diary.io99.xyz](https://diary.io99.xyz) — Cloudflare Workers |
| 合约 | [0x09e8c43372CB00eC109D029e321dC7FFf0bb1e28](https://arbiscan.io/address/0x09e8c43372CB00eC109D029e321dC7FFf0bb1e28) |
| 合约部署区块 | `419201926` |
| 部署交易 | [Arbiscan](https://arbiscan.io/tx/0x73a463a7af59b2a93167700880c0dab7a921dcf615fd5a8455c8dc99384fef98) |
| The Graph Studio | [diary](https://thegraph.com/studio/subgraph/diary) — Arbitrum `v0.0.3` |
| GraphQL | `https://api.studio.thegraph.com/query/1723159/diary/v0.0.3` |

**当前只维护 Arbitrum 的部署配置。** Ethereum / Sepolia 的旧代码与设置可从 Git 历史中恢复，不参与现行构建部署。

## 技术架构

- Svelte 5、Vite 7、Tailwind CSS v4
- ethers.js v6、Reown AppKit / WalletConnect v2
- Solidity 合约事件（旧 Arbitrum 合约的事件带时间戳）
- The Graph Studio 子图（`diary-chain-subgraph/`）
- Cloudflare Workers 静态资源托管（`wrangler.toml`）

写入函数：`writeEntry(string _content)`；写入事件：

```solidity
event EntryCreated(address indexed user, uint256 timestamp, string content);
```

日记时间戳取自链上事件的 `timestamp` 参数。旧合约无 `diaryFee()` 接口，前端不应查询或附加该费用。

### 日记读取

默认通过 The Graph 的 `v0.0.3` GraphQL 索引检索。索引尚未同步完毕时可能暂时只显示部分记录；没有设置子图 URL 或请求失败时，会回退到分块 `eth_getLogs`（需要连接钱包，历史扫描可能较慢）。

扫描从已验证的部署区块 `419201926` 开始。前端相关配置在 `frontend/.env.arbitrum`；请勿将任何私钥、Graph 部署密钥存入该文件或提交到 Git。

## 本地运行

```powershell
cd frontend
npm install
npm run dev
# 等同于 npm run dev:arbitrum
```

默认打开 `http://localhost:5173`。连接钱包后可查看自己的记录和关注地址的记录。使用手机访问局域网 HTTP 地址时，钱包连接可能受 HTTPS 安全上下文限制。

## 构建与 Cloudflare 部署

```powershell
cd frontend
npm run build
cd ..
npx wrangler deploy
```

`wrangler.toml` 指向 `frontend/dist`，正式域名为 `diary.io99.xyz`。部署前确认构建使用 Arbitrum 模式（已设为默认），并验证图索引已能读取历史事件。

## The Graph Studio 部署

在 `diary-chain-subgraph/` 下：

```powershell
npm install
npm run codegen
npm run build
npm run deploy
```

`npm run deploy` 部署到现有 Studio 项目 `diary`；需要已通过安全途径配置的 Graph 部署授权。当前子图主配置为 `subgraph.yaml`，网络地址和起始区块记录在 `networks.json`。

每次发布新的 Studio 子图版本，都需要将新 GraphQL 版本 URL 同步更新到 `frontend/.env.arbitrum`，并重新构建发布网页。

## 历史数据与恢复

以前使用过的合约仍然可以通过相应链的区块浏览器及 RPC 独立查询，切换网站或索引不影响链上的旧数据：

| 链 | 合约 | 说明 |
|---|---|---|
| Ethereum（2026-10-03 新版） | [0x493e084c3959d2728a3277c18ee47ffcc41eff24](https://etherscan.io/address/0x493e084c3959d2728a3277c18ee47ffcc41eff24) | 部署区块 `26108868`，事件不含 `timestamp` 字段 |
| Ethereum（旧版） | [0xc316f67824A3508eD4a568391ABc47a4318E5593](https://etherscan.io/address/0xc316f67824A3508eD4a568391ABc47a4318E5593) | 部署区块 `24567728` |
| Sepolia | [0x3E249b0da8F0a112Ad9b0a9b7cf907712C213021](https://sepolia.etherscan.io/address/0x3E249b0da8F0a112Ad9b0a9b7cf907712C213021) | 历史测试合约 |

历史数据恢复可以使用 `eth_getLogs`，并按事件 ABI 解析 `user`、`timestamp`、`content`、区块和交易哈希。旧数据中以 `AES:` 开头的记录需要原来的加密密码，钱包私钥不能代替该密码。

以太坊新版子图历史接口 `https://api.studio.thegraph.com/query/1723159/diary/v0.0.2` 曾验证可读取旧数据，但目前不再维护其部署流程；源码和部署配置留存于 Git 历史。

## 历史备注

此前 Netlify 部署已经废弃，现行仓库不再包含 `netlify.toml`。项目的变更过程见 [worklog.md](worklog.md)。
