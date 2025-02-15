#!/# Common
# *Set Environment Variables For Local Development Only*
# command to run: source set_env.sh

# Core Settings
export ALLOWED_HOSTS="127.0.0.1,localhost"

# DB config
export POSTGRES_HOST='localhost'
export POSTGRES_PORT='5432'
export POSTGRES_USER='postgres'
export POSTGRES_PASSWORD=''
export POSTGRES_NAME='ai_code_editor'
export POSTGRES_POOL_SIZE='5'
export POSTGRES_MAX_OVERFLOW='10'

# Redis Config
export REDIS_HOST='localhost'
export REDIS_PORT='6379'
export REDIS_DB='0'
export REDIS_PASSWORD=''

# JWT Config
export JWT_SECRET_KEY="test" # only for development
export JWT_ALGORITHM="HS256"
export JWT_ACCESS_TOKEN_EXPIRE_MINUTES='1800'

# OpenAI Config
export OPENAI_API_KEY="Sorry, this key is classified! :)"
export OPENAI_API_MODEL='gpt-4o-mini'