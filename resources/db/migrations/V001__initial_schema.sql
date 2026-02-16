CREATE TYPE status AS ENUM (
  'success',
  'warning',
  'failure',
  'running'
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