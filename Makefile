NODE = understat-extension
CONDA_ENV = knime-understat-nodes-env
BUILD_ENV = knime-ext-bundling

create/conda:
	conda env create -f environment.yml   

lint:
	conda run --name ${CONDA_ENV} flake8

unit:
	conda run --name ${CONDA_ENV} pytest

tests: lint unit

create/builder:
	conda create -n ${BUILD_ENV} -c knime -c conda-forge knime-extension-bundling

build:
	conda run --name ${BUILD_ENV} build_python_extension.py . build_${NODE}
