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


def register_collection_atoms(collection):
    '''Given a collection return a registry of all of its atoms (elements).

    Registries are dictionaries with selfLink keys, and PathElement values.
    A registry provides a snapshot of all resources of a type on the device.
    '''
    resource_registry = {}
    for resource in collection.get_collection():
            resource_registry[resource.selfLink] = resource
    return resource_registry
    

def register_OC_atoms(organizing_collection):
    '''Given an OrganizingCollection (OC) return a registry of its atoms.

    Registries are dictionaries with selfLink keys, and PathElement values.
    A registry provides a snapshot of all resources of a type on the device.
    '''
    OC_atoms_registry = {}
    OC_types = organizing_collection._meta_data['allowed_lazy_attributes']
    for OC_type in OC_types:
        collection = getattr(organizing_collection, OC_type.__name__.lower())
        OC_atoms_registry.update(register_collection_atoms(collection))
    return OC_atoms_registry
