# Definimos la versión de Python que queremos utilizar
ARG PYTHON_VERSION=3.10.4

FROM python:${PYTHON_VERSION}-alpine AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app

# Creamos un usuario para ejecutar nuestra aplicación
RUN adduser -u 5678 --disabled-password --gecos "" python && chown -R python /app
USER python

# Etapa de construcción
FROM base AS build

# Copiamos los archivos Pipfile y Pipfile.lock a la imagen
COPY --chown=python:python Pipfile* ./

# Instalamos pipenv y creamos el entorno virtual
RUN pip install pipenv && \
    PIP_DISABLE_PIP_VERSION_CHECK=1 PIPENV_VENV_IN_PROJECT=1 python -m pipenv install --deploy

# Etapa de producción
FROM base AS prod

# Agregamos el directorio del entorno virtual al PATH
ENV PATH=/app/.venv/bin:$PATH

# Copiamos el entorno virtual desde la etapa de construcción
COPY --from=build /app/.venv /app/.venv/

# Copiamos el resto de los archivos de nuestra aplicación
COPY --chown=python:python . .

# Definimos el punto de entrada y los argumentos por defecto
ENTRYPOINT [ "/app/docker-entrypoint.sh" ]
CMD [ "-k", "config.worker.ScoringUvicornWorker", "-b", "0.0.0.0" ]
