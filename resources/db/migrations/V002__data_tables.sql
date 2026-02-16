CREATE TABLE wildfire_global_accepted_final (
  batch_process_id uuid NOT NULL,
  id bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
  content_hash text NOT NULL,
  country text NOT NULL,
  year smallint NOT NULL,
  month varchar(9) NOT NULL,
  region text NOT NULL,
  fires_count smallint NOT NULL,
  burned_area_hectares integer NOT NULL,
  cause text NOT NULL,
  temperature_celsius smallint NOT NULL,
  humidity_percent smallint NOT NULL,
  wind_speed_kmh smallint NOT NULL,
  CONSTRAINT wildfire_global_accepted_batch_process_id_fkey FOREIGN KEY (batch_process_id)
    REFERENCES batch_process(id)
    ON UPDATE NO ACTION
    ON DELETE CASCADE,
  CONSTRAINT wildfire_global_accepted_pkey PRIMARY KEY (id),
  CONSTRAINT wildfire_global_accepted_content_key UNIQUE (
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
);

CREATE TABLE wildfire_global_accepted_stage (
  batch_process_id uuid NOT NULL,
  content_hash text NOT NULL,
  country text NOT NULL,
  year smallint NOT NULL,
  month varchar(9) NOT NULL,
  region text NOT NULL,
  fires_count smallint NOT NULL,
  burned_area_hectares integer NOT NULL,
  cause text NOT NULL,
  temperature_celsius smallint NOT NULL,
  humidity_percent smallint NOT NULL,
  wind_speed_kmh smallint NOT NULL
);

CREATE TABLE wildfire_global_rejected_final (
  batch_process_id uuid NOT NULL,
  id bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
  content_hash text NOT NULL,
  rejected_reason text NOT NULL,
  country text,
  year text,
  month text,
  region text,
  fires_count text,
  burned_area_hectares text,
  cause text,
  temperature_celsius text,
  humidity_percent text,
  wind_speed_kmh text,
  CONSTRAINT wildfire_global_rejected_batch_process_id_fkey FOREIGN KEY (batch_process_id)
    REFERENCES batch_process(id)
    ON UPDATE NO ACTION
    ON DELETE CASCADE,
  CONSTRAINT wildfire_global_rejected_pkey PRIMARY KEY (id),
  CONSTRAINT wildfire_global_rejected_content_key UNIQUE (
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
);

CREATE TABLE wildfire_global_rejected_stage (
  batch_process_id uuid NOT NULL,
  content_hash text NOT NULL,
  rejected_reason text NOT NULL,
  country text,
  year text,
  month text,
  region text,
  fires_count text,
  burned_area_hectares text,
  cause text,
  temperature_celsius text,
  humidity_percent text,
  wind_speed_kmh text
);

CREATE TABLE tornado_usa_accepted_final (
  batch_process_id uuid NOT NULL,
  id bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
  content_hash text NOT NULL,
  year smallint NOT NULL,
  month smallint NOT NULL,
  day smallint NOT NULL,
  date date NOT NULL,
  state character(2) NOT NULL,
  magnitude smallint NOT NULL,
  injury_count smallint NOT NULL,
  fatality_count smallint NOT NULL,
  latitude_start real NOT NULL,
  latitude_end real NOT NULL,
  longitude_start real NOT NULL,
  longitude_end real NOT NULL,
  length_miles real NOT NULL,
  width_yards smallint NOT NULL,
  CONSTRAINT tornado_usa_accepted_batch_process_id_fkey FOREIGN KEY (batch_process_id)
    REFERENCES batch_process(id)
    ON UPDATE NO ACTION
    ON DELETE CASCADE,
  CONSTRAINT tornado_usa_accepted_pkey PRIMARY KEY (id),
  CONSTRAINT tornado_usa_accepted_content_key UNIQUE (
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
);

CREATE TABLE tornado_usa_accepted_stage (
  batch_process_id uuid NOT NULL,
  content_hash text NOT NULL,
  year smallint NOT NULL,
  month smallint NOT NULL,
  day smallint NOT NULL,
  date date NOT NULL,
  state character(2) NOT NULL,
  magnitude smallint NOT NULL,
  injury_count smallint NOT NULL,
  fatality_count smallint NOT NULL,
  latitude_start real NOT NULL,
  latitude_end real NOT NULL,
  longitude_start real NOT NULL,
  longitude_end real NOT NULL,
  length_miles real NOT NULL,
  width_yards smallint NOT NULL
);

CREATE TABLE tornado_usa_rejected_final (
  batch_process_id uuid NOT NULL,
  id bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
  content_hash text NOT NULL,
  rejected_reason text NOT NULL,
  year text,
  month text,
  day text,
  date text,
  state text,
  magnitude text,
  injury_count text,
  fatality_count text,
  latitude_start text,
  latitude_end text,
  longitude_start text,
  longitude_end text,
  length_miles text,
  width_yards text,
  CONSTRAINT tornado_usa_batch_process_id_fkey FOREIGN KEY (batch_process_id)
    REFERENCES batch_process(id)
    ON UPDATE NO ACTION
    ON DELETE CASCADE,
  CONSTRAINT tornado_usa_pkey PRIMARY KEY (id),
  CONSTRAINT tornado_usa_rejected_content_key UNIQUE (
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
);

CREATE TABLE tornado_usa_rejected_stage (
  batch_process_id uuid NOT NULL,
  content_hash text NOT NULL,
  rejected_reason text NOT NULL,
  year text,
  month text,
  day text,
  date text,
  state text,
  magnitude text,
  injury_count text,
  fatality_count text,
  latitude_start text,
  latitude_end text,
  longitude_start text,
  longitude_end text,
  length_miles text,
  width_yards text
);
