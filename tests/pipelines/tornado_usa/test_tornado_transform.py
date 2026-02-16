import pandas as pd
import project.pipelines.tornado_usa.transform as tmod


def test_transform_moves_dupes_into_rejected(monkeypatch):

    df_in = pd.DataFrame({"x": [1, 1, 2]})


    monkeypatch.setattr(tmod, "rename_columns", lambda config, source_index, df: df)


    df_accepted = pd.DataFrame({"id": [1, 1, 2]})
    df_rejected = pd.DataFrame({"id": [99], "reason": ["bad"]})
    monkeypatch.setattr(tmod, "validate_chain", lambda df, funcs: (df_accepted, df_rejected))


    df_accepted_deduped = pd.DataFrame({"id": [1, 2]})
    df_dupes = pd.DataFrame({"id": [1], "reason": ["duplicate"]})
    monkeypatch.setattr(tmod, "dedupe_keep_first", lambda df: (df_accepted_deduped, df_dupes))

    out_accepted, out_rejected = tmod.transform(config=None, source_index=0, df=df_in)

    assert out_accepted.reset_index(drop=True).equals(df_accepted_deduped.reset_index(drop=True))
    assert len(out_rejected) == 2  
    assert sorted(out_rejected["id"].tolist()) == [1, 99]