CREATE TYPE status AS ENUM (
  'success',
  'warning',
  'failure'
);

CREATE TABLE main_process(
  id uuid NOT NULL,
  name text NOT NULL,
  status status NOT NULL,
  start_timestamp timestamptz NOT NULL,
  final_timestamp timestamptz,
  CONSTRAINT main_process_pkey PRIMARY KEY (id)
);

CREATE TABLE batch_process(
  main_process_id uuid NOT NULL,
  id uuid NOT NULL,
  name text NOT NULL,
  status status NOT NULL,
  start_timestamp timestamptz NOT NULL,
  final_timestamp timestamptz,
  CONSTRAINT batch_process_pkey PRIMARY KEY (id),
  CONSTRAINT batch_process_main_process_id_fkey FOREIGN KEY (main_process_id)
    REFERENCES main_process(id)
    ON UPDATE NO ACTION
    ON DELETE CASCADE
);

CREATE TABLE wildfire_global_accepted (
  batch_process_id uuid NOT NULL,
  id integer GENERATED ALWAYS AS IDENTITY,
  country text NOT NULL,
  year smallint NOT NULL,
  month varchar(9) NOT NULL,
  region text NOT NULL,
  firest_count smallint NOT NULL,
  burned_area_hectares integer NOT NULL,
  cause text NOT NULL,
  temperature_celsius smallint NOT NULL,
  humidity_percent smallint NOT NULL,
  wind_speed_kmh smallint NOT NULL,
  CONSTRAINT wildfire_global_accepted_pkey PRIMARY KEY (id),
  CONSTRAINT wildfire_global_accepted_batch_process_id_fkey FOREIGN KEY (batch_process_id)
    REFERENCES batch_process(id)
    ON UPDATE NO ACTION
    ON DELETE CASCADE
);

CREATE TABLE wildfire_global_rejected (
  batch_process_id uuid NOT NULL,
  id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
  country text,
  year text,
  month text,
  region text,
  firest_count text,
  burned_area_hectares text,
  cause text,
  temperature_celsius text,
  humidity_percent text,
  wind_speed_kmh text,
  CONSTRAINT wildfire_global_rejected_pkey PRIMARY KEY (id),
  CONSTRAINT wildfire_global_rejected_batch_process_id_fkey FOREIGN KEY (batch_process_id)
    REFERENCES batch_process(id)
    ON UPDATE NO ACTION
    ON DELETE CASCADE
);

CREATE TABLE tornado_usa_accepted (
  batch_process_id uuid NOT NULL,
  id integer GENERATED ALWAYS AS IDENTITY,
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
  CONSTRAINT tornado_usa_accepted_pkey PRIMARY KEY (id),
  CONSTRAINT tornado_usa_accepted_batch_process_id_fkey FOREIGN KEY (batch_process_id)
    REFERENCES batch_process(id)
    ON UPDATE NO ACTION
    ON DELETE CASCADE
);

CREATE TABLE tornado_usa_rejected (
  batch_process_id uuid NOT NULL,
  id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
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
  CONSTRAINT tornado_usa_pkey PRIMARY KEY (id),
  CONSTRAINT tornado_usa_batch_process_id_fkey FOREIGN KEY (batch_process_id)
    REFERENCES batch_process(id)
    ON UPDATE NO ACTION
    ON DELETE CASCADE
);
