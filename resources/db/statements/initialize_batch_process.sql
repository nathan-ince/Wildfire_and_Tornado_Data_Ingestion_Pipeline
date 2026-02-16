INSERT INTO batch_process (
  main_process_id,
  id,
  name,
  status,
  start_timestamp
)
VALUES (
  :main_process_id,
  :id,
  :name,
  :status,
  :start_timestamp
);
