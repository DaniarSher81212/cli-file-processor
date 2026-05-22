# Базовый образ — официальный Python 3.12 на минимальном Debian (slim).
# slim весит ~50MB против ~900MB у полного образа.
FROM python:3.12-slim

# WORKDIR — рабочая папка внутри контейнера.
# Все следующие команды выполняются относительно неё.
WORKDIR /app

# Сначала копируем pyproject.toml и src/ отдельно от остального кода.
# Docker кеширует каждый слой. Если поменялся только README —
# слой с pip install не пересобирается, берётся из кеша.
COPY pyproject.toml .
COPY src/ ./src/

# Устанавливаем пакет и все зависимости из pyproject.toml.
# --no-cache-dir — не сохранять кеш pip внутри образа, экономит место.
RUN pip install --no-cache-dir .

# Создаём папки для входных и выходных данных.
RUN mkdir -p data/input data/output

# ENTRYPOINT — команда которая запускается при старте контейнера.
# docker run <image> scan → выполнится: cli-file-processor scan
ENTRYPOINT ["cli-file-processor"]

# CMD — аргументы по умолчанию если не передано ничего.
# docker run <image>      → cli-file-processor --help
CMD ["--help"]
