# Copyright 2019 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of Agenoria and is released under the MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.

VERSION 0.7
PROJECT jiuguangw/agenoria

FROM python:3.10
WORKDIR /agenoria

# Install dependencies from pyproject.toml
deps:
    # Convert the dependencies from pyproject.toml into requirements.txt and pip install them
    COPY pyproject.toml ./pyproject.toml
    RUN pip install toml-to-requirements
    RUN toml-to-req --toml-file pyproject.toml --include-optional --optional-lists dev
    RUN pip install -r requirements.txt

# Install package
install:
    FROM +deps
    COPY . .
    RUN pip install -e .[dev]

# Run pre-commit
lint:
    FROM +install
    RUN pre-commit run --all-files

# Run pytest and save coverage report
test:
    FROM +install
    RUN pytest --cov=./ --cov-report=xml
    SAVE ARTIFACT coverage.xml AS LOCAL coverage.xml

all:
    BUILD +lint
    BUILD +test
