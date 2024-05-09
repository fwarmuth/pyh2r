FROM adamatics/pypoetry:3.12-1.8.1

# Copy project files
COPY . /app

# Set working directory
WORKDIR /app

# Install via poetry
RUN poetry install

# Entrypoint Start two services
ENTRYPOINT ["poetry", "run", "pyh2r-start"]

