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

source: build/f5-oslbaasv1-driver_$(VERSION)_all.src \
	build/f5-oslbaasv1-agent_$(VERSION)_all.src \
	build/f5-bigip-common_$(VERSION)_all.src

debs: build/f5-oslbaasv1-driver_$(VERSION)_all.deb \
      build/f5-oslbaasv1-agent_$(VERSION)_all.deb \
      build/f5-bigip-common_$(VERSION)_all.deb

rpms: build/f5-oslbaasv1-driver-$(VERSION).noarch.rpm \
      build/f5-oslbaasv1-agent-$(VERSION).noarch.rpm \
      build/f5-bigip-common-$(VERSION).noarch.rpm

build/f5-oslbaasv1-driver_$(VERSION)_all.src:
	(cd driver; \
	export PROJECT_DIR=$(PROJECT_DIR); \
	export VERSION=$(VERSION); \
	export RELEASE=$(RELEASE); \
	python setup.py sdist; \
	rm -rf MANIFEST; \
	)
	mkdir -p build
	cp driver/dist/f5-oslbaasv1-driver-$(VERSION).tar.gz build/

build/f5-oslbaasv1-agent_$(VERSION)_all.src:
	(cd agent; \
	export PROJECT_DIR=$(PROJECT_DIR); \
	export VERSION=$(VERSION); \
	export RELEASE=$(RELEASE); \
	python setup.py sdist; \
	rm -rf MANIFEST; \
	)
	mkdir -p build
	cp agent/dist/f5-oslbaasv1-agent-$(VERSION).tar.gz build/

build/f5-bigip-common_$(VERSION)_all.src:
	(cd common; \
	export PROJECT_DIR=$(PROJECT_DIR); \
	export VERSION=$(VERSION); \
	export RELEASE=$(RELEASE); \
	python setup.py sdist; \
	rm -rf MANIFEST; \
	)
	mkdir -p build
	cp common/dist/f5-bigip-common-$(VERSION).tar.gz build/

build/f5-bigip-common_$(VERSION)_all.deb:
	(cd common; \
	rm -rf deb_dist; \
	export PROJECT_DIR=$(PROJECT_DIR); \
	export VERSION=$(VERSION); \
	export RELEASE=$(RELEASE); \
	python setup.py --command-packages=stdeb.command bdist_deb; \
	rm -f stdeb.cfg; \
	) 
	mkdir -p build
	cp common/deb_dist/f5-bigip-common_$(VERSION)-$(RELEASE)_all.deb build/

build/f5-oslbaasv1-driver_$(VERSION)_all.deb:
	(cd driver; \
	rm -rf deb_dist; \
	export PROJECT_DIR=$(PROJECT_DIR); \
	export VERSION=$(VERSION); \
	export RELEASE=$(RELEASE); \
	python setup.py --command-packages=stdeb.command bdist_deb; \
	rm -f stdeb.cfg; \
	) 
	mkdir -p build
	cp driver/deb_dist/f5-oslbaasv1-driver_$(VERSION)-$(RELEASE)_all.deb build/
	
build/f5-oslbaasv1-agent_$(VERSION)_all.deb:
	(cd agent; \
	rm -rf deb_dist; \
	export PROJECT_DIR=$(PROJECT_DIR); \
	export VERSION=$(VERSION); \
	export RELEASE=$(RELEASE); \
	python setup.py --command-packages=stdeb.command bdist_deb; \
	rm -f stdeb.cfg; \
	)
	mkdir -p build
	cp agent/deb_dist/f5-oslbaasv1-agent_$(VERSION)-$(RELEASE)_all.deb build/

build/f5-bigip-common-$(VERSION).noarch.rpm:
	(cd common; \
	export PROJECT_DIR=$(PROJECT_DIR); \
	export VERSION=$(VERSION); \
	export RELEASE=$(RELEASE); \
	python setup.py bdist_rpm; \
	rm -f setup.cfg; \
	) 
	mkdir -p build
	cp common/dist/f5-bigip-common-$(VERSION)-$(RELEASE).noarch.rpm build

build/f5-oslbaasv1-driver-$(VERSION).noarch.rpm:
	(cd driver; \
	export PROJECT_DIR=$(PROJECT_DIR); \
	export VERSION=$(VERSION); \
	export RELEASE=$(RELEASE); \
	python setup.py bdist_rpm; \
    	rm -f setup.cfg; \
	) 
	mkdir -p build
	cp driver/dist/f5-oslbaasv1-driver-$(VERSION)-$(RELEASE).noarch.rpm build

