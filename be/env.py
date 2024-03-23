from pydantic_settings import BaseSettings, SettingsConfigDict


class PrivateEnv(BaseSettings):
    model_config = SettingsConfigDict(env_file='.private.env', env_file_encoding='utf-8', case_sensitive=False)
    auth_secret: str


class Env(BaseSettings):
    private: PrivateEnv = PrivateEnv()
    dsn: str


environment = Env(_env_file='.env', _env_file_encoding='utf-8')
