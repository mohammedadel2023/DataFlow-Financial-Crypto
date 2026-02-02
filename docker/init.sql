-- create batch table that will sotre the batch data (scraped)
CREATE TABLE IF NOT EXISTS batch_data (
    id BIGSERIAL PRIMARY KEY,
    content_hash CHAR(64) UNIQUE NOT NULL, -- (Title + Publish Date) to check buplicate 
    title TEXT NOT NULL,
    publish_date DATE,
    scraped_at TIMESTAMPTZ DEFAULT NOW()
);

-- create stream table that will sotre the stream data
CREATE TABLE IF NOT EXISTS stream_data (
    id BIGSERIAL PRIMARY KEY,
    content_hash CHAR(64) UNIQUE NOT NULL, -- (Unique Content Identifier)
    title TEXT NOT NULL,
    summary_text TEXT,                     -- Text version for RAG context
    scraped_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Optimization Indexes
-- Instant cleanup index for the 30-day rule
CREATE INDEX idx_stream_ttl ON stream_data (scraped_at);
-- Cleanup index for batch if you decide to prune it later
CREATE INDEX idx_batch_ttl ON batch_data (scraped_at);

-- Full-Text Search (For your RAG to find relevant hashes by keyword)
CREATE INDEX idx_batch_title_search ON batch_data USING gin(to_tsvector('english', title));