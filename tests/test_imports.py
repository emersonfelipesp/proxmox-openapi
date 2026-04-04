"""Test that all modules can be imported successfully."""


def test_import_main():
    """Test that main module can be imported."""
    import proxmox_openapi.main

    assert proxmox_openapi.main is not None


def test_import_mock_main():
    """Test that mock_main module can be imported."""
    import proxmox_openapi.mock_main

    assert proxmox_openapi.mock_main is not None


def test_import_schema():
    """Test that schema module can be imported."""
    import proxmox_openapi.schema

    assert proxmox_openapi.schema is not None


def test_import_exception():
    """Test that exception module can be imported."""
    import proxmox_openapi.exception

    assert proxmox_openapi.exception is not None


def test_import_logger():
    """Test that logger module can be imported."""
    import proxmox_openapi.logger

    assert proxmox_openapi.logger is not None
