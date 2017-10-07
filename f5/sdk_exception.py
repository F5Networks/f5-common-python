# coding=utf-8
# Copyright 2016 F5 Networks Inc.

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
#
"""A base exception for all exceptions in this library."""


class F5SDKError(Exception):
    """Import and subclass this exception in all exceptions in this library."""
    def __init__(self, *args, **kwargs):
        super(F5SDKError, self).__init__(*args, **kwargs)


class AttemptedMutationOfReadOnly(F5SDKError):
    """Read only parameters cannot be set."""
    pass


class BooleansToReduceHaveSameValue(F5SDKError):
    """Dict contains two keys with same boolean value."""
    pass


class DeviceProvidesIncompatibleKey(F5SDKError):
    """Raise this when server JSON keys are incompatible with Python."""
    pass


class DisallowedCreationParameter(F5SDKError):
    """Exception when partition is passed to create for guest resource."""
    pass


class DisallowedReadParameter(F5SDKError):
    """Exception when partition is passed to load for guest resource."""
    pass


class EmptyContent(F5SDKError):
    """Raise an error if the returned content size is 0."""
    pass


class ExclusiveAttributesPresent(F5SDKError):
    """Raises this when exclusive attributes are present."""
    pass


class FileMustNotHaveDotISOExtension(F5SDKError):
    """Raise this when file has ISO extension."""
    def __init__(self, filename):
        super(FileMustNotHaveDotISOExtension, self).__init__(filename)


class GenerationMismatch(F5SDKError):
    """The server reported BIG-IP® is not the expacted value."""
    pass


class ImageFilesMustHaveDotISOExtension(F5SDKError):
    """Raise this when Image files do not have ISO extensions."""
    def __init__(self, filename):
        super(ImageFilesMustHaveDotISOExtension, self).__init__(filename)


class InvalidCommand(F5SDKError):
    """Raise this if command argument supplied is invalid."""
    pass


class InvalidForceType(ValueError):
    """Must be of type bool."""
    pass


class InvalidName(ValueError):
    """Raised during creation when a given resource name is invalid."""
    pass


class InvalidResource(F5SDKError):
    """Raise this when a caller tries to invoke an unsupported CRUDL op.

    All resources support `refresh` and `raw`.
    Only `Resource`'s support `load`, `create`, `update`, and `delete`.
    """
    pass


class KindTypeMismatch(F5SDKError):
    """Raise this when server JSON keys are incorrect for the Resource type."""
    pass


class LazyAttributesRequired(F5SDKError):
    """Raised when a object accesses a lazy attribute that is not listed."""
    pass


class MemberStateModifyUnsupported(F5SDKError):
    """Modify of node with state=unchecked is unsupported."""
    pass


class MissingHttpHeader(F5SDKError):
    """We raise this when the expected http header in response is missing."""
    pass


class MissingRequiredCreationParameter(F5SDKError):
    """Various values MUST be provided to create different Resources."""
    pass


class MissingRequiredCommandParameter(F5SDKError):
    """Various values MUST be provided to execute a command."""
    pass


class MissingRequiredReadParameter(F5SDKError):
    """Various values MUST be provided to refresh some Resources."""
    pass


class MissingUpdateParameter(F5SDKError):
    """Raises this when update requires specific parameters together."""
    pass


class NodeStateModifyUnsupported(F5SDKError):
    """Modify of node with state=unchecked is unsupported."""
    pass


class NonExtantApplication(F5SDKError):
    """Raise if the dos profile application sub-collection

    resource does not exist on the device.
    """
    pass


class NonExtantPolicyRule(F5SDKError):
    """Raise if a rule does not exist on the device."""
    pass


class NonExtantFirewallRule(F5SDKError):
    """Raise if the policy does not exist on the device."""
    pass


class NonExtantVirtualPolicy(F5SDKError):
    """Raise if the policy does not exist on the device."""
    pass


class OperationNotSupportedOnPublishedPolicy(F5SDKError):
    """Raise if update/modify attempted on published policy."""
    pass


class RequestParamKwargCollision(F5SDKError):
    """Raise where requests parameter collides

    with a method parameter of the same name.
    """
    pass


class TagModeDisallowedForTMOSVersion(F5SDKError):
    """Raise if tagmode is not supported for given TMOS version."""
    pass


class TransactionSubmitException(F5SDKError):
    """Raise this when Transaction commit fails."""
    pass


class URICreationCollision(F5SDKError):
    """self._meta_data['uri'] can only be assigned once. In create or load."""
    pass


class UnregisteredKind(F5SDKError):
    """The returned server JSON `kind` key wasn't expected by this Resource."""
    pass


class UnsupportedMethod(F5SDKError):
    """Raise this if a method supplied is unsupported."""
    pass


class UnsupportedTmosVersion(F5SDKError):
    """Raise the error if a class of an API is instantiated,

    on a TMOS version where API was not yet implemented/supported.
    """
    pass


class UnsupportedOperation(F5SDKError):
    """Object does not support the method that was called."""
    pass


class UtilError(F5SDKError):
    """Raise this if command excecution returns an error."""
    pass


class DraftPolicyNotSupportedInTMOSVersion(F5SDKError):
    """Raise when using Drafts in a legacy TMOS version

    Raise this if handling Draft work in a Policy class that is
    used by legacy, and current, versions of BIG-IP
    """
    pass


class ConstraintError(F5SDKError):
    """Raise when a supplied value is outside the limits for that attribute."""
    pass


class RequiredOneOf(F5SDKError):
    """Raise this if more than one of required argument sets is provided."""
    def __init__(self, required_one_of):
        errors = []
        message = 'Creation requires one of the following lists of args {0}'
        for require in required_one_of:
            requires = ','.join(require)
            error = '( {0} )'.format(requires)
            errors.append(error)
        msg = message.format(' or '.join(errors))
        super(RequiredOneOf, self).__init__(msg)
