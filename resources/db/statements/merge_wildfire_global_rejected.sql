MERGE INTO wildfire_global_accepted_final AS final
USING wildfire_global_accepted_stage AS stage
ON (
  final.country = stage.country AND
  final.year = stage.year AND
  final.month = stage.month AND
  final.region = stage.region AND
  final.fires_count = stage.fires_count AND
  final.burned_area_hectares = stage.burned_area_hectares AND
  final.cause = stage.cause AND
  final.temperature_celsius = stage.temperature_celsius AND
  final.humidity_percent = stage.humidity_percent AND
  final.wind_speed_kmh = stage.wind_speed_kmh
)
WHEN MATCHED AND final.content_hash IS DISTINCT FROM stage.content_hash THEN
  UPDATE SET
    batch_process_id = stage.batch_process_id,
    content_hash = stage.content_hash,
    rejected_reason = stage.rejected_reason,
    country = stage.country,
    year = stage.year,
    month = stage.month,
    region = stage.region,
    fires_count = stage.fires_count,
    burned_area_hectares = stage.burned_area_hectares,
    cause = stage.cause,
    temperature_celsius = stage.temperature_celsius,
    humidity_percent = stage.humidity_percent,
    wind_speed_kmh = stage.wind_speed_kmh
WHEN NOT MATCHED THEN
  INSERT (
    batch_process_id,
    content_hash,
    rejected_reason,
    country,
    year,
    month,
    region,
    fires_count,
    burned_area_hectares,
    cause,
    temperature_celsius,
    humidity_percent,
    wind_speed_kmh
  )
  VALUES (
    stage.batch_process_id,
    stage.content_hash,
    stage.rejected_reason,
    stage.country,
    stage.year,
    stage.month,
    stage.region,
    stage.fires_count,
    stage.burned_area_hectares,
    stage.cause,
    stage.temperature_celsius,
    stage.humidity_percent,
    stage.wind_speed_kmh
  );
