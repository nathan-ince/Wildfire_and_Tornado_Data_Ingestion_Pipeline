MERGE INTO tornado_usa_accepted_final AS final
USING tornado_usa_accepted_stage AS stage
ON (
  final.year = stage.year AND
  final.month = stage.month AND
  final.day = stage.day AND
  final.date = stage.date AND
  final.state = stage.state AND
  final.magnitude = stage.magnitude AND
  final.injury_count = stage.injury_count AND
  final.fatality_count = stage.fatality_count AND
  final.latitude_start = stage.latitude_start AND
  final.latitude_end = stage.latitude_end AND
  final.longitude_start = stage.longitude_start AND
  final.longitude_end = stage.longitude_end AND
  final.length_miles = stage.length_miles AND
  final.width_yards = stage.width_yards
)
WHEN MATCHED AND final.content_hash IS DISTINCT FROM stage.content_hash THEN
  UPDATE SET
    batch_process_id = stage.batch_process_id,
    content_hash = stage.content_hash,
    year = stage.year,
    month = stage.month,
    day = stage.day,
    date = stage.date,
    state = stage.state,
    magnitude = stage.magnitude,
    injury_count = stage.injury_count,
    fatality_count = stage.fatality_count,
    latitude_start = stage.latitude_start,
    latitude_end = stage.latitude_end,
    longitude_start = stage.longitude_start,
    longitude_end = stage.longitude_end,
    length_miles = stage.length_miles,
    width_yards = stage.width_yards
WHEN NOT MATCHED THEN
  INSERT (
    batch_process_id,
    content_hash,
    year,
    month,
    day,
    date,
    state,
    magnitude,
    injury_count,
    fatality_count,
    latitude_start,
    latitude_end,
    longitude_start,
    longitude_end,
    length_miles,
    width_yards
  )
  VALUES (
    stage.batch_process_id,
    stage.content_hash,
    stage.year,
    stage.month,
    stage.day,
    stage.date,
    stage.state,
    stage.magnitude,
    stage.injury_count,
    stage.fatality_count,
    stage.latitude_start,
    stage.latitude_end,
    stage.longitude_start,
    stage.longitude_end,
    stage.length_miles,
    stage.width_yards
  );
