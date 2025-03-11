-- name: create_telemetry
CREATE TABLE IF NOT EXISTS telemetry (
    telemetry_id SERIAL PRIMARY KEY,
    event_name TEXT UNIQUE NOT NULL,
    amount BIGINT NOT NULL DEFAULT 1
);


-- name: create_user
CREATE TABLE IF NOT EXISTS "user" (
    user_id BIGINT PRIMARY KEY,
    last_fm_username TEXT DEFAULT '',
    weather_location TEXT DEFAULT 'seoul'
);

-- name: create_reminder
CREATE TABLE IF NOT EXISTS reminder (
    reminder_id INT CHECK (reminder_id BETWEEN 100000000 AND 999999999) PRIMARY KEY,
    user_id BIGINT REFERENCES "user"(user_id) NOT NULL,
    time BIGINT NOT NULL,
    message_link TEXT NOT NULL,
    message TEXT NOT NULL
);


-- name: create_server
CREATE TABLE IF NOT EXISTS server (
    server_id BIGINT PRIMARY KEY,
    audit_log_channel_id BIGINT DEFAULT 0,
    default_role_id BIGINT  DEFAULT 0
);

-- name: create_hidden_channel
CREATE TABLE IF NOT EXISTS hidden_channel (
    channel_id BIGINT PRIMARY KEY,
    server_id BIGINT REFERENCES server(server_id) NOT NULL
);

-- name: create_level_ignore_channel
CREATE TABLE IF NOT EXISTS level_ignore_channel (
    channel_id BIGINT PRIMARY KEY,
    server_id BIGINT REFERENCES server(server_id) NOT NULL
);

-- name: create_level_role
CREATE TABLE IF NOT EXISTS level_role (
    role_id BIGINT PRIMARY KEY,
    server_id BIGINT REFERENCES server(server_id) NOT NULL,
    level SMALLINT NOT NULL
);

-- name: create_custom_command
CREATE TABLE IF NOT EXISTS custom_command (
    custom_command_id SERIAL PRIMARY KEY,
    server_id BIGINT REFERENCES server(server_id) NOT NULL,
    command_name TEXT NOT NULL,
    command_text TEXT NOT NULL
);


-- name: create_keyword
CREATE TABLE IF NOT EXISTS keyword (
    keyword_id SERIAL PRIMARY KEY,
    server_id BIGINT REFERENCES server(server_id) NOT NULL,
    user_id BIGINT REFERENCES "user"(user_id) NOT NULL,
    keyword TEXT NOT NULL
);

-- name: create_feedback
CREATE TABLE IF NOT EXISTS feedback (
    feedback_id SERIAL PRIMARY KEY,
    server_id BIGINT REFERENCES server(server_id) NOT NULL,
    user_id BIGINT REFERENCES "user"(user_id) NOT NULL,
    time_stamp TEXT NOT NULL,
    message TEXT NOT NULL
);

-- name: create_level
CREATE TABLE IF NOT EXISTS level (
    server_id BIGINT REFERENCES server(server_id),
    user_id BIGINT REFERENCES "user"(user_id),
    PRIMARY KEY (server_id, user_id),
    xp_cooldown BIGINT NOT NULL DEFAULT 0,
    total_xp BIGINT NOT NULL DEFAULT 0
);

-- name: create_statistic
CREATE TABLE IF NOT EXISTS statistic (
    server_id BIGINT REFERENCES server(server_id) NOT NULL,
    user_id BIGINT REFERENCES "user"(user_id) NOT NULL,
    PRIMARY KEY (server_id, user_id),
    attachment_count BIGINT NOT NULL DEFAULT 0,
    char_count BIGINT NOT NULL DEFAULT 0,
    client_command_count BIGINT NOT NULL DEFAULT 0,
    emote_count BIGINT NOT NULL DEFAULT 0,
    link_count BIGINT NOT NULL DEFAULT 0,
    message_count BIGINT NOT NULL DEFAULT 0,
    reply_count BIGINT NOT NULL DEFAULT 0,
    sticker_count BIGINT NOT NULL DEFAULT 0,
    word_count BIGINT NOT NULL DEFAULT 0
);