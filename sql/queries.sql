-- name: insert
INSERT INTO :_table (:_columns)
VALUES (:_values);

-- name: delete_where
DELETE FROM :_table
WHERE (:_where_columns) = (:_where_values)
LIMIT :_limit;

-- name: update_where
UPDATE :_table
SET :_columns = :_values
WHERE (:_where_columns) = (:_where_values)
LIMIT :_limit;

-- name: select_where
SELECT :_selects
FROM :_table
WHERE (:_where_columns) = (:_where_values)
ORDER BY :_order
LIMIT :_limit;


-- name: insert_unique
INSERT INTO :_table (:_columns)
SELECT :_values
WHERE NOT EXISTS (
    SELECT *
    FROM :_table 
    WHERE (:_where_columns) = (:_where_values)
);

-- name: telemetry_increment
INSERT INTO :_table (:_columns) 
VALUES (:_values)
ON DUPLICATE KEY UPDATE amount = amount + 1;

-- name: user_rank
SELECT rank FROM (
    SELECT ROW_NUMBER() OVER (ORDER BY xp DESC) as rank
    FROM level
    WHERE server = %s
) r
WHERE user = %s;