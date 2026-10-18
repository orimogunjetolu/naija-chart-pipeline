-- How did each song move since its previous chart day?
CREATE OR REPLACE VIEW chart_movement AS
SELECT
    chart_date,
    position,
    title,
    artist,
    LAG(position) OVER (PARTITION BY track_id ORDER BY chart_date) AS prev_position,
    LAG(position) OVER (PARTITION BY track_id ORDER BY chart_date) - position AS places_gained
FROM chart_entries;
