# NOTE:
# 
# You need to install these packages on Ubunutu 12.04 to make this work:
# 
#     sudo apt-get install -y make python-stdeb fakeroot python-all rpm pep8 pylint
# 
# 
PROJECT_DIR := $(shell pwd)
VERSION := $(shell cat VERSION|tr -d '\n';)
RELEASE := $(shell cat RELEASE|tr -d '\n';)

default: debs rpms source

source: build/f5-bigip-common_$(VERSION)_all.src

debs: build/f5-bigip-common_$(VERSION)_all.deb

rpms: build/f5-bigip-common-$(VERSION).noarch.rpm

docker_rpms:
	(docker build -t rpm-pkg-builder ./Docker/redhat)
	docker run -v $(PROJECT_DIR):/var/build/ rpm-pkg-builder /bin/bash /build-rpms.sh

docker_debs:
	(docker build -t deb-pkg-builder ./Docker/debian)
	docker run -v $(PROJECT_DIR):/var/build/ deb-pkg-builder /bin/bash /build-debs.sh

build/f5-bigip-common_$(VERSION)_all.src:
	(export PROJECT_DIR=$(PROJECT_DIR); \
	export VERSION=$(VERSION); \
	export RELEASE=$(RELEASE); \
	python setup.py sdist; \
	rm -rf MANIFEST; \
	)
	mkdir -p build
	cp dist/f5-bigip-common-$(VERSION).tar.gz build/

build/f5-bigip-common_$(VERSION)_all.deb:
	(rm -rf deb_dist; \
	export PROJECT_DIR=$(PROJECT_DIR); \
	export VERSION=$(VERSION); \
	export RELEASE=$(RELEASE); \
	python setup.py --command-packages=stdeb.command bdist_deb; \
	rm -f stdeb.cfg; \
	) 
	mkdir -p build
	cp deb_dist/f5-bigip-common_$(VERSION)-$(RELEASE)_all.deb build/

build/f5-bigip-common-$(VERSION).noarch.rpm:
	(export PROJECT_DIR=$(PROJECT_DIR); \
	export VERSION=$(VERSION); \
	export RELEASE=$(RELEASE); \
	python setup.py bdist_rpm; \
	rm -f setup.cfg; \
	) 
	mkdir -p build
	cp dist/f5-bigip-common-$(VERSION)-$(RELEASE).noarch.rpm build

pdf:
	html2pdf $(PROJECT_DIR)/doc/f5-oslbaasv1-readme.html \
             $(PROJECT_DIR)/doc/f5-oslbaasv1-readme.pdf

clean: clean-debs clean-rpms clean-source

clean-debs:
	find . -name "*.pyc" -exec rm -rf {} \;
	rm -f MANIFEST
	rm -f build/f5-bigip-common_*.deb
	( \
	rm -rf deb_dist; \
	rm -rf build; \
	)

clean-rpms:
	find . -name "*.pyc" -exec rm -rf {} \;
	rm -f MANIFEST
	rm -rf f5-bigip-common*
	rm -f build/f5-bigip-common-*.rpm
	( \
	rm -rf dist; \
	rm -rf build; \
	)

clean-source:
	rm -rf *.egg-info
	rm -rf build/*.tar.gz
	rm -rf common/*.tar.gz
	rm -rf common/dist

BDIR := f5/oslbaasv1agent/drivers/bigip
IDIR := f5/bigip/interfaces
PYCTL := f5/bigip/pycontrol
NDIR := /usr/lib/python2.7/dist-packages/neutron

flake8:
	flake8 .

# pep8-common:
# 	(pep8 f5/__init__.py; \
#          pep8 f5/bigip/__init__.py; \
#          pep8 f5/bigip/bigip.py; \
#          pep8 f5/bigip/exceptions.py; \
#          pep8 $(IDIR)/__init__.py; \
#          pep8 $(IDIR)/arp.py; \
#          pep8 $(IDIR)/cluster.py; \
#          pep8 $(IDIR)/device.py; \
#          pep8 $(IDIR)/iapp.py; \
#          pep8 $(IDIR)/interface.py; \
#          pep8 $(IDIR)/l2gre.py; \
#          pep8 $(IDIR)/monitor.py; \
#          pep8 $(IDIR)/nat.py; \
#          pep8 $(IDIR)/pool.py; \
#          pep8 $(IDIR)/route.py; \
#          pep8 $(IDIR)/rule.py; \
#          pep8 $(IDIR)/selfip.py; \
#          pep8 $(IDIR)/snat.py; \
#          pep8 $(IDIR)/ssl.py; \
#          pep8 $(IDIR)/stat.py; \
#          pep8 $(IDIR)/system.py; \
#          pep8 $(IDIR)/virtual_server.py; \
#          pep8 $(IDIR)/vlan.py; \
#          pep8 $(IDIR)/vxlan.py; \
#          pep8 $(PYCTL)/__init__.py; \
#          pep8 $(PYCTL)/pycontrol.py; \
#          pep8 f5/bigiq/__init__.py; \
#          pep8 f5/bigiq/bigiq.py; \
#          pep8 f5/common/__init__.py; \
#          pep8 f5/common/constants.py; \
#          pep8 f5/common/logger.py; \
#         )       

PYHOOK := 'import sys;sys.path.insert(1,".")'
PYLINT := pylint --additional-builtins=_ --init-hook=$(PYHOOK)
