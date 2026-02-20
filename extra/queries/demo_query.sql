SELECT
	mp.id AS main_process_id,
	mp.name AS main_process_name,
	bp.id AS bp_id,
	bp.status AS bp_status,
	bp.start_timestamp AS bp_start_timestamp,
	bp.final_timestamp as bp_final_timestamp, (
		SELECT count(*)
		FROM tornado_usa_accepted_final AS ta
		WHERE ta.batch_process_id = bp.id) AS ta_changed_count, (
		SELECT count(*) AS wgac
		FROM tornado_usa_rejected_final AS tr
		WHERE tr.batch_process_id = bp.id) AS tr_changecount, (
		SELECT count(*)
		FROM wildfire_global_accepted_final AS wa
		WHERE wa.batch_process_id = bp.id) AS wa_count, (
		SELECT count(*)
		FROM wildfire_global_rejected_final AS wr
		WHERE wr.batch_process_id = bp.id) AS wr_count
FROM main_process AS mp
LEFT JOIN batch_process AS bp
ON mp.id = bp.main_process_id
ORDER BY bp.start_timestamp;