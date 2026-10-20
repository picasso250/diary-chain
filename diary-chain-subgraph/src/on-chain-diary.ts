import { EntryCreated as EntryCreatedEvent } from "../generated/OnChainDiary/OnChainDiary"
import { Entry } from "../generated/schema"

// The legacy Arbitrum contract includes timestamp directly in the event.
export function handleEntryCreated(event: EntryCreatedEvent): void {
  let entry = new Entry(
    event.transaction.hash.toHex() + "-" + event.logIndex.toString()
  )
  entry.user = event.params.user
  entry.timestamp = event.params.timestamp
  entry.content = event.params.content
  entry.blockNumber = event.block.number
  entry.txHash = event.transaction.hash.toHexString()
  entry.save()
}
