INSERT INTO batch_process (
  main_process_id,
  id,
  status,
  start_timestamp
)
VALUES (
  :main_process_id,
  :id,
  :status,
  :start_timestamp
);
