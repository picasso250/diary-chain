# worklog — Diary Chain

## 2026-06-20

- 审计发现 README 与实际项目严重脱节：
  - 未记录 Cloudflare Workers / Arbitrum 部署拓扑
  - 未记录多链（Ethereum / Arbitrum / Sepolia）架构
  - 钱包库表述过时（仅 ethers.js → 实际使用 Reown AppKit）
  - 构建命令表缺失
- 重写 README：更新部署拓扑、Tech Stack、构建命令表、合约地址
- 删除 render.yaml（Render 已不再使用）
- 将 GitHub 仓库描述改为「每一条记录，都像刻在石碑上。」

## 2026-10-03

- 部署 Ethereum 新合约 `0x493e084c3959d2728a3277c18ee47ffcc41eff24`，区块 `26108868`。
- 支持零金额写入与自愿打赏；验证链上字节码、owner 和零金额调用。
- 部署 Subgraph v0.0.2，更新前端合约地址、查询地址及起始区块。
- 新合约独立扫描缓存；无钱包也读取索引，空索引不触发历史区块扫描。
- Cloudflare 正式站已发布，版本 `b08da76e-b0cc-4516-83d9-ca4206a0bf9c`；验证线上构建包含新合约、起始区块和 v0.0.2 查询地址。
- 移除 Arbitrum 钱包网络、构建命令与环境文件；默认生产构建改为 Ethereum，保留历史合约数据取回文档。

## 2026-10-20

- 恢复 Arbitrum 前端构建、钱包网络配置和旧合约事件 ABI；Ethereum 网站默认构建保持不变。
- 核实 Arbitrum 旧合约 `0x09e8c43372CB00eC109D029e321dC7FFf0bb1e28` 部署于区块 `419201926`，创建交易 `0x73a463a7af59b2a93167700880c0dab7a921dcf615fd5a8455c8dc99384fef98`。
- 旧合约仅提供 `writeEntry(string)`，事件为 `EntryCreated(indexed address,uint256,string)`；无需 ETH 日记费读取函数。
- The Graph Studio **同一 `diary` 子图**发布 Arbitrum v0.0.3：`https://api.studio.thegraph.com/query/1723159/diary/v0.0.3`；前端 Arbitrum 构建已改用该 URL。Ethereum v0.0.2 版本接口仍有效。
- 子图代码生成/构建及 Graph Studio 部署成功；v0.0.3 初次查询时尚未完成历史索引同步。
- 用户本地已验证 Arbitrum 历史日记在时间线中正常显示，授权将正式站切回 Arbitrum。
- 根据最终决定，仓库改为 Arbitrum 单链现行配置：前端默认 dev/build、唯一 env、子图默认 manifest 和 ABI 均指向 Arbitrum；Ethereum/Sepolia 配置保留于 Git 历史，不在当前分支继续维护。
- 删除废弃的 `netlify.toml` 及 README 中的 Netlify 说明；Cloudflare Workers 为唯一正式发布目标。

### 待办（尚未执行）

- [ ] 在 Arbiscan 验证 Arbitrum 旧日记合约源码：`0x09e8c43372CB00eC109D029e321dC7FFf0bb1e28`。创建交易 `0x73a463a7af59b2a93167700880c0dab7a921dcf615fd5a8455c8dc99384fef98`（区块 `419201926`）；确认匹配的 Solidity 版本、优化设置、构造参数和部署字节码后提交验证，不要盲目使用当前 backend 的新版源码。
