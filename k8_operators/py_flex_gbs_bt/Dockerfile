FROM gcr.io/dataflow-templates-base/python3-template-launcher-base:latest

ARG WORKDIR=/dataflow/template
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

COPY requirements.txt .
COPY main.py .
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="${WORKDIR}/main.py"

RUN pip install -U -r ./requirements.txt