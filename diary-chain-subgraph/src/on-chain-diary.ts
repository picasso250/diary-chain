// 从 generated 目录导入我们真正关心的事件类型
import {
  EntryCreated as EntryCreatedEvent
} from "../generated/OnChainDiary/OnChainDiary"

// 从 generated 目录导入我们在 schema.graphql 中定义的实体类型
import { Entry } from "../generated/schema"

/**
 * 处理 EntryCreated 事件的函数
 * 当合约发出 EntryCreated 事件时，这个函数会被调用
 */
export function handleEntryCreated(event: EntryCreatedEvent): void {
  // 创建新的 Entry 实体，使用交易哈希 + 日志索引作为唯一ID
  let entry = new Entry(
    event.transaction.hash.toHex() + "-" + event.logIndex.toString()
  )

  entry.user = event.params.user
  entry.timestamp = event.params.timestamp
  entry.content = event.params.content
  entry.blockNumber = event.block.number
  entry.txHash = event.transaction.hash.toHexString()

  // 保存实体
  entry.save()
}
