import pytest
from pathlib import Path
from buscador_pep.config import read_configuration, Configuration

def test_read_configuration_valid(tmp_path: Path):
    # Crear un archivo de configuración válido
    config_file = tmp_path / "config.toml"
    config_file.write_text(
        """
        [user_profile]
        overview = "Resumen de prueba"
        [user_profile.filters]
        location = "Test Location"
        industry = "Test Industry"
        job_opening_status = "Test Status"
        job_category = "Test Category"
        pay_range = "Test Range"
        legal_status = "Test Legal"
        """
    )
    config = read_configuration(config_file)
    # Verificar valores
    assert config.portal_url == "https://www.empleospublicos.cl/"
    assert config.user_profile.overview == "Resumen de prueba"
    filters = config.user_profile.filters
    assert filters.location == "Test Location"
    assert filters.industry == "Test Industry"
    assert filters.job_opening_status == "Test Status"
    assert filters.job_category == "Test Category"
    assert filters.pay_range == "Test Range"
    assert filters.legal_status == "Test Legal"

def test_read_configuration_missing_user_profile(tmp_path: Path):
    # Crear un archivo sin la clave 'user_profile'
    config_file = tmp_path / "config.toml"
    config_file.write_text(
        """
        some_other_key = "valor"
        """
    )
    with pytest.raises(KeyError):
        read_configuration(config_file)
