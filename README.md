# Moni Score
## Entorno de produccion

- Clonar ambos repositorios: Este mismo y el del [frontend](https://github.com/juansa6201/moni_score_test_front/).
- Pararse en la carpeta del backend.
- Modificar las variables de entorno. El ejemplo tiene la configuración necesaria. ACLARACION: Descomentar las lineas correspondientes a la db postgres.

  ```sh
  cp .env.example .env
  ```
- Correr el archivo docker-compose.yml.
  ```sh
  docker-compose up
  ```

## Entorno de desarrollo

- Instalar [pipenv](https://pipenv.pypa.io/en/latest/).

- Instalar las dependencias del proyecto

  ```sh
  PIPENV_VENV_IN_PROJECT=1 pipenv install --dev
  ```

- Modificar las variables de entorno. El ejemplo tiene la configuración necesaria para levantar un entorno de dev

  ```sh
  cp .env.example .env
  ```

- Levantar una shell con pipenv (activa el virtualenv generado y carga las variables de entorno)

  ```sh
  pipenv shell
  ```

  También se puede usar `pipenv run` para ejecutar comandos dentro del virtualenv.

- Instalar los pre-commit hooks. Esto va a ejecutar lo mismo que `pipenv run lint` antes de hacer un commit.

  ```sh
  pre-commit install
  ```

- Lint manual.

  ```sh
  pipenv run lint
  ```

## Scripts

- `pipenv run dev` Iniciar el servidor de desarrollo
- `pipenv run lint` Ejecuta el pre-commit hook (black, flake8, mypy, etc)
- `pipenv run mypy` Ejecuta mypy (checkeo de tipado estático)
