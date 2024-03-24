from pydantic_settings import BaseSettings, SettingsConfigDict


class PrivateEnv(BaseSettings):
    model_config = SettingsConfigDict(env_file='.private.env', env_file_encoding='utf-8', case_sensitive=False)
    auth_secret: str


class Env(BaseSettings):
    private: PrivateEnv = PrivateEnv()
    dsn: str
    cookie_max_age: int = 60 * 60 * 24 * 365 * 5  # I won't be around in 5 years to deal with this

environment = Env(_env_file='.env', _env_file_encoding='utf-8')
