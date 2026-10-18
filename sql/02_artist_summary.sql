-- Which artists dominate the Nigerian chart?
CREATE OR REPLACE VIEW artist_summary AS
SELECT
    artist,
    COUNT(DISTINCT track_id)  AS songs_charted,
    MIN(position)             AS best_position,
    COUNT(DISTINCT chart_date) AS days_on_chart
FROM chart_entries
GROUP BY artist
ORDER BY songs_charted DESC, best_position;
