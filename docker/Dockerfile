FROM adamatics/pypoetry:3.12-1.8.1

## Install ffmpeg
# Due to base image problems
RUN chmod 1777 /tmp && apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Set working directory
WORKDIR /app

# Install via poetry
RUN poetry install

# Entrypoint Start two services
ENTRYPOINT ["poetry", "run", "pyh2r-start"]
