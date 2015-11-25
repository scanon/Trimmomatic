SERVICE = trimmomatic
SERVICE_CAPS = Trimmomatic
SPEC_FILE = Trimmomatic.spec
URL = https://kbase.us/services/trimmomatic
DIR = $(shell pwd)
LIB_DIR = lib
SCRIPTS_DIR = scripts
TEST_DIR = test
LBIN_DIR = bin
TARGET ?= /kb/deployment
JARS_DIR = $(TARGET)/lib/jars
EXECUTABLE_SCRIPT_NAME = run_$(SERVICE_CAPS)_async_job.sh
STARTUP_SCRIPT_NAME = start_server.sh
TEST_SCRIPT_NAME = run_tests.sh
KB_RUNTIME ?= /kb/runtime
ANT = $(KB_RUNTIME)/ant/bin/ant

default: compile-kb-module build-startup-script build-executable-script build-test-script

.PHONY: test

compile-kb-module:
	kb-sdk compile $(SPEC_FILE) \
		--out $(LIB_DIR) \
		--plclname $(SERVICE_CAPS)::$(SERVICE_CAPS)Client \
		--jsclname javascript/Client \
		--pyclname $(SERVICE_CAPS).$(SERVICE_CAPS)Client \
		--javasrc src \
		--java \
		--pysrvname $(SERVICE_CAPS).$(SERVICE_CAPS)Server \
		--pyimplname $(SERVICE_CAPS).$(SERVICE_CAPS)Impl;
	chmod +x $(SCRIPTS_DIR)/entrypoint.sh

build-executable-script:
	mkdir -p $(LBIN_DIR)
	echo '#!/bin/bash' > $(LBIN_DIR)/$(EXECUTABLE_SCRIPT_NAME)
	echo 'export PYTHONPATH=$(DIR)/$(LIB_DIR):$$PATH:$$PYTHONPATH' >> $(LBIN_DIR)/$(EXECUTABLE_SCRIPT_NAME)
	echo 'python $(DIR)/$(LIB_DIR)/$(SERVICE_CAPS)/$(SERVICE_CAPS)Server.py $$1 $$2 $$3' >> $(LBIN_DIR)/$(EXECUTABLE_SCRIPT_NAME)
	chmod +x $(LBIN_DIR)/$(EXECUTABLE_SCRIPT_NAME)

build-startup-script:
	mkdir -p $(LBIN_DIR)
	echo '#!/bin/bash' > $(SCRIPTS_DIR)/$(STARTUP_SCRIPT_NAME)
	echo 'export KB_DEPLOYMENT_CONFIG=$(DIR)/deploy.cfg' >> $(SCRIPTS_DIR)/$(STARTUP_SCRIPT_NAME)
	echo 'export PYTHONPATH=$(DIR)/$(LIB_DIR):$$PATH:$$PYTHONPATH' >> $(SCRIPTS_DIR)/$(STARTUP_SCRIPT_NAME)
	echo 'uwsgi --master --processes 5 --threads 5 --http :5000 --wsgi-file $(DIR)/$(LIB_DIR)/$(SERVICE_CAPS)/$(SERVICE_CAPS)Server.py' >> $(SCRIPTS_DIR)/$(STARTUP_SCRIPT_NAME)
	chmod +x $(SCRIPTS_DIR)/$(STARTUP_SCRIPT_NAME)

build-test-script:
	echo '#!/bin/bash' > $(TEST_DIR)/$(TEST_SCRIPT_NAME)
	echo 'script_dir=$$(dirname "$$(readlink -f "$$0")")' >> $(TEST_DIR)/$(TEST_SCRIPT_NAME)
	echo 'export KB_DEPLOYMENT_CONFIG=$$script_dir/../deploy.cfg' >> $(TEST_DIR)/$(TEST_SCRIPT_NAME)
	echo 'export KB_AUTH_TOKEN=`cat /kb/module/work/token`' >> $(TEST_DIR)/$(TEST_SCRIPT_NAME)
	echo 'export PYTHONPATH=$$script_dir/../$(LIB_DIR):$$PATH:$$PYTHONPATH' >> $(TEST_DIR)/$(TEST_SCRIPT_NAME)
	echo 'cd $$script_dir/../$(TEST_DIR)' >> $(TEST_DIR)/$(TEST_SCRIPT_NAME)
	echo 'python -m unittest discover -p "*_test.py"' >> $(TEST_DIR)/$(TEST_SCRIPT_NAME)
	chmod +x $(TEST_DIR)/$(TEST_SCRIPT_NAME)

docker-test:
	docker build -t $(SERVICE):test .
	docker run -it -v $(shell pwd)/work:/kb/module/work --rm $(SERVICE):test test

test:
	bash $(TEST_DIR)/$(TEST_SCRIPT_NAME)

old-test:
	echo "Run your tests stupid"
	nosetests -x -v -s
	ls -l

clean:
	rm -rfv $(LBIN_DIR)
