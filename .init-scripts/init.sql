CREATE TABLE IF NOT EXISTS messages (
    msg_id BIGINT PRIMARY KEY,
    chat_id BIGINT,
    chat_name TEXT,
    sender_id BIGINT,
    sender_name TEXT,
    sender_username TEXT,
    text TEXT,
    ocr_text TEXT,
    image_base64 TEXT,
    timestamp TIMESTAMP
);

