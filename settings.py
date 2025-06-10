from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).parent
ENV_FILE = Path(__file__).parent / ".env"


class OctopusSettings(BaseSettings):
    ftp_host: str = "ftp_host"
    ftp_user: str = "ftp_user"
    ftp_password: str = "ftp_password"
    ftp_path: str = "ftp_path"

    path_to_file: Path = BASE_DIR / "files"

    email: str = "my_email@technolight.ru"
    password: str = "mypassword"

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


class Settings(BaseSettings):
    octopus_settings: OctopusSettings = OctopusSettings()


settings = Settings()
