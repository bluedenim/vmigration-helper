FROM python:3

WORKDIR /code

RUN pip install --upgrade pip

# Install and setup Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
RUN echo export PATH=\$PATH:\$HOME/.poetry/bin >> /root/.bashrc
