import pandas as pd
from unittest.mock import MagicMock

import project.pipelines.wildfire_global.transform as wildfire_transform_module


def test_transform_valid():
    wildfire_transform_module.rename_columns = lambda config, source_index, df: df

    accepted = pd.DataFrame({"id": [1, 1, 2]})
    rejected = pd.DataFrame({"id": [99], "rejected_reason": ["bad"]})
    wildfire_transform_module.validate_chain = lambda df, funcs: (accepted, rejected)

    wildfire_transform_module.compute_record_hash_series_exclude = (lambda df, exclude=None: pd.Series(["H"] * len(df), index=df.index))

    out_accepted, out_rejected = wildfire_transform_module.transform(config=MagicMock(), source_index=0, df=pd.DataFrame({"x": [0]}))

    assert out_accepted["id"].tolist() == [1, 2]
    assert "content_hash" in out_accepted.columns
    assert "content_hash" in out_rejected.columns