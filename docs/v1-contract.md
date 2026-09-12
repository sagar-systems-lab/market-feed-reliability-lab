\# V1 Contract



\## Purpose



This project exercises failure handling in a synthetic WebSocket

market-data feed.



The objective is not to model a specific exchange. It is to make

stream-state failures observable and testable.



\## Message model



The feed exposes two message classes:



\- snapshot

\- update



Every update carries a monotonically increasing sequence number.



\## Consumer rules



A consumer may apply an update only when its sequence follows the

last accepted sequence.



Duplicate updates are ignored.



A sequence gap or out-of-order update invalidates local state.



Invalid state must not continue consuming incremental updates as if

the stream were healthy.



Recovery requires a fresh snapshot before incremental processing

resumes.



A transport reconnect alone does not restore valid market state.



\## Faults exercised in V1



\- duplicate update

\- dropped update

\- out-of-order update

\- artificial delay

\- forced disconnect



\## Evidence



V1 is considered complete when automated tests demonstrate:



1\. contiguous updates are accepted

2\. duplicate updates are not applied twice

3\. sequence gaps invalidate local state

4\. recovery restores state from a snapshot

5\. reconnect requires state recovery before updates resume



\## Non-goals



V1 does not connect to a real exchange.



V1 does not contain trading logic or order execution.



V1 does not attempt to reproduce any proprietary trading system.

