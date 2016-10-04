# Copyright 2016 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import logging
from pprint import pprint as pp
from six import itervalues

from f5.bigip.mixins import UnsupportedTmosVersion
from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.tm.asm import Asm


def register_collection_atoms(collection):
    '''Given a collection return a registry of all of its atoms (elements).

    Registries are dictionaries with selfLink keys, and PathElement values.
    A registry provides a snapshot of all resources of a type on the device.
    '''
    resource_registry = {}
    try:
        resources = collection.get_collection()
    except Exception as ex:
        logging.debug(ex)
        return resource_registry
    for resource in resources:
            try:
                resource_registry[resource.selfLink] = resource
            except KeyError as ex:
                pp(resource.raw)
                raise ex
            except UnsupportedTmosVersion as ex:
                logging.debug(ex)
                continue
    return resource_registry


def register_OC_atoms(organizing_collection):
    '''Given an OrganizingCollection (OC) return a registry of its atoms.

    Registries are dictionaries with selfLink keys, and PathElement values.
    A registry provides a snapshot of all resources of a type on the device.
    '''
    OC_atoms_registry = {}
    OC_types = organizing_collection._meta_data['allowed_lazy_attributes']
    # Removing ASM as this causes some intermittent problems on Jenkins,
    # whereby device snapshot tries to delete factory signatures, resulting in
    # REST error and test failures when
    if Asm in OC_types:
        OC_types.remove(Asm)
    for OC_type in OC_types:
        try:
            lazy_instance =\
                getattr(organizing_collection, OC_type.__name__.lower())
        except UnsupportedTmosVersion as ex:
            logging.debug(ex)
            continue
        if isinstance(lazy_instance, Collection):
            OC_atoms_registry.update(register_collection_atoms(lazy_instance))
        elif isinstance(lazy_instance, OrganizingCollection):
            OC_atoms_registry.update(register_OC_atoms(lazy_instance))
    return OC_atoms_registry


def register_device(mgmt_rt):
    OCs = [getattr(mgmt_rt, c.__name__.lower())
           for c in mgmt_rt._meta_data['allowed_lazy_attributes']]
    grand_registry = {}
    for OC in OCs:
        grand_registry.update(register_OC_atoms(OC))
    return grand_registry


def register_loadbalancer_elements(mgmt_rt):
    monitor_registry = register_OC_atoms(mgmt_rt.tm.ltm.monitor)
    pool_registry = register_collection_atoms(mgmt_rt.tm.ltm.pools)
    snat_registry = register_collection_atoms(mgmt_rt.tm.ltm.snats)
    virtual_registry = register_collection_atoms(mgmt_rt.tm.ltm.virtuals)
    virtual_address_s_registry =\
        register_collection_atoms(mgmt_rt.tm.ltm.virtual_address_s)
    member_registry = {}
    for pool in list(itervalues(pool_registry)):
        mc = pool.members_s
        member_registry.update(register_collection_atoms(mc))
    folder_registry = register_collection_atoms(mgmt_rt.tm.sys.folders)
    registries = {'monitor_registry': monitor_registry,
                  'pool_registry': pool_registry,
                  'snat_registry': snat_registry,
                  'virtual_registry': virtual_registry,
                  'virtual_address_s_registry': virtual_address_s_registry,
                  'member_registry': member_registry,
                  'folder_registry': folder_registry}
    return registries
