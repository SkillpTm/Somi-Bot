-- name: insert_row
INSERT INTO :table_name (:column_names)
VALUES (:placeholder_values);

-- name: insert_unique_row
INSERT INTO :table_name (:column_names)
VALUES (:placeholder_values)
ON CONFLICT (:conflict_columns) DO NOTHING;

-- name: select_where
SELECT :select_columns
FROM :table_name
WHERE (:column_names) = (:placeholder_values);

-- name: update_rows_where
UPDATE :table_name
SET (:set_column_names) = (:set_placeholder_values)
WHERE (:column_names) = (:placeholder_values);

-- name: delete_rows_where
DELETE FROM :table_name
WHERE (:column_names) = (:placeholder_values);


-- name: telemetry_increment_amount
INSERT INTO telemetry (event_name, amount)
VALUES ($1, 1)
ON CONFLICT (event_name)
DO UPDATE SET amount += 1;

-- name: telemetry_total_amount
SELECT SUM(amount)
FROM telemetry;

-- name: increase_total_xp
UPDATE level
SET
    xp_cooldown = EXTRACT(EPOCH FROM NOW()) + FLOOR(RANDOM() * (65 - 55 + 1)) + 55
    total_xp = total_xp + (FLOOR(RANDOM() * (15 - 10 + 1)) + 10)
WHERE (:column_names) = (:placeholder_values);

-- name: select_user_xp_rank
SELECT user_id, total_xp, ROW_NUMBER() OVER (
    ORDER BY total_xp DESC
    WHERE (:column_names) = (:placeholder_values)
    LIMIT :limit_value
)
FROM level;