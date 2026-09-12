\# Market Feed Reliability Lab



A small testbed for failure handling in WebSocket market-data feeds.



The feed is synthetic. It is not tied to a real exchange.



The main idea is simple: a live socket does not always mean the local market state is valid.



\## What it covers



\- snapshot and incremental updates

\- sequence checks

\- duplicate updates

\- missing updates

\- reordered updates

\- state invalidation

\- reconnect handling

\- snapshot-based recovery



\## Example



A healthy feed stays valid:



```text

healthy            valid=True  seq=103 applied=3 duplicates=0 invalidations=0

```



A duplicate is counted but does not corrupt state:



```text

duplicate          valid=True  seq=103 applied=3 duplicates=1 invalidations=0

```



A sequence gap invalidates the local state:



```text

sequence gap       valid=False seq=101 applied=1 duplicates=0 invalidations=1

```



After a reconnect, a fresh snapshot restores state before updates continue:



```text

reconnect          valid=True  seq=201 applied=2 duplicates=0 invalidations=1

```



\## Run it



Python 3.14 or newer is required.



```bash

python -m venv .venv

python -m pip install -e ".\[dev]"

python -m pytest -q

python examples/run\_demo.py

```



\## Layout



```text

src/market\_feed\_lab/

&#x20;   client.py

&#x20;   faults.py

&#x20;   metrics.py

&#x20;   orderbook.py

&#x20;   protocol.py

&#x20;   server.py



tests/

examples/

docs/

```



\## Notes



This project focuses on feed integrity and recovery behavior.



It does not connect to a real exchange, place orders, or contain trading strategy code.
