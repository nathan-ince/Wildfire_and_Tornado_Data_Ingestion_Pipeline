from project.orchestration.types import Status


def test_status_values():
    assert Status.get_value_set() == {"running", "success", "warning", "failure"}


def test_status_define():
    assert Status.define("success", log_error=False) is Status.Success