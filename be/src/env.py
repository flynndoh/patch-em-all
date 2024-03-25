from pydantic_settings import BaseSettings, SettingsConfigDict


class Env(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', secrets_dir='/run/secrets',
                                      case_sensitive=False)

    dsn: str
    cookie_max_age: int = 60 * 60 * 24 * 365 * 5  # I won't be around in 5 years to deal with this
    auth_secret: str


environment = Env()