build/f5-oslbaasv1-agent-$(VERSION).noarch.rpm:
	(cd agent; \
	export PROJECT_DIR=$(PROJECT_DIR); \
	export VERSION=$(VERSION); \
	export RELEASE=$(RELEASE); \
	python setup.py bdist_rpm; \
	rm -f setup.cfg; \
	)
	mkdir -p build
	cp agent/dist/f5-oslbaasv1-agent-$(VERSION)-$(RELEASE).noarch.rpm build

pdf:
	html2pdf $(PROJECT_DIR)/doc/f5-oslbaasv1-readme.html \
             $(PROJECT_DIR)/doc/f5-oslbaasv1-readme.pdf

clean: clean-debs clean-rpms clean-source

clean-debs:
	find . -name "*.pyc" -exec rm -rf {} \;
	rm -f driver/MANIFEST
	rm -f agent/MANIFEST
	rm -f common/MANIFEST
	rm -f build/f5-bigip-common_*.deb
	(cd common; \
	rm -rf deb_dist; \
	rm -rf build; \
	)
	rm -f build/f5-oslbaasv1-agent_*.deb
	(cd agent; \
	rm -rf deb_dist; \
	rm -rf build; \
	)
	rm -rf build; \
	(cd driver; \
	rm -rf deb_dist; \
	rm -rf build; \
	)

clean-rpms:
	find . -name "*.pyc" -exec rm -rf {} \;
	rm -f common/MANIFEST
	rm -f driver/MANIFEST
	rm -f agent/MANIFEST 
	rm -f build/f5-bigip-common-*.rpm
	(cd common; \
	rm -rf dist; \
	rm -rf build; \
	)
	rm -f build/f5-oslbaasv1-agent-*.rpm
	(cd agent; \
	rm -rf dist; \
	rm -rf build; \
	)
	rm -f build/f5-oslbaasv1-driver-*.rpm
	(cd driver; \
	rm -rf dist; \
	rm -rf build; \
	)

