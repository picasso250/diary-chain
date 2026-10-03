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
