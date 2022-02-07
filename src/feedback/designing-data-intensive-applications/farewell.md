1. Distributed transaction limits
2. Batch processing with Stream, vice versa
3. No-SQL(low-level) v.s. SQL(high level) -> derived data system v.s. database
    - un-bundling databases
    - database inside out -> secondary index/full text search/...
    - derived system as application code
    - database not a variable(don't know about changed)
4. transaction drawback
    - not good at distributed
    - application flaws also affect data
    - network break on TCP closing (client-server or server-db) cause duplicate
5. separate integrity and concurrency(timelines)

--8<-- "abbreviations/ddia.md"