clean-source:
	rm -rf build/*.tar.gz
	rm -rf common/dist
	rm -rf driver/dist
	rm -rf driver/driver
	rm -rf driver/doc
	rm -rf agent/dist
	rm -rf agent/agent
	rm -rf agent/doc

BDIR := f5/oslbaasv1agent/drivers/bigip
IDIR := f5/bigip/interfaces
PYCTL := f5/bigip/pycontrol
NDIR := /usr/lib/python2.7/dist-packages/neutron

pep8: pep8-driver pep8-agent 

pep8-driver:
	(cd driver; \
	     pep8 f5/oslbaasv1driver/__init__.py; \
         pep8 f5/oslbaasv1driver/drivers/agent_scheduler.py; \
         pep8 f5/oslbaasv1driver/drivers/plugin_driver.py; \
         pep8 f5/oslbaasv1driver/drivers/rpc.py; \
         pep8 f5/oslbaasv1driver/drivers/constants.py; \
        )    

pep8-agent:
	(cd agent; \
	 pep8 f5/oslbaasv1agent/__init__.py; \
	 pep8 f5/oslbaasv1agent/drivers/__init__.py; \
	 pep8 $(BDIR)/__init__.py; \
         pep8 $(BDIR)/agent_api.py; \
         pep8 $(BDIR)/agent_manager.py; \
         pep8 $(BDIR)/agent.py; \
         pep8 $(BDIR)/constants.py; \
         pep8 $(BDIR)/exceptions.py; \
         pep8 $(BDIR)/fdb_connector_ml2.py; \
         pep8 $(BDIR)/fdb_connector.py; \
         pep8 $(BDIR)/icontrol_driver.py; \
         pep8 $(BDIR)/l2.py; \
         pep8 $(BDIR)/l3_binding.py; \
         pep8 $(BDIR)/lbaas.py; \
         pep8 $(BDIR)/lbaas_driver.py; \
         pep8 $(BDIR)/lbaas_iapp.py; \
         pep8 $(BDIR)/lbaas_bigiq.py; \
         pep8 $(BDIR)/lbaas_bigip.py; \
         pep8 $(BDIR)/network_direct.py; \
         pep8 $(BDIR)/rpc.py; \
         pep8 $(BDIR)/selfips.py; \
         pep8 $(BDIR)/snats.py; \
         pep8 $(BDIR)/pools.py; \
         pep8 $(BDIR)/tenants.py; \
         pep8 $(BDIR)/vcmp.py; \
         pep8 $(BDIR)/vips.py; \
         pep8 $(BDIR)/utils.py; \
        )

pep8-common:
	(cd common; \
         pep8 f5/__init__.py; \
         pep8 f5/bigip/__init__.py; \
         pep8 f5/bigip/bigip.py; \
         pep8 f5/bigip/exceptions.py; \
         pep8 $(IDIR)/__init__.py; \
         pep8 $(IDIR)/arp.py; \
         pep8 $(IDIR)/cluster.py; \
         pep8 $(IDIR)/device.py; \
         pep8 $(IDIR)/iapp.py; \
         pep8 $(IDIR)/l2gre.py; \
         pep8 $(IDIR)/monitor.py; \
         pep8 $(IDIR)/nat.py; \
         pep8 $(IDIR)/pool.py; \
         pep8 $(IDIR)/route.py; \
         pep8 $(IDIR)/rule.py; \
         pep8 $(IDIR)/selfip.py; \
         pep8 $(IDIR)/snat.py; \
         pep8 $(IDIR)/system.py; \
         pep8 $(IDIR)/virtual_server.py; \
         pep8 $(IDIR)/vlan.py; \
         pep8 $(IDIR)/vxlan.py; \
         pep8 $(PYCTL)/__init__.py; \
         pep8 $(PYCTL)/pycontrol.py; \
         pep8 f5/bigiq/__init__.py; \
         pep8 f5/bigiq/bigiq.py; \
         pep8 f5/common/__init__.py; \
         pep8 f5/common/constants.py; \
         pep8 f5/common/logger.py; \
         pep8 $(IDIR)/constants.py; \
        )       
        
PYHOOK := 'import sys;sys.path.insert(1,".")'
PYLINT := pylint --additional-builtins=_ --init-hook=$(PYHOOK)

pylint: pylint-agent pylint-driver

pylint-agent:
	(cd agent; \
         mkdir neutron; \
         touch neutron/__init__.py; \
         mkdir neutron/services; \
         touch neutron/services/__init__.py; \
         mkdir neutron/services/loadbalancer; \
         touch neutron/services/loadbalancer/__init__.py; \
         mkdir neutron/services/loadbalancer/drivers; \
         touch neutron/services/loadbalancer/drivers/__init__.py; \
         ln -s $(NDIR)/common neutron/common; \
         ln -s $(NDIR)/openstack neutron/openstack; \
         ln -s $(NDIR)/plugins neutron/plugins; \
         ln -s $(NDIR)/services/constants neutron/services/constants; \
         ln -s $(NDIR)/services/loadbalancer/constants.py \
               neutron/services/loadbalancer/constants.py; \
         ln -s ../../common/f5/bigip f5/bigip; \
         $(PYLINT) f5/bigiq/bigiq.py; \
         $(PYLINT) $(BDIR)/fdb_connector.py; \
         $(PYLINT) $(BDIR)/fdb_connector_ml2.py; \
         $(PYLINT) $(BDIR)/lbaas_driver.py; \
         $(PYLINT) $(BDIR)/icontrol_driver.py; \
         $(PYLINT) $(BDIR)/lbaas.py; \
         $(PYLINT) $(BDIR)/lbaas_iapp.py; \
         $(PYLINT) $(BDIR)/lbaas_bigiq.py; \
         $(PYLINT) $(BDIR)/lbaas_bigip.py; \
         $(PYLINT) $(BDIR)/l2.py; \
         $(PYLINT) $(BDIR)/l3_binding.py; \
         $(PYLINT) $(BDIR)/network_direct.py; \
         $(PYLINT) $(BDIR)/pools.py; \
         $(PYLINT) $(BDIR)/selfips.py; \
         $(PYLINT) $(BDIR)/snats.py; \
         $(PYLINT) $(BDIR)/tenants.py; \
         $(PYLINT) $(BDIR)/vcmp.py; \
         $(PYLINT) $(BDIR)/vips.py; \
         $(PYLINT) $(BDIR)/utils.py; \
         $(PYLINT) $(IDIR)/__init__.py; \
         $(PYLINT) $(IDIR)/arp.py; \
         $(PYLINT) $(IDIR)/iapp.py; \
         $(PYLINT) $(IDIR)/l2gre.py; \
         $(PYLINT) $(IDIR)/route.py; \
         $(PYLINT) $(IDIR)/system.py; \
         $(PYLINT) $(IDIR)/virtual_server.py; \
         $(PYLINT) $(IDIR)/vxlan.py; \
         rm -v f5/bigip; \
         rm -v neutron/plugins; \
         rm -v neutron/openstack; \
         rm -v neutron/common; \
         rm -v neutron/services/constants; \
         rm -v neutron/services/loadbalancer/constants.py; \
         rm -v neutron/services/loadbalancer/drivers/__init__.py; \
         rm -v neutron/services/loadbalancer/__init__.py; \
         rm -v neutron/services/__init__.py; \
         rm -v neutron/__init__.py; \
         rm -rf ./neutron; \
        )

pylint-driver:
	(cd driver; \
         mkdir neutron; \
         touch neutron/__init__.py; \
         mkdir neutron/services; \
         touch neutron/services/__init__.py; \
         mkdir neutron/services/loadbalancer; \
         touch neutron/services/loadbalancer/__init__.py; \
         mkdir neutron/services/loadbalancer/drivers; \
         touch neutron/services/loadbalancer/drivers/__init__.py; \
         ln -s $(NDIR)/api neutron/api; \
         ln -s $(NDIR)/common neutron/common; \
         ln -s $(NDIR)/context.py neutron/context.py; \
         ln -s $(NDIR)/db neutron/db; \
         ln -s $(NDIR)/extensions neutron/extensions; \
         ln -s $(NDIR)/openstack neutron/openstack; \
         ln -s $(NDIR)/plugins neutron/plugins; \
         ln -s $(NDIR)/services/constants neutron/services/constants; \
         ln -s $(NDIR)/services/loadbalancer/constants.py \
               neutron/services/loadbalancer/constants.py; \
         $(PYLINT) f5/oslbaasv1driver/drivers/plugin_driver.py; \
         $(PYLINT) f5/oslbaasv1driver/drivers/agent_scheduler.py; \
         $(PYLINT) f5/oslbaasv1driver/drivers/rpc.py; \
         $(PYLINT) f5/oslbaasv1driver/drivers/log/plugin_driver.py; \
         rm -v neutron/api; \
         rm -v neutron/plugins; \
         rm -v neutron/openstack; \
         rm -v neutron/common; \
         rm -v neutron/context.py; \
         rm -v neutron/db; \
         rm -v neutron/extensions; \
         rm -v neutron/services/constants; \
         rm -v neutron/services/loadbalancer/constants.py; \
         rm -v neutron/services/loadbalancer/drivers/__init__.py; \
         rm -v neutron/services/loadbalancer/__init__.py; \
         rm -v neutron/services/__init__.py; \
         rm -v neutron/__init__.py; \
         rm -rf ./neutron; \
        )

test-agent:
	(cd agent; \
         > neutron/__init__.py; \
         > neutron/services/__init__.py; \
         > neutron/services/loadbalancer/__init__.py; \
         > neutron/services/loadbalancer/drivers/__init__.py; \
         ln -s $(NDIR)/common neutron/common; \
         ln -s $(NDIR)/openstack neutron/openstack; \
         ln -s $(NDIR)/plugins neutron/plugins; \
         ln -s $(NDIR)/services/constants neutron/services/constants; \
         ln -s $(NDIR)/services/loadbalancer/constants.py \
               neutron/services/loadbalancer/constants.py; \
         cp ../test/test.py .; \
         python test.py; \
         rm test.py; \
         rm -vf neutron/plugins; \
         rm -vf neutron/openstack; \
         rm -vf neutron/common; \
         rm -vf neutron/services/constants; \
         rm -vf neutron/services/loadbalancer/constants.py; \
         rm -vf neutron/services/loadbalancer/constants.pyc; \
         rm -vf neutron/services/loadbalancer/drivers/__init__.py; \
         rm -vf neutron/services/loadbalancer/drivers/__init__.pyc; \
         rm -vf neutron/services/loadbalancer/__init__.py; \
         rm -vf neutron/services/loadbalancer/__init__.pyc; \
         rm -vf neutron/services/__init__.py; \
         rm -vf neutron/services/__init__.pyc; \
         rm -vf neutron/__init__.py; \
         rm -vf neutron/__init__.pyc; \
         )
