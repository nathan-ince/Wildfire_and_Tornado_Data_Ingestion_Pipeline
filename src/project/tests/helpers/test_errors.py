from project.helpers.errors import AbstractError


def test_abstract_error_stores_message_and_kwargs():
    err = AbstractError("failed", "bad input", foo="bar")

    assert err.message == "failed :: bad input"
    assert err.kwargs["error"] == "AbstractError"
    assert err.kwargs["foo"] == "bar"