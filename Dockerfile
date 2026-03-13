FROM python:3.9
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install -y \
    curl \
    vim

RUN useradd -u 1000 -g root -s /bin/bash -m vmigration
USER vmigration

WORKDIR /code

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# RUN echo export PATH=\$PATH:\$HOME/.local/bin >> /root/.bashrc
ENV HOME=/home/vmigration

# NOTE: $HOME, not ${HOME}
ENV PATH="$HOME/.local/bin:${PATH}"

COPY --chown=vmigration:root . /code

RUN uv sync 
