from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    STATIC_ROOT: str = '../front/dist/' 

    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_URL: str = f'redis://{REDIS_HOST}'

    REDIS_RFAB_GLOBAL_KEY_PREFIX: str = 'rfab'

    REDIS_PLANT_MODEL_KEY_PREFIX: str = f'{REDIS_RFAB_GLOBAL_KEY_PREFIX}:plant'

    REDIS_JBOD_STAT_KEY_PREFIX: str = f'{REDIS_RFAB_GLOBAL_KEY_PREFIX}:jbodstat'
    REDIS_DUT_INFO_KEY_PREFIX: str = f'{REDIS_RFAB_GLOBAL_KEY_PREFIX}:dutinfo'

    REDIS_PLANT_UPDATE_CH_PREFIX: str = f'{REDIS_RFAB_GLOBAL_KEY_PREFIX}:update'
    REDIS_ACTION_CH_PREFIX: str = f'{REDIS_RFAB_GLOBAL_KEY_PREFIX}:action'

    REDIS_LOG_CH_NAME: str = f'{REDIS_RFAB_GLOBAL_KEY_PREFIX}:log'
    REDIS_ERROR_CH_NAME: str = f'{REDIS_RFAB_GLOBAL_KEY_PREFIX}:err'

settings = Settings()

