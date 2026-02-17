from pandas import DataFrame
from project.models.config import Config

def rename_columns(config: Config, source_index: int, df: DataFrame):
  source = config.sources[source_index]
  return df[list(source.mapping.keys())].rename(columns={mapping[0]: mapping[1].name for mapping in source.mapping.items()})