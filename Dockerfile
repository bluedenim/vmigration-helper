FROM python:3.9

WORKDIR /code

RUN pip install --upgrade pip

# Install and setup Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN echo export PATH=\$PATH:\$HOME/.local/bin >> /root/.bashrc
