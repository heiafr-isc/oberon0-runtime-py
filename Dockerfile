# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

FROM python:3.12

WORKDIR /app
COPY . /app/

RUN pip install poetry
RUN poetry install

ENTRYPOINT [ "poetry", "run", "oberon0-rt" ]
CMD []
