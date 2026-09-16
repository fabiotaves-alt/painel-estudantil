from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Aplicação
    app_name: str = "Dashboard Acadêmico API"
    app_version: str = "0.1.0"
    debug: bool = False

    # Servidor
    host: str = "127.0.0.1"
    port: int = 8000

    # Banco de dados
    database_url: str = "sqlite+aiosqlite:///./dashboard.db"

    # Segurança
    api_token_header: str = "X-API-Token"

    @property
    def api_url(self) -> str:
        return f"http://{self.host}:{self.port}"


settings = Settings()
