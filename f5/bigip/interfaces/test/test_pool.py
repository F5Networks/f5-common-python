import pytest

@pytest.mark.usefixtures("return_mock_imports")
class TestPool:
    import_modules_to_mock = ['f5.bigip']

    def test_get_description(self):
        from .. import pool
