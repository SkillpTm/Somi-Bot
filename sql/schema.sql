CREATE TABLE IF NOT EXISTS telemetry (
    event_name VARCHAR(64) PRIMARY KEY,
    amount BIGINT NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS user (
    id BIGINT PRIMARY KEY,
    last_fm_username VARCHAR(255),
    weather_location VARCHAR(255) NOT NULL DEFAULT 'seoul',
	timezone VARCHAR(64) NOT NULL DEFAULT 'Asia/Seoul'
);

CREATE TABLE IF NOT EXISTS reminder (
    id INT PRIMARY KEY CHECK (id BETWEEN 100000000 AND 999999999),
    user BIGINT NOT NULL,
    reminder_time BIGINT NOT NULL,
    link VARCHAR(255) NOT NULL,
    message VARCHAR(4096) NOT NULL,

	FOREIGN KEY (user) REFERENCES user(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS server (
    id BIGINT PRIMARY KEY,
    default_role_id BIGINT,
	ban_log BIGINT,
	bot_command_log BIGINT,
	delete_log BIGINT,
	edit_log BIGINT,
	join_log BIGINT,
	kick_log BIGINT,
	leave_log BIGINT,
	mute_log BIGINT,
	name_log BIGINT,
	purge_log BIGINT,
	remove_log BIGINT,
	unban_log BIGINT,
	unmute_log BIGINT
);

CREATE TABLE IF NOT EXISTS hidden_channel (
    id BIGINT PRIMARY KEY,
    server BIGINT NOT NULL,

	FOREIGN KEY (server) REFERENCES server(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS level_ignore_channel (
    id BIGINT PRIMARY KEY,
    server BIGINT NOT NULL,

	FOREIGN KEY (server) REFERENCES server(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS level_role (
    id BIGINT PRIMARY KEY,
    server BIGINT NOT NULL,
	level SMALLINT NOT NULL,

	FOREIGN KEY (server) REFERENCES server(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS custom_command (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    server BIGINT NOT NULL,
    name VARCHAR(64) NOT NULL,
    text VARCHAR(1023) NOT NULL,

	FOREIGN KEY (server) REFERENCES server(id) ON DELETE CASCADE,
	UNIQUE KEY unique_server_name (server, name)
);

CREATE TABLE IF NOT EXISTS keyword (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
	user BIGINT NOT NULL,
    server BIGINT NOT NULL,
	keyword VARCHAR(64) NOT NULL,

	FOREIGN KEY (user) REFERENCES user(id) ON DELETE CASCADE,
	FOREIGN KEY (server) REFERENCES server(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS feedback (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
	user BIGINT NOT NULL,
    server BIGINT NOT NULL,
	message VARCHAR(4096) NOT NULL,
	created_at BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS level (
	id BIGINT AUTO_INCREMENT PRIMARY KEY,
	user BIGINT NOT NULL,
    server BIGINT NOT NULL,
    cooldown BIGINT NOT NULL DEFAULT 0,
    xp BIGINT NOT NULL DEFAULT 0,

	FOREIGN KEY (server) REFERENCES server(id) ON DELETE CASCADE,
	UNIQUE KEY unique_user_server (user, server)
);

CREATE TABLE IF NOT EXISTS statistic (
	id BIGINT AUTO_INCREMENT PRIMARY KEY,
	user BIGINT NOT NULL,
    server BIGINT NOT NULL,
    attachment_count BIGINT NOT NULL DEFAULT 0,
	bot_command_count BIGINT NOT NULL DEFAULT 0,
    char_count BIGINT NOT NULL DEFAULT 0,
	delete_count BIGINT NOT NULL DEFAULT 0,
	edit_count BIGINT NOT NULL DEFAULT 0,
    emote_count BIGINT NOT NULL DEFAULT 0,
    link_count BIGINT NOT NULL DEFAULT 0,
    message_count BIGINT NOT NULL DEFAULT 0,
	reaction_count BIGINT NOT NULL DEFAULT 0,
    reply_count BIGINT NOT NULL DEFAULT 0,
    sticker_count BIGINT NOT NULL DEFAULT 0,
    word_count BIGINT NOT NULL DEFAULT 0,

	FOREIGN KEY (user) REFERENCES user(id) ON DELETE CASCADE,
	FOREIGN KEY (server) REFERENCES server(id) ON DELETE CASCADE,
	UNIQUE KEY unique_user_server (user, server)
);