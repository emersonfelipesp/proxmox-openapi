"""Generated Pydantic v2 schemas from Proxmox OpenAPI output."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, RootModel


class ProxmoxBaseModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra='allow')

class GetAccessResponseItem(ProxmoxBaseModel):
    subdir: str | None = Field(None)

class GetAccessResponse(RootModel[list[GetAccessResponseItem]]):
    root: list[GetAccessResponseItem] = Field(...)

class GetAccessAclResponseItem(ProxmoxBaseModel):
    path: str | None = Field(None, description='Access control path')
    propagate: bool | None = Field(None, description='Allow to propagate (inherit) permissions.')
    roleid: str | None = Field(None)
    type: str | None = Field(None)
    ugid: str | None = Field(None)

class GetAccessAclResponse(RootModel[list[GetAccessAclResponseItem]]):
    root: list[GetAccessAclResponseItem] = Field(...)

class PutAccessAclRequest(ProxmoxBaseModel):
    delete: bool | None = Field(None, description='Remove permissions (instead of adding it).')
    groups: str | None = Field(None, description='List of groups.')
    path: str = Field(..., description='Access control path')
    propagate: bool | None = Field(None, description='Allow to propagate (inherit) permissions.')
    roles: str = Field(..., description='List of roles.')
    tokens: str | None = Field(None, description='List of API tokens.')
    users: str | None = Field(None, description='List of users.')

class PutAccessAclResponse(RootModel[None]):
    root: None = Field(...)

class GetAccessDomainsResponseItem(ProxmoxBaseModel):
    comment: str | None = Field(None, description='A comment. The GUI use this text when you select a domain (Realm) on the login window.')
    realm: str | None = Field(None)
    tfa: str | None = Field(None, description='Two-factor authentication provider.')
    type: str | None = Field(None)

class GetAccessDomainsResponse(RootModel[list[GetAccessDomainsResponseItem]]):
    root: list[GetAccessDomainsResponseItem] = Field(...)

class PostAccessDomainsRequest(ProxmoxBaseModel):
    acr_values: str | None = Field(None, alias="acr-values", description='Specifies the Authentication Context Class Reference values that theAuthorization Server is being requested to use for the Auth Request.')
    autocreate: bool | None = Field(None, description='Automatically create users if they do not exist.')
    base_dn: str | None = Field(None, description='LDAP base domain name')
    bind_dn: str | None = Field(None, description='LDAP bind domain name')
    capath: str | None = Field(None, description='Path to the CA certificate store')
    case_sensitive: bool | None = Field(None, alias="case-sensitive", description='username is case-sensitive')
    cert: str | None = Field(None, description='Path to the client certificate')
    certkey: str | None = Field(None, description='Path to the client certificate key')
    check_connection: bool | None = Field(None, alias="check-connection", description='Check bind connection to the server.')
    client_id: str | None = Field(None, alias="client-id", description='OpenID Client ID')
    client_key: str | None = Field(None, alias="client-key", description='OpenID Client Key')
    comment: str | None = Field(None, description='Description.')
    default: bool | None = Field(None, description='Use this as default realm')
    domain: str | None = Field(None, description='AD domain name')
    filter: str | None = Field(None, description='LDAP filter for user sync.')
    group_classes: str | None = Field(None, description='The objectclasses for groups.')
    group_dn: str | None = Field(None, description='LDAP base domain name for group sync. If not set, the base_dn will be used.')
    group_filter: str | None = Field(None, description='LDAP filter for group sync.')
    group_name_attr: str | None = Field(None, description='LDAP attribute representing a groups name. If not set or found, the first value of the DN will be used as name.')
    groups_autocreate: bool | None = Field(None, alias="groups-autocreate", description='Automatically create groups if they do not exist.')
    groups_claim: str | None = Field(None, alias="groups-claim", description='OpenID claim used to retrieve groups with.')
    groups_overwrite: bool | None = Field(None, alias="groups-overwrite", description='All groups will be overwritten for the user on login.')
    issuer_url: str | None = Field(None, alias="issuer-url", description='OpenID Issuer Url')
    mode: str | None = Field(None, description='LDAP protocol mode.')
    password: str | None = Field(None, description="LDAP bind password. Will be stored in '/etc/pve/priv/realm/<REALM>.pw'.")
    port: int | None = Field(None, description='Server port.')
    prompt: str | None = Field(None, description='Specifies whether the Authorization Server prompts the End-User for reauthentication and consent.')
    query_userinfo: bool | None = Field(None, alias="query-userinfo", description='Enables querying the userinfo endpoint for claims values.')
    realm: str = Field(..., description='Authentication domain ID')
    scopes: str | None = Field(None, description="Specifies the scopes (user details) that should be authorized and returned, for example 'email' or 'profile'.")
    secure: bool | None = Field(None, description="Use secure LDAPS protocol. DEPRECATED: use 'mode' instead.")
    server1: str | None = Field(None, description='Server IP address (or DNS name)')
    server2: str | None = Field(None, description='Fallback Server IP address (or DNS name)')
    sslversion: str | None = Field(None, description="LDAPS TLS/SSL version. It's not recommended to use version older than 1.2!")
    sync_defaults_options: str | None = Field(None, alias="sync-defaults-options", description='The default options for behavior of synchronizations.')
    sync_attributes: str | None = Field(None, description="Comma separated list of key=value pairs for specifying which LDAP attributes map to which PVE user field. For example, to map the LDAP attribute 'mail' to PVEs 'email', write  'email=mail'. By default, each PVE user field is represented  by an LDAP attribute of the same name.")
    tfa: str | None = Field(None, description='Use Two-factor authentication.')
    type: str = Field(..., description='Realm type.')
    user_attr: str | None = Field(None, description='LDAP user attribute name')
    user_classes: str | None = Field(None, description='The objectclasses for users.')
    username_claim: str | None = Field(None, alias="username-claim", description='OpenID claim used to generate the unique username.')
    verify: bool | None = Field(None, description="Verify the server's SSL certificate")

class PostAccessDomainsResponse(RootModel[None]):
    root: None = Field(...)

class DeleteAccessDomainsRealmRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteAccessDomainsRealmResponse(RootModel[None]):
    root: None = Field(...)

class GetAccessDomainsRealmResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PutAccessDomainsRealmRequest(ProxmoxBaseModel):
    acr_values: str | None = Field(None, alias="acr-values", description='Specifies the Authentication Context Class Reference values that theAuthorization Server is being requested to use for the Auth Request.')
    autocreate: bool | None = Field(None, description='Automatically create users if they do not exist.')
    base_dn: str | None = Field(None, description='LDAP base domain name')
    bind_dn: str | None = Field(None, description='LDAP bind domain name')
    capath: str | None = Field(None, description='Path to the CA certificate store')
    case_sensitive: bool | None = Field(None, alias="case-sensitive", description='username is case-sensitive')
    cert: str | None = Field(None, description='Path to the client certificate')
    certkey: str | None = Field(None, description='Path to the client certificate key')
    check_connection: bool | None = Field(None, alias="check-connection", description='Check bind connection to the server.')
    client_id: str | None = Field(None, alias="client-id", description='OpenID Client ID')
    client_key: str | None = Field(None, alias="client-key", description='OpenID Client Key')
    comment: str | None = Field(None, description='Description.')
    default: bool | None = Field(None, description='Use this as default realm')
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    domain: str | None = Field(None, description='AD domain name')
    filter: str | None = Field(None, description='LDAP filter for user sync.')
    group_classes: str | None = Field(None, description='The objectclasses for groups.')
    group_dn: str | None = Field(None, description='LDAP base domain name for group sync. If not set, the base_dn will be used.')
    group_filter: str | None = Field(None, description='LDAP filter for group sync.')
    group_name_attr: str | None = Field(None, description='LDAP attribute representing a groups name. If not set or found, the first value of the DN will be used as name.')
    groups_autocreate: bool | None = Field(None, alias="groups-autocreate", description='Automatically create groups if they do not exist.')
    groups_claim: str | None = Field(None, alias="groups-claim", description='OpenID claim used to retrieve groups with.')
    groups_overwrite: bool | None = Field(None, alias="groups-overwrite", description='All groups will be overwritten for the user on login.')
    issuer_url: str | None = Field(None, alias="issuer-url", description='OpenID Issuer Url')
    mode: str | None = Field(None, description='LDAP protocol mode.')
    password: str | None = Field(None, description="LDAP bind password. Will be stored in '/etc/pve/priv/realm/<REALM>.pw'.")
    port: int | None = Field(None, description='Server port.')
    prompt: str | None = Field(None, description='Specifies whether the Authorization Server prompts the End-User for reauthentication and consent.')
    query_userinfo: bool | None = Field(None, alias="query-userinfo", description='Enables querying the userinfo endpoint for claims values.')
    scopes: str | None = Field(None, description="Specifies the scopes (user details) that should be authorized and returned, for example 'email' or 'profile'.")
    secure: bool | None = Field(None, description="Use secure LDAPS protocol. DEPRECATED: use 'mode' instead.")
    server1: str | None = Field(None, description='Server IP address (or DNS name)')
    server2: str | None = Field(None, description='Fallback Server IP address (or DNS name)')
    sslversion: str | None = Field(None, description="LDAPS TLS/SSL version. It's not recommended to use version older than 1.2!")
    sync_defaults_options: str | None = Field(None, alias="sync-defaults-options", description='The default options for behavior of synchronizations.')
    sync_attributes: str | None = Field(None, description="Comma separated list of key=value pairs for specifying which LDAP attributes map to which PVE user field. For example, to map the LDAP attribute 'mail' to PVEs 'email', write  'email=mail'. By default, each PVE user field is represented  by an LDAP attribute of the same name.")
    tfa: str | None = Field(None, description='Use Two-factor authentication.')
    user_attr: str | None = Field(None, description='LDAP user attribute name')
    user_classes: str | None = Field(None, description='The objectclasses for users.')
    verify: bool | None = Field(None, description="Verify the server's SSL certificate")

class PutAccessDomainsRealmResponse(RootModel[None]):
    root: None = Field(...)

class PostAccessDomainsRealmSyncRequest(ProxmoxBaseModel):
    dry_run: bool | None = Field(None, alias="dry-run", description='If set, does not write anything.')
    enable_new: bool | None = Field(None, alias="enable-new", description='Enable newly synced users immediately.')
    full: bool | None = Field(None, description="DEPRECATED: use 'remove-vanished' instead. If set, uses the LDAP Directory as source of truth, deleting users or groups not returned from the sync and removing all locally modified properties of synced users. If not set, only syncs information which is present in the synced data, and does not delete or modify anything else.")
    purge: bool | None = Field(None, description="DEPRECATED: use 'remove-vanished' instead. Remove ACLs for users or groups which were removed from the config during a sync.")
    remove_vanished: str | None = Field(None, alias="remove-vanished", description="A semicolon-separated list of things to remove when they or the user vanishes during a sync. The following values are possible: 'entry' removes the user/group when not returned from the sync. 'properties' removes the set properties on existing user/group that do not appear in the source (even custom ones). 'acl' removes acls when the user/group is not returned from the sync. Instead of a list it also can be 'none' (the default).")
    scope: str | None = Field(None, description='Select what to sync.')

class PostAccessDomainsRealmSyncResponse(RootModel[str]):
    root: str = Field(..., description='Worker Task-UPID')

class GetAccessGroupsResponseItem(ProxmoxBaseModel):
    comment: str | None = Field(None)
    groupid: str | None = Field(None)
    users: str | None = Field(None, description='list of users which form this group')

class GetAccessGroupsResponse(RootModel[list[GetAccessGroupsResponseItem]]):
    root: list[GetAccessGroupsResponseItem] = Field(...)

class PostAccessGroupsRequest(ProxmoxBaseModel):
    comment: str | None = Field(None)
    groupid: str = Field(...)

class PostAccessGroupsResponse(RootModel[None]):
    root: None = Field(...)

class DeleteAccessGroupsGroupidRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteAccessGroupsGroupidResponse(RootModel[None]):
    root: None = Field(...)

class GetAccessGroupsGroupidResponse(ProxmoxBaseModel):
    comment: str | None = Field(None)
    members: list[str] = Field(...)

class PutAccessGroupsGroupidRequest(ProxmoxBaseModel):
    comment: str | None = Field(None)

class PutAccessGroupsGroupidResponse(RootModel[None]):
    root: None = Field(...)

class GetAccessOpenidResponseItem(ProxmoxBaseModel):
    subdir: str | None = Field(None)

class GetAccessOpenidResponse(RootModel[list[GetAccessOpenidResponseItem]]):
    root: list[GetAccessOpenidResponseItem] = Field(...)

class PostAccessOpenidAuthUrlRequest(ProxmoxBaseModel):
    realm: str = Field(..., description='Authentication domain ID')
    redirect_url: str = Field(..., alias="redirect-url", description='Redirection Url. The client should set this to the used server url (location.origin).')

class PostAccessOpenidAuthUrlResponse(RootModel[str]):
    root: str = Field(..., description='Redirection URL.')

class PostAccessOpenidLoginRequest(ProxmoxBaseModel):
    code: str = Field(..., description='OpenId authorization code.')
    redirect_url: str = Field(..., alias="redirect-url", description='Redirection Url. The client should set this to the used server url (location.origin).')
    state: str = Field(..., description='OpenId state.')

class PostAccessOpenidLoginResponse(ProxmoxBaseModel):
    csrfprevention_token: str = Field(..., alias="CSRFPreventionToken")
    cap: dict[str, object] = Field(...)
    clustername: str | None = Field(None)
    ticket: str = Field(...)
    username: str = Field(...)

class PutAccessPasswordRequest(ProxmoxBaseModel):
    confirmation_password: str | None = Field(None, alias="confirmation-password", description='The current password of the user performing the change.')
    password: str = Field(..., description='The new password.')
    userid: str = Field(..., description='Full User ID, in the `name@realm` format.')

class PutAccessPasswordResponse(RootModel[None]):
    root: None = Field(...)

class GetAccessPermissionsResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class GetAccessRolesResponseItem(ProxmoxBaseModel):
    privs: str | None = Field(None)
    roleid: str | None = Field(None)
    special: bool | None = Field(None)

class GetAccessRolesResponse(RootModel[list[GetAccessRolesResponseItem]]):
    root: list[GetAccessRolesResponseItem] = Field(...)

class PostAccessRolesRequest(ProxmoxBaseModel):
    privs: str | None = Field(None)
    roleid: str = Field(...)

class PostAccessRolesResponse(RootModel[None]):
    root: None = Field(...)

class DeleteAccessRolesRoleidRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteAccessRolesRoleidResponse(RootModel[None]):
    root: None = Field(...)

class GetAccessRolesRoleidResponse(ProxmoxBaseModel):
    datastore_allocate: bool | None = Field(None, alias="Datastore.Allocate")
    datastore_allocate_space: bool | None = Field(None, alias="Datastore.AllocateSpace")
    datastore_allocate_template: bool | None = Field(None, alias="Datastore.AllocateTemplate")
    datastore_audit: bool | None = Field(None, alias="Datastore.Audit")
    group_allocate: bool | None = Field(None, alias="Group.Allocate")
    mapping_audit: bool | None = Field(None, alias="Mapping.Audit")
    mapping_modify: bool | None = Field(None, alias="Mapping.Modify")
    mapping_use: bool | None = Field(None, alias="Mapping.Use")
    permissions_modify: bool | None = Field(None, alias="Permissions.Modify")
    pool_allocate: bool | None = Field(None, alias="Pool.Allocate")
    pool_audit: bool | None = Field(None, alias="Pool.Audit")
    realm_allocate: bool | None = Field(None, alias="Realm.Allocate")
    realm_allocate_user: bool | None = Field(None, alias="Realm.AllocateUser")
    sdn_allocate: bool | None = Field(None, alias="SDN.Allocate")
    sdn_audit: bool | None = Field(None, alias="SDN.Audit")
    sdn_use: bool | None = Field(None, alias="SDN.Use")
    sys_access_network: bool | None = Field(None, alias="Sys.AccessNetwork")
    sys_audit: bool | None = Field(None, alias="Sys.Audit")
    sys_console: bool | None = Field(None, alias="Sys.Console")
    sys_incoming: bool | None = Field(None, alias="Sys.Incoming")
    sys_modify: bool | None = Field(None, alias="Sys.Modify")
    sys_power_mgmt: bool | None = Field(None, alias="Sys.PowerMgmt")
    sys_syslog: bool | None = Field(None, alias="Sys.Syslog")
    user_modify: bool | None = Field(None, alias="User.Modify")
    vm_allocate: bool | None = Field(None, alias="VM.Allocate")
    vm_audit: bool | None = Field(None, alias="VM.Audit")
    vm_backup: bool | None = Field(None, alias="VM.Backup")
    vm_clone: bool | None = Field(None, alias="VM.Clone")
    vm_config_cdrom: bool | None = Field(None, alias="VM.Config.CDROM")
    vm_config_cpu: bool | None = Field(None, alias="VM.Config.CPU")
    vm_config_cloudinit: bool | None = Field(None, alias="VM.Config.Cloudinit")
    vm_config_disk: bool | None = Field(None, alias="VM.Config.Disk")
    vm_config_hwtype: bool | None = Field(None, alias="VM.Config.HWType")
    vm_config_memory: bool | None = Field(None, alias="VM.Config.Memory")
    vm_config_network: bool | None = Field(None, alias="VM.Config.Network")
    vm_config_options: bool | None = Field(None, alias="VM.Config.Options")
    vm_console: bool | None = Field(None, alias="VM.Console")
    vm_guest_agent_audit: bool | None = Field(None, alias="VM.GuestAgent.Audit")
    vm_guest_agent_file_read: bool | None = Field(None, alias="VM.GuestAgent.FileRead")
    vm_guest_agent_file_system_mgmt: bool | None = Field(None, alias="VM.GuestAgent.FileSystemMgmt")
    vm_guest_agent_file_write: bool | None = Field(None, alias="VM.GuestAgent.FileWrite")
    vm_guest_agent_unrestricted: bool | None = Field(None, alias="VM.GuestAgent.Unrestricted")
    vm_migrate: bool | None = Field(None, alias="VM.Migrate")
    vm_power_mgmt: bool | None = Field(None, alias="VM.PowerMgmt")
    vm_replicate: bool | None = Field(None, alias="VM.Replicate")
    vm_snapshot: bool | None = Field(None, alias="VM.Snapshot")
    vm_snapshot_rollback: bool | None = Field(None, alias="VM.Snapshot.Rollback")

class PutAccessRolesRoleidRequest(ProxmoxBaseModel):
    append: bool | None = Field(None)
    privs: str | None = Field(None)

class PutAccessRolesRoleidResponse(RootModel[None]):
    root: None = Field(...)

class GetAccessTfaResponseItem(ProxmoxBaseModel):
    entries: list[dict[str, object]] | None = Field(None)
    tfa_locked_until: int | None = Field(None, alias="tfa-locked-until", description='Contains a timestamp until when a user is locked out of 2nd factors.')
    totp_locked: bool | None = Field(None, alias="totp-locked", description='True if the user is currently locked out of TOTP factors.')
    userid: str | None = Field(None, description='User this entry belongs to.')

class GetAccessTfaResponse(RootModel[list[GetAccessTfaResponseItem]]):
    root: list[GetAccessTfaResponseItem] = Field(..., description='The list tuples of user and TFA entries.')

class GetAccessTfaUseridResponseItem(ProxmoxBaseModel):
    created: int | None = Field(None, description='Creation time of this entry as unix epoch.')
    description: str | None = Field(None, description='User chosen description for this entry.')
    enable: bool | None = Field(None, description='Whether this TFA entry is currently enabled.')
    id: str | None = Field(None, description='The id used to reference this entry.')
    type: str | None = Field(None, description='TFA Entry Type.')

class GetAccessTfaUseridResponse(RootModel[list[GetAccessTfaUseridResponseItem]]):
    root: list[GetAccessTfaUseridResponseItem] = Field(..., description="A list of the user's TFA entries.")

class PostAccessTfaUseridRequest(ProxmoxBaseModel):
    challenge: str | None = Field(None, description='When responding to a u2f challenge: the original challenge string')
    description: str | None = Field(None, description='A description to distinguish multiple entries from one another')
    password: str | None = Field(None, description='The current password of the user performing the change.')
    totp: str | None = Field(None, description='A totp URI.')
    type: str = Field(..., description='TFA Entry Type.')
    value: str | None = Field(None, description='The current value for the provided totp URI, or a Webauthn/U2F challenge response')

class PostAccessTfaUseridResponse(ProxmoxBaseModel):
    challenge: str | None = Field(None, description='When adding u2f entries, this contains a challenge the user must respond to in order to finish the registration.')
    id: str = Field(..., description='The id of a newly added TFA entry.')
    recovery: list[str] | None = Field(None, description='When adding recovery codes, this contains the list of codes to be displayed to the user')

class DeleteAccessTfaUseridIdRequest(ProxmoxBaseModel):
    password: str | None = Field(None, description='The current password of the user performing the change.')

class DeleteAccessTfaUseridIdResponse(RootModel[None]):
    root: None = Field(...)

class GetAccessTfaUseridIdResponse(ProxmoxBaseModel):
    created: int = Field(..., description='Creation time of this entry as unix epoch.')
    description: str = Field(..., description='User chosen description for this entry.')
    enable: bool | None = Field(None, description='Whether this TFA entry is currently enabled.')
    id: str = Field(..., description='The id used to reference this entry.')
    type: str = Field(..., description='TFA Entry Type.')

class PutAccessTfaUseridIdRequest(ProxmoxBaseModel):
    description: str | None = Field(None, description='A description to distinguish multiple entries from one another')
    enable: bool | None = Field(None, description='Whether the entry should be enabled for login.')
    password: str | None = Field(None, description='The current password of the user performing the change.')

class PutAccessTfaUseridIdResponse(RootModel[None]):
    root: None = Field(...)

class GetAccessTicketResponse(RootModel[None]):
    root: None = Field(...)

class PostAccessTicketRequest(ProxmoxBaseModel):
    new_format: bool | None = Field(None, alias="new-format", description='This parameter is now ignored and assumed to be 1.')
    otp: str | None = Field(None, description='One-time password for Two-factor authentication.')
    password: str = Field(..., description='The secret password. This can also be a valid ticket.')
    path: str | None = Field(None, description="Verify ticket, and check if user have access 'privs' on 'path'")
    privs: str | None = Field(None, description="Verify ticket, and check if user have access 'privs' on 'path'")
    realm: str | None = Field(None, description='You can optionally pass the realm using this parameter. Normally the realm is simply added to the username <username>@<realm>.')
    tfa_challenge: str | None = Field(None, alias="tfa-challenge", description='The signed TFA challenge string the user wants to respond to.')
    username: str = Field(..., description='User name')

class PostAccessTicketResponse(ProxmoxBaseModel):
    csrfprevention_token: str | None = Field(None, alias="CSRFPreventionToken")
    clustername: str | None = Field(None)
    ticket: str | None = Field(None)
    username: str = Field(...)

class GetAccessUsersResponseItem(ProxmoxBaseModel):
    comment: str | None = Field(None)
    email: str | None = Field(None)
    enable: bool | None = Field(None, description="Enable the account (default). You can set this to '0' to disable the account")
    expire: int | None = Field(None, description="Account expiration date (seconds since epoch). '0' means no expiration date.")
    firstname: str | None = Field(None)
    groups: str | None = Field(None)
    keys: str | None = Field(None, description='Keys for two factor auth (yubico).')
    lastname: str | None = Field(None)
    realm_type: str | None = Field(None, alias="realm-type", description='The type of the users realm')
    tfa_locked_until: int | None = Field(None, alias="tfa-locked-until", description='Contains a timestamp until when a user is locked out of 2nd factors.')
    tokens: list[dict[str, object]] | None = Field(None)
    totp_locked: bool | None = Field(None, alias="totp-locked", description='True if the user is currently locked out of TOTP factors.')
    userid: str | None = Field(None, description='Full User ID, in the `name@realm` format.')

class GetAccessUsersResponse(RootModel[list[GetAccessUsersResponseItem]]):
    root: list[GetAccessUsersResponseItem] = Field(...)

class PostAccessUsersRequest(ProxmoxBaseModel):
    comment: str | None = Field(None)
    email: str | None = Field(None)
    enable: bool | None = Field(None, description="Enable the account (default). You can set this to '0' to disable the account")
    expire: int | None = Field(None, description="Account expiration date (seconds since epoch). '0' means no expiration date.")
    firstname: str | None = Field(None)
    groups: str | None = Field(None)
    keys: str | None = Field(None, description='Keys for two factor auth (yubico).')
    lastname: str | None = Field(None)
    password: str | None = Field(None, description='Initial password.')
    userid: str = Field(..., description='Full User ID, in the `name@realm` format.')

class PostAccessUsersResponse(RootModel[None]):
    root: None = Field(...)

class DeleteAccessUsersUseridRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteAccessUsersUseridResponse(RootModel[None]):
    root: None = Field(...)

class GetAccessUsersUseridResponse(ProxmoxBaseModel):
    comment: str | None = Field(None)
    email: str | None = Field(None)
    enable: bool | None = Field(None, description="Enable the account (default). You can set this to '0' to disable the account")
    expire: int | None = Field(None, description="Account expiration date (seconds since epoch). '0' means no expiration date.")
    firstname: str | None = Field(None)
    groups: list[str] | None = Field(None)
    keys: str | None = Field(None, description='Keys for two factor auth (yubico).')
    lastname: str | None = Field(None)
    tokens: dict[str, object] | None = Field(None)

class PutAccessUsersUseridRequest(ProxmoxBaseModel):
    append: bool | None = Field(None)
    comment: str | None = Field(None)
    email: str | None = Field(None)
    enable: bool | None = Field(None, description="Enable the account (default). You can set this to '0' to disable the account")
    expire: int | None = Field(None, description="Account expiration date (seconds since epoch). '0' means no expiration date.")
    firstname: str | None = Field(None)
    groups: str | None = Field(None)
    keys: str | None = Field(None, description='Keys for two factor auth (yubico).')
    lastname: str | None = Field(None)

class PutAccessUsersUseridResponse(RootModel[None]):
    root: None = Field(...)

class GetAccessUsersUseridTfaResponse(ProxmoxBaseModel):
    realm: str | None = Field(None, description='The type of TFA the users realm has set, if any.')
    types: list[str] | None = Field(None, description="Array of the user configured TFA types, if any. Only available if 'multiple' was not passed.")
    user: str | None = Field(None, description="The type of TFA the user has set, if any. Only set if 'multiple' was not passed.")

class GetAccessUsersUseridTokenResponseItem(ProxmoxBaseModel):
    comment: str | None = Field(None)
    expire: int | None = Field(None, description="API token expiration date (seconds since epoch). '0' means no expiration date.")
    privsep: bool | None = Field(None, description='Restrict API token privileges with separate ACLs (default), or give full privileges of corresponding user.')
    tokenid: str | None = Field(None, description='User-specific token identifier.')

class GetAccessUsersUseridTokenResponse(RootModel[list[GetAccessUsersUseridTokenResponseItem]]):
    root: list[GetAccessUsersUseridTokenResponseItem] = Field(...)

class DeleteAccessUsersUseridTokenTokenidRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteAccessUsersUseridTokenTokenidResponse(RootModel[None]):
    root: None = Field(...)

class GetAccessUsersUseridTokenTokenidResponse(ProxmoxBaseModel):
    comment: str | None = Field(None)
    expire: int | None = Field(None, description="API token expiration date (seconds since epoch). '0' means no expiration date.")
    privsep: bool | None = Field(None, description='Restrict API token privileges with separate ACLs (default), or give full privileges of corresponding user.')

class PostAccessUsersUseridTokenTokenidRequest(ProxmoxBaseModel):
    comment: str | None = Field(None)
    expire: int | None = Field(None, description="API token expiration date (seconds since epoch). '0' means no expiration date.")
    privsep: bool | None = Field(None, description='Restrict API token privileges with separate ACLs (default), or give full privileges of corresponding user.')

class PostAccessUsersUseridTokenTokenidResponse(ProxmoxBaseModel):
    full_tokenid: str = Field(..., alias="full-tokenid", description='The full token id.')
    info: dict[str, object] = Field(...)
    value: str = Field(..., description='API token value used for authentication.')

class PutAccessUsersUseridTokenTokenidRequest(ProxmoxBaseModel):
    comment: str | None = Field(None)
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    expire: int | None = Field(None, description="API token expiration date (seconds since epoch). '0' means no expiration date.")
    privsep: bool | None = Field(None, description='Restrict API token privileges with separate ACLs (default), or give full privileges of corresponding user.')

class PutAccessUsersUseridTokenTokenidResponse(ProxmoxBaseModel):
    comment: str | None = Field(None)
    expire: int | None = Field(None, description="API token expiration date (seconds since epoch). '0' means no expiration date.")
    privsep: bool | None = Field(None, description='Restrict API token privileges with separate ACLs (default), or give full privileges of corresponding user.')

class PutAccessUsersUseridUnlockTfaRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PutAccessUsersUseridUnlockTfaResponse(RootModel[bool]):
    root: bool = Field(...)

class PostAccessVncticketRequest(ProxmoxBaseModel):
    authid: str = Field(..., description='UserId or token')
    path: str = Field(..., description="Verify ticket, and check if user have access 'privs' on 'path'")
    privs: str = Field(..., description="Verify ticket, and check if user have access 'privs' on 'path'")
    vncticket: str = Field(..., description='The VNC ticket.')

class PostAccessVncticketResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetClusterAcmeResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetClusterAcmeAccountResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class PostClusterAcmeAccountRequest(ProxmoxBaseModel):
    contact: str = Field(..., description='Contact email addresses.')
    directory: str | None = Field(None, description='URL of ACME CA directory endpoint.')
    eab_hmac_key: str | None = Field(None, alias="eab-hmac-key", description='HMAC key for External Account Binding.')
    eab_kid: str | None = Field(None, alias="eab-kid", description='Key Identifier for External Account Binding.')
    name: str | None = Field(None, description='ACME account config file name.')
    tos_url: str | None = Field(None, description='URL of CA TermsOfService - setting this indicates agreement.')

class PostClusterAcmeAccountResponse(RootModel[str]):
    root: str = Field(...)

class DeleteClusterAcmeAccountNameRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteClusterAcmeAccountNameResponse(RootModel[str]):
    root: str = Field(...)

class GetClusterAcmeAccountNameResponse(ProxmoxBaseModel):
    account: dict[str, object] | None = Field(None)
    directory: str | None = Field(None, description='URL of ACME CA directory endpoint.')
    location: str | None = Field(None)
    tos: str | None = Field(None)

class PutClusterAcmeAccountNameRequest(ProxmoxBaseModel):
    contact: str | None = Field(None, description='Contact email addresses.')

class PutClusterAcmeAccountNameResponse(RootModel[str]):
    root: str = Field(...)

class GetClusterAcmeChallengeSchemaResponseItem(ProxmoxBaseModel):
    id: str | None = Field(None)
    name: str | None = Field(None, description='Human readable name, falls back to id')
    schema: dict[str, object] | None = Field(None)
    type: str | None = Field(None)

class GetClusterAcmeChallengeSchemaResponse(RootModel[list[GetClusterAcmeChallengeSchemaResponseItem]]):
    root: list[GetClusterAcmeChallengeSchemaResponseItem] = Field(...)

class GetClusterAcmeDirectoriesResponseItem(ProxmoxBaseModel):
    name: str | None = Field(None)
    url: str | None = Field(None, description='URL of ACME CA directory endpoint.')

class GetClusterAcmeDirectoriesResponse(RootModel[list[GetClusterAcmeDirectoriesResponseItem]]):
    root: list[GetClusterAcmeDirectoriesResponseItem] = Field(...)

class GetClusterAcmeMetaResponse(ProxmoxBaseModel):
    caa_identities: list[str] | None = Field(None, alias="caaIdentities", description='Hostnames referring to the ACME servers.')
    external_account_required: bool | None = Field(None, alias="externalAccountRequired", description='EAB Required')
    terms_of_service: str | None = Field(None, alias="termsOfService", description='ACME TermsOfService URL.')
    website: str | None = Field(None, description='URL to more information about the ACME server.')

class GetClusterAcmePluginsResponseItem(ProxmoxBaseModel):
    api: str | None = Field(None, description='API plugin name')
    data: str | None = Field(None, description='DNS plugin data. (base64 encoded)')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Flag to disable the config.')
    nodes: str | None = Field(None, description='List of cluster node names.')
    plugin: str | None = Field(None, description='Unique identifier for ACME plugin instance.')
    type: str | None = Field(None, description='ACME challenge type.')
    validation_delay: int | None = Field(None, alias="validation-delay", description='Extra delay in seconds to wait before requesting validation. Allows to cope with a long TTL of DNS records.')

class GetClusterAcmePluginsResponse(RootModel[list[GetClusterAcmePluginsResponseItem]]):
    root: list[GetClusterAcmePluginsResponseItem] = Field(...)

class PostClusterAcmePluginsRequest(ProxmoxBaseModel):
    api: str | None = Field(None, description='API plugin name')
    data: str | None = Field(None, description='DNS plugin data. (base64 encoded)')
    disable: bool | None = Field(None, description='Flag to disable the config.')
    id: str = Field(..., description='ACME Plugin ID name')
    nodes: str | None = Field(None, description='List of cluster node names.')
    type: str = Field(..., description='ACME challenge type.')
    validation_delay: int | None = Field(None, alias="validation-delay", description='Extra delay in seconds to wait before requesting validation. Allows to cope with a long TTL of DNS records.')

class PostClusterAcmePluginsResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterAcmePluginsIdRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteClusterAcmePluginsIdResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterAcmePluginsIdResponse(ProxmoxBaseModel):
    api: str | None = Field(None, description='API plugin name')
    data: str | None = Field(None, description='DNS plugin data. (base64 encoded)')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Flag to disable the config.')
    nodes: str | None = Field(None, description='List of cluster node names.')
    plugin: str = Field(..., description='Unique identifier for ACME plugin instance.')
    type: str = Field(..., description='ACME challenge type.')
    validation_delay: int | None = Field(None, alias="validation-delay", description='Extra delay in seconds to wait before requesting validation. Allows to cope with a long TTL of DNS records.')

class PutClusterAcmePluginsIdRequest(ProxmoxBaseModel):
    api: str | None = Field(None, description='API plugin name')
    data: str | None = Field(None, description='DNS plugin data. (base64 encoded)')
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Flag to disable the config.')
    nodes: str | None = Field(None, description='List of cluster node names.')
    validation_delay: int | None = Field(None, alias="validation-delay", description='Extra delay in seconds to wait before requesting validation. Allows to cope with a long TTL of DNS records.')

class PutClusterAcmePluginsIdResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterAcmeTosResponse(RootModel[str]):
    root: str = Field(..., description='ACME TermsOfService URL.')

class GetClusterBackupResponseItem(ProxmoxBaseModel):
    id: str | None = Field(None, description='The job ID.')

class GetClusterBackupResponse(RootModel[list[GetClusterBackupResponseItem]]):
    root: list[GetClusterBackupResponseItem] = Field(...)

class PostClusterBackupRequest(ProxmoxBaseModel):
    all: bool | None = Field(None, description='Backup all known guest systems on this host.')
    bwlimit: int | None = Field(None, description='Limit I/O bandwidth (in KiB/s).')
    comment: str | None = Field(None, description='Description for the Job.')
    compress: str | None = Field(None, description='Compress dump file.')
    dow: str | None = Field(None, description='Day of week selection.')
    dumpdir: str | None = Field(None, description='Store resulting files to specified directory.')
    enabled: bool | None = Field(None, description='Enable or disable the job.')
    exclude: str | None = Field(None, description='Exclude specified guest systems (assumes --all)')
    exclude_path: list[str] | None = Field(None, alias="exclude-path", description="Exclude certain files/directories (shell globs). Paths starting with '/' are anchored to the container's root, other paths match relative to each subdirectory.")
    fleecing: str | None = Field(None, description='Options for backup fleecing (VM only).')
    id: str | None = Field(None, description='Job ID (will be autogenerated).')
    ionice: int | None = Field(None, description='Set IO priority when using the BFQ scheduler. For snapshot and suspend mode backups of VMs, this only affects the compressor. A value of 8 means the idle priority is used, otherwise the best-effort priority is used with the specified value.')
    lockwait: int | None = Field(None, description='Maximal time to wait for the global lock (minutes).')
    mailnotification: str | None = Field(None, description='Deprecated: use notification targets/matchers instead. Specify when to send a notification mail')
    mailto: str | None = Field(None, description='Deprecated: Use notification targets/matchers instead. Comma-separated list of email addresses or users that should receive email notifications.')
    maxfiles: int | None = Field(None, description="Deprecated: use 'prune-backups' instead. Maximal number of backup files per guest system.")
    mode: str | None = Field(None, description='Backup mode.')
    node: str | None = Field(None, description='Only run if executed on this node.')
    notes_template: str | None = Field(None, alias="notes-template", description="Template string for generating notes for the backup(s). It can contain variables which will be replaced by their values. Currently supported are {{cluster}}, {{guestname}}, {{node}}, and {{vmid}}, but more might be added in the future. Needs to be a single line, newline and backslash need to be escaped as '\\n' and '\\\\' respectively.")
    notification_mode: str | None = Field(None, alias="notification-mode", description="Determine which notification system to use. If set to 'legacy-sendmail', vzdump will consider the mailto/mailnotification parameters and send emails to the specified address(es) via the 'sendmail' command. If set to 'notification-system', a notification will be sent via PVE's notification system, and the mailto and mailnotification will be ignored. If set to 'auto' (default setting), an email will be sent if mailto is set, and the notification system will be used if not.")
    pbs_change_detection_mode: str | None = Field(None, alias="pbs-change-detection-mode", description='PBS mode used to detect file changes and switch encoding format for container backups.')
    performance: str | None = Field(None, description='Other performance-related settings.')
    pigz: int | None = Field(None, description='Use pigz instead of gzip when N>0. N=1 uses half of cores, N>1 uses N as thread count.')
    pool: str | None = Field(None, description='Backup all known guest systems included in the specified pool.')
    protected: bool | None = Field(None, description='If true, mark backup(s) as protected.')
    prune_backups: str | None = Field(None, alias="prune-backups", description='Use these retention options instead of those from the storage configuration.')
    quiet: bool | None = Field(None, description='Be quiet.')
    remove: bool | None = Field(None, description="Prune older backups according to 'prune-backups'.")
    repeat_missed: bool | None = Field(None, alias="repeat-missed", description='If true, the job will be run as soon as possible if it was missed while the scheduler was not running.')
    schedule: str | None = Field(None, description='Backup schedule. The format is a subset of `systemd` calendar events.')
    script: str | None = Field(None, description='Use specified hook script.')
    starttime: str | None = Field(None, description='Job Start time.')
    stdexcludes: bool | None = Field(None, description='Exclude temporary files and logs.')
    stop: bool | None = Field(None, description='Stop running backup jobs on this host.')
    stopwait: int | None = Field(None, description='Maximal time to wait until a guest system is stopped (minutes).')
    storage: str | None = Field(None, description='Store resulting file to this storage.')
    tmpdir: str | None = Field(None, description='Store temporary files to specified directory.')
    vmid: str | None = Field(None, description='The ID of the guest system you want to backup.')
    zstd: int | None = Field(None, description='Zstd threads. N=0 uses half of the available cores, if N is set to a value bigger than 0, N is used as thread count.')

class PostClusterBackupResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterBackupInfoResponseItem(ProxmoxBaseModel):
    subdir: str | None = Field(None, description='API sub-directory endpoint')

class GetClusterBackupInfoResponse(RootModel[list[GetClusterBackupInfoResponseItem]]):
    root: list[GetClusterBackupInfoResponseItem] = Field(..., description='Directory index.')

class GetClusterBackupInfoNotBackedUpResponseItem(ProxmoxBaseModel):
    name: str | None = Field(None, description='Name of the guest')
    type: str | None = Field(None, description='Type of the guest.')
    vmid: int | None = Field(None, description='VMID of the guest.')

class GetClusterBackupInfoNotBackedUpResponse(RootModel[list[GetClusterBackupInfoNotBackedUpResponseItem]]):
    root: list[GetClusterBackupInfoNotBackedUpResponseItem] = Field(..., description='Contains the guest objects.')

class DeleteClusterBackupIdRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteClusterBackupIdResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterBackupIdResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PutClusterBackupIdRequest(ProxmoxBaseModel):
    all: bool | None = Field(None, description='Backup all known guest systems on this host.')
    bwlimit: int | None = Field(None, description='Limit I/O bandwidth (in KiB/s).')
    comment: str | None = Field(None, description='Description for the Job.')
    compress: str | None = Field(None, description='Compress dump file.')
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    dow: str | None = Field(None, description='Day of week selection.')
    dumpdir: str | None = Field(None, description='Store resulting files to specified directory.')
    enabled: bool | None = Field(None, description='Enable or disable the job.')
    exclude: str | None = Field(None, description='Exclude specified guest systems (assumes --all)')
    exclude_path: list[str] | None = Field(None, alias="exclude-path", description="Exclude certain files/directories (shell globs). Paths starting with '/' are anchored to the container's root, other paths match relative to each subdirectory.")
    fleecing: str | None = Field(None, description='Options for backup fleecing (VM only).')
    ionice: int | None = Field(None, description='Set IO priority when using the BFQ scheduler. For snapshot and suspend mode backups of VMs, this only affects the compressor. A value of 8 means the idle priority is used, otherwise the best-effort priority is used with the specified value.')
    lockwait: int | None = Field(None, description='Maximal time to wait for the global lock (minutes).')
    mailnotification: str | None = Field(None, description='Deprecated: use notification targets/matchers instead. Specify when to send a notification mail')
    mailto: str | None = Field(None, description='Deprecated: Use notification targets/matchers instead. Comma-separated list of email addresses or users that should receive email notifications.')
    maxfiles: int | None = Field(None, description="Deprecated: use 'prune-backups' instead. Maximal number of backup files per guest system.")
    mode: str | None = Field(None, description='Backup mode.')
    node: str | None = Field(None, description='Only run if executed on this node.')
    notes_template: str | None = Field(None, alias="notes-template", description="Template string for generating notes for the backup(s). It can contain variables which will be replaced by their values. Currently supported are {{cluster}}, {{guestname}}, {{node}}, and {{vmid}}, but more might be added in the future. Needs to be a single line, newline and backslash need to be escaped as '\\n' and '\\\\' respectively.")
    notification_mode: str | None = Field(None, alias="notification-mode", description="Determine which notification system to use. If set to 'legacy-sendmail', vzdump will consider the mailto/mailnotification parameters and send emails to the specified address(es) via the 'sendmail' command. If set to 'notification-system', a notification will be sent via PVE's notification system, and the mailto and mailnotification will be ignored. If set to 'auto' (default setting), an email will be sent if mailto is set, and the notification system will be used if not.")
    pbs_change_detection_mode: str | None = Field(None, alias="pbs-change-detection-mode", description='PBS mode used to detect file changes and switch encoding format for container backups.')
    performance: str | None = Field(None, description='Other performance-related settings.')
    pigz: int | None = Field(None, description='Use pigz instead of gzip when N>0. N=1 uses half of cores, N>1 uses N as thread count.')
    pool: str | None = Field(None, description='Backup all known guest systems included in the specified pool.')
    protected: bool | None = Field(None, description='If true, mark backup(s) as protected.')
    prune_backups: str | None = Field(None, alias="prune-backups", description='Use these retention options instead of those from the storage configuration.')
    quiet: bool | None = Field(None, description='Be quiet.')
    remove: bool | None = Field(None, description="Prune older backups according to 'prune-backups'.")
    repeat_missed: bool | None = Field(None, alias="repeat-missed", description='If true, the job will be run as soon as possible if it was missed while the scheduler was not running.')
    schedule: str | None = Field(None, description='Backup schedule. The format is a subset of `systemd` calendar events.')
    script: str | None = Field(None, description='Use specified hook script.')
    starttime: str | None = Field(None, description='Job Start time.')
    stdexcludes: bool | None = Field(None, description='Exclude temporary files and logs.')
    stop: bool | None = Field(None, description='Stop running backup jobs on this host.')
    stopwait: int | None = Field(None, description='Maximal time to wait until a guest system is stopped (minutes).')
    storage: str | None = Field(None, description='Store resulting file to this storage.')
    tmpdir: str | None = Field(None, description='Store temporary files to specified directory.')
    vmid: str | None = Field(None, description='The ID of the guest system you want to backup.')
    zstd: int | None = Field(None, description='Zstd threads. N=0 uses half of the available cores, if N is set to a value bigger than 0, N is used as thread count.')

class PutClusterBackupIdResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterBackupIdIncludedVolumesResponse(ProxmoxBaseModel):
    children: list[dict[str, object]] = Field(...)

class GetClusterBulkActionResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetClusterBulkActionGuestResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class PostClusterBulkActionGuestMigrateRequest(ProxmoxBaseModel):
    maxworkers: int | None = Field(None, description='How many parallel tasks at maximum should be started.')
    online: bool | None = Field(None, description='Enable live migration for VMs and restart migration for CTs.')
    target: str = Field(..., description='Target node.')
    vms: list[int] | None = Field(None, description='Only consider guests from this list of VMIDs.')
    with_local_disks: bool | None = Field(None, alias="with-local-disks", description='Enable live storage migration for local disk')

class PostClusterBulkActionGuestMigrateResponse(RootModel[str]):
    root: str = Field(..., description='UPID of the worker')

class PostClusterBulkActionGuestShutdownRequest(ProxmoxBaseModel):
    force_stop: bool | None = Field(None, alias="force-stop", description='Makes sure the Guest stops after the timeout.')
    maxworkers: int | None = Field(None, description='How many parallel tasks at maximum should be started.')
    timeout: int | None = Field(None, description='Default shutdown timeout in seconds if none is configured for the guest.')
    vms: list[int] | None = Field(None, description='Only consider guests from this list of VMIDs.')

class PostClusterBulkActionGuestShutdownResponse(RootModel[str]):
    root: str = Field(..., description='UPID of the worker')

class PostClusterBulkActionGuestStartRequest(ProxmoxBaseModel):
    maxworkers: int | None = Field(None, description='How many parallel tasks at maximum should be started.')
    timeout: int | None = Field(None, description='Default start timeout in seconds. Only valid for VMs. (default depends on the guest configuration).')
    vms: list[int] | None = Field(None, description='Only consider guests from this list of VMIDs.')

class PostClusterBulkActionGuestStartResponse(RootModel[str]):
    root: str = Field(..., description='UPID of the worker')

class PostClusterBulkActionGuestSuspendRequest(ProxmoxBaseModel):
    maxworkers: int | None = Field(None, description='How many parallel tasks at maximum should be started.')
    statestorage: str | None = Field(None, description='The storage for the VM state.')
    to_disk: bool | None = Field(None, alias="to-disk", description='If set, suspends the guests to disk. Will be resumed on next start.')
    vms: list[int] | None = Field(None, description='Only consider guests from this list of VMIDs.')

class PostClusterBulkActionGuestSuspendResponse(RootModel[str]):
    root: str = Field(..., description='UPID of the worker')

class GetClusterCephResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetClusterCephFlagsResponseItem(ProxmoxBaseModel):
    description: str | None = Field(None, description='Flag description.')
    name: str | None = Field(None, description='Flag name.')
    value: bool | None = Field(None, description='Flag value.')

class GetClusterCephFlagsResponse(RootModel[list[GetClusterCephFlagsResponseItem]]):
    root: list[GetClusterCephFlagsResponseItem] = Field(...)

class PutClusterCephFlagsRequest(ProxmoxBaseModel):
    nobackfill: bool | None = Field(None, description='Backfilling of PGs is suspended.')
    nodeep_scrub: bool | None = Field(None, alias="nodeep-scrub", description='Deep Scrubbing is disabled.')
    nodown: bool | None = Field(None, description='OSD failure reports are being ignored, such that the monitors will not mark OSDs down.')
    noin: bool | None = Field(None, description='OSDs that were previously marked out will not be marked back in when they start.')
    noout: bool | None = Field(None, description='OSDs will not automatically be marked out after the configured interval.')
    norebalance: bool | None = Field(None, description='Rebalancing of PGs is suspended.')
    norecover: bool | None = Field(None, description='Recovery of PGs is suspended.')
    noscrub: bool | None = Field(None, description='Scrubbing is disabled.')
    notieragent: bool | None = Field(None, description='Cache tiering activity is suspended.')
    noup: bool | None = Field(None, description='OSDs are not allowed to start.')
    pause: bool | None = Field(None, description='Pauses read and writes.')

class PutClusterCephFlagsResponse(RootModel[str]):
    root: str = Field(...)

class GetClusterCephFlagsFlagResponse(RootModel[bool]):
    root: bool = Field(...)

class PutClusterCephFlagsFlagRequest(ProxmoxBaseModel):
    value: bool = Field(..., description='The new value of the flag')

class PutClusterCephFlagsFlagResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterCephMetadataResponse(ProxmoxBaseModel):
    mds: dict[str, object] = Field(..., description='Metadata servers configured in the cluster and their properties.')
    mgr: dict[str, object] = Field(..., description='Managers configured in the cluster and their properties.')
    mon: dict[str, object] = Field(..., description='Monitors configured in the cluster and their properties.')
    node: dict[str, object] = Field(..., description='Ceph version installed on the nodes.')
    osd: list[object] = Field(..., description='OSDs configured in the cluster and their properties.')

class GetClusterCephStatusResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class GetClusterConfigResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class PostClusterConfigRequest(ProxmoxBaseModel):
    clustername: str = Field(..., description='The name of the cluster.')
    link_n: str | None = Field(None, alias="link[n]", description='Address and priority information of a single corosync link. (up to 8 links supported; link0..link7)')
    nodeid: int | None = Field(None, description='Node id for this node.')
    votes: int | None = Field(None, description='Number of votes for this node.')

class PostClusterConfigResponse(RootModel[str]):
    root: str = Field(...)

class GetClusterConfigApiversionResponse(RootModel[int]):
    root: int = Field(..., description='Cluster Join API version, currently 1')

class GetClusterConfigJoinResponse(ProxmoxBaseModel):
    config_digest: str = Field(...)
    nodelist: list[dict[str, object]] = Field(...)
    preferred_node: str = Field(..., description='The cluster node name.')
    totem: dict[str, object] = Field(...)

class PostClusterConfigJoinRequest(ProxmoxBaseModel):
    fingerprint: str = Field(..., description='Certificate SHA 256 fingerprint.')
    force: bool | None = Field(None, description='Do not throw error if node already exists.')
    hostname: str = Field(..., description='Hostname (or IP) of an existing cluster member.')
    link_n: str | None = Field(None, alias="link[n]", description='Address and priority information of a single corosync link. (up to 8 links supported; link0..link7)')
    nodeid: int | None = Field(None, description='Node id for this node.')
    password: str = Field(..., description='Superuser (root) password of peer node.')
    votes: int | None = Field(None, description='Number of votes for this node')

class PostClusterConfigJoinResponse(RootModel[str]):
    root: str = Field(...)

class GetClusterConfigNodesResponseItem(ProxmoxBaseModel):
    node: str | None = Field(None)

class GetClusterConfigNodesResponse(RootModel[list[GetClusterConfigNodesResponseItem]]):
    root: list[GetClusterConfigNodesResponseItem] = Field(...)

class DeleteClusterConfigNodesNodeRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteClusterConfigNodesNodeResponse(RootModel[None]):
    root: None = Field(...)

class PostClusterConfigNodesNodeRequest(ProxmoxBaseModel):
    apiversion: int | None = Field(None, description='The JOIN_API_VERSION of the new node.')
    force: bool | None = Field(None, description='Do not throw error if node already exists.')
    link_n: str | None = Field(None, alias="link[n]", description='Address and priority information of a single corosync link. (up to 8 links supported; link0..link7)')
    new_node_ip: str | None = Field(None, description='IP Address of node to add. Used as fallback if no links are given.')
    nodeid: int | None = Field(None, description='Node id for this node.')
    votes: int | None = Field(None, description='Number of votes for this node')

class PostClusterConfigNodesNodeResponse(ProxmoxBaseModel):
    corosync_authkey: str = Field(...)
    corosync_conf: str = Field(...)
    warnings: list[str] = Field(...)

class GetClusterConfigQdeviceResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class GetClusterConfigTotemResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class GetClusterFirewallResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetClusterFirewallAliasesResponseItem(ProxmoxBaseModel):
    cidr: str | None = Field(None)
    comment: str | None = Field(None)
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    name: str | None = Field(None)

class GetClusterFirewallAliasesResponse(RootModel[list[GetClusterFirewallAliasesResponseItem]]):
    root: list[GetClusterFirewallAliasesResponseItem] = Field(...)

class PostClusterFirewallAliasesRequest(ProxmoxBaseModel):
    cidr: str = Field(..., description='Network/IP specification in CIDR format.')
    comment: str | None = Field(None)
    name: str = Field(..., description='Alias name.')

class PostClusterFirewallAliasesResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterFirewallAliasesNameRequest(ProxmoxBaseModel):
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteClusterFirewallAliasesNameResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterFirewallAliasesNameResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PutClusterFirewallAliasesNameRequest(ProxmoxBaseModel):
    cidr: str = Field(..., description='Network/IP specification in CIDR format.')
    comment: str | None = Field(None)
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    rename: str | None = Field(None, description='Rename an existing alias.')

class PutClusterFirewallAliasesNameResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterFirewallGroupsResponseItem(ProxmoxBaseModel):
    comment: str | None = Field(None)
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    group: str | None = Field(None, description='Security Group name.')

class GetClusterFirewallGroupsResponse(RootModel[list[GetClusterFirewallGroupsResponseItem]]):
    root: list[GetClusterFirewallGroupsResponseItem] = Field(...)

class PostClusterFirewallGroupsRequest(ProxmoxBaseModel):
    comment: str | None = Field(None)
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    group: str = Field(..., description='Security Group name.')
    rename: str | None = Field(None, description="Rename/update an existing security group. You can set 'rename' to the same value as 'name' to update the 'comment' of an existing group.")

class PostClusterFirewallGroupsResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterFirewallGroupsGroupRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteClusterFirewallGroupsGroupResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterFirewallGroupsGroupResponseItem(ProxmoxBaseModel):
    action: str | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: str | None = Field(None, description='Descriptive comment')
    dest: str | None = Field(None, description='Restrict packet destination address')
    dport: str | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: str | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: str | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: str | None = Field(None, description='Log level for firewall rule')
    macro: str | None = Field(None, description='Use predefined standard macro')
    pos: int | None = Field(None, description='Rule position in the ruleset')
    proto: str | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: str | None = Field(None, description='Restrict packet source address')
    sport: str | None = Field(None, description='Restrict TCP/UDP source port')
    type: str | None = Field(None, description='Rule type')

class GetClusterFirewallGroupsGroupResponse(RootModel[list[GetClusterFirewallGroupsGroupResponseItem]]):
    root: list[GetClusterFirewallGroupsGroupResponseItem] = Field(...)

class PostClusterFirewallGroupsGroupRequest(ProxmoxBaseModel):
    action: str = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: str | None = Field(None, description='Descriptive comment.')
    dest: str | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: str | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: str | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: str | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: str | None = Field(None, description='Log level for firewall rule.')
    macro: str | None = Field(None, description='Use predefined standard macro.')
    pos: int | None = Field(None, description='Update rule at position <pos>.')
    proto: str | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: str | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: str | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: str = Field(..., description='Rule type.')

class PostClusterFirewallGroupsGroupResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterFirewallGroupsGroupPosRequest(ProxmoxBaseModel):
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteClusterFirewallGroupsGroupPosResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterFirewallGroupsGroupPosResponse(ProxmoxBaseModel):
    action: str = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: str | None = Field(None, description='Descriptive comment')
    dest: str | None = Field(None, description='Restrict packet destination address')
    dport: str | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: str | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: str | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: str | None = Field(None, description='Log level for firewall rule')
    macro: str | None = Field(None, description='Use predefined standard macro')
    pos: int = Field(..., description='Rule position in the ruleset')
    proto: str | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: str | None = Field(None, description='Restrict packet source address')
    sport: str | None = Field(None, description='Restrict TCP/UDP source port')
    type: str = Field(..., description='Rule type')

class PutClusterFirewallGroupsGroupPosRequest(ProxmoxBaseModel):
    action: str | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: str | None = Field(None, description='Descriptive comment.')
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    dest: str | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: str | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: str | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: str | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: str | None = Field(None, description='Log level for firewall rule.')
    macro: str | None = Field(None, description='Use predefined standard macro.')
    moveto: int | None = Field(None, description='Move rule to new position <moveto>. Other arguments are ignored.')
    proto: str | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: str | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: str | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: str | None = Field(None, description='Rule type.')

class PutClusterFirewallGroupsGroupPosResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterFirewallIpsetResponseItem(ProxmoxBaseModel):
    comment: str | None = Field(None)
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    name: str | None = Field(None, description='IP set name.')

class GetClusterFirewallIpsetResponse(RootModel[list[GetClusterFirewallIpsetResponseItem]]):
    root: list[GetClusterFirewallIpsetResponseItem] = Field(...)

class PostClusterFirewallIpsetRequest(ProxmoxBaseModel):
    comment: str | None = Field(None)
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    name: str = Field(..., description='IP set name.')
    rename: str | None = Field(None, description="Rename an existing IPSet. You can set 'rename' to the same value as 'name' to update the 'comment' of an existing IPSet.")

class PostClusterFirewallIpsetResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterFirewallIpsetNameRequest(ProxmoxBaseModel):
    force: bool | None = Field(None, description='Delete all members of the IPSet, if there are any.')

class DeleteClusterFirewallIpsetNameResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterFirewallIpsetNameResponseItem(ProxmoxBaseModel):
    cidr: str | None = Field(None)
    comment: str | None = Field(None)
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    nomatch: bool | None = Field(None)

class GetClusterFirewallIpsetNameResponse(RootModel[list[GetClusterFirewallIpsetNameResponseItem]]):
    root: list[GetClusterFirewallIpsetNameResponseItem] = Field(...)

class PostClusterFirewallIpsetNameRequest(ProxmoxBaseModel):
    cidr: str = Field(..., description='Network/IP specification in CIDR format.')
    comment: str | None = Field(None)
    nomatch: bool | None = Field(None)

class PostClusterFirewallIpsetNameResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterFirewallIpsetNameCidrRequest(ProxmoxBaseModel):
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteClusterFirewallIpsetNameCidrResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterFirewallIpsetNameCidrResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PutClusterFirewallIpsetNameCidrRequest(ProxmoxBaseModel):
    comment: str | None = Field(None)
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    nomatch: bool | None = Field(None)

class PutClusterFirewallIpsetNameCidrResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterFirewallMacrosResponseItem(ProxmoxBaseModel):
    descr: str | None = Field(None, description='More verbose description (if available).')
    macro: str | None = Field(None, description='Macro name.')

class GetClusterFirewallMacrosResponse(RootModel[list[GetClusterFirewallMacrosResponseItem]]):
    root: list[GetClusterFirewallMacrosResponseItem] = Field(...)

class GetClusterFirewallOptionsResponse(ProxmoxBaseModel):
    ebtables: bool | None = Field(None, description='Enable ebtables rules cluster wide.')
    enable: int | None = Field(None, description='Enable or disable the firewall cluster wide.')
    log_ratelimit: str | None = Field(None, description='Log ratelimiting settings')
    policy_forward: str | None = Field(None, description='Forward policy.')
    policy_in: str | None = Field(None, description='Input policy.')
    policy_out: str | None = Field(None, description='Output policy.')

class PutClusterFirewallOptionsRequest(ProxmoxBaseModel):
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    ebtables: bool | None = Field(None, description='Enable ebtables rules cluster wide.')
    enable: int | None = Field(None, description='Enable or disable the firewall cluster wide.')
    log_ratelimit: str | None = Field(None, description='Log ratelimiting settings')
    policy_forward: str | None = Field(None, description='Forward policy.')
    policy_in: str | None = Field(None, description='Input policy.')
    policy_out: str | None = Field(None, description='Output policy.')

class PutClusterFirewallOptionsResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterFirewallRefsResponseItem(ProxmoxBaseModel):
    comment: str | None = Field(None)
    name: str | None = Field(None)
    ref: str | None = Field(None)
    scope: str | None = Field(None)
    type: str | None = Field(None)

class GetClusterFirewallRefsResponse(RootModel[list[GetClusterFirewallRefsResponseItem]]):
    root: list[GetClusterFirewallRefsResponseItem] = Field(...)

class GetClusterFirewallRulesResponseItem(ProxmoxBaseModel):
    action: str | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: str | None = Field(None, description='Descriptive comment')
    dest: str | None = Field(None, description='Restrict packet destination address')
    dport: str | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: str | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: str | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: str | None = Field(None, description='Log level for firewall rule')
    macro: str | None = Field(None, description='Use predefined standard macro')
    pos: int | None = Field(None, description='Rule position in the ruleset')
    proto: str | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: str | None = Field(None, description='Restrict packet source address')
    sport: str | None = Field(None, description='Restrict TCP/UDP source port')
    type: str | None = Field(None, description='Rule type')

class GetClusterFirewallRulesResponse(RootModel[list[GetClusterFirewallRulesResponseItem]]):
    root: list[GetClusterFirewallRulesResponseItem] = Field(...)

class PostClusterFirewallRulesRequest(ProxmoxBaseModel):
    action: str = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: str | None = Field(None, description='Descriptive comment.')
    dest: str | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: str | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: str | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: str | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: str | None = Field(None, description='Log level for firewall rule.')
    macro: str | None = Field(None, description='Use predefined standard macro.')
    pos: int | None = Field(None, description='Update rule at position <pos>.')
    proto: str | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: str | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: str | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: str = Field(..., description='Rule type.')

class PostClusterFirewallRulesResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterFirewallRulesPosRequest(ProxmoxBaseModel):
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteClusterFirewallRulesPosResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterFirewallRulesPosResponse(ProxmoxBaseModel):
    action: str = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: str | None = Field(None, description='Descriptive comment')
    dest: str | None = Field(None, description='Restrict packet destination address')
    dport: str | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: str | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: str | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: str | None = Field(None, description='Log level for firewall rule')
    macro: str | None = Field(None, description='Use predefined standard macro')
    pos: int = Field(..., description='Rule position in the ruleset')
    proto: str | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: str | None = Field(None, description='Restrict packet source address')
    sport: str | None = Field(None, description='Restrict TCP/UDP source port')
    type: str = Field(..., description='Rule type')

class PutClusterFirewallRulesPosRequest(ProxmoxBaseModel):
    action: str | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: str | None = Field(None, description='Descriptive comment.')
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    dest: str | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: str | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: str | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: str | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: str | None = Field(None, description='Log level for firewall rule.')
    macro: str | None = Field(None, description='Use predefined standard macro.')
    moveto: int | None = Field(None, description='Move rule to new position <moveto>. Other arguments are ignored.')
    proto: str | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: str | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: str | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: str | None = Field(None, description='Rule type.')

class PutClusterFirewallRulesPosResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterHaResponseItem(ProxmoxBaseModel):
    id: str | None = Field(None)

class GetClusterHaResponse(RootModel[list[GetClusterHaResponseItem]]):
    root: list[GetClusterHaResponseItem] = Field(...)

class GetClusterHaGroupsResponseItem(ProxmoxBaseModel):
    group: str | None = Field(None)

class GetClusterHaGroupsResponse(RootModel[list[GetClusterHaGroupsResponseItem]]):
    root: list[GetClusterHaGroupsResponseItem] = Field(...)

class PostClusterHaGroupsRequest(ProxmoxBaseModel):
    comment: str | None = Field(None, description='Description.')
    group: str = Field(..., description='The HA group identifier.')
    nodes: str = Field(..., description='List of cluster node names with optional priority.')
    nofailback: bool | None = Field(None, description='The CRM tries to run services on the node with the highest priority. If a node with higher priority comes online, the CRM migrates the service to that node. Enabling nofailback prevents that behavior.')
    restricted: bool | None = Field(None, description='Resources bound to restricted groups may only run on nodes defined by the group.')
    type: str | None = Field(None, description='Group type.')

class PostClusterHaGroupsResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterHaGroupsGroupRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteClusterHaGroupsGroupResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterHaGroupsGroupResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PutClusterHaGroupsGroupRequest(ProxmoxBaseModel):
    comment: str | None = Field(None, description='Description.')
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    nodes: str | None = Field(None, description='List of cluster node names with optional priority.')
    nofailback: bool | None = Field(None, description='The CRM tries to run services on the node with the highest priority. If a node with higher priority comes online, the CRM migrates the service to that node. Enabling nofailback prevents that behavior.')
    restricted: bool | None = Field(None, description='Resources bound to restricted groups may only run on nodes defined by the group.')

class PutClusterHaGroupsGroupResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterHaResourcesResponseItem(ProxmoxBaseModel):
    sid: str | None = Field(None)

class GetClusterHaResourcesResponse(RootModel[list[GetClusterHaResourcesResponseItem]]):
    root: list[GetClusterHaResourcesResponseItem] = Field(...)

class PostClusterHaResourcesRequest(ProxmoxBaseModel):
    comment: str | None = Field(None, description='Description.')
    failback: bool | None = Field(None, description='Automatically migrate HA resource to the node with the highest priority according to their node affinity  rules, if a node with a higher priority than the current node comes online.')
    group: str | None = Field(None, description='The HA group identifier.')
    max_relocate: int | None = Field(None, description='Maximal number of service relocate tries when a service failes to start.')
    max_restart: int | None = Field(None, description='Maximal number of tries to restart the service on a node after its start failed.')
    sid: str = Field(..., description='HA resource ID. This consists of a resource type followed by a resource specific name, separated with colon (example: vm:100 / ct:100). For virtual machines and containers, you can simply use the VM or CT id as a shortcut (example: 100).')
    state: str | None = Field(None, description='Requested resource state.')
    type: str | None = Field(None, description='Resource type.')

class PostClusterHaResourcesResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterHaResourcesSidRequest(ProxmoxBaseModel):
    purge: bool | None = Field(None, description='Remove this resource from rules that reference it, deleting the rule if this resource is the only resource in the rule')

class DeleteClusterHaResourcesSidResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterHaResourcesSidResponse(ProxmoxBaseModel):
    comment: str | None = Field(None, description='Description.')
    digest: str = Field(..., description='Can be used to prevent concurrent modifications.')
    failback: bool | None = Field(None, description='The HA resource is automatically migrated to the node with the highest priority according to their node affinity rule, if a node with a higher priority than the current node comes online.')
    group: str | None = Field(None, description='The HA group identifier.')
    max_relocate: int | None = Field(None, description='Maximal number of service relocate tries when a service failes to start.')
    max_restart: int | None = Field(None, description='Maximal number of tries to restart the service on a node after its start failed.')
    sid: str = Field(..., description='HA resource ID. This consists of a resource type followed by a resource specific name, separated with colon (example: vm:100 / ct:100). For virtual machines and containers, you can simply use the VM or CT id as a shortcut (example: 100).')
    state: str | None = Field(None, description='Requested resource state.')
    type: str = Field(..., description='The type of the resources.')

class PutClusterHaResourcesSidRequest(ProxmoxBaseModel):
    comment: str | None = Field(None, description='Description.')
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    failback: bool | None = Field(None, description='Automatically migrate HA resource to the node with the highest priority according to their node affinity  rules, if a node with a higher priority than the current node comes online.')
    group: str | None = Field(None, description='The HA group identifier.')
    max_relocate: int | None = Field(None, description='Maximal number of service relocate tries when a service failes to start.')
    max_restart: int | None = Field(None, description='Maximal number of tries to restart the service on a node after its start failed.')
    state: str | None = Field(None, description='Requested resource state.')

class PutClusterHaResourcesSidResponse(RootModel[None]):
    root: None = Field(...)

class PostClusterHaResourcesSidMigrateRequest(ProxmoxBaseModel):
    node: str = Field(..., description='Target node.')

class PostClusterHaResourcesSidMigrateResponse(ProxmoxBaseModel):
    blocking_resources: list[dict[str, object]] | None = Field(None, alias="blocking-resources", description='HA resources, which are blocking the given HA resource from being migrated to the requested target node.')
    comigrated_resources: list[object] | None = Field(None, alias="comigrated-resources", description='HA resources, which are migrated to the same requested target node as the given HA resource, because these are in positive affinity with the HA resource.')
    requested_node: str = Field(..., alias="requested-node", description='Node, which was requested to be migrated to.')
    sid: str = Field(..., description='HA resource, which is requested to be migrated.')

class PostClusterHaResourcesSidRelocateRequest(ProxmoxBaseModel):
    node: str = Field(..., description='Target node.')

class PostClusterHaResourcesSidRelocateResponse(ProxmoxBaseModel):
    blocking_resources: list[dict[str, object]] | None = Field(None, alias="blocking-resources", description='HA resources, which are blocking the given HA resource from being relocated to the requested target node.')
    comigrated_resources: list[str] | None = Field(None, alias="comigrated-resources", description='HA resources, which are relocated to the same requested target node as the given HA resource, because these are in positive affinity with the HA resource.')
    requested_node: str = Field(..., alias="requested-node", description='Node, which was requested to be relocated to.')
    sid: str = Field(..., description='HA resource, which is requested to be relocated.')

class GetClusterHaRulesResponseItem(ProxmoxBaseModel):
    rule: str | None = Field(None)

class GetClusterHaRulesResponse(RootModel[list[GetClusterHaRulesResponseItem]]):
    root: list[GetClusterHaRulesResponseItem] = Field(...)

class PostClusterHaRulesRequest(ProxmoxBaseModel):
    affinity: str | None = Field(None, description="Describes whether the HA resources are supposed to be kept on the same node ('positive'), or are supposed to be kept on separate nodes ('negative').")
    comment: str | None = Field(None, description='HA rule description.')
    disable: bool | None = Field(None, description='Whether the HA rule is disabled.')
    nodes: str | None = Field(None, description='List of cluster node names with optional priority.')
    resources: str = Field(..., description='List of HA resource IDs. This consists of a list of resource types followed by a resource specific name separated with a colon (example: vm:100,ct:101).')
    rule: str = Field(..., description='HA rule identifier.')
    strict: bool | None = Field(None, description='Describes whether the node affinity rule is strict or non-strict.')
    type: str = Field(..., description='HA rule type.')

class PostClusterHaRulesResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterHaRulesRuleRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteClusterHaRulesRuleResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterHaRulesRuleResponse(ProxmoxBaseModel):
    rule: str = Field(..., description='HA rule identifier.')
    type: str = Field(..., description='HA rule type.')

class PutClusterHaRulesRuleRequest(ProxmoxBaseModel):
    affinity: str | None = Field(None, description="Describes whether the HA resources are supposed to be kept on the same node ('positive'), or are supposed to be kept on separate nodes ('negative').")
    comment: str | None = Field(None, description='HA rule description.')
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Whether the HA rule is disabled.')
    nodes: str | None = Field(None, description='List of cluster node names with optional priority.')
    resources: str | None = Field(None, description='List of HA resource IDs. This consists of a list of resource types followed by a resource specific name separated with a colon (example: vm:100,ct:101).')
    strict: bool | None = Field(None, description='Describes whether the node affinity rule is strict or non-strict.')
    type: str = Field(..., description='HA rule type.')

class PutClusterHaRulesRuleResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterHaStatusResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetClusterHaStatusCurrentResponseItem(ProxmoxBaseModel):
    crm_state: str | None = Field(None, description="For type 'service'. Service state as seen by the CRM.")
    failback: bool | None = Field(None, description='The HA resource is automatically migrated to the node with the highest priority according to their node affinity rule, if a node with a higher priority than the current node comes online.')
    id: str | None = Field(None, description='Status entry ID (quorum, master, lrm:<node>, service:<sid>).')
    max_relocate: int | None = Field(None, description="For type 'service'.")
    max_restart: int | None = Field(None, description="For type 'service'.")
    node: str | None = Field(None, description='Node associated to status entry.')
    quorate: bool | None = Field(None, description="For type 'quorum'. Whether the cluster is quorate or not.")
    request_state: str | None = Field(None, description="For type 'service'. Requested service state.")
    sid: str | None = Field(None, description="For type 'service'. Service ID.")
    state: str | None = Field(None, description="For type 'service'. Verbose service state.")
    status: str | None = Field(None, description='Status of the entry (value depends on type).')
    timestamp: int | None = Field(None, description="For type 'lrm','master'. Timestamp of the status information.")
    type: object | None = Field(None, description='Type of status entry.')

class GetClusterHaStatusCurrentResponse(RootModel[list[GetClusterHaStatusCurrentResponseItem]]):
    root: list[GetClusterHaStatusCurrentResponseItem] = Field(...)

class GetClusterHaStatusManagerStatusResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class GetClusterJobsResponseItem(ProxmoxBaseModel):
    subdir: str | None = Field(None, description='API sub-directory endpoint')

class GetClusterJobsResponse(RootModel[list[GetClusterJobsResponseItem]]):
    root: list[GetClusterJobsResponseItem] = Field(..., description='Directory index.')

class GetClusterJobsRealmSyncResponseItem(ProxmoxBaseModel):
    comment: str | None = Field(None, description='A comment for the job.')
    enabled: bool | None = Field(None, description='If the job is enabled or not.')
    id: str | None = Field(None, description='The ID of the entry.')
    last_run: int | None = Field(None, alias="last-run", description='Last execution time of the job in seconds since the beginning of the UNIX epoch')
    next_run: int | None = Field(None, alias="next-run", description='Next planned execution time of the job in seconds since the beginning of the UNIX epoch.')
    realm: str | None = Field(None, description='Authentication domain ID')
    remove_vanished: str | None = Field(None, alias="remove-vanished", description="A semicolon-separated list of things to remove when they or the user vanishes during a sync. The following values are possible: 'entry' removes the user/group when not returned from the sync. 'properties' removes the set properties on existing user/group that do not appear in the source (even custom ones). 'acl' removes acls when the user/group is not returned from the sync. Instead of a list it also can be 'none' (the default).")
    schedule: str | None = Field(None, description='The configured sync schedule.')
    scope: str | None = Field(None, description='Select what to sync.')

class GetClusterJobsRealmSyncResponse(RootModel[list[GetClusterJobsRealmSyncResponseItem]]):
    root: list[GetClusterJobsRealmSyncResponseItem] = Field(...)

class DeleteClusterJobsRealmSyncIdRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteClusterJobsRealmSyncIdResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterJobsRealmSyncIdResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostClusterJobsRealmSyncIdRequest(ProxmoxBaseModel):
    comment: str | None = Field(None, description='Description for the Job.')
    enable_new: bool | None = Field(None, alias="enable-new", description='Enable newly synced users immediately.')
    enabled: bool | None = Field(None, description='Determines if the job is enabled.')
    realm: str | None = Field(None, description='Authentication domain ID')
    remove_vanished: str | None = Field(None, alias="remove-vanished", description="A semicolon-separated list of things to remove when they or the user vanishes during a sync. The following values are possible: 'entry' removes the user/group when not returned from the sync. 'properties' removes the set properties on existing user/group that do not appear in the source (even custom ones). 'acl' removes acls when the user/group is not returned from the sync. Instead of a list it also can be 'none' (the default).")
    schedule: str = Field(..., description='Backup schedule. The format is a subset of `systemd` calendar events.')
    scope: str | None = Field(None, description='Select what to sync.')

class PostClusterJobsRealmSyncIdResponse(RootModel[None]):
    root: None = Field(...)

class PutClusterJobsRealmSyncIdRequest(ProxmoxBaseModel):
    comment: str | None = Field(None, description='Description for the Job.')
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    enable_new: bool | None = Field(None, alias="enable-new", description='Enable newly synced users immediately.')
    enabled: bool | None = Field(None, description='Determines if the job is enabled.')
    remove_vanished: str | None = Field(None, alias="remove-vanished", description="A semicolon-separated list of things to remove when they or the user vanishes during a sync. The following values are possible: 'entry' removes the user/group when not returned from the sync. 'properties' removes the set properties on existing user/group that do not appear in the source (even custom ones). 'acl' removes acls when the user/group is not returned from the sync. Instead of a list it also can be 'none' (the default).")
    schedule: str = Field(..., description='Backup schedule. The format is a subset of `systemd` calendar events.')
    scope: str | None = Field(None, description='Select what to sync.')

class PutClusterJobsRealmSyncIdResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterJobsScheduleAnalyzeResponseItem(ProxmoxBaseModel):
    timestamp: int | None = Field(None, description='UNIX timestamp for the run.')
    utc: str | None = Field(None, description='UTC timestamp for the run.')

class GetClusterJobsScheduleAnalyzeResponse(RootModel[list[GetClusterJobsScheduleAnalyzeResponseItem]]):
    root: list[GetClusterJobsScheduleAnalyzeResponseItem] = Field(..., description='An array of the next <iterations> events since <starttime>.')

class GetClusterLogResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetClusterMappingResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetClusterMappingDirResponseItem(ProxmoxBaseModel):
    checks: list[dict[str, object]] | None = Field(None, description="A list of checks, only present if 'check-node' is set.")
    description: str | None = Field(None, description='A description of the logical mapping.')
    id: str | None = Field(None, description='The logical ID of the mapping.')
    map: list[str] | None = Field(None, description='The entries of the mapping.')

class GetClusterMappingDirResponse(RootModel[list[GetClusterMappingDirResponseItem]]):
    root: list[GetClusterMappingDirResponseItem] = Field(...)

class PostClusterMappingDirRequest(ProxmoxBaseModel):
    description: str | None = Field(None, description='Description of the directory mapping')
    id: str = Field(..., description='The ID of the directory mapping')
    map: list[str] = Field(..., description='A list of maps for the cluster nodes.')

class PostClusterMappingDirResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterMappingDirIdRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteClusterMappingDirIdResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterMappingDirIdResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PutClusterMappingDirIdRequest(ProxmoxBaseModel):
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    description: str | None = Field(None, description='Description of the directory mapping')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    map: list[str] | None = Field(None, description='A list of maps for the cluster nodes.')

class PutClusterMappingDirIdResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterMappingPciResponseItem(ProxmoxBaseModel):
    checks: list[dict[str, object]] | None = Field(None, description="A list of checks, only present if 'check_node' is set.")
    description: str | None = Field(None, description='A description of the logical mapping.')
    id: str | None = Field(None, description='The logical ID of the mapping.')
    map: list[str] | None = Field(None, description='The entries of the mapping.')

class GetClusterMappingPciResponse(RootModel[list[GetClusterMappingPciResponseItem]]):
    root: list[GetClusterMappingPciResponseItem] = Field(...)

class PostClusterMappingPciRequest(ProxmoxBaseModel):
    description: str | None = Field(None, description='Description of the logical PCI device.')
    id: str = Field(..., description='The ID of the logical PCI mapping.')
    live_migration_capable: bool | None = Field(None, alias="live-migration-capable", description='Marks the device(s) as being able to be live-migrated (Experimental). This needs hardware and driver support to work.')
    map: list[str] = Field(..., description='A list of maps for the cluster nodes.')
    mdev: bool | None = Field(None, description='Marks the device(s) as being capable of providing mediated devices.')

class PostClusterMappingPciResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterMappingPciIdRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteClusterMappingPciIdResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterMappingPciIdResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PutClusterMappingPciIdRequest(ProxmoxBaseModel):
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    description: str | None = Field(None, description='Description of the logical PCI device.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    live_migration_capable: bool | None = Field(None, alias="live-migration-capable", description='Marks the device(s) as being able to be live-migrated (Experimental). This needs hardware and driver support to work.')
    map: list[str] | None = Field(None, description='A list of maps for the cluster nodes.')
    mdev: bool | None = Field(None, description='Marks the device(s) as being capable of providing mediated devices.')

class PutClusterMappingPciIdResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterMappingUsbResponseItem(ProxmoxBaseModel):
    description: str | None = Field(None, description='A description of the logical mapping.')
    error: object | None = Field(None, description="A list of errors when 'check_node' is given.")
    id: str | None = Field(None, description='The logical ID of the mapping.')
    map: list[str] | None = Field(None, description='The entries of the mapping.')

class GetClusterMappingUsbResponse(RootModel[list[GetClusterMappingUsbResponseItem]]):
    root: list[GetClusterMappingUsbResponseItem] = Field(...)

class PostClusterMappingUsbRequest(ProxmoxBaseModel):
    description: str | None = Field(None, description='Description of the logical USB device.')
    id: str = Field(..., description='The ID of the logical USB mapping.')
    map: list[str] = Field(..., description='A list of maps for the cluster nodes.')

class PostClusterMappingUsbResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterMappingUsbIdRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteClusterMappingUsbIdResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterMappingUsbIdResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PutClusterMappingUsbIdRequest(ProxmoxBaseModel):
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    description: str | None = Field(None, description='Description of the logical USB device.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    map: list[str] = Field(..., description='A list of maps for the cluster nodes.')

class PutClusterMappingUsbIdResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterMetricsResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetClusterMetricsExportResponse(ProxmoxBaseModel):
    data: list[dict[str, object]] = Field(..., description='Array of system metrics. Metrics are sorted by their timestamp.')

class GetClusterMetricsServerResponseItem(ProxmoxBaseModel):
    disable: bool | None = Field(None, description='Flag to disable the plugin.')
    id: str | None = Field(None, description='The ID of the entry.')
    port: int | None = Field(None, description='Server network port')
    server: str | None = Field(None, description='Server dns name or IP address')
    type: str | None = Field(None, description='Plugin type.')

class GetClusterMetricsServerResponse(RootModel[list[GetClusterMetricsServerResponseItem]]):
    root: list[GetClusterMetricsServerResponseItem] = Field(...)

class DeleteClusterMetricsServerIdRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteClusterMetricsServerIdResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterMetricsServerIdResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostClusterMetricsServerIdRequest(ProxmoxBaseModel):
    api_path_prefix: str | None = Field(None, alias="api-path-prefix", description="An API path prefix inserted between '<host>:<port>/' and '/api2/'. Can be useful if the InfluxDB service runs behind a reverse proxy.")
    bucket: str | None = Field(None, description='The InfluxDB bucket/db. Only necessary when using the http v2 api.')
    disable: bool | None = Field(None, description='Flag to disable the plugin.')
    influxdbproto: str | None = Field(None)
    max_body_size: int | None = Field(None, alias="max-body-size", description='InfluxDB max-body-size in bytes. Requests are batched up to this size.')
    mtu: int | None = Field(None, description='MTU for metrics transmission over UDP')
    organization: str | None = Field(None, description='The InfluxDB organization. Only necessary when using the http v2 api. Has no meaning when using v2 compatibility api.')
    otel_compression: str | None = Field(None, alias="otel-compression", description='Compression algorithm for requests')
    otel_headers: str | None = Field(None, alias="otel-headers", description='Custom HTTP headers (JSON format, base64 encoded)')
    otel_max_body_size: int | None = Field(None, alias="otel-max-body-size", description='Maximum request body size in bytes')
    otel_path: str | None = Field(None, alias="otel-path", description='OTLP endpoint path')
    otel_protocol: str | None = Field(None, alias="otel-protocol", description='HTTP protocol')
    otel_resource_attributes: str | None = Field(None, alias="otel-resource-attributes", description='Additional resource attributes as JSON, base64 encoded')
    otel_timeout: int | None = Field(None, alias="otel-timeout", description='HTTP request timeout in seconds')
    otel_verify_ssl: bool | None = Field(None, alias="otel-verify-ssl", description='Verify SSL certificates')
    path: str | None = Field(None, description='root graphite path (ex: proxmox.mycluster.mykey)')
    port: int = Field(..., description='server network port')
    proto: str | None = Field(None, description='Protocol to send graphite data. TCP or UDP (default)')
    server: str = Field(..., description='server dns name or IP address')
    timeout: int | None = Field(None, description='graphite TCP socket timeout (default=1)')
    token: str | None = Field(None, description="The InfluxDB access token. Only necessary when using the http v2 api. If the v2 compatibility api is used, use 'user:password' instead.")
    type: str = Field(..., description='Plugin type.')
    verify_certificate: bool | None = Field(None, alias="verify-certificate", description='Set to 0 to disable certificate verification for https endpoints.')

class PostClusterMetricsServerIdResponse(RootModel[None]):
    root: None = Field(...)

class PutClusterMetricsServerIdRequest(ProxmoxBaseModel):
    api_path_prefix: str | None = Field(None, alias="api-path-prefix", description="An API path prefix inserted between '<host>:<port>/' and '/api2/'. Can be useful if the InfluxDB service runs behind a reverse proxy.")
    bucket: str | None = Field(None, description='The InfluxDB bucket/db. Only necessary when using the http v2 api.')
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Flag to disable the plugin.')
    influxdbproto: str | None = Field(None)
    max_body_size: int | None = Field(None, alias="max-body-size", description='InfluxDB max-body-size in bytes. Requests are batched up to this size.')
    mtu: int | None = Field(None, description='MTU for metrics transmission over UDP')
    organization: str | None = Field(None, description='The InfluxDB organization. Only necessary when using the http v2 api. Has no meaning when using v2 compatibility api.')
    otel_compression: str | None = Field(None, alias="otel-compression", description='Compression algorithm for requests')
    otel_headers: str | None = Field(None, alias="otel-headers", description='Custom HTTP headers (JSON format, base64 encoded)')
    otel_max_body_size: int | None = Field(None, alias="otel-max-body-size", description='Maximum request body size in bytes')
    otel_path: str | None = Field(None, alias="otel-path", description='OTLP endpoint path')
    otel_protocol: str | None = Field(None, alias="otel-protocol", description='HTTP protocol')
    otel_resource_attributes: str | None = Field(None, alias="otel-resource-attributes", description='Additional resource attributes as JSON, base64 encoded')
    otel_timeout: int | None = Field(None, alias="otel-timeout", description='HTTP request timeout in seconds')
    otel_verify_ssl: bool | None = Field(None, alias="otel-verify-ssl", description='Verify SSL certificates')
    path: str | None = Field(None, description='root graphite path (ex: proxmox.mycluster.mykey)')
    port: int = Field(..., description='server network port')
    proto: str | None = Field(None, description='Protocol to send graphite data. TCP or UDP (default)')
    server: str = Field(..., description='server dns name or IP address')
    timeout: int | None = Field(None, description='graphite TCP socket timeout (default=1)')
    token: str | None = Field(None, description="The InfluxDB access token. Only necessary when using the http v2 api. If the v2 compatibility api is used, use 'user:password' instead.")
    verify_certificate: bool | None = Field(None, alias="verify-certificate", description='Set to 0 to disable certificate verification for https endpoints.')

class PutClusterMetricsServerIdResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterNextidResponse(RootModel[int]):
    root: int = Field(..., description='The next free VMID.')

class GetClusterNotificationsResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetClusterNotificationsEndpointsResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetClusterNotificationsEndpointsGotifyResponseItem(ProxmoxBaseModel):
    comment: str | None = Field(None, description='Comment')
    disable: bool | None = Field(None, description='Disable this target')
    name: str | None = Field(None, description='The name of the endpoint.')
    origin: str | None = Field(None, description='Show if this entry was created by a user or was built-in')
    server: str | None = Field(None, description='Server URL')

class GetClusterNotificationsEndpointsGotifyResponse(RootModel[list[GetClusterNotificationsEndpointsGotifyResponseItem]]):
    root: list[GetClusterNotificationsEndpointsGotifyResponseItem] = Field(...)

class PostClusterNotificationsEndpointsGotifyRequest(ProxmoxBaseModel):
    comment: str | None = Field(None, description='Comment')
    disable: bool | None = Field(None, description='Disable this target')
    name: str = Field(..., description='The name of the endpoint.')
    server: str = Field(..., description='Server URL')
    token: str = Field(..., description='Secret token')

class PostClusterNotificationsEndpointsGotifyResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterNotificationsEndpointsGotifyNameRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteClusterNotificationsEndpointsGotifyNameResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterNotificationsEndpointsGotifyNameResponse(ProxmoxBaseModel):
    comment: str | None = Field(None, description='Comment')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Disable this target')
    name: str = Field(..., description='The name of the endpoint.')
    server: str = Field(..., description='Server URL')

class PutClusterNotificationsEndpointsGotifyNameRequest(ProxmoxBaseModel):
    comment: str | None = Field(None, description='Comment')
    delete: list[str] | None = Field(None, description='A list of settings you want to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Disable this target')
    server: str | None = Field(None, description='Server URL')
    token: str | None = Field(None, description='Secret token')

class PutClusterNotificationsEndpointsGotifyNameResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterNotificationsEndpointsSendmailResponseItem(ProxmoxBaseModel):
    author: str | None = Field(None, description='Author of the mail')
    comment: str | None = Field(None, description='Comment')
    disable: bool | None = Field(None, description='Disable this target')
    from_address: str | None = Field(None, alias="from-address", description='`From` address for the mail')
    mailto: list[str] | None = Field(None, description='List of email recipients')
    mailto_user: list[str] | None = Field(None, alias="mailto-user", description='List of users')
    name: str | None = Field(None, description='The name of the endpoint.')
    origin: str | None = Field(None, description='Show if this entry was created by a user or was built-in')

class GetClusterNotificationsEndpointsSendmailResponse(RootModel[list[GetClusterNotificationsEndpointsSendmailResponseItem]]):
    root: list[GetClusterNotificationsEndpointsSendmailResponseItem] = Field(...)

class PostClusterNotificationsEndpointsSendmailRequest(ProxmoxBaseModel):
    author: str | None = Field(None, description='Author of the mail')
    comment: str | None = Field(None, description='Comment')
    disable: bool | None = Field(None, description='Disable this target')
    from_address: str | None = Field(None, alias="from-address", description='`From` address for the mail')
    mailto: list[str] | None = Field(None, description='List of email recipients')
    mailto_user: list[str] | None = Field(None, alias="mailto-user", description='List of users')
    name: str = Field(..., description='The name of the endpoint.')

class PostClusterNotificationsEndpointsSendmailResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterNotificationsEndpointsSendmailNameRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteClusterNotificationsEndpointsSendmailNameResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterNotificationsEndpointsSendmailNameResponse(ProxmoxBaseModel):
    author: str | None = Field(None, description='Author of the mail')
    comment: str | None = Field(None, description='Comment')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Disable this target')
    from_address: str | None = Field(None, alias="from-address", description='`From` address for the mail')
    mailto: list[str] | None = Field(None, description='List of email recipients')
    mailto_user: list[str] | None = Field(None, alias="mailto-user", description='List of users')
    name: str = Field(..., description='The name of the endpoint.')

class PutClusterNotificationsEndpointsSendmailNameRequest(ProxmoxBaseModel):
    author: str | None = Field(None, description='Author of the mail')
    comment: str | None = Field(None, description='Comment')
    delete: list[str] | None = Field(None, description='A list of settings you want to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Disable this target')
    from_address: str | None = Field(None, alias="from-address", description='`From` address for the mail')
    mailto: list[str] | None = Field(None, description='List of email recipients')
    mailto_user: list[str] | None = Field(None, alias="mailto-user", description='List of users')

class PutClusterNotificationsEndpointsSendmailNameResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterNotificationsEndpointsSmtpResponseItem(ProxmoxBaseModel):
    author: str | None = Field(None, description="Author of the mail. Defaults to 'Proxmox VE'.")
    comment: str | None = Field(None, description='Comment')
    disable: bool | None = Field(None, description='Disable this target')
    from_address: str | None = Field(None, alias="from-address", description='`From` address for the mail')
    mailto: list[str] | None = Field(None, description='List of email recipients')
    mailto_user: list[str] | None = Field(None, alias="mailto-user", description='List of users')
    mode: str | None = Field(None, description='Determine which encryption method shall be used for the connection.')
    name: str | None = Field(None, description='The name of the endpoint.')
    origin: str | None = Field(None, description='Show if this entry was created by a user or was built-in')
    port: int | None = Field(None, description='The port to be used. Defaults to 465 for TLS based connections, 587 for STARTTLS based connections and port 25 for insecure plain-text connections.')
    server: str | None = Field(None, description='The address of the SMTP server.')
    username: str | None = Field(None, description='Username for SMTP authentication')

class GetClusterNotificationsEndpointsSmtpResponse(RootModel[list[GetClusterNotificationsEndpointsSmtpResponseItem]]):
    root: list[GetClusterNotificationsEndpointsSmtpResponseItem] = Field(...)

class PostClusterNotificationsEndpointsSmtpRequest(ProxmoxBaseModel):
    author: str | None = Field(None, description="Author of the mail. Defaults to 'Proxmox VE'.")
    comment: str | None = Field(None, description='Comment')
    disable: bool | None = Field(None, description='Disable this target')
    from_address: str = Field(..., alias="from-address", description='`From` address for the mail')
    mailto: list[str] | None = Field(None, description='List of email recipients')
    mailto_user: list[str] | None = Field(None, alias="mailto-user", description='List of users')
    mode: str | None = Field(None, description='Determine which encryption method shall be used for the connection.')
    name: str = Field(..., description='The name of the endpoint.')
    password: str | None = Field(None, description='Password for SMTP authentication')
    port: int | None = Field(None, description='The port to be used. Defaults to 465 for TLS based connections, 587 for STARTTLS based connections and port 25 for insecure plain-text connections.')
    server: str = Field(..., description='The address of the SMTP server.')
    username: str | None = Field(None, description='Username for SMTP authentication')

class PostClusterNotificationsEndpointsSmtpResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterNotificationsEndpointsSmtpNameRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteClusterNotificationsEndpointsSmtpNameResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterNotificationsEndpointsSmtpNameResponse(ProxmoxBaseModel):
    author: str | None = Field(None, description="Author of the mail. Defaults to 'Proxmox VE'.")
    comment: str | None = Field(None, description='Comment')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Disable this target')
    from_address: str = Field(..., alias="from-address", description='`From` address for the mail')
    mailto: list[str] | None = Field(None, description='List of email recipients')
    mailto_user: list[str] | None = Field(None, alias="mailto-user", description='List of users')
    mode: str | None = Field(None, description='Determine which encryption method shall be used for the connection.')
    name: str = Field(..., description='The name of the endpoint.')
    port: int | None = Field(None, description='The port to be used. Defaults to 465 for TLS based connections, 587 for STARTTLS based connections and port 25 for insecure plain-text connections.')
    server: str = Field(..., description='The address of the SMTP server.')
    username: str | None = Field(None, description='Username for SMTP authentication')

class PutClusterNotificationsEndpointsSmtpNameRequest(ProxmoxBaseModel):
    author: str | None = Field(None, description="Author of the mail. Defaults to 'Proxmox VE'.")
    comment: str | None = Field(None, description='Comment')
    delete: list[str] | None = Field(None, description='A list of settings you want to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Disable this target')
    from_address: str | None = Field(None, alias="from-address", description='`From` address for the mail')
    mailto: list[str] | None = Field(None, description='List of email recipients')
    mailto_user: list[str] | None = Field(None, alias="mailto-user", description='List of users')
    mode: str | None = Field(None, description='Determine which encryption method shall be used for the connection.')
    password: str | None = Field(None, description='Password for SMTP authentication')
    port: int | None = Field(None, description='The port to be used. Defaults to 465 for TLS based connections, 587 for STARTTLS based connections and port 25 for insecure plain-text connections.')
    server: str | None = Field(None, description='The address of the SMTP server.')
    username: str | None = Field(None, description='Username for SMTP authentication')

class PutClusterNotificationsEndpointsSmtpNameResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterNotificationsEndpointsWebhookResponseItem(ProxmoxBaseModel):
    body: str | None = Field(None, description='HTTP body, base64 encoded')
    comment: str | None = Field(None, description='Comment')
    disable: bool | None = Field(None, description='Disable this target')
    header: list[str] | None = Field(None, description='HTTP headers to set. These have to be formatted as a property string in the format name=<name>,value=<base64 of value>')
    method: str | None = Field(None, description='HTTP method')
    name: str | None = Field(None, description='The name of the endpoint.')
    origin: str | None = Field(None, description='Show if this entry was created by a user or was built-in')
    secret: list[str] | None = Field(None, description='Secrets to set. These have to be formatted as a property string in the format name=<name>,value=<base64 of value>')
    url: str | None = Field(None, description='Server URL')

class GetClusterNotificationsEndpointsWebhookResponse(RootModel[list[GetClusterNotificationsEndpointsWebhookResponseItem]]):
    root: list[GetClusterNotificationsEndpointsWebhookResponseItem] = Field(...)

class PostClusterNotificationsEndpointsWebhookRequest(ProxmoxBaseModel):
    body: str | None = Field(None, description='HTTP body, base64 encoded')
    comment: str | None = Field(None, description='Comment')
    disable: bool | None = Field(None, description='Disable this target')
    header: list[str] | None = Field(None, description='HTTP headers to set. These have to be formatted as a property string in the format name=<name>,value=<base64 of value>')
    method: str = Field(..., description='HTTP method')
    name: str = Field(..., description='The name of the endpoint.')
    secret: list[str] | None = Field(None, description='Secrets to set. These have to be formatted as a property string in the format name=<name>,value=<base64 of value>')
    url: str = Field(..., description='Server URL')

class PostClusterNotificationsEndpointsWebhookResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterNotificationsEndpointsWebhookNameRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteClusterNotificationsEndpointsWebhookNameResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterNotificationsEndpointsWebhookNameResponse(ProxmoxBaseModel):
    body: str | None = Field(None, description='HTTP body, base64 encoded')
    comment: str | None = Field(None, description='Comment')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Disable this target')
    header: list[str] | None = Field(None, description='HTTP headers to set. These have to be formatted as a property string in the format name=<name>,value=<base64 of value>')
    method: str = Field(..., description='HTTP method')
    name: str = Field(..., description='The name of the endpoint.')
    secret: list[str] | None = Field(None, description='Secrets to set. These have to be formatted as a property string in the format name=<name>,value=<base64 of value>')
    url: str = Field(..., description='Server URL')

class PutClusterNotificationsEndpointsWebhookNameRequest(ProxmoxBaseModel):
    body: str | None = Field(None, description='HTTP body, base64 encoded')
    comment: str | None = Field(None, description='Comment')
    delete: list[str] | None = Field(None, description='A list of settings you want to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Disable this target')
    header: list[str] | None = Field(None, description='HTTP headers to set. These have to be formatted as a property string in the format name=<name>,value=<base64 of value>')
    method: str | None = Field(None, description='HTTP method')
    secret: list[str] | None = Field(None, description='Secrets to set. These have to be formatted as a property string in the format name=<name>,value=<base64 of value>')
    url: str | None = Field(None, description='Server URL')

class PutClusterNotificationsEndpointsWebhookNameResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterNotificationsMatcherFieldValuesResponseItem(ProxmoxBaseModel):
    comment: str | None = Field(None, description='Additional comment for this value.')
    field: str | None = Field(None, description='Field this value belongs to.')
    value: str | None = Field(None, description='Notification metadata value known by the system.')

class GetClusterNotificationsMatcherFieldValuesResponse(RootModel[list[GetClusterNotificationsMatcherFieldValuesResponseItem]]):
    root: list[GetClusterNotificationsMatcherFieldValuesResponseItem] = Field(...)

class GetClusterNotificationsMatcherFieldsResponseItem(ProxmoxBaseModel):
    name: str | None = Field(None, description='Name of the field.')

class GetClusterNotificationsMatcherFieldsResponse(RootModel[list[GetClusterNotificationsMatcherFieldsResponseItem]]):
    root: list[GetClusterNotificationsMatcherFieldsResponseItem] = Field(...)

class GetClusterNotificationsMatchersResponseItem(ProxmoxBaseModel):
    comment: str | None = Field(None, description='Comment')
    disable: bool | None = Field(None, description='Disable this matcher')
    invert_match: bool | None = Field(None, alias="invert-match", description='Invert match of the whole matcher')
    match_calendar: list[str] | None = Field(None, alias="match-calendar", description='Match notification timestamp')
    match_field: list[str] | None = Field(None, alias="match-field", description='Metadata fields to match (regex or exact match). Must be in the form (regex|exact):<field>=<value>')
    match_severity: list[str] | None = Field(None, alias="match-severity", description='Notification severities to match')
    mode: str | None = Field(None, description="Choose between 'all' and 'any' for when multiple properties are specified")
    name: str | None = Field(None, description='Name of the matcher.')
    origin: str | None = Field(None, description='Show if this entry was created by a user or was built-in')
    target: list[str] | None = Field(None, description='Targets to notify on match')

class GetClusterNotificationsMatchersResponse(RootModel[list[GetClusterNotificationsMatchersResponseItem]]):
    root: list[GetClusterNotificationsMatchersResponseItem] = Field(...)

class PostClusterNotificationsMatchersRequest(ProxmoxBaseModel):
    comment: str | None = Field(None, description='Comment')
    disable: bool | None = Field(None, description='Disable this matcher')
    invert_match: bool | None = Field(None, alias="invert-match", description='Invert match of the whole matcher')
    match_calendar: list[str] | None = Field(None, alias="match-calendar", description='Match notification timestamp')
    match_field: list[str] | None = Field(None, alias="match-field", description='Metadata fields to match (regex or exact match). Must be in the form (regex|exact):<field>=<value>')
    match_severity: list[str] | None = Field(None, alias="match-severity", description='Notification severities to match')
    mode: str | None = Field(None, description="Choose between 'all' and 'any' for when multiple properties are specified")
    name: str = Field(..., description='Name of the matcher.')
    target: list[str] | None = Field(None, description='Targets to notify on match')

class PostClusterNotificationsMatchersResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterNotificationsMatchersNameRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteClusterNotificationsMatchersNameResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterNotificationsMatchersNameResponse(ProxmoxBaseModel):
    comment: str | None = Field(None, description='Comment')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Disable this matcher')
    invert_match: bool | None = Field(None, alias="invert-match", description='Invert match of the whole matcher')
    match_calendar: list[str] | None = Field(None, alias="match-calendar", description='Match notification timestamp')
    match_field: list[str] | None = Field(None, alias="match-field", description='Metadata fields to match (regex or exact match). Must be in the form (regex|exact):<field>=<value>')
    match_severity: list[str] | None = Field(None, alias="match-severity", description='Notification severities to match')
    mode: str | None = Field(None, description="Choose between 'all' and 'any' for when multiple properties are specified")
    name: str = Field(..., description='Name of the matcher.')
    target: list[str] | None = Field(None, description='Targets to notify on match')

class PutClusterNotificationsMatchersNameRequest(ProxmoxBaseModel):
    comment: str | None = Field(None, description='Comment')
    delete: list[str] | None = Field(None, description='A list of settings you want to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Disable this matcher')
    invert_match: bool | None = Field(None, alias="invert-match", description='Invert match of the whole matcher')
    match_calendar: list[str] | None = Field(None, alias="match-calendar", description='Match notification timestamp')
    match_field: list[str] | None = Field(None, alias="match-field", description='Metadata fields to match (regex or exact match). Must be in the form (regex|exact):<field>=<value>')
    match_severity: list[str] | None = Field(None, alias="match-severity", description='Notification severities to match')
    mode: str | None = Field(None, description="Choose between 'all' and 'any' for when multiple properties are specified")
    target: list[str] | None = Field(None, description='Targets to notify on match')

class PutClusterNotificationsMatchersNameResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterNotificationsTargetsResponseItem(ProxmoxBaseModel):
    comment: str | None = Field(None, description='Comment')
    disable: bool | None = Field(None, description='Show if this target is disabled')
    name: str | None = Field(None, description='Name of the target.')
    origin: str | None = Field(None, description='Show if this entry was created by a user or was built-in')
    type: str | None = Field(None, description='Type of the target.')

class GetClusterNotificationsTargetsResponse(RootModel[list[GetClusterNotificationsTargetsResponseItem]]):
    root: list[GetClusterNotificationsTargetsResponseItem] = Field(...)

class PostClusterNotificationsTargetsNameTestRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostClusterNotificationsTargetsNameTestResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterOptionsResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PutClusterOptionsRequest(ProxmoxBaseModel):
    bwlimit: str | None = Field(None, description='Set I/O bandwidth limit for various operations (in KiB/s).')
    consent_text: str | None = Field(None, alias="consent-text", description='Consent text that is displayed before logging in.')
    console: str | None = Field(None, description='Select the default Console viewer. You can either use the builtin java applet (VNC; deprecated and maps to html5), an external virt-viewer comtatible application (SPICE), an HTML5 based vnc viewer (noVNC), or an HTML5 based console client (xtermjs). If the selected viewer is not available (e.g. SPICE not activated for the VM), the fallback is noVNC.')
    crs: str | None = Field(None, description='Cluster resource scheduling settings.')
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    description: str | None = Field(None, description='Datacenter description. Shown in the web-interface datacenter notes panel. This is saved as comment inside the configuration file.')
    email_from: str | None = Field(None, description='Specify email address to send notification from (default is root@$hostname)')
    fencing: str | None = Field(None, description="Set the fencing mode of the HA cluster. Hardware mode needs a valid configuration of fence devices in /etc/pve/ha/fence.cfg. With both all two modes are used.\n\nWARNING: 'hardware' and 'both' are EXPERIMENTAL & WIP")
    ha: str | None = Field(None, description='Cluster wide HA settings.')
    http_proxy: str | None = Field(None, description="Specify external http proxy which is used for downloads (example: 'http://username:password@host:port/')")
    keyboard: str | None = Field(None, description='Default keybord layout for vnc server.')
    language: str | None = Field(None, description='Default GUI language.')
    mac_prefix: str | None = Field(None, description="Prefix for the auto-generated MAC addresses of virtual guests. The default 'BC:24:11' is the OUI assigned by the IEEE to Proxmox Server Solutions GmbH for a 24-bit large MAC block. You're allowed to use this in local networks, i.e., those not directly reachable by the public (e.g., in a LAN or behind NAT).")
    max_workers: int | None = Field(None, description="Defines how many workers (per node) are maximal started  on actions like 'stopall VMs' or task from the ha-manager.")
    migration: str | None = Field(None, description='For cluster wide migration settings.')
    migration_unsecure: bool | None = Field(None, description="Migration is secure using SSH tunnel by default. For secure private networks you can disable it to speed up migration. Deprecated, use the 'migration' property instead!")
    next_id: str | None = Field(None, alias="next-id", description='Control the range for the free VMID auto-selection pool.')
    notify: str | None = Field(None, description='Cluster-wide notification settings.')
    registered_tags: str | None = Field(None, alias="registered-tags", description="A list of tags that require a `Sys.Modify` on '/' to set and delete. Tags set here that are also in 'user-tag-access' also require `Sys.Modify`.")
    replication: str | None = Field(None, description='For cluster wide replication settings.')
    tag_style: str | None = Field(None, alias="tag-style", description='Tag style options.')
    u2f: str | None = Field(None, description='u2f')
    user_tag_access: str | None = Field(None, alias="user-tag-access", description='Privilege options for user-settable tags')
    webauthn: str | None = Field(None, description='webauthn configuration')

class PutClusterOptionsResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterReplicationResponseItem(ProxmoxBaseModel):
    comment: str | None = Field(None, description='Description.')
    disable: bool | None = Field(None, description='Flag to disable/deactivate the entry.')
    guest: int | None = Field(None, description='Guest ID.')
    id: str | None = Field(None, description="Replication Job ID. The ID is composed of a Guest ID and a job number, separated by a hyphen, i.e. '<GUEST>-<JOBNUM>'.")
    jobnum: int | None = Field(None, description='Unique, sequential ID assigned to each job.')
    rate: float | None = Field(None, description='Rate limit in mbps (megabytes per second) as floating point number.')
    remove_job: str | None = Field(None, description="Mark the replication job for removal. The job will remove all local replication snapshots. When set to 'full', it also tries to remove replicated volumes on the target. The job then removes itself from the configuration file.")
    schedule: str | None = Field(None, description='Storage replication schedule. The format is a subset of `systemd` calendar events.')
    source: str | None = Field(None, description='For internal use, to detect if the guest was stolen.')
    target: str | None = Field(None, description='Target node.')
    type: str | None = Field(None, description='Section type.')

class GetClusterReplicationResponse(RootModel[list[GetClusterReplicationResponseItem]]):
    root: list[GetClusterReplicationResponseItem] = Field(...)

class PostClusterReplicationRequest(ProxmoxBaseModel):
    comment: str | None = Field(None, description='Description.')
    disable: bool | None = Field(None, description='Flag to disable/deactivate the entry.')
    id: str = Field(..., description="Replication Job ID. The ID is composed of a Guest ID and a job number, separated by a hyphen, i.e. '<GUEST>-<JOBNUM>'.")
    rate: float | None = Field(None, description='Rate limit in mbps (megabytes per second) as floating point number.')
    remove_job: str | None = Field(None, description="Mark the replication job for removal. The job will remove all local replication snapshots. When set to 'full', it also tries to remove replicated volumes on the target. The job then removes itself from the configuration file.")
    schedule: str | None = Field(None, description='Storage replication schedule. The format is a subset of `systemd` calendar events.')
    source: str | None = Field(None, description='For internal use, to detect if the guest was stolen.')
    target: str = Field(..., description='Target node.')
    type: str = Field(..., description='Section type.')

class PostClusterReplicationResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterReplicationIdRequest(ProxmoxBaseModel):
    force: bool | None = Field(None, description='Will remove the jobconfig entry, but will not cleanup.')
    keep: bool | None = Field(None, description='Keep replicated data at target (do not remove).')

class DeleteClusterReplicationIdResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterReplicationIdResponse(ProxmoxBaseModel):
    comment: str | None = Field(None, description='Description.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Flag to disable/deactivate the entry.')
    guest: int = Field(..., description='Guest ID.')
    id: str = Field(..., description="Replication Job ID. The ID is composed of a Guest ID and a job number, separated by a hyphen, i.e. '<GUEST>-<JOBNUM>'.")
    jobnum: int = Field(..., description='Unique, sequential ID assigned to each job.')
    rate: float | None = Field(None, description='Rate limit in mbps (megabytes per second) as floating point number.')
    remove_job: str | None = Field(None, description="Mark the replication job for removal. The job will remove all local replication snapshots. When set to 'full', it also tries to remove replicated volumes on the target. The job then removes itself from the configuration file.")
    schedule: str | None = Field(None, description='Storage replication schedule. The format is a subset of `systemd` calendar events.')
    source: str | None = Field(None, description='For internal use, to detect if the guest was stolen.')
    target: str = Field(..., description='Target node.')
    type: str = Field(..., description='Section type.')

class PutClusterReplicationIdRequest(ProxmoxBaseModel):
    comment: str | None = Field(None, description='Description.')
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Flag to disable/deactivate the entry.')
    rate: float | None = Field(None, description='Rate limit in mbps (megabytes per second) as floating point number.')
    remove_job: str | None = Field(None, description="Mark the replication job for removal. The job will remove all local replication snapshots. When set to 'full', it also tries to remove replicated volumes on the target. The job then removes itself from the configuration file.")
    schedule: str | None = Field(None, description='Storage replication schedule. The format is a subset of `systemd` calendar events.')
    source: str | None = Field(None, description='For internal use, to detect if the guest was stolen.')

class PutClusterReplicationIdResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterResourcesResponseItem(ProxmoxBaseModel):
    cgroup_mode: int | None = Field(None, alias="cgroup-mode", description="The cgroup mode the node operates under (for type 'node').")
    content: str | None = Field(None, description="Allowed storage content types (for type 'storage').")
    cpu: float | None = Field(None, description="CPU utilization (for types 'node', 'qemu' and 'lxc').")
    disk: int | None = Field(None, description="Used disk space in bytes (for type 'storage'), used root image space for VMs (for types 'qemu' and 'lxc').")
    diskread: int | None = Field(None, description="The number of bytes the guest read from its block devices since the guest was started. This info is not available for all storage types. (for types 'qemu' and 'lxc')")
    diskwrite: int | None = Field(None, description="The number of bytes the guest wrote to its block devices since the guest was started. This info is not available for all storage types. (for types 'qemu' and 'lxc')")
    hastate: str | None = Field(None, description='HA service status (for HA managed VMs).')
    id: str | None = Field(None, description='Resource id.')
    level: str | None = Field(None, description="Support level (for type 'node').")
    lock: str | None = Field(None, description="The guest's current config lock (for types 'qemu' and 'lxc')")
    maxcpu: float | None = Field(None, description="Number of available CPUs (for types 'node', 'qemu' and 'lxc').")
    maxdisk: int | None = Field(None, description="Storage size in bytes (for type 'storage'), root image size for VMs (for types 'qemu' and 'lxc').")
    maxmem: int | None = Field(None, description="Number of available memory in bytes (for types 'node', 'qemu' and 'lxc').")
    mem: int | None = Field(None, description="Used memory in bytes (for types 'node', 'qemu' and 'lxc').")
    memhost: int | None = Field(None, description="Used memory in bytes from the point of view of the host (for types 'qemu').")
    name: str | None = Field(None, description='Name of the resource.')
    netin: int | None = Field(None, description="The amount of traffic in bytes that was sent to the guest over the network since it was started. (for types 'qemu' and 'lxc')")
    netout: int | None = Field(None, description="The amount of traffic in bytes that was sent from the guest over the network since it was started. (for types 'qemu' and 'lxc')")
    network: str | None = Field(None, description="The name of a Network entity (for type 'network').")
    network_type: str | None = Field(None, alias="network-type", description="The type of network resource (for type 'network').")
    node: str | None = Field(None, description="The cluster node name (for types 'node', 'storage', 'qemu', and 'lxc').")
    plugintype: str | None = Field(None, description='More specific type, if available.')
    pool: str | None = Field(None, description="The pool name (for types 'pool', 'qemu' and 'lxc').")
    protocol: str | None = Field(None, description="The protocol of a fabric (for type 'network', network-type 'fabric').")
    sdn: str | None = Field(None, description="The name of an SDN entity (for type 'sdn')")
    status: str | None = Field(None, description='Resource type dependent status.')
    storage: str | None = Field(None, description="The storage identifier (for type 'storage').")
    tags: str | None = Field(None, description="The guest's tags (for types 'qemu' and 'lxc')")
    template: bool | None = Field(None, description="Determines if the guest is a template. (for types 'qemu' and 'lxc')")
    type: str | None = Field(None, description='Resource type.')
    uptime: int | None = Field(None, description="Uptime of node or virtual guest in seconds (for types 'node', 'qemu' and 'lxc').")
    vmid: int | None = Field(None, description="The numerical vmid (for types 'qemu' and 'lxc').")
    zone_type: str | None = Field(None, alias="zone-type", description="The type of an SDN zone (for type 'sdn').")

class GetClusterResourcesResponse(RootModel[list[GetClusterResourcesResponseItem]]):
    root: list[GetClusterResourcesResponseItem] = Field(...)

class GetClusterSdnResponseItem(ProxmoxBaseModel):
    id: str | None = Field(None)

class GetClusterSdnResponse(RootModel[list[GetClusterSdnResponseItem]]):
    root: list[GetClusterSdnResponseItem] = Field(...)

class PutClusterSdnRequest(ProxmoxBaseModel):
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    release_lock: bool | None = Field(None, alias="release-lock", description='When lock-token has been provided and configuration successfully commited, release the lock automatically afterwards')

class PutClusterSdnResponse(RootModel[str]):
    root: str = Field(...)

class GetClusterSdnControllersResponseItem(ProxmoxBaseModel):
    asn: int | None = Field(None, description='The local ASN of the controller. BGP & EVPN only.')
    bgp_multipath_as_relax: bool | None = Field(None, alias="bgp-multipath-as-relax", description='Consider different AS paths of equal length for multipath computation. BGP only.')
    controller: str | None = Field(None, description='Name of the controller.')
    digest: str | None = Field(None, description='Digest of the controller section.')
    ebgp: bool | None = Field(None, description='Enable eBGP (remote-as external). BGP only.')
    ebgp_multihop: int | None = Field(None, alias="ebgp-multihop", description='Set maximum amount of hops for eBGP peers. Needs ebgp set to 1. BGP only.')
    isis_domain: str | None = Field(None, alias="isis-domain", description='Name of the IS-IS domain. IS-IS only.')
    isis_ifaces: str | None = Field(None, alias="isis-ifaces", description='Comma-separated list of interfaces where IS-IS should be active. IS-IS only.')
    isis_net: str | None = Field(None, alias="isis-net", description='Network Entity title for this node in the IS-IS network. IS-IS only.')
    loopback: str | None = Field(None, description='Name of the loopback/dummy interface that provides the Router-IP. BGP only.')
    node: str | None = Field(None, description='Node(s) where this controller is active.')
    peers: str | None = Field(None, description='Comma-separated list of the peers IP addresses.')
    pending: dict[str, object] | None = Field(None, description='Changes that have not yet been applied to the running configuration.')
    state: str | None = Field(None, description='State of the SDN configuration object.')
    type: str | None = Field(None, description='Type of the controller')

class GetClusterSdnControllersResponse(RootModel[list[GetClusterSdnControllersResponseItem]]):
    root: list[GetClusterSdnControllersResponseItem] = Field(...)

class PostClusterSdnControllersRequest(ProxmoxBaseModel):
    asn: int | None = Field(None, description='autonomous system number')
    bgp_multipath_as_path_relax: bool | None = Field(None, alias="bgp-multipath-as-path-relax", description='Consider different AS paths of equal length for multipath computation.')
    controller: str = Field(..., description='The SDN controller object identifier.')
    ebgp: bool | None = Field(None, description='Enable eBGP (remote-as external).')
    ebgp_multihop: int | None = Field(None, alias="ebgp-multihop", description='Set maximum amount of hops for eBGP peers.')
    fabric: str | None = Field(None, description='SDN fabric to use as underlay for this EVPN controller.')
    isis_domain: str | None = Field(None, alias="isis-domain", description='Name of the IS-IS domain.')
    isis_ifaces: str | None = Field(None, alias="isis-ifaces", description='Comma-separated list of interfaces where IS-IS should be active.')
    isis_net: str | None = Field(None, alias="isis-net", description='Network Entity title for this node in the IS-IS network.')
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    loopback: str | None = Field(None, description='Name of the loopback/dummy interface that provides the Router-IP.')
    node: str | None = Field(None, description='The cluster node name.')
    peers: str | None = Field(None, description='peers address list.')
    type: str = Field(..., description='Plugin type.')

class PostClusterSdnControllersResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterSdnControllersControllerRequest(ProxmoxBaseModel):
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')

class DeleteClusterSdnControllersControllerResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterSdnControllersControllerResponse(ProxmoxBaseModel):
    asn: int | None = Field(None, description='The local ASN of the controller. BGP & EVPN only.')
    bgp_multipath_as_relax: bool | None = Field(None, alias="bgp-multipath-as-relax", description='Consider different AS paths of equal length for multipath computation. BGP only.')
    controller: str = Field(..., description='Name of the controller.')
    digest: str | None = Field(None, description='Digest of the controller section.')
    ebgp: bool | None = Field(None, description='Enable eBGP (remote-as external). BGP only.')
    ebgp_multihop: int | None = Field(None, alias="ebgp-multihop", description='Set maximum amount of hops for eBGP peers. Needs ebgp set to 1. BGP only.')
    isis_domain: str | None = Field(None, alias="isis-domain", description='Name of the IS-IS domain. IS-IS only.')
    isis_ifaces: str | None = Field(None, alias="isis-ifaces", description='Comma-separated list of interfaces where IS-IS should be active. IS-IS only.')
    isis_net: str | None = Field(None, alias="isis-net", description='Network Entity title for this node in the IS-IS network. IS-IS only.')
    loopback: str | None = Field(None, description='Name of the loopback/dummy interface that provides the Router-IP. BGP only.')
    node: str | None = Field(None, description='Node(s) where this controller is active.')
    peers: str | None = Field(None, description='Comma-separated list of the peers IP addresses.')
    pending: dict[str, object] | None = Field(None, description='Changes that have not yet been applied to the running configuration.')
    state: str | None = Field(None, description='State of the SDN configuration object.')
    type: str = Field(..., description='Type of the controller')

class PutClusterSdnControllersControllerRequest(ProxmoxBaseModel):
    asn: int | None = Field(None, description='autonomous system number')
    bgp_multipath_as_path_relax: bool | None = Field(None, alias="bgp-multipath-as-path-relax", description='Consider different AS paths of equal length for multipath computation.')
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    ebgp: bool | None = Field(None, description='Enable eBGP (remote-as external).')
    ebgp_multihop: int | None = Field(None, alias="ebgp-multihop", description='Set maximum amount of hops for eBGP peers.')
    fabric: str | None = Field(None, description='SDN fabric to use as underlay for this EVPN controller.')
    isis_domain: str | None = Field(None, alias="isis-domain", description='Name of the IS-IS domain.')
    isis_ifaces: str | None = Field(None, alias="isis-ifaces", description='Comma-separated list of interfaces where IS-IS should be active.')
    isis_net: str | None = Field(None, alias="isis-net", description='Network Entity title for this node in the IS-IS network.')
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    loopback: str | None = Field(None, description='Name of the loopback/dummy interface that provides the Router-IP.')
    node: str | None = Field(None, description='The cluster node name.')
    peers: str | None = Field(None, description='peers address list.')

class PutClusterSdnControllersControllerResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterSdnDnsResponseItem(ProxmoxBaseModel):
    dns: str | None = Field(None)
    type: str | None = Field(None)

class GetClusterSdnDnsResponse(RootModel[list[GetClusterSdnDnsResponseItem]]):
    root: list[GetClusterSdnDnsResponseItem] = Field(...)

class PostClusterSdnDnsRequest(ProxmoxBaseModel):
    dns: str = Field(..., description='The SDN dns object identifier.')
    fingerprint: str | None = Field(None, description='Certificate SHA 256 fingerprint.')
    key: str = Field(...)
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    reversemaskv6: int | None = Field(None)
    reversev6mask: int | None = Field(None)
    ttl: int | None = Field(None)
    type: str = Field(..., description='Plugin type.')
    url: str = Field(...)

class PostClusterSdnDnsResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterSdnDnsDnsRequest(ProxmoxBaseModel):
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')

class DeleteClusterSdnDnsDnsResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterSdnDnsDnsResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PutClusterSdnDnsDnsRequest(ProxmoxBaseModel):
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    fingerprint: str | None = Field(None, description='Certificate SHA 256 fingerprint.')
    key: str | None = Field(None)
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    reversemaskv6: int | None = Field(None)
    ttl: int | None = Field(None)
    url: str | None = Field(None)

class PutClusterSdnDnsDnsResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterSdnFabricsResponseItem(ProxmoxBaseModel):
    subdir: str | None = Field(None)

class GetClusterSdnFabricsResponse(RootModel[list[GetClusterSdnFabricsResponseItem]]):
    root: list[GetClusterSdnFabricsResponseItem] = Field(...)

class GetClusterSdnFabricsAllResponse(ProxmoxBaseModel):
    fabrics: list[dict[str, object]] = Field(...)
    nodes: list[dict[str, object]] = Field(...)

class GetClusterSdnFabricsFabricResponseItem(ProxmoxBaseModel):
    area: str | None = Field(None, description='OSPF area. Either a IPv4 address or a 32-bit number. Gets validated in rust.')
    csnp_interval: float | None = Field(None, description='The csnp_interval property for Openfabric')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    hello_interval: float | None = Field(None, description='The hello_interval property for Openfabric')
    id: str | None = Field(None, description='Identifier for SDN fabrics')
    ip6_prefix: str | None = Field(None, description='The IP prefix for Node IPs')
    ip_prefix: str | None = Field(None, description='The IP prefix for Node IPs')
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    protocol: str | None = Field(None, description='Type of configuration entry in an SDN Fabric section config')

class GetClusterSdnFabricsFabricResponse(RootModel[list[GetClusterSdnFabricsFabricResponseItem]]):
    root: list[GetClusterSdnFabricsFabricResponseItem] = Field(...)

class PostClusterSdnFabricsFabricRequest(ProxmoxBaseModel):
    area: str | None = Field(None, description='OSPF area. Either a IPv4 address or a 32-bit number. Gets validated in rust.')
    csnp_interval: float | None = Field(None, description='The csnp_interval property for Openfabric')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    hello_interval: float | None = Field(None, description='The hello_interval property for Openfabric')
    id: str = Field(..., description='Identifier for SDN fabrics')
    ip6_prefix: str | None = Field(None, description='The IP prefix for Node IPs')
    ip_prefix: str | None = Field(None, description='The IP prefix for Node IPs')
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    protocol: str = Field(..., description='Type of configuration entry in an SDN Fabric section config')

class PostClusterSdnFabricsFabricResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterSdnFabricsFabricIdRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteClusterSdnFabricsFabricIdResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterSdnFabricsFabricIdResponse(ProxmoxBaseModel):
    area: str | None = Field(None, description='OSPF area. Either a IPv4 address or a 32-bit number. Gets validated in rust.')
    csnp_interval: float | None = Field(None, description='The csnp_interval property for Openfabric')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    hello_interval: float | None = Field(None, description='The hello_interval property for Openfabric')
    id: str = Field(..., description='Identifier for SDN fabrics')
    ip6_prefix: str | None = Field(None, description='The IP prefix for Node IPs')
    ip_prefix: str | None = Field(None, description='The IP prefix for Node IPs')
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    protocol: str = Field(..., description='Type of configuration entry in an SDN Fabric section config')

class PutClusterSdnFabricsFabricIdRequest(ProxmoxBaseModel):
    area: str | None = Field(None, description='OSPF area. Either a IPv4 address or a 32-bit number. Gets validated in rust.')
    csnp_interval: float | None = Field(None, description='The csnp_interval property for Openfabric')
    delete: list[str] = Field(...)
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    hello_interval: float | None = Field(None, description='The hello_interval property for Openfabric')
    ip6_prefix: str | None = Field(None, description='The IP prefix for Node IPs')
    ip_prefix: str | None = Field(None, description='The IP prefix for Node IPs')
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    protocol: str = Field(..., description='Type of configuration entry in an SDN Fabric section config')

class PutClusterSdnFabricsFabricIdResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterSdnFabricsNodeResponseItem(ProxmoxBaseModel):
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    fabric_id: str | None = Field(None, description='Identifier for SDN fabrics')
    interfaces: list[str] | None = Field(None)
    ip: str | None = Field(None, description='IPv4 address for this node')
    ip6: str | None = Field(None, description='IPv6 address for this node')
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    node_id: str | None = Field(None, description='Identifier for nodes in an SDN fabric')
    protocol: str | None = Field(None, description='Type of configuration entry in an SDN Fabric section config')

class GetClusterSdnFabricsNodeResponse(RootModel[list[GetClusterSdnFabricsNodeResponseItem]]):
    root: list[GetClusterSdnFabricsNodeResponseItem] = Field(...)

class GetClusterSdnFabricsNodeFabricIdResponseItem(ProxmoxBaseModel):
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    fabric_id: str | None = Field(None, description='Identifier for SDN fabrics')
    interfaces: list[str] | None = Field(None)
    ip: str | None = Field(None, description='IPv4 address for this node')
    ip6: str | None = Field(None, description='IPv6 address for this node')
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    node_id: str | None = Field(None, description='Identifier for nodes in an SDN fabric')
    protocol: str | None = Field(None, description='Type of configuration entry in an SDN Fabric section config')

class GetClusterSdnFabricsNodeFabricIdResponse(RootModel[list[GetClusterSdnFabricsNodeFabricIdResponseItem]]):
    root: list[GetClusterSdnFabricsNodeFabricIdResponseItem] = Field(...)

class PostClusterSdnFabricsNodeFabricIdRequest(ProxmoxBaseModel):
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    interfaces: list[str] = Field(...)
    ip: str | None = Field(None, description='IPv4 address for this node')
    ip6: str | None = Field(None, description='IPv6 address for this node')
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    node_id: str = Field(..., description='Identifier for nodes in an SDN fabric')
    protocol: str = Field(..., description='Type of configuration entry in an SDN Fabric section config')

class PostClusterSdnFabricsNodeFabricIdResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterSdnFabricsNodeFabricIdNodeIdRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteClusterSdnFabricsNodeFabricIdNodeIdResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterSdnFabricsNodeFabricIdNodeIdResponse(ProxmoxBaseModel):
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    fabric_id: str = Field(..., description='Identifier for SDN fabrics')
    interfaces: list[str] = Field(...)
    ip: str | None = Field(None, description='IPv4 address for this node')
    ip6: str | None = Field(None, description='IPv6 address for this node')
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    node_id: str = Field(..., description='Identifier for nodes in an SDN fabric')
    protocol: str = Field(..., description='Type of configuration entry in an SDN Fabric section config')

class PutClusterSdnFabricsNodeFabricIdNodeIdRequest(ProxmoxBaseModel):
    delete: list[str] | None = Field(None)
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    interfaces: list[str] = Field(...)
    ip: str | None = Field(None, description='IPv4 address for this node')
    ip6: str | None = Field(None, description='IPv6 address for this node')
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    protocol: str = Field(..., description='Type of configuration entry in an SDN Fabric section config')

class PutClusterSdnFabricsNodeFabricIdNodeIdResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterSdnIpamsResponseItem(ProxmoxBaseModel):
    ipam: str | None = Field(None)
    type: str | None = Field(None)

class GetClusterSdnIpamsResponse(RootModel[list[GetClusterSdnIpamsResponseItem]]):
    root: list[GetClusterSdnIpamsResponseItem] = Field(...)

class PostClusterSdnIpamsRequest(ProxmoxBaseModel):
    fingerprint: str | None = Field(None, description='Certificate SHA 256 fingerprint.')
    ipam: str = Field(..., description='The SDN ipam object identifier.')
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    section: int | None = Field(None)
    token: str | None = Field(None)
    type: str = Field(..., description='Plugin type.')
    url: str | None = Field(None)

class PostClusterSdnIpamsResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterSdnIpamsIpamRequest(ProxmoxBaseModel):
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')

class DeleteClusterSdnIpamsIpamResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterSdnIpamsIpamResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PutClusterSdnIpamsIpamRequest(ProxmoxBaseModel):
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    fingerprint: str | None = Field(None, description='Certificate SHA 256 fingerprint.')
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    section: int | None = Field(None)
    token: str | None = Field(None)
    url: str | None = Field(None)

class PutClusterSdnIpamsIpamResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterSdnIpamsIpamStatusResponse(RootModel[list[object]]):
    root: list[object] = Field(...)

class DeleteClusterSdnLockRequest(ProxmoxBaseModel):
    force: bool | None = Field(None, description='if true, allow releasing lock without providing the token')
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')

class DeleteClusterSdnLockResponse(RootModel[None]):
    root: None = Field(...)

class PostClusterSdnLockRequest(ProxmoxBaseModel):
    allow_pending: bool | None = Field(None, alias="allow-pending", description='if true, allow acquiring lock even though there are pending changes')

class PostClusterSdnLockResponse(RootModel[str]):
    root: str = Field(...)

class PostClusterSdnRollbackRequest(ProxmoxBaseModel):
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    release_lock: bool | None = Field(None, alias="release-lock", description='When lock-token has been provided and configuration successfully rollbacked, release the lock automatically afterwards')

class PostClusterSdnRollbackResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterSdnVnetsResponseItem(ProxmoxBaseModel):
    alias: str | None = Field(None, description='Alias name of the VNet.')
    digest: str | None = Field(None, description='Digest of the VNet section.')
    isolate_ports: bool | None = Field(None, alias="isolate-ports", description='If true, sets the isolated property for all interfaces on the bridge of this VNet.')
    pending: dict[str, object] | None = Field(None, description='Changes that have not yet been applied to the running configuration.')
    state: str | None = Field(None, description='State of the SDN configuration object.')
    tag: int | None = Field(None, description='VLAN Tag (for VLAN or QinQ zones) or VXLAN VNI (for VXLAN or EVPN zones).')
    type: str | None = Field(None, description='Type of the VNet.')
    vlanaware: bool | None = Field(None, description='Allow VLANs to pass through this VNet.')
    vnet: str | None = Field(None, description='Name of the VNet.')
    zone: str | None = Field(None, description='Name of the zone this VNet belongs to.')

class GetClusterSdnVnetsResponse(RootModel[list[GetClusterSdnVnetsResponseItem]]):
    root: list[GetClusterSdnVnetsResponseItem] = Field(...)

class PostClusterSdnVnetsRequest(ProxmoxBaseModel):
    alias: str | None = Field(None, description='Alias name of the VNet.')
    isolate_ports: bool | None = Field(None, alias="isolate-ports", description='If true, sets the isolated property for all interfaces on the bridge of this VNet.')
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    tag: int | None = Field(None, description='VLAN Tag (for VLAN or QinQ zones) or VXLAN VNI (for VXLAN or EVPN zones).')
    type: str | None = Field(None, description='Type of the VNet.')
    vlanaware: bool | None = Field(None, description='Allow VLANs to pass through this vnet.')
    vnet: str = Field(..., description='The SDN vnet object identifier.')
    zone: str = Field(..., description='Name of the zone this VNet belongs to.')

class PostClusterSdnVnetsResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterSdnVnetsVnetRequest(ProxmoxBaseModel):
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')

class DeleteClusterSdnVnetsVnetResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterSdnVnetsVnetResponse(ProxmoxBaseModel):
    alias: str | None = Field(None, description='Alias name of the VNet.')
    digest: str | None = Field(None, description='Digest of the VNet section.')
    isolate_ports: bool | None = Field(None, alias="isolate-ports", description='If true, sets the isolated property for all interfaces on the bridge of this VNet.')
    pending: dict[str, object] | None = Field(None, description='Changes that have not yet been applied to the running configuration.')
    state: str | None = Field(None, description='State of the SDN configuration object.')
    tag: int | None = Field(None, description='VLAN Tag (for VLAN or QinQ zones) or VXLAN VNI (for VXLAN or EVPN zones).')
    type: str = Field(..., description='Type of the VNet.')
    vlanaware: bool | None = Field(None, description='Allow VLANs to pass through this VNet.')
    vnet: str = Field(..., description='Name of the VNet.')
    zone: str | None = Field(None, description='Name of the zone this VNet belongs to.')

class PutClusterSdnVnetsVnetRequest(ProxmoxBaseModel):
    alias: str | None = Field(None, description='Alias name of the VNet.')
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    isolate_ports: bool | None = Field(None, alias="isolate-ports", description='If true, sets the isolated property for all interfaces on the bridge of this VNet.')
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    tag: int | None = Field(None, description='VLAN Tag (for VLAN or QinQ zones) or VXLAN VNI (for VXLAN or EVPN zones).')
    vlanaware: bool | None = Field(None, description='Allow VLANs to pass through this vnet.')
    zone: str | None = Field(None, description='Name of the zone this VNet belongs to.')

class PutClusterSdnVnetsVnetResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterSdnVnetsVnetFirewallResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetClusterSdnVnetsVnetFirewallOptionsResponse(ProxmoxBaseModel):
    enable: bool | None = Field(None, description='Enable/disable firewall rules.')
    log_level_forward: str | None = Field(None, description='Log level for forwarded traffic.')
    policy_forward: str | None = Field(None, description='Forward policy.')

class PutClusterSdnVnetsVnetFirewallOptionsRequest(ProxmoxBaseModel):
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    enable: bool | None = Field(None, description='Enable/disable firewall rules.')
    log_level_forward: str | None = Field(None, description='Log level for forwarded traffic.')
    policy_forward: str | None = Field(None, description='Forward policy.')

class PutClusterSdnVnetsVnetFirewallOptionsResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterSdnVnetsVnetFirewallRulesResponseItem(ProxmoxBaseModel):
    action: str | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: str | None = Field(None, description='Descriptive comment')
    dest: str | None = Field(None, description='Restrict packet destination address')
    dport: str | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: str | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: str | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: str | None = Field(None, description='Log level for firewall rule')
    macro: str | None = Field(None, description='Use predefined standard macro')
    pos: int | None = Field(None, description='Rule position in the ruleset')
    proto: str | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: str | None = Field(None, description='Restrict packet source address')
    sport: str | None = Field(None, description='Restrict TCP/UDP source port')
    type: str | None = Field(None, description='Rule type')

class GetClusterSdnVnetsVnetFirewallRulesResponse(RootModel[list[GetClusterSdnVnetsVnetFirewallRulesResponseItem]]):
    root: list[GetClusterSdnVnetsVnetFirewallRulesResponseItem] = Field(...)

class PostClusterSdnVnetsVnetFirewallRulesRequest(ProxmoxBaseModel):
    action: str = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: str | None = Field(None, description='Descriptive comment.')
    dest: str | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: str | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: str | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: str | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: str | None = Field(None, description='Log level for firewall rule.')
    macro: str | None = Field(None, description='Use predefined standard macro.')
    pos: int | None = Field(None, description='Update rule at position <pos>.')
    proto: str | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: str | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: str | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: str = Field(..., description='Rule type.')

class PostClusterSdnVnetsVnetFirewallRulesResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterSdnVnetsVnetFirewallRulesPosRequest(ProxmoxBaseModel):
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteClusterSdnVnetsVnetFirewallRulesPosResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterSdnVnetsVnetFirewallRulesPosResponse(ProxmoxBaseModel):
    action: str = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: str | None = Field(None, description='Descriptive comment')
    dest: str | None = Field(None, description='Restrict packet destination address')
    dport: str | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: str | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: str | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: str | None = Field(None, description='Log level for firewall rule')
    macro: str | None = Field(None, description='Use predefined standard macro')
    pos: int = Field(..., description='Rule position in the ruleset')
    proto: str | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: str | None = Field(None, description='Restrict packet source address')
    sport: str | None = Field(None, description='Restrict TCP/UDP source port')
    type: str = Field(..., description='Rule type')

class PutClusterSdnVnetsVnetFirewallRulesPosRequest(ProxmoxBaseModel):
    action: str | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: str | None = Field(None, description='Descriptive comment.')
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    dest: str | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: str | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: str | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: str | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: str | None = Field(None, description='Log level for firewall rule.')
    macro: str | None = Field(None, description='Use predefined standard macro.')
    moveto: int | None = Field(None, description='Move rule to new position <moveto>. Other arguments are ignored.')
    proto: str | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: str | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: str | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: str | None = Field(None, description='Rule type.')

class PutClusterSdnVnetsVnetFirewallRulesPosResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterSdnVnetsVnetIpsRequest(ProxmoxBaseModel):
    ip: str = Field(..., description='The IP address to delete')
    mac: str | None = Field(None, description='Unicast MAC address.')
    zone: str = Field(..., description='The SDN zone object identifier.')

class DeleteClusterSdnVnetsVnetIpsResponse(RootModel[None]):
    root: None = Field(...)

class PostClusterSdnVnetsVnetIpsRequest(ProxmoxBaseModel):
    ip: str = Field(..., description='The IP address to associate with the given MAC address')
    mac: str | None = Field(None, description='Unicast MAC address.')
    zone: str = Field(..., description='The SDN zone object identifier.')

class PostClusterSdnVnetsVnetIpsResponse(RootModel[None]):
    root: None = Field(...)

class PutClusterSdnVnetsVnetIpsRequest(ProxmoxBaseModel):
    ip: str = Field(..., description='The IP address to associate with the given MAC address')
    mac: str | None = Field(None, description='Unicast MAC address.')
    vmid: int | None = Field(None, description='The (unique) ID of the VM.')
    zone: str = Field(..., description='The SDN zone object identifier.')

class PutClusterSdnVnetsVnetIpsResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterSdnVnetsVnetSubnetsResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class PostClusterSdnVnetsVnetSubnetsRequest(ProxmoxBaseModel):
    dhcp_dns_server: str | None = Field(None, alias="dhcp-dns-server", description='IP address for the DNS server')
    dhcp_range: list[str] | None = Field(None, alias="dhcp-range", description='A list of DHCP ranges for this subnet')
    dnszoneprefix: str | None = Field(None, description="dns domain zone prefix  ex: 'adm' -> <hostname>.adm.mydomain.com")
    gateway: str | None = Field(None, description='Subnet Gateway: Will be assign on vnet for layer3 zones')
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    snat: bool | None = Field(None, description='enable masquerade for this subnet if pve-firewall')
    subnet: str = Field(..., description='The SDN subnet object identifier.')
    type: str = Field(...)

class PostClusterSdnVnetsVnetSubnetsResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterSdnVnetsVnetSubnetsSubnetRequest(ProxmoxBaseModel):
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')

class DeleteClusterSdnVnetsVnetSubnetsSubnetResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterSdnVnetsVnetSubnetsSubnetResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PutClusterSdnVnetsVnetSubnetsSubnetRequest(ProxmoxBaseModel):
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    dhcp_dns_server: str | None = Field(None, alias="dhcp-dns-server", description='IP address for the DNS server')
    dhcp_range: list[str] | None = Field(None, alias="dhcp-range", description='A list of DHCP ranges for this subnet')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dnszoneprefix: str | None = Field(None, description="dns domain zone prefix  ex: 'adm' -> <hostname>.adm.mydomain.com")
    gateway: str | None = Field(None, description='Subnet Gateway: Will be assign on vnet for layer3 zones')
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    snat: bool | None = Field(None, description='enable masquerade for this subnet if pve-firewall')

class PutClusterSdnVnetsVnetSubnetsSubnetResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterSdnZonesResponseItem(ProxmoxBaseModel):
    advertise_subnets: bool | None = Field(None, alias="advertise-subnets", description='Advertise IP prefixes (Type-5 routes) instead of MAC/IP pairs (Type-2 routes). EVPN zone only.')
    bridge: str | None = Field(None, description='the bridge for which VLANs should be managed. VLAN & QinQ zone only.')
    bridge_disable_mac_learning: bool | None = Field(None, alias="bridge-disable-mac-learning", description='Disable auto mac learning. VLAN zone only.')
    controller: str | None = Field(None, description='ID of the controller for this zone. EVPN zone only.')
    dhcp: str | None = Field(None, description='Name of DHCP server backend for this zone.')
    digest: str | None = Field(None, description='Digest of the controller section.')
    disable_arp_nd_suppression: bool | None = Field(None, alias="disable-arp-nd-suppression", description='Suppress IPv4 ARP && IPv6 Neighbour Discovery messages. EVPN zone only.')
    dns: str | None = Field(None, description='ID of the DNS server for this zone.')
    dnszone: str | None = Field(None, description='Domain name for this zone.')
    exitnodes: str | None = Field(None, description='List of PVE Nodes that should act as exit node for this zone. EVPN zone only.')
    exitnodes_local_routing: bool | None = Field(None, alias="exitnodes-local-routing", description='Create routes on the exit nodes, so they can connect to EVPN guests. EVPN zone only.')
    exitnodes_primary: str | None = Field(None, alias="exitnodes-primary", description='Force traffic through this exitnode first. EVPN zone only.')
    ipam: str | None = Field(None, description='ID of the IPAM for this zone.')
    mac: str | None = Field(None, description='MAC address of the anycast router for this zone.')
    mtu: int | None = Field(None, description='MTU of the zone, will be used for the created VNet bridges.')
    nodes: str | None = Field(None, description='Nodes where this zone should be created.')
    peers: str | None = Field(None, description='Comma-separated list of peers, that are part of the VXLAN zone. Usually the IPs of the nodes. VXLAN zone only.')
    pending: dict[str, object] | None = Field(None, description='Changes that have not yet been applied to the running configuration.')
    reversedns: str | None = Field(None, description='ID of the reverse DNS server for this zone.')
    rt_import: str | None = Field(None, alias="rt-import", description='Route-Targets that should be imported into the VRF of this zone via BGP. EVPN zone only.')
    state: str | None = Field(None, description='State of the SDN configuration object.')
    tag: int | None = Field(None, description='Service-VLAN Tag (outer VLAN). QinQ zone only')
    type: str | None = Field(None, description='Type of the zone.')
    vlan_protocol: str | None = Field(None, alias="vlan-protocol", description='VLAN protocol for the creation of the QinQ zone. QinQ zone only.')
    vrf_vxlan: int | None = Field(None, alias="vrf-vxlan", description='VNI for the zone VRF. EVPN zone only.')
    vxlan_port: int | None = Field(None, alias="vxlan-port", description='UDP port that should be used for the VXLAN tunnel (default 4789). VXLAN zone only.')
    zone: str | None = Field(None, description='Name of the zone.')

class GetClusterSdnZonesResponse(RootModel[list[GetClusterSdnZonesResponseItem]]):
    root: list[GetClusterSdnZonesResponseItem] = Field(...)

class PostClusterSdnZonesRequest(ProxmoxBaseModel):
    advertise_subnets: bool | None = Field(None, alias="advertise-subnets", description='Advertise IP prefixes (Type-5 routes) instead of MAC/IP pairs (Type-2 routes).')
    bridge: str | None = Field(None, description='The bridge for which VLANs should be managed.')
    bridge_disable_mac_learning: bool | None = Field(None, alias="bridge-disable-mac-learning", description='Disable auto mac learning.')
    controller: str | None = Field(None, description='Controller for this zone.')
    dhcp: str | None = Field(None, description='Type of the DHCP backend for this zone')
    disable_arp_nd_suppression: bool | None = Field(None, alias="disable-arp-nd-suppression", description='Suppress IPv4 ARP && IPv6 Neighbour Discovery messages.')
    dns: str | None = Field(None, description='dns api server')
    dnszone: str | None = Field(None, description='dns domain zone  ex: mydomain.com')
    dp_id: int | None = Field(None, alias="dp-id", description='Faucet dataplane id')
    exitnodes: str | None = Field(None, description='List of cluster node names.')
    exitnodes_local_routing: bool | None = Field(None, alias="exitnodes-local-routing", description='Allow exitnodes to connect to EVPN guests.')
    exitnodes_primary: str | None = Field(None, alias="exitnodes-primary", description='Force traffic through this exitnode first.')
    fabric: str | None = Field(None, description='SDN fabric to use as underlay for this VXLAN zone.')
    ipam: str | None = Field(None, description='use a specific ipam')
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    mac: str | None = Field(None, description='Anycast logical router mac address.')
    mtu: int | None = Field(None, description='MTU of the zone, will be used for the created VNet bridges.')
    nodes: str | None = Field(None, description='List of cluster node names.')
    peers: str | None = Field(None, description='Comma-separated list of peers, that are part of the VXLAN zone. Usually the IPs of the nodes.')
    reversedns: str | None = Field(None, description='reverse dns api server')
    rt_import: str | None = Field(None, alias="rt-import", description='List of Route Targets that should be imported into the VRF of the zone.')
    tag: int | None = Field(None, description='Service-VLAN Tag (outer VLAN)')
    type: str = Field(..., description='Plugin type.')
    vlan_protocol: str | None = Field(None, alias="vlan-protocol", description='Which VLAN protocol should be used for the creation of the QinQ zone.')
    vrf_vxlan: int | None = Field(None, alias="vrf-vxlan", description='VNI for the zone VRF.')
    vxlan_port: int | None = Field(None, alias="vxlan-port", description='UDP port that should be used for the VXLAN tunnel (default 4789).')
    zone: str = Field(..., description='The SDN zone object identifier.')

class PostClusterSdnZonesResponse(RootModel[None]):
    root: None = Field(...)

class DeleteClusterSdnZonesZoneRequest(ProxmoxBaseModel):
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')

class DeleteClusterSdnZonesZoneResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterSdnZonesZoneResponse(ProxmoxBaseModel):
    advertise_subnets: bool | None = Field(None, alias="advertise-subnets", description='Advertise IP prefixes (Type-5 routes) instead of MAC/IP pairs (Type-2 routes). EVPN zone only.')
    bridge: str | None = Field(None, description='the bridge for which VLANs should be managed. VLAN & QinQ zone only.')
    bridge_disable_mac_learning: bool | None = Field(None, alias="bridge-disable-mac-learning", description='Disable auto mac learning. VLAN zone only.')
    controller: str | None = Field(None, description='ID of the controller for this zone. EVPN zone only.')
    dhcp: str | None = Field(None, description='Name of DHCP server backend for this zone.')
    digest: str | None = Field(None, description='Digest of the controller section.')
    disable_arp_nd_suppression: bool | None = Field(None, alias="disable-arp-nd-suppression", description='Suppress IPv4 ARP && IPv6 Neighbour Discovery messages. EVPN zone only.')
    dns: str | None = Field(None, description='ID of the DNS server for this zone.')
    dnszone: str | None = Field(None, description='Domain name for this zone.')
    exitnodes: str | None = Field(None, description='List of PVE Nodes that should act as exit node for this zone. EVPN zone only.')
    exitnodes_local_routing: bool | None = Field(None, alias="exitnodes-local-routing", description='Create routes on the exit nodes, so they can connect to EVPN guests. EVPN zone only.')
    exitnodes_primary: str | None = Field(None, alias="exitnodes-primary", description='Force traffic through this exitnode first. EVPN zone only.')
    ipam: str | None = Field(None, description='ID of the IPAM for this zone.')
    mac: str | None = Field(None, description='MAC address of the anycast router for this zone.')
    mtu: int | None = Field(None, description='MTU of the zone, will be used for the created VNet bridges.')
    nodes: str | None = Field(None, description='Nodes where this zone should be created.')
    peers: str | None = Field(None, description='Comma-separated list of peers, that are part of the VXLAN zone. Usually the IPs of the nodes. VXLAN zone only.')
    pending: dict[str, object] | None = Field(None, description='Changes that have not yet been applied to the running configuration.')
    reversedns: str | None = Field(None, description='ID of the reverse DNS server for this zone.')
    rt_import: str | None = Field(None, alias="rt-import", description='Route-Targets that should be imported into the VRF of this zone via BGP. EVPN zone only.')
    state: str | None = Field(None, description='State of the SDN configuration object.')
    tag: int | None = Field(None, description='Service-VLAN Tag (outer VLAN). QinQ zone only')
    type: str = Field(..., description='Type of the zone.')
    vlan_protocol: str | None = Field(None, alias="vlan-protocol", description='VLAN protocol for the creation of the QinQ zone. QinQ zone only.')
    vrf_vxlan: int | None = Field(None, alias="vrf-vxlan", description='VNI for the zone VRF. EVPN zone only.')
    vxlan_port: int | None = Field(None, alias="vxlan-port", description='UDP port that should be used for the VXLAN tunnel (default 4789). VXLAN zone only.')
    zone: str = Field(..., description='Name of the zone.')

class PutClusterSdnZonesZoneRequest(ProxmoxBaseModel):
    advertise_subnets: bool | None = Field(None, alias="advertise-subnets", description='Advertise IP prefixes (Type-5 routes) instead of MAC/IP pairs (Type-2 routes).')
    bridge: str | None = Field(None, description='The bridge for which VLANs should be managed.')
    bridge_disable_mac_learning: bool | None = Field(None, alias="bridge-disable-mac-learning", description='Disable auto mac learning.')
    controller: str | None = Field(None, description='Controller for this zone.')
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    dhcp: str | None = Field(None, description='Type of the DHCP backend for this zone')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable_arp_nd_suppression: bool | None = Field(None, alias="disable-arp-nd-suppression", description='Suppress IPv4 ARP && IPv6 Neighbour Discovery messages.')
    dns: str | None = Field(None, description='dns api server')
    dnszone: str | None = Field(None, description='dns domain zone  ex: mydomain.com')
    dp_id: int | None = Field(None, alias="dp-id", description='Faucet dataplane id')
    exitnodes: str | None = Field(None, description='List of cluster node names.')
    exitnodes_local_routing: bool | None = Field(None, alias="exitnodes-local-routing", description='Allow exitnodes to connect to EVPN guests.')
    exitnodes_primary: str | None = Field(None, alias="exitnodes-primary", description='Force traffic through this exitnode first.')
    fabric: str | None = Field(None, description='SDN fabric to use as underlay for this VXLAN zone.')
    ipam: str | None = Field(None, description='use a specific ipam')
    lock_token: str | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    mac: str | None = Field(None, description='Anycast logical router mac address.')
    mtu: int | None = Field(None, description='MTU of the zone, will be used for the created VNet bridges.')
    nodes: str | None = Field(None, description='List of cluster node names.')
    peers: str | None = Field(None, description='Comma-separated list of peers, that are part of the VXLAN zone. Usually the IPs of the nodes.')
    reversedns: str | None = Field(None, description='reverse dns api server')
    rt_import: str | None = Field(None, alias="rt-import", description='List of Route Targets that should be imported into the VRF of the zone.')
    tag: int | None = Field(None, description='Service-VLAN Tag (outer VLAN)')
    vlan_protocol: str | None = Field(None, alias="vlan-protocol", description='Which VLAN protocol should be used for the creation of the QinQ zone.')
    vrf_vxlan: int | None = Field(None, alias="vrf-vxlan", description='VNI for the zone VRF.')
    vxlan_port: int | None = Field(None, alias="vxlan-port", description='UDP port that should be used for the VXLAN tunnel (default 4789).')

class PutClusterSdnZonesZoneResponse(RootModel[None]):
    root: None = Field(...)

class GetClusterStatusResponseItem(ProxmoxBaseModel):
    id: str | None = Field(None)
    ip: str | None = Field(None, description='[node] IP of the resolved nodename.')
    level: str | None = Field(None, description='[node] Proxmox VE Subscription level, indicates if eligible for enterprise support as well as access to the stable Proxmox VE Enterprise Repository.')
    local: bool | None = Field(None, description='[node] Indicates if this is the responding node.')
    name: str | None = Field(None)
    nodeid: int | None = Field(None, description='[node] ID of the node from the corosync configuration.')
    nodes: int | None = Field(None, description='[cluster] Nodes count, including offline nodes.')
    online: bool | None = Field(None, description='[node] Indicates if the node is online or offline.')
    quorate: bool | None = Field(None, description='[cluster] Indicates if there is a majority of nodes online to make decisions')
    type: str | None = Field(None, description='Indicates the type, either cluster or node. The type defines the object properties e.g. quorate available for type cluster.')
    version: int | None = Field(None, description='[cluster] Current version of the corosync configuration file.')

class GetClusterStatusResponse(RootModel[list[GetClusterStatusResponseItem]]):
    root: list[GetClusterStatusResponseItem] = Field(...)

class GetClusterTasksResponseItem(ProxmoxBaseModel):
    upid: str | None = Field(None)

class GetClusterTasksResponse(RootModel[list[GetClusterTasksResponseItem]]):
    root: list[GetClusterTasksResponseItem] = Field(...)

class GetNodesResponseItem(ProxmoxBaseModel):
    cpu: float | None = Field(None, description='CPU utilization.')
    level: str | None = Field(None, description='Support level.')
    maxcpu: int | None = Field(None, description='Number of available CPUs.')
    maxmem: int | None = Field(None, description='Number of available memory in bytes.')
    mem: int | None = Field(None, description='Used memory in bytes.')
    node: str | None = Field(None, description='The cluster node name.')
    ssl_fingerprint: str | None = Field(None, description='The SSL fingerprint for the node certificate.')
    status: str | None = Field(None, description='Node status.')
    uptime: int | None = Field(None, description='Node uptime in seconds.')

class GetNodesResponse(RootModel[list[GetNodesResponseItem]]):
    root: list[GetNodesResponseItem] = Field(...)

class GetNodesNodeResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeAplinfoResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class PostNodesNodeAplinfoRequest(ProxmoxBaseModel):
    storage: str = Field(..., description='The storage where the template will be stored')
    template: str = Field(..., description='The template which will downloaded')

class PostNodesNodeAplinfoResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeAptResponseItem(ProxmoxBaseModel):
    id: str | None = Field(None)

class GetNodesNodeAptResponse(RootModel[list[GetNodesNodeAptResponseItem]]):
    root: list[GetNodesNodeAptResponseItem] = Field(...)

class GetNodesNodeAptChangelogResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeAptRepositoriesResponse(ProxmoxBaseModel):
    digest: str = Field(..., description='Common digest of all files.')
    errors: list[dict[str, object]] = Field(..., description='List of problematic repository files.')
    files: list[dict[str, object]] = Field(..., description='List of parsed repository files.')
    infos: list[dict[str, object]] = Field(..., description='Additional information/warnings for APT repositories.')
    standard_repos: list[dict[str, object]] = Field(..., alias="standard-repos", description='List of standard repositories and their configuration status')

class PostNodesNodeAptRepositoriesRequest(ProxmoxBaseModel):
    digest: str | None = Field(None, description='Digest to detect modifications.')
    enabled: bool | None = Field(None, description='Whether the repository should be enabled or not.')
    index: int = Field(..., description='Index within the file (starting from 0).')
    path: str = Field(..., description='Path to the containing file.')

class PostNodesNodeAptRepositoriesResponse(RootModel[None]):
    root: None = Field(...)

class PutNodesNodeAptRepositoriesRequest(ProxmoxBaseModel):
    digest: str | None = Field(None, description='Digest to detect modifications.')
    handle: str = Field(..., description='Handle that identifies a repository.')

class PutNodesNodeAptRepositoriesResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeAptUpdateResponseItem(ProxmoxBaseModel):
    arch: str | None = Field(None, alias="Arch", description='Package Architecture.')
    description: str | None = Field(None, alias="Description", description='Package description.')
    notify_status: str | None = Field(None, alias="NotifyStatus", description='Version for which PVE has already sent an update notification for.')
    old_version: str | None = Field(None, alias="OldVersion", description='Old version currently installed.')
    origin: str | None = Field(None, alias="Origin", description="Package origin, e.g., 'Proxmox' or 'Debian'.")
    package: str | None = Field(None, alias="Package", description='Package name.')
    priority: str | None = Field(None, alias="Priority", description='Package priority.')
    section: str | None = Field(None, alias="Section", description='Package section.')
    title: str | None = Field(None, alias="Title", description='Package title.')
    version: str | None = Field(None, alias="Version", description='New version to be updated to.')

class GetNodesNodeAptUpdateResponse(RootModel[list[GetNodesNodeAptUpdateResponseItem]]):
    root: list[GetNodesNodeAptUpdateResponseItem] = Field(...)

class PostNodesNodeAptUpdateRequest(ProxmoxBaseModel):
    notify: bool | None = Field(None, description='Send notification about new packages.')
    quiet: bool | None = Field(None, description='Only produces output suitable for logging, omitting progress indicators.')

class PostNodesNodeAptUpdateResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeAptVersionsResponseItem(ProxmoxBaseModel):
    arch: str | None = Field(None, alias="Arch", description='Package Architecture.')
    current_state: str | None = Field(None, alias="CurrentState", description='Current state of the package installed on the system.')
    description: str | None = Field(None, alias="Description", description='Package description.')
    manager_version: str | None = Field(None, alias="ManagerVersion", description='Version of the currently running pve-manager API server.')
    notify_status: str | None = Field(None, alias="NotifyStatus", description='Version for which PVE has already sent an update notification for.')
    old_version: str | None = Field(None, alias="OldVersion", description='Old version currently installed.')
    origin: str | None = Field(None, alias="Origin", description="Package origin, e.g., 'Proxmox' or 'Debian'.")
    package: str | None = Field(None, alias="Package", description='Package name.')
    priority: str | None = Field(None, alias="Priority", description='Package priority.')
    running_kernel: str | None = Field(None, alias="RunningKernel", description="Kernel release, only for package 'proxmox-ve'.")
    section: str | None = Field(None, alias="Section", description='Package section.')
    title: str | None = Field(None, alias="Title", description='Package title.')
    version: str | None = Field(None, alias="Version", description='New version to be updated to.')

class GetNodesNodeAptVersionsResponse(RootModel[list[GetNodesNodeAptVersionsResponseItem]]):
    root: list[GetNodesNodeAptVersionsResponseItem] = Field(...)

class GetNodesNodeCapabilitiesResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeCapabilitiesQemuResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeCapabilitiesQemuCpuResponseItem(ProxmoxBaseModel):
    custom: bool | None = Field(None, description='True if this is a custom CPU model.')
    name: str | None = Field(None, description="Name of the CPU model. Identifies it for subsequent API calls. Prefixed with 'custom-' for custom models.")
    vendor: str | None = Field(None, description="CPU vendor visible to the guest when this model is selected. Vendor of 'reported-model' in case of custom models.")

class GetNodesNodeCapabilitiesQemuCpuResponse(RootModel[list[GetNodesNodeCapabilitiesQemuCpuResponseItem]]):
    root: list[GetNodesNodeCapabilitiesQemuCpuResponseItem] = Field(...)

class GetNodesNodeCapabilitiesQemuCpuFlagsResponseItem(ProxmoxBaseModel):
    description: str | None = Field(None, description='Description of the CPU flag.')
    name: str | None = Field(None, description='Name of the CPU flag.')

class GetNodesNodeCapabilitiesQemuCpuFlagsResponse(RootModel[list[GetNodesNodeCapabilitiesQemuCpuFlagsResponseItem]]):
    root: list[GetNodesNodeCapabilitiesQemuCpuFlagsResponseItem] = Field(...)

class GetNodesNodeCapabilitiesQemuMachinesResponseItem(ProxmoxBaseModel):
    changes: str | None = Field(None, description='Notable changes of a version, currently only set for +pveX versions.')
    id: str | None = Field(None, description='Full name of machine type and version.')
    type: str | None = Field(None, description='The machine type.')
    version: str | None = Field(None, description='The machine version.')

class GetNodesNodeCapabilitiesQemuMachinesResponse(RootModel[list[GetNodesNodeCapabilitiesQemuMachinesResponseItem]]):
    root: list[GetNodesNodeCapabilitiesQemuMachinesResponseItem] = Field(...)

class GetNodesNodeCapabilitiesQemuMigrationResponse(ProxmoxBaseModel):
    has_dbus_vmstate: bool = Field(..., alias="has-dbus-vmstate", description='Whether the host supports live-migrating additional VM state via the dbus-vmstate helper.')

class GetNodesNodeCephResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeCephCfgResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeCephCfgDbResponseItem(ProxmoxBaseModel):
    can_update_at_runtime: bool | None = Field(None)
    level: str | None = Field(None)
    mask: str | None = Field(None)
    name: str | None = Field(None)
    section: str | None = Field(None)
    value: str | None = Field(None)

class GetNodesNodeCephCfgDbResponse(RootModel[list[GetNodesNodeCephCfgDbResponseItem]]):
    root: list[GetNodesNodeCephCfgDbResponseItem] = Field(...)

class GetNodesNodeCephCfgRawResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeCephCfgValueResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class GetNodesNodeCephCmdSafetyResponse(ProxmoxBaseModel):
    safe: bool = Field(..., description='If it is safe to run the command.')
    status: str | None = Field(None, description='Status message given by Ceph.')

class GetNodesNodeCephCrushResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeCephFsResponseItem(ProxmoxBaseModel):
    data_pool: str | None = Field(None, description='The name of the data pool.')
    metadata_pool: str | None = Field(None, description='The name of the metadata pool.')
    name: str | None = Field(None, description='The ceph filesystem name.')

class GetNodesNodeCephFsResponse(RootModel[list[GetNodesNodeCephFsResponseItem]]):
    root: list[GetNodesNodeCephFsResponseItem] = Field(...)

class PostNodesNodeCephFsNameRequest(ProxmoxBaseModel):
    add_storage: bool | None = Field(None, alias="add-storage", description='Configure the created CephFS as storage for this cluster.')
    pg_num: int | None = Field(None, description='Number of placement groups for the backing data pool. The metadata pool will use a quarter of this.')

class PostNodesNodeCephFsNameResponse(RootModel[str]):
    root: str = Field(...)

class PostNodesNodeCephInitRequest(ProxmoxBaseModel):
    cluster_network: str | None = Field(None, alias="cluster-network", description='Declare a separate cluster network, OSDs will routeheartbeat, object replication and recovery traffic over it')
    disable_cephx: bool | None = Field(None, description='Disable cephx authentication.\n\nWARNING: cephx is a security feature protecting against man-in-the-middle attacks. Only consider disabling cephx if your network is private!')
    min_size: int | None = Field(None, description='Minimum number of available replicas per object to allow I/O')
    network: str | None = Field(None, description='Use specific network for all ceph related traffic')
    pg_bits: int | None = Field(None, description='Placement group bits, used to specify the default number of placement groups.\n\nDepreacted. This setting was deprecated in recent Ceph versions.')
    size: int | None = Field(None, description='Targeted number of replicas per object')

class PostNodesNodeCephInitResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeCephLogResponseItem(ProxmoxBaseModel):
    n: int | None = Field(None, description='Line number')
    t: str | None = Field(None, description='Line text')

class GetNodesNodeCephLogResponse(RootModel[list[GetNodesNodeCephLogResponseItem]]):
    root: list[GetNodesNodeCephLogResponseItem] = Field(...)

class GetNodesNodeCephMdsResponseItem(ProxmoxBaseModel):
    addr: str | None = Field(None)
    host: str | None = Field(None)
    name: str | None = Field(None, description='The name (ID) for the MDS')
    rank: int | None = Field(None)
    standby_replay: bool | None = Field(None, description='If true, the standby MDS is polling the active MDS for faster recovery (hot standby).')
    state: str | None = Field(None, description='State of the MDS')

class GetNodesNodeCephMdsResponse(RootModel[list[GetNodesNodeCephMdsResponseItem]]):
    root: list[GetNodesNodeCephMdsResponseItem] = Field(...)

class DeleteNodesNodeCephMdsNameRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteNodesNodeCephMdsNameResponse(RootModel[str]):
    root: str = Field(...)

class PostNodesNodeCephMdsNameRequest(ProxmoxBaseModel):
    hotstandby: bool | None = Field(None, description='Determines whether a ceph-mds daemon should poll and replay the log of an active MDS. Faster switch on MDS failure, but needs more idle resources.')

class PostNodesNodeCephMdsNameResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeCephMgrResponseItem(ProxmoxBaseModel):
    addr: str | None = Field(None)
    host: str | None = Field(None)
    name: str | None = Field(None, description='The name (ID) for the MGR')
    state: str | None = Field(None, description='State of the MGR')

class GetNodesNodeCephMgrResponse(RootModel[list[GetNodesNodeCephMgrResponseItem]]):
    root: list[GetNodesNodeCephMgrResponseItem] = Field(...)

class DeleteNodesNodeCephMgrIdRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteNodesNodeCephMgrIdResponse(RootModel[str]):
    root: str = Field(...)

class PostNodesNodeCephMgrIdRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeCephMgrIdResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeCephMonResponseItem(ProxmoxBaseModel):
    addr: str | None = Field(None)
    ceph_version: str | None = Field(None)
    ceph_version_short: str | None = Field(None)
    direxists: str | None = Field(None)
    host: bool | None = Field(None)
    name: str | None = Field(None)
    quorum: bool | None = Field(None)
    rank: int | None = Field(None)
    service: int | None = Field(None)
    state: str | None = Field(None)

class GetNodesNodeCephMonResponse(RootModel[list[GetNodesNodeCephMonResponseItem]]):
    root: list[GetNodesNodeCephMonResponseItem] = Field(...)

class DeleteNodesNodeCephMonMonidRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteNodesNodeCephMonMonidResponse(RootModel[str]):
    root: str = Field(...)

class PostNodesNodeCephMonMonidRequest(ProxmoxBaseModel):
    mon_address: str | None = Field(None, alias="mon-address", description='Overwrites autodetected monitor IP address(es). Must be in the public network(s) of Ceph.')

class PostNodesNodeCephMonMonidResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeCephOsdResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeCephOsdRequest(ProxmoxBaseModel):
    crush_device_class: str | None = Field(None, alias="crush-device-class", description='Set the device class of the OSD in crush.')
    db_dev: str | None = Field(None, description='Block device name for block.db.')
    db_dev_size: float | None = Field(None, description='Size in GiB for block.db.')
    dev: str = Field(..., description='Block device name.')
    encrypted: bool | None = Field(None, description='Enables encryption of the OSD.')
    osds_per_device: int | None = Field(None, alias="osds-per-device", description='OSD services per physical device. Only useful for fast NVMe devices"\n\t\t    ." to utilize their performance better.')
    wal_dev: str | None = Field(None, description='Block device name for block.wal.')
    wal_dev_size: float | None = Field(None, description='Size in GiB for block.wal.')

class PostNodesNodeCephOsdResponse(RootModel[str]):
    root: str = Field(...)

class DeleteNodesNodeCephOsdOsdidRequest(ProxmoxBaseModel):
    cleanup: bool | None = Field(None, description='If set, we remove partition table entries.')

class DeleteNodesNodeCephOsdOsdidResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeCephOsdOsdidResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class PostNodesNodeCephOsdOsdidInRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeCephOsdOsdidInResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeCephOsdOsdidLvInfoResponse(ProxmoxBaseModel):
    creation_time: str = Field(..., description='Creation time as reported by `lvs`.')
    lv_name: str = Field(..., description='Name of the logical volume (LV).')
    lv_path: str = Field(..., description='Path to the logical volume (LV).')
    lv_size: int = Field(..., description='Size of the logical volume (LV).')
    lv_uuid: str = Field(..., description='UUID of the logical volume (LV).')
    vg_name: str = Field(..., description='Name of the volume group (VG).')

class GetNodesNodeCephOsdOsdidMetadataResponse(ProxmoxBaseModel):
    devices: list[dict[str, object]] = Field(..., description='Array containing data about devices')
    osd: dict[str, object] = Field(..., description='General information about the OSD')

class PostNodesNodeCephOsdOsdidOutRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeCephOsdOsdidOutResponse(RootModel[None]):
    root: None = Field(...)

class PostNodesNodeCephOsdOsdidScrubRequest(ProxmoxBaseModel):
    deep: bool | None = Field(None, description='If set, instructs a deep scrub instead of a normal one.')

class PostNodesNodeCephOsdOsdidScrubResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeCephPoolResponseItem(ProxmoxBaseModel):
    application_metadata: dict[str, object] | None = Field(None)
    autoscale_status: dict[str, object] | None = Field(None)
    bytes_used: int | None = Field(None)
    crush_rule: int | None = Field(None)
    crush_rule_name: str | None = Field(None)
    min_size: int | None = Field(None)
    percent_used: float | None = Field(None)
    pg_autoscale_mode: str | None = Field(None)
    pg_num: int | None = Field(None)
    pg_num_final: int | None = Field(None)
    pg_num_min: int | None = Field(None)
    pool: int | None = Field(None)
    pool_name: str | None = Field(None)
    size: int | None = Field(None)
    target_size: int | None = Field(None)
    target_size_ratio: float | None = Field(None)
    type: str | None = Field(None)

class GetNodesNodeCephPoolResponse(RootModel[list[GetNodesNodeCephPoolResponseItem]]):
    root: list[GetNodesNodeCephPoolResponseItem] = Field(...)

class PostNodesNodeCephPoolRequest(ProxmoxBaseModel):
    add_storages: bool | None = Field(None, description='Configure VM and CT storage using the new pool.')
    application: str | None = Field(None, description='The application of the pool.')
    crush_rule: str | None = Field(None, description='The rule to use for mapping object placement in the cluster.')
    erasure_coding: str | None = Field(None, alias="erasure-coding", description="Create an erasure coded pool for RBD with an accompaning replicated pool for metadata storage. With EC, the common ceph options 'size', 'min_size' and 'crush_rule' parameters will be applied to the metadata pool.")
    min_size: int | None = Field(None, description='Minimum number of replicas per object')
    name: str = Field(..., description='The name of the pool. It must be unique.')
    pg_autoscale_mode: str | None = Field(None, description='The automatic PG scaling mode of the pool.')
    pg_num: int | None = Field(None, description='Number of placement groups.')
    pg_num_min: int | None = Field(None, description='Minimal number of placement groups.')
    size: int | None = Field(None, description='Number of replicas per object')
    target_size: str | None = Field(None, description='The estimated target size of the pool for the PG autoscaler.')
    target_size_ratio: float | None = Field(None, description='The estimated target ratio of the pool for the PG autoscaler.')

class PostNodesNodeCephPoolResponse(RootModel[str]):
    root: str = Field(...)

class DeleteNodesNodeCephPoolNameRequest(ProxmoxBaseModel):
    force: bool | None = Field(None, description='If true, destroys pool even if in use')
    remove_ecprofile: bool | None = Field(None, description='Remove the erasure code profile. Defaults to true, if applicable.')
    remove_storages: bool | None = Field(None, description='Remove all pveceph-managed storages configured for this pool')

class DeleteNodesNodeCephPoolNameResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeCephPoolNameResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class PutNodesNodeCephPoolNameRequest(ProxmoxBaseModel):
    application: str | None = Field(None, description='The application of the pool.')
    crush_rule: str | None = Field(None, description='The rule to use for mapping object placement in the cluster.')
    min_size: int | None = Field(None, description='Minimum number of replicas per object')
    pg_autoscale_mode: str | None = Field(None, description='The automatic PG scaling mode of the pool.')
    pg_num: int | None = Field(None, description='Number of placement groups.')
    pg_num_min: int | None = Field(None, description='Minimal number of placement groups.')
    size: int | None = Field(None, description='Number of replicas per object')
    target_size: str | None = Field(None, description='The estimated target size of the pool for the PG autoscaler.')
    target_size_ratio: float | None = Field(None, description='The estimated target ratio of the pool for the PG autoscaler.')

class PutNodesNodeCephPoolNameResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeCephPoolNameStatusResponse(ProxmoxBaseModel):
    application: str | None = Field(None, description='The application of the pool.')
    application_list: list[object] | None = Field(None)
    autoscale_status: dict[str, object] | None = Field(None)
    crush_rule: str | None = Field(None, description='The rule to use for mapping object placement in the cluster.')
    fast_read: bool = Field(...)
    hashpspool: bool = Field(...)
    id: int = Field(...)
    min_size: int | None = Field(None, description='Minimum number of replicas per object')
    name: str = Field(..., description='The name of the pool. It must be unique.')
    nodeep_scrub: bool = Field(..., alias="nodeep-scrub")
    nodelete: bool = Field(...)
    nopgchange: bool = Field(...)
    noscrub: bool = Field(...)
    nosizechange: bool = Field(...)
    pg_autoscale_mode: str | None = Field(None, description='The automatic PG scaling mode of the pool.')
    pg_num: int | None = Field(None, description='Number of placement groups.')
    pg_num_min: int | None = Field(None, description='Minimal number of placement groups.')
    pgp_num: int = Field(...)
    size: int | None = Field(None, description='Number of replicas per object')
    statistics: dict[str, object] | None = Field(None)
    target_size: str | None = Field(None, description='The estimated target size of the pool for the PG autoscaler.')
    target_size_ratio: float | None = Field(None, description='The estimated target ratio of the pool for the PG autoscaler.')
    use_gmt_hitset: bool = Field(...)
    write_fadvise_dontneed: bool = Field(...)

class PostNodesNodeCephRestartRequest(ProxmoxBaseModel):
    service: str | None = Field(None, description='Ceph service name.')

class PostNodesNodeCephRestartResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeCephRulesResponseItem(ProxmoxBaseModel):
    name: str | None = Field(None, description='Name of the CRUSH rule.')

class GetNodesNodeCephRulesResponse(RootModel[list[GetNodesNodeCephRulesResponseItem]]):
    root: list[GetNodesNodeCephRulesResponseItem] = Field(...)

class PostNodesNodeCephStartRequest(ProxmoxBaseModel):
    service: str | None = Field(None, description='Ceph service name.')

class PostNodesNodeCephStartResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeCephStatusResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeCephStopRequest(ProxmoxBaseModel):
    service: str | None = Field(None, description='Ceph service name.')

class PostNodesNodeCephStopResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeCertificatesResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeCertificatesAcmeResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class DeleteNodesNodeCertificatesAcmeCertificateRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteNodesNodeCertificatesAcmeCertificateResponse(RootModel[str]):
    root: str = Field(...)

class PostNodesNodeCertificatesAcmeCertificateRequest(ProxmoxBaseModel):
    force: bool | None = Field(None, description='Overwrite existing custom certificate.')

class PostNodesNodeCertificatesAcmeCertificateResponse(RootModel[str]):
    root: str = Field(...)

class PutNodesNodeCertificatesAcmeCertificateRequest(ProxmoxBaseModel):
    force: bool | None = Field(None, description='Force renewal even if expiry is more than 30 days away.')

class PutNodesNodeCertificatesAcmeCertificateResponse(RootModel[str]):
    root: str = Field(...)

class DeleteNodesNodeCertificatesCustomRequest(ProxmoxBaseModel):
    restart: bool | None = Field(None, description='Restart pveproxy.')

class DeleteNodesNodeCertificatesCustomResponse(RootModel[None]):
    root: None = Field(...)

class PostNodesNodeCertificatesCustomRequest(ProxmoxBaseModel):
    certificates: str = Field(..., description='PEM encoded certificate (chain).')
    force: bool | None = Field(None, description='Overwrite existing custom or ACME certificate files.')
    key: str | None = Field(None, description='PEM encoded private key.')
    restart: bool | None = Field(None, description='Restart pveproxy.')

class PostNodesNodeCertificatesCustomResponse(ProxmoxBaseModel):
    filename: str | None = Field(None)
    fingerprint: str | None = Field(None, description='Certificate SHA 256 fingerprint.')
    issuer: str | None = Field(None, description='Certificate issuer name.')
    notafter: int | None = Field(None, description="Certificate's notAfter timestamp (UNIX epoch).")
    notbefore: int | None = Field(None, description="Certificate's notBefore timestamp (UNIX epoch).")
    pem: str | None = Field(None, description='Certificate in PEM format')
    public_key_bits: int | None = Field(None, alias="public-key-bits", description="Certificate's public key size")
    public_key_type: str | None = Field(None, alias="public-key-type", description="Certificate's public key algorithm")
    san: list[str] | None = Field(None, description="List of Certificate's SubjectAlternativeName entries.")
    subject: str | None = Field(None, description='Certificate subject name.')

class GetNodesNodeCertificatesInfoResponseItem(ProxmoxBaseModel):
    filename: str | None = Field(None)
    fingerprint: str | None = Field(None, description='Certificate SHA 256 fingerprint.')
    issuer: str | None = Field(None, description='Certificate issuer name.')
    notafter: int | None = Field(None, description="Certificate's notAfter timestamp (UNIX epoch).")
    notbefore: int | None = Field(None, description="Certificate's notBefore timestamp (UNIX epoch).")
    pem: str | None = Field(None, description='Certificate in PEM format')
    public_key_bits: int | None = Field(None, alias="public-key-bits", description="Certificate's public key size")
    public_key_type: str | None = Field(None, alias="public-key-type", description="Certificate's public key algorithm")
    san: list[str] | None = Field(None, description="List of Certificate's SubjectAlternativeName entries.")
    subject: str | None = Field(None, description='Certificate subject name.')

class GetNodesNodeCertificatesInfoResponse(RootModel[list[GetNodesNodeCertificatesInfoResponseItem]]):
    root: list[GetNodesNodeCertificatesInfoResponseItem] = Field(...)

class GetNodesNodeConfigResponse(ProxmoxBaseModel):
    acme: str | None = Field(None, description='Node specific ACME settings.')
    acmedomain_n: str | None = Field(None, alias="acmedomain[n]", description='ACME domain and validation plugin')
    ballooning_target: int | None = Field(None, alias="ballooning-target", description='RAM usage target for ballooning (in percent of total memory)')
    description: str | None = Field(None, description='Description for the Node. Shown in the web-interface node notes panel. This is saved as comment inside the configuration file.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.')
    startall_onboot_delay: int | None = Field(None, alias="startall-onboot-delay", description='Initial delay in seconds, before starting all the Virtual Guests with on-boot enabled.')
    wakeonlan: str | None = Field(None, description='Node specific wake on LAN settings.')

class PutNodesNodeConfigRequest(ProxmoxBaseModel):
    acme: str | None = Field(None, description='Node specific ACME settings.')
    acmedomain_n: str | None = Field(None, alias="acmedomain[n]", description='ACME domain and validation plugin')
    ballooning_target: int | None = Field(None, alias="ballooning-target", description='RAM usage target for ballooning (in percent of total memory)')
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    description: str | None = Field(None, description='Description for the Node. Shown in the web-interface node notes panel. This is saved as comment inside the configuration file.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.')
    startall_onboot_delay: int | None = Field(None, alias="startall-onboot-delay", description='Initial delay in seconds, before starting all the Virtual Guests with on-boot enabled.')
    wakeonlan: str | None = Field(None, description='Node specific wake on LAN settings.')

class PutNodesNodeConfigResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeDisksResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeDisksDirectoryResponseItem(ProxmoxBaseModel):
    device: str | None = Field(None, description='The mounted device.')
    options: str | None = Field(None, description='The mount options.')
    path: str | None = Field(None, description='The mount path.')
    type: str | None = Field(None, description='The filesystem type.')
    unitfile: str | None = Field(None, description='The path of the mount unit.')

class GetNodesNodeDisksDirectoryResponse(RootModel[list[GetNodesNodeDisksDirectoryResponseItem]]):
    root: list[GetNodesNodeDisksDirectoryResponseItem] = Field(...)

class PostNodesNodeDisksDirectoryRequest(ProxmoxBaseModel):
    add_storage: bool | None = Field(None, description='Configure storage using the directory.')
    device: str = Field(..., description='The block device you want to create the filesystem on.')
    filesystem: str | None = Field(None, description='The desired filesystem.')
    name: str = Field(..., description='The storage identifier.')

class PostNodesNodeDisksDirectoryResponse(RootModel[str]):
    root: str = Field(...)

class DeleteNodesNodeDisksDirectoryNameRequest(ProxmoxBaseModel):
    cleanup_config: bool | None = Field(None, alias="cleanup-config", description='Marks associated storage(s) as not available on this node anymore or removes them from the configuration (if configured for this node only).')
    cleanup_disks: bool | None = Field(None, alias="cleanup-disks", description='Also wipe disk so it can be repurposed afterwards.')

class DeleteNodesNodeDisksDirectoryNameResponse(RootModel[str]):
    root: str = Field(...)

class PostNodesNodeDisksInitgptRequest(ProxmoxBaseModel):
    disk: str = Field(..., description='Block device name')
    uuid: str | None = Field(None, description='UUID for the GPT table')

class PostNodesNodeDisksInitgptResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeDisksListResponseItem(ProxmoxBaseModel):
    devpath: str | None = Field(None, description='The device path')
    gpt: bool | None = Field(None)
    health: str | None = Field(None)
    model: str | None = Field(None)
    mounted: bool | None = Field(None)
    osdid: int | None = Field(None)
    osdid_list: list[int] | None = Field(None, alias="osdid-list")
    parent: str | None = Field(None, description='For partitions only. The device path of the disk the partition resides on.')
    serial: str | None = Field(None)
    size: int | None = Field(None)
    used: str | None = Field(None)
    vendor: str | None = Field(None)
    wwn: str | None = Field(None)

class GetNodesNodeDisksListResponse(RootModel[list[GetNodesNodeDisksListResponseItem]]):
    root: list[GetNodesNodeDisksListResponseItem] = Field(...)

class GetNodesNodeDisksLvmResponse(ProxmoxBaseModel):
    children: list[dict[str, object]] = Field(...)
    leaf: bool = Field(...)

class PostNodesNodeDisksLvmRequest(ProxmoxBaseModel):
    add_storage: bool | None = Field(None, description='Configure storage using the Volume Group')
    device: str = Field(..., description='The block device you want to create the volume group on')
    name: str = Field(..., description='The storage identifier.')

class PostNodesNodeDisksLvmResponse(RootModel[str]):
    root: str = Field(...)

class DeleteNodesNodeDisksLvmNameRequest(ProxmoxBaseModel):
    cleanup_config: bool | None = Field(None, alias="cleanup-config", description='Marks associated storage(s) as not available on this node anymore or removes them from the configuration (if configured for this node only).')
    cleanup_disks: bool | None = Field(None, alias="cleanup-disks", description='Also wipe disks so they can be repurposed afterwards.')

class DeleteNodesNodeDisksLvmNameResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeDisksLvmthinResponseItem(ProxmoxBaseModel):
    lv: str | None = Field(None, description='The name of the thinpool.')
    lv_size: int | None = Field(None, description='The size of the thinpool in bytes.')
    metadata_size: int | None = Field(None, description='The size of the metadata lv in bytes.')
    metadata_used: int | None = Field(None, description='The used bytes of the metadata lv.')
    used: int | None = Field(None, description='The used bytes of the thinpool.')
    vg: str | None = Field(None, description='The associated volume group.')

class GetNodesNodeDisksLvmthinResponse(RootModel[list[GetNodesNodeDisksLvmthinResponseItem]]):
    root: list[GetNodesNodeDisksLvmthinResponseItem] = Field(...)

class PostNodesNodeDisksLvmthinRequest(ProxmoxBaseModel):
    add_storage: bool | None = Field(None, description='Configure storage using the thinpool.')
    device: str = Field(..., description='The block device you want to create the thinpool on.')
    name: str = Field(..., description='The storage identifier.')

class PostNodesNodeDisksLvmthinResponse(RootModel[str]):
    root: str = Field(...)

class DeleteNodesNodeDisksLvmthinNameRequest(ProxmoxBaseModel):
    cleanup_config: bool | None = Field(None, alias="cleanup-config", description='Marks associated storage(s) as not available on this node anymore or removes them from the configuration (if configured for this node only).')
    cleanup_disks: bool | None = Field(None, alias="cleanup-disks", description='Also wipe disks so they can be repurposed afterwards.')
    volume_group: str = Field(..., alias="volume-group", description='The storage identifier.')

class DeleteNodesNodeDisksLvmthinNameResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeDisksSmartResponse(ProxmoxBaseModel):
    attributes: list[object] | None = Field(None)
    health: str = Field(...)
    text: str | None = Field(None)
    type: str | None = Field(None)

class PutNodesNodeDisksWipediskRequest(ProxmoxBaseModel):
    disk: str = Field(..., description='Block device name')

class PutNodesNodeDisksWipediskResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeDisksZfsResponseItem(ProxmoxBaseModel):
    alloc: int | None = Field(None)
    dedup: float | None = Field(None)
    frag: int | None = Field(None)
    free: int | None = Field(None)
    health: str | None = Field(None)
    name: str | None = Field(None)
    size: int | None = Field(None)

class GetNodesNodeDisksZfsResponse(RootModel[list[GetNodesNodeDisksZfsResponseItem]]):
    root: list[GetNodesNodeDisksZfsResponseItem] = Field(...)

class PostNodesNodeDisksZfsRequest(ProxmoxBaseModel):
    add_storage: bool | None = Field(None, description='Configure storage using the zpool.')
    ashift: int | None = Field(None, description='Pool sector size exponent.')
    compression: str | None = Field(None, description='The compression algorithm to use.')
    devices: str = Field(..., description='The block devices you want to create the zpool on.')
    draid_config: str | None = Field(None, alias="draid-config")
    name: str = Field(..., description='The storage identifier.')
    raidlevel: str = Field(..., description='The RAID level to use.')

class PostNodesNodeDisksZfsResponse(RootModel[str]):
    root: str = Field(...)

class DeleteNodesNodeDisksZfsNameRequest(ProxmoxBaseModel):
    cleanup_config: bool | None = Field(None, alias="cleanup-config", description='Marks associated storage(s) as not available on this node anymore or removes them from the configuration (if configured for this node only).')
    cleanup_disks: bool | None = Field(None, alias="cleanup-disks", description='Also wipe disks so they can be repurposed afterwards.')

class DeleteNodesNodeDisksZfsNameResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeDisksZfsNameResponse(ProxmoxBaseModel):
    action: str | None = Field(None, description='Information about the recommended action to fix the state.')
    children: list[dict[str, object]] = Field(..., description='The pool configuration information, including the vdevs for each section (e.g. spares, cache), may be nested.')
    errors: str = Field(..., description='Information about the errors on the zpool.')
    name: str = Field(..., description='The name of the zpool.')
    scan: str | None = Field(None, description='Information about the last/current scrub.')
    state: str = Field(..., description='The state of the zpool.')
    status: str | None = Field(None, description='Information about the state of the zpool.')

class GetNodesNodeDnsResponse(ProxmoxBaseModel):
    dns1: str | None = Field(None, description='First name server IP address.')
    dns2: str | None = Field(None, description='Second name server IP address.')
    dns3: str | None = Field(None, description='Third name server IP address.')
    search: str | None = Field(None, description='Search domain for host-name lookup.')

class PutNodesNodeDnsRequest(ProxmoxBaseModel):
    dns1: str | None = Field(None, description='First name server IP address.')
    dns2: str | None = Field(None, description='Second name server IP address.')
    dns3: str | None = Field(None, description='Third name server IP address.')
    search: str = Field(..., description='Search domain for host-name lookup.')

class PutNodesNodeDnsResponse(RootModel[None]):
    root: None = Field(...)

class PostNodesNodeExecuteRequest(ProxmoxBaseModel):
    commands: str = Field(..., description='JSON encoded array of commands.')

class PostNodesNodeExecuteResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeFirewallResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeFirewallLogResponseItem(ProxmoxBaseModel):
    n: int | None = Field(None, description='Line number')
    t: str | None = Field(None, description='Line text')

class GetNodesNodeFirewallLogResponse(RootModel[list[GetNodesNodeFirewallLogResponseItem]]):
    root: list[GetNodesNodeFirewallLogResponseItem] = Field(...)

class GetNodesNodeFirewallOptionsResponse(ProxmoxBaseModel):
    enable: bool | None = Field(None, description='Enable host firewall rules.')
    log_level_forward: str | None = Field(None, description='Log level for forwarded traffic.')
    log_level_in: str | None = Field(None, description='Log level for incoming traffic.')
    log_level_out: str | None = Field(None, description='Log level for outgoing traffic.')
    log_nf_conntrack: bool | None = Field(None, description='Enable logging of conntrack information.')
    ndp: bool | None = Field(None, description='Enable NDP (Neighbor Discovery Protocol).')
    nf_conntrack_allow_invalid: bool | None = Field(None, description='Allow invalid packets on connection tracking.')
    nf_conntrack_helpers: str | None = Field(None, description='Enable conntrack helpers for specific protocols. Supported protocols: amanda, ftp, irc, netbios-ns, pptp, sane, sip, snmp, tftp')
    nf_conntrack_max: int | None = Field(None, description='Maximum number of tracked connections.')
    nf_conntrack_tcp_timeout_established: int | None = Field(None, description='Conntrack established timeout.')
    nf_conntrack_tcp_timeout_syn_recv: int | None = Field(None, description='Conntrack syn recv timeout.')
    nftables: bool | None = Field(None, description='Enable nftables based firewall (tech preview)')
    nosmurfs: bool | None = Field(None, description='Enable SMURFS filter.')
    protection_synflood: bool | None = Field(None, description='Enable synflood protection')
    protection_synflood_burst: int | None = Field(None, description='Synflood protection rate burst by ip src.')
    protection_synflood_rate: int | None = Field(None, description='Synflood protection rate syn/sec by ip src.')
    smurf_log_level: str | None = Field(None, description='Log level for SMURFS filter.')
    tcp_flags_log_level: str | None = Field(None, description='Log level for illegal tcp flags filter.')
    tcpflags: bool | None = Field(None, description='Filter illegal combinations of TCP flags.')

class PutNodesNodeFirewallOptionsRequest(ProxmoxBaseModel):
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    enable: bool | None = Field(None, description='Enable host firewall rules.')
    log_level_forward: str | None = Field(None, description='Log level for forwarded traffic.')
    log_level_in: str | None = Field(None, description='Log level for incoming traffic.')
    log_level_out: str | None = Field(None, description='Log level for outgoing traffic.')
    log_nf_conntrack: bool | None = Field(None, description='Enable logging of conntrack information.')
    ndp: bool | None = Field(None, description='Enable NDP (Neighbor Discovery Protocol).')
    nf_conntrack_allow_invalid: bool | None = Field(None, description='Allow invalid packets on connection tracking.')
    nf_conntrack_helpers: str | None = Field(None, description='Enable conntrack helpers for specific protocols. Supported protocols: amanda, ftp, irc, netbios-ns, pptp, sane, sip, snmp, tftp')
    nf_conntrack_max: int | None = Field(None, description='Maximum number of tracked connections.')
    nf_conntrack_tcp_timeout_established: int | None = Field(None, description='Conntrack established timeout.')
    nf_conntrack_tcp_timeout_syn_recv: int | None = Field(None, description='Conntrack syn recv timeout.')
    nftables: bool | None = Field(None, description='Enable nftables based firewall (tech preview)')
    nosmurfs: bool | None = Field(None, description='Enable SMURFS filter.')
    protection_synflood: bool | None = Field(None, description='Enable synflood protection')
    protection_synflood_burst: int | None = Field(None, description='Synflood protection rate burst by ip src.')
    protection_synflood_rate: int | None = Field(None, description='Synflood protection rate syn/sec by ip src.')
    smurf_log_level: str | None = Field(None, description='Log level for SMURFS filter.')
    tcp_flags_log_level: str | None = Field(None, description='Log level for illegal tcp flags filter.')
    tcpflags: bool | None = Field(None, description='Filter illegal combinations of TCP flags.')

class PutNodesNodeFirewallOptionsResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeFirewallRulesResponseItem(ProxmoxBaseModel):
    action: str | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: str | None = Field(None, description='Descriptive comment')
    dest: str | None = Field(None, description='Restrict packet destination address')
    dport: str | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: str | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: str | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: str | None = Field(None, description='Log level for firewall rule')
    macro: str | None = Field(None, description='Use predefined standard macro')
    pos: int | None = Field(None, description='Rule position in the ruleset')
    proto: str | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: str | None = Field(None, description='Restrict packet source address')
    sport: str | None = Field(None, description='Restrict TCP/UDP source port')
    type: str | None = Field(None, description='Rule type')

class GetNodesNodeFirewallRulesResponse(RootModel[list[GetNodesNodeFirewallRulesResponseItem]]):
    root: list[GetNodesNodeFirewallRulesResponseItem] = Field(...)

class PostNodesNodeFirewallRulesRequest(ProxmoxBaseModel):
    action: str = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: str | None = Field(None, description='Descriptive comment.')
    dest: str | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: str | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: str | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: str | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: str | None = Field(None, description='Log level for firewall rule.')
    macro: str | None = Field(None, description='Use predefined standard macro.')
    pos: int | None = Field(None, description='Update rule at position <pos>.')
    proto: str | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: str | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: str | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: str = Field(..., description='Rule type.')

class PostNodesNodeFirewallRulesResponse(RootModel[None]):
    root: None = Field(...)

class DeleteNodesNodeFirewallRulesPosRequest(ProxmoxBaseModel):
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteNodesNodeFirewallRulesPosResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeFirewallRulesPosResponse(ProxmoxBaseModel):
    action: str = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: str | None = Field(None, description='Descriptive comment')
    dest: str | None = Field(None, description='Restrict packet destination address')
    dport: str | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: str | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: str | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: str | None = Field(None, description='Log level for firewall rule')
    macro: str | None = Field(None, description='Use predefined standard macro')
    pos: int = Field(..., description='Rule position in the ruleset')
    proto: str | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: str | None = Field(None, description='Restrict packet source address')
    sport: str | None = Field(None, description='Restrict TCP/UDP source port')
    type: str = Field(..., description='Rule type')

class PutNodesNodeFirewallRulesPosRequest(ProxmoxBaseModel):
    action: str | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: str | None = Field(None, description='Descriptive comment.')
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    dest: str | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: str | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: str | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: str | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: str | None = Field(None, description='Log level for firewall rule.')
    macro: str | None = Field(None, description='Use predefined standard macro.')
    moveto: int | None = Field(None, description='Move rule to new position <moveto>. Other arguments are ignored.')
    proto: str | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: str | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: str | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: str | None = Field(None, description='Rule type.')

class PutNodesNodeFirewallRulesPosResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeHardwareResponseItem(ProxmoxBaseModel):
    type: str | None = Field(None)

class GetNodesNodeHardwareResponse(RootModel[list[GetNodesNodeHardwareResponseItem]]):
    root: list[GetNodesNodeHardwareResponseItem] = Field(...)

class GetNodesNodeHardwarePciResponseItem(ProxmoxBaseModel):
    class_: str | None = Field(None, alias="class", description='The PCI Class of the device.')
    device: str | None = Field(None, description='The Device ID.')
    device_name: str | None = Field(None)
    id: str | None = Field(None, description='The PCI ID.')
    iommugroup: int | None = Field(None, description='The IOMMU group in which the device is in. If no IOMMU group is detected, it is set to -1.')
    mdev: bool | None = Field(None, description='If set, marks that the device is capable of creating mediated devices.')
    subsystem_device: str | None = Field(None, description='The Subsystem Device ID.')
    subsystem_device_name: str | None = Field(None)
    subsystem_vendor: str | None = Field(None, description='The Subsystem Vendor ID.')
    subsystem_vendor_name: str | None = Field(None)
    vendor: str | None = Field(None, description='The Vendor ID.')
    vendor_name: str | None = Field(None)

class GetNodesNodeHardwarePciResponse(RootModel[list[GetNodesNodeHardwarePciResponseItem]]):
    root: list[GetNodesNodeHardwarePciResponseItem] = Field(...)

class GetNodesNodeHardwarePciPciIdOrMappingResponseItem(ProxmoxBaseModel):
    method: str | None = Field(None)

class GetNodesNodeHardwarePciPciIdOrMappingResponse(RootModel[list[GetNodesNodeHardwarePciPciIdOrMappingResponseItem]]):
    root: list[GetNodesNodeHardwarePciPciIdOrMappingResponseItem] = Field(...)

class GetNodesNodeHardwarePciPciIdOrMappingMdevResponseItem(ProxmoxBaseModel):
    available: int | None = Field(None, description='The number of still available instances of this type.')
    description: str | None = Field(None, description='Additional description of the type.')
    name: str | None = Field(None, description='A human readable name for the type.')
    type: str | None = Field(None, description='The name of the mdev type.')

class GetNodesNodeHardwarePciPciIdOrMappingMdevResponse(RootModel[list[GetNodesNodeHardwarePciPciIdOrMappingMdevResponseItem]]):
    root: list[GetNodesNodeHardwarePciPciIdOrMappingMdevResponseItem] = Field(...)

class GetNodesNodeHardwareUsbResponseItem(ProxmoxBaseModel):
    busnum: int | None = Field(None)
    class_: int | None = Field(None, alias="class")
    devnum: int | None = Field(None)
    level: int | None = Field(None)
    manufacturer: str | None = Field(None)
    port: int | None = Field(None)
    prodid: str | None = Field(None)
    product: str | None = Field(None)
    serial: str | None = Field(None)
    speed: str | None = Field(None)
    usbpath: str | None = Field(None)
    vendid: str | None = Field(None)

class GetNodesNodeHardwareUsbResponse(RootModel[list[GetNodesNodeHardwareUsbResponseItem]]):
    root: list[GetNodesNodeHardwareUsbResponseItem] = Field(...)

class GetNodesNodeHostsResponse(ProxmoxBaseModel):
    data: str = Field(..., description='The content of /etc/hosts.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class PostNodesNodeHostsRequest(ProxmoxBaseModel):
    data: str = Field(..., description='The target content of /etc/hosts.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class PostNodesNodeHostsResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeJournalResponse(RootModel[list[str]]):
    root: list[str] = Field(...)

class GetNodesNodeLxcResponseItem(ProxmoxBaseModel):
    cpu: float | None = Field(None, description='Current CPU usage.')
    cpus: float | None = Field(None, description='Maximum usable CPUs.')
    disk: int | None = Field(None, description='Root disk image space-usage in bytes.')
    diskread: int | None = Field(None, description="The amount of bytes the guest read from it's block devices since the guest was started. (Note: This info is not available for all storage types.)")
    diskwrite: int | None = Field(None, description="The amount of bytes the guest wrote from it's block devices since the guest was started. (Note: This info is not available for all storage types.)")
    lock: str | None = Field(None, description='The current config lock, if any.')
    maxdisk: int | None = Field(None, description='Root disk image size in bytes.')
    maxmem: int | None = Field(None, description='Maximum memory in bytes.')
    maxswap: int | None = Field(None, description='Maximum SWAP memory in bytes.')
    mem: int | None = Field(None, description='Currently used memory in bytes.')
    name: str | None = Field(None, description='Container name.')
    netin: int | None = Field(None, description='The amount of traffic in bytes that was sent to the guest over the network since it was started.')
    netout: int | None = Field(None, description='The amount of traffic in bytes that was sent from the guest over the network since it was started.')
    pressurecpusome: float | None = Field(None, description='CPU Some pressure stall average over the last 10 seconds.')
    pressureiofull: float | None = Field(None, description='IO Full pressure stall average over the last 10 seconds.')
    pressureiosome: float | None = Field(None, description='IO Some pressure stall average over the last 10 seconds.')
    pressurememoryfull: float | None = Field(None, description='Memory Full pressure stall average over the last 10 seconds.')
    pressurememorysome: float | None = Field(None, description='Memory Some pressure stall average over the last 10 seconds.')
    status: str | None = Field(None, description='LXC Container status.')
    tags: str | None = Field(None, description='The current configured tags, if any.')
    template: bool | None = Field(None, description='Determines if the guest is a template.')
    uptime: int | None = Field(None, description='Uptime in seconds.')
    vmid: int | None = Field(None, description='The (unique) ID of the VM.')

class GetNodesNodeLxcResponse(RootModel[list[GetNodesNodeLxcResponseItem]]):
    root: list[GetNodesNodeLxcResponseItem] = Field(...)

class PostNodesNodeLxcRequest(ProxmoxBaseModel):
    arch: str | None = Field(None, description='OS architecture type.')
    bwlimit: float | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    cmode: str | None = Field(None, description="Console mode. By default, the console command tries to open a connection to one of the available tty devices. By setting cmode to 'console' it tries to attach to /dev/console instead. If you set cmode to 'shell', it simply invokes a shell inside the container (no login).")
    console: bool | None = Field(None, description='Attach a console device (/dev/console) to the container.')
    cores: int | None = Field(None, description='The number of cores assigned to the container. A container can use all available cores by default.')
    cpulimit: float | None = Field(None, description="Limit of CPU usage.\n\nNOTE: If the computer has 2 CPUs, it has a total of '2' CPU time. Value '0' indicates no CPU limit.")
    cpuunits: int | None = Field(None, description='CPU weight for a container, will be clamped to [1, 10000] in cgroup v2.')
    debug: bool | None = Field(None, description='Try to be more verbose. For now this only enables debug log-level on start.')
    description: str | None = Field(None, description="Description for the Container. Shown in the web-interface CT's summary. This is saved as comment inside the configuration file.")
    dev_n: str | None = Field(None, alias="dev[n]", description='Device to pass through to the container')
    entrypoint: str | None = Field(None, description='Command to run as init, optionally with arguments; may start with an absolute path, relative path, or a binary in $PATH.')
    env: str | None = Field(None, description='The container runtime environment as NUL-separated list. Replaces any lxc.environment.runtime entries in the config.')
    features: str | None = Field(None, description='Allow containers access to advanced features.')
    force: bool | None = Field(None, description='Allow to overwrite existing container.')
    ha_managed: bool | None = Field(None, alias="ha-managed", description='Add the CT as a HA resource after it was created.')
    hookscript: str | None = Field(None, description='Script that will be executed during various steps in the containers lifetime.')
    hostname: str | None = Field(None, description='Set a host name for the container.')
    ignore_unpack_errors: bool | None = Field(None, alias="ignore-unpack-errors", description='Ignore errors when extracting the template.')
    lock: str | None = Field(None, description='Lock/unlock the container.')
    memory: int | None = Field(None, description='Amount of RAM for the container in MB.')
    mp_n: str | None = Field(None, alias="mp[n]", description='Use volume as container mount point. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume.')
    nameserver: str | None = Field(None, description='Sets DNS server IP address for a container. Create will automatically use the setting from the host if you neither set searchdomain nor nameserver.')
    net_n: str | None = Field(None, alias="net[n]", description='Specifies network interfaces for the container.')
    onboot: bool | None = Field(None, description='Specifies whether a container will be started during system bootup.')
    ostemplate: str = Field(..., description='The OS template or backup file.')
    ostype: str | None = Field(None, description="OS type. This is used to setup configuration inside the container, and corresponds to lxc setup scripts in /usr/share/lxc/config/<ostype>.common.conf. Value 'unmanaged' can be used to skip and OS specific setup.")
    password: str | None = Field(None, description='Sets root password inside container.')
    pool: str | None = Field(None, description='Add the VM to the specified pool.')
    protection: bool | None = Field(None, description="Sets the protection flag of the container. This will prevent the CT or CT's disk remove/update operation.")
    restore: bool | None = Field(None, description='Mark this as restore task.')
    rootfs: str | None = Field(None, description='Use volume as container root.')
    searchdomain: str | None = Field(None, description='Sets DNS search domains for a container. Create will automatically use the setting from the host if you neither set searchdomain nor nameserver.')
    ssh_public_keys: str | None = Field(None, alias="ssh-public-keys", description='Setup public SSH keys (one key per line, OpenSSH format).')
    start: bool | None = Field(None, description='Start the CT after its creation finished successfully.')
    startup: str | None = Field(None, description="Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the 'up' or 'down' delay in seconds, which specifies a delay to wait before the next VM is started or stopped.")
    storage: str | None = Field(None, description='Default Storage.')
    swap: int | None = Field(None, description='Amount of SWAP for the container in MB.')
    tags: str | None = Field(None, description='Tags of the Container. This is only meta information.')
    template: bool | None = Field(None, description='Enable/disable Template.')
    timezone: str | None = Field(None, description="Time zone to use in the container. If option isn't set, then nothing will be done. Can be set to 'host' to match the host time zone, or an arbitrary time zone option from /usr/share/zoneinfo/zone.tab")
    tty: int | None = Field(None, description='Specify the number of tty available to the container')
    unique: bool | None = Field(None, description='Assign a unique random ethernet address.')
    unprivileged: bool | None = Field(None, description='Makes the container run as unprivileged user. For creation, the default is 1. For restore, the default is the value from the backup. (Should not be modified manually.)')
    unused_n: str | None = Field(None, alias="unused[n]", description='Reference to unused volumes. This is used internally, and should not be modified manually.')
    vmid: int = Field(..., description='The (unique) ID of the VM.')

class PostNodesNodeLxcResponse(RootModel[str]):
    root: str = Field(...)

class DeleteNodesNodeLxcVmidRequest(ProxmoxBaseModel):
    destroy_unreferenced_disks: bool | None = Field(None, alias="destroy-unreferenced-disks", description='If set, destroy additionally all disks with the VMID from all enabled storages which are not referenced in the config.')
    force: bool | None = Field(None, description='Force destroy, even if running.')
    purge: bool | None = Field(None, description='Remove container from all related configurations. For example, backup jobs, replication jobs or HA. Related ACLs and Firewall entries will *always* be removed.')

class DeleteNodesNodeLxcVmidResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeLxcVmidResponseItem(ProxmoxBaseModel):
    subdir: str | None = Field(None)

class GetNodesNodeLxcVmidResponse(RootModel[list[GetNodesNodeLxcVmidResponseItem]]):
    root: list[GetNodesNodeLxcVmidResponseItem] = Field(...)

class PostNodesNodeLxcVmidCloneRequest(ProxmoxBaseModel):
    bwlimit: float | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    description: str | None = Field(None, description='Description for the new CT.')
    full: bool | None = Field(None, description='Create a full copy of all disks. This is always done when you clone a normal CT. For CT templates, we try to create a linked clone by default.')
    hostname: str | None = Field(None, description='Set a hostname for the new CT.')
    newid: int = Field(..., description='VMID for the clone.')
    pool: str | None = Field(None, description='Add the new CT to the specified pool.')
    snapname: str | None = Field(None, description='The name of the snapshot.')
    storage: str | None = Field(None, description='Target storage for full clone.')
    target: str | None = Field(None, description='Target node. Only allowed if the original VM is on shared storage.')

class PostNodesNodeLxcVmidCloneResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeLxcVmidConfigResponse(ProxmoxBaseModel):
    arch: str | None = Field(None, description='OS architecture type.')
    cmode: str | None = Field(None, description="Console mode. By default, the console command tries to open a connection to one of the available tty devices. By setting cmode to 'console' it tries to attach to /dev/console instead. If you set cmode to 'shell', it simply invokes a shell inside the container (no login).")
    console: bool | None = Field(None, description='Attach a console device (/dev/console) to the container.')
    cores: int | None = Field(None, description='The number of cores assigned to the container. A container can use all available cores by default.')
    cpulimit: float | None = Field(None, description="Limit of CPU usage.\n\nNOTE: If the computer has 2 CPUs, it has a total of '2' CPU time. Value '0' indicates no CPU limit.")
    cpuunits: int | None = Field(None, description='CPU weight for a container, will be clamped to [1, 10000] in cgroup v2.')
    debug: bool | None = Field(None, description='Try to be more verbose. For now this only enables debug log-level on start.')
    description: str | None = Field(None, description="Description for the Container. Shown in the web-interface CT's summary. This is saved as comment inside the configuration file.")
    dev_n: str | None = Field(None, alias="dev[n]", description='Device to pass through to the container')
    digest: str = Field(..., description='SHA1 digest of configuration file. This can be used to prevent concurrent modifications.')
    entrypoint: str | None = Field(None, description='Command to run as init, optionally with arguments; may start with an absolute path, relative path, or a binary in $PATH.')
    env: str | None = Field(None, description='The container runtime environment as NUL-separated list. Replaces any lxc.environment.runtime entries in the config.')
    features: str | None = Field(None, description='Allow containers access to advanced features.')
    hookscript: str | None = Field(None, description='Script that will be executed during various steps in the containers lifetime.')
    hostname: str | None = Field(None, description='Set a host name for the container.')
    lock: str | None = Field(None, description='Lock/unlock the container.')
    lxc: list[list[str]] | None = Field(None, description='Array of lxc low-level configurations ([[key1, value1], [key2, value2] ...]).')
    memory: int | None = Field(None, description='Amount of RAM for the container in MB.')
    mp_n: str | None = Field(None, alias="mp[n]", description='Use volume as container mount point. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume.')
    nameserver: str | None = Field(None, description='Sets DNS server IP address for a container. Create will automatically use the setting from the host if you neither set searchdomain nor nameserver.')
    net_n: str | None = Field(None, alias="net[n]", description='Specifies network interfaces for the container.')
    onboot: bool | None = Field(None, description='Specifies whether a container will be started during system bootup.')
    ostype: str | None = Field(None, description="OS type. This is used to setup configuration inside the container, and corresponds to lxc setup scripts in /usr/share/lxc/config/<ostype>.common.conf. Value 'unmanaged' can be used to skip and OS specific setup.")
    protection: bool | None = Field(None, description="Sets the protection flag of the container. This will prevent the CT or CT's disk remove/update operation.")
    rootfs: str | None = Field(None, description='Use volume as container root.')
    searchdomain: str | None = Field(None, description='Sets DNS search domains for a container. Create will automatically use the setting from the host if you neither set searchdomain nor nameserver.')
    startup: str | None = Field(None, description="Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the 'up' or 'down' delay in seconds, which specifies a delay to wait before the next VM is started or stopped.")
    swap: int | None = Field(None, description='Amount of SWAP for the container in MB.')
    tags: str | None = Field(None, description='Tags of the Container. This is only meta information.')
    template: bool | None = Field(None, description='Enable/disable Template.')
    timezone: str | None = Field(None, description="Time zone to use in the container. If option isn't set, then nothing will be done. Can be set to 'host' to match the host time zone, or an arbitrary time zone option from /usr/share/zoneinfo/zone.tab")
    tty: int | None = Field(None, description='Specify the number of tty available to the container')
    unprivileged: bool | None = Field(None, description='Makes the container run as unprivileged user. For creation, the default is 1. For restore, the default is the value from the backup. (Should not be modified manually.)')
    unused_n: str | None = Field(None, alias="unused[n]", description='Reference to unused volumes. This is used internally, and should not be modified manually.')

class PutNodesNodeLxcVmidConfigRequest(ProxmoxBaseModel):
    arch: str | None = Field(None, description='OS architecture type.')
    cmode: str | None = Field(None, description="Console mode. By default, the console command tries to open a connection to one of the available tty devices. By setting cmode to 'console' it tries to attach to /dev/console instead. If you set cmode to 'shell', it simply invokes a shell inside the container (no login).")
    console: bool | None = Field(None, description='Attach a console device (/dev/console) to the container.')
    cores: int | None = Field(None, description='The number of cores assigned to the container. A container can use all available cores by default.')
    cpulimit: float | None = Field(None, description="Limit of CPU usage.\n\nNOTE: If the computer has 2 CPUs, it has a total of '2' CPU time. Value '0' indicates no CPU limit.")
    cpuunits: int | None = Field(None, description='CPU weight for a container, will be clamped to [1, 10000] in cgroup v2.')
    debug: bool | None = Field(None, description='Try to be more verbose. For now this only enables debug log-level on start.')
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    description: str | None = Field(None, description="Description for the Container. Shown in the web-interface CT's summary. This is saved as comment inside the configuration file.")
    dev_n: str | None = Field(None, alias="dev[n]", description='Device to pass through to the container')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.')
    entrypoint: str | None = Field(None, description='Command to run as init, optionally with arguments; may start with an absolute path, relative path, or a binary in $PATH.')
    env: str | None = Field(None, description='The container runtime environment as NUL-separated list. Replaces any lxc.environment.runtime entries in the config.')
    features: str | None = Field(None, description='Allow containers access to advanced features.')
    hookscript: str | None = Field(None, description='Script that will be executed during various steps in the containers lifetime.')
    hostname: str | None = Field(None, description='Set a host name for the container.')
    lock: str | None = Field(None, description='Lock/unlock the container.')
    memory: int | None = Field(None, description='Amount of RAM for the container in MB.')
    mp_n: str | None = Field(None, alias="mp[n]", description='Use volume as container mount point. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume.')
    nameserver: str | None = Field(None, description='Sets DNS server IP address for a container. Create will automatically use the setting from the host if you neither set searchdomain nor nameserver.')
    net_n: str | None = Field(None, alias="net[n]", description='Specifies network interfaces for the container.')
    onboot: bool | None = Field(None, description='Specifies whether a container will be started during system bootup.')
    ostype: str | None = Field(None, description="OS type. This is used to setup configuration inside the container, and corresponds to lxc setup scripts in /usr/share/lxc/config/<ostype>.common.conf. Value 'unmanaged' can be used to skip and OS specific setup.")
    protection: bool | None = Field(None, description="Sets the protection flag of the container. This will prevent the CT or CT's disk remove/update operation.")
    revert: str | None = Field(None, description='Revert a pending change.')
    rootfs: str | None = Field(None, description='Use volume as container root.')
    searchdomain: str | None = Field(None, description='Sets DNS search domains for a container. Create will automatically use the setting from the host if you neither set searchdomain nor nameserver.')
    startup: str | None = Field(None, description="Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the 'up' or 'down' delay in seconds, which specifies a delay to wait before the next VM is started or stopped.")
    swap: int | None = Field(None, description='Amount of SWAP for the container in MB.')
    tags: str | None = Field(None, description='Tags of the Container. This is only meta information.')
    template: bool | None = Field(None, description='Enable/disable Template.')
    timezone: str | None = Field(None, description="Time zone to use in the container. If option isn't set, then nothing will be done. Can be set to 'host' to match the host time zone, or an arbitrary time zone option from /usr/share/zoneinfo/zone.tab")
    tty: int | None = Field(None, description='Specify the number of tty available to the container')
    unprivileged: bool | None = Field(None, description='Makes the container run as unprivileged user. For creation, the default is 1. For restore, the default is the value from the backup. (Should not be modified manually.)')
    unused_n: str | None = Field(None, alias="unused[n]", description='Reference to unused volumes. This is used internally, and should not be modified manually.')

class PutNodesNodeLxcVmidConfigResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeLxcVmidFeatureResponse(ProxmoxBaseModel):
    has_feature: bool = Field(..., alias="hasFeature")

class GetNodesNodeLxcVmidFirewallResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeLxcVmidFirewallAliasesResponseItem(ProxmoxBaseModel):
    cidr: str | None = Field(None)
    comment: str | None = Field(None)
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    name: str | None = Field(None)

class GetNodesNodeLxcVmidFirewallAliasesResponse(RootModel[list[GetNodesNodeLxcVmidFirewallAliasesResponseItem]]):
    root: list[GetNodesNodeLxcVmidFirewallAliasesResponseItem] = Field(...)

class PostNodesNodeLxcVmidFirewallAliasesRequest(ProxmoxBaseModel):
    cidr: str = Field(..., description='Network/IP specification in CIDR format.')
    comment: str | None = Field(None)
    name: str = Field(..., description='Alias name.')

class PostNodesNodeLxcVmidFirewallAliasesResponse(RootModel[None]):
    root: None = Field(...)

class DeleteNodesNodeLxcVmidFirewallAliasesNameRequest(ProxmoxBaseModel):
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteNodesNodeLxcVmidFirewallAliasesNameResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeLxcVmidFirewallAliasesNameResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PutNodesNodeLxcVmidFirewallAliasesNameRequest(ProxmoxBaseModel):
    cidr: str = Field(..., description='Network/IP specification in CIDR format.')
    comment: str | None = Field(None)
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    rename: str | None = Field(None, description='Rename an existing alias.')

class PutNodesNodeLxcVmidFirewallAliasesNameResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeLxcVmidFirewallIpsetResponseItem(ProxmoxBaseModel):
    comment: str | None = Field(None)
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    name: str | None = Field(None, description='IP set name.')

class GetNodesNodeLxcVmidFirewallIpsetResponse(RootModel[list[GetNodesNodeLxcVmidFirewallIpsetResponseItem]]):
    root: list[GetNodesNodeLxcVmidFirewallIpsetResponseItem] = Field(...)

class PostNodesNodeLxcVmidFirewallIpsetRequest(ProxmoxBaseModel):
    comment: str | None = Field(None)
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    name: str = Field(..., description='IP set name.')
    rename: str | None = Field(None, description="Rename an existing IPSet. You can set 'rename' to the same value as 'name' to update the 'comment' of an existing IPSet.")

class PostNodesNodeLxcVmidFirewallIpsetResponse(RootModel[None]):
    root: None = Field(...)

class DeleteNodesNodeLxcVmidFirewallIpsetNameRequest(ProxmoxBaseModel):
    force: bool | None = Field(None, description='Delete all members of the IPSet, if there are any.')

class DeleteNodesNodeLxcVmidFirewallIpsetNameResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeLxcVmidFirewallIpsetNameResponseItem(ProxmoxBaseModel):
    cidr: str | None = Field(None)
    comment: str | None = Field(None)
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    nomatch: bool | None = Field(None)

class GetNodesNodeLxcVmidFirewallIpsetNameResponse(RootModel[list[GetNodesNodeLxcVmidFirewallIpsetNameResponseItem]]):
    root: list[GetNodesNodeLxcVmidFirewallIpsetNameResponseItem] = Field(...)

class PostNodesNodeLxcVmidFirewallIpsetNameRequest(ProxmoxBaseModel):
    cidr: str = Field(..., description='Network/IP specification in CIDR format.')
    comment: str | None = Field(None)
    nomatch: bool | None = Field(None)

class PostNodesNodeLxcVmidFirewallIpsetNameResponse(RootModel[None]):
    root: None = Field(...)

class DeleteNodesNodeLxcVmidFirewallIpsetNameCidrRequest(ProxmoxBaseModel):
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteNodesNodeLxcVmidFirewallIpsetNameCidrResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeLxcVmidFirewallIpsetNameCidrResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PutNodesNodeLxcVmidFirewallIpsetNameCidrRequest(ProxmoxBaseModel):
    comment: str | None = Field(None)
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    nomatch: bool | None = Field(None)

class PutNodesNodeLxcVmidFirewallIpsetNameCidrResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeLxcVmidFirewallLogResponseItem(ProxmoxBaseModel):
    n: int | None = Field(None, description='Line number')
    t: str | None = Field(None, description='Line text')

class GetNodesNodeLxcVmidFirewallLogResponse(RootModel[list[GetNodesNodeLxcVmidFirewallLogResponseItem]]):
    root: list[GetNodesNodeLxcVmidFirewallLogResponseItem] = Field(...)

class GetNodesNodeLxcVmidFirewallOptionsResponse(ProxmoxBaseModel):
    dhcp: bool | None = Field(None, description='Enable DHCP.')
    enable: bool | None = Field(None, description='Enable/disable firewall rules.')
    ipfilter: bool | None = Field(None, description="Enable default IP filters. This is equivalent to adding an empty ipfilter-net<id> ipset for every interface. Such ipsets implicitly contain sane default restrictions such as restricting IPv6 link local addresses to the one derived from the interface's MAC address. For containers the configured IP addresses will be implicitly added.")
    log_level_in: str | None = Field(None, description='Log level for incoming traffic.')
    log_level_out: str | None = Field(None, description='Log level for outgoing traffic.')
    macfilter: bool | None = Field(None, description='Enable/disable MAC address filter.')
    ndp: bool | None = Field(None, description='Enable NDP (Neighbor Discovery Protocol).')
    policy_in: str | None = Field(None, description='Input policy.')
    policy_out: str | None = Field(None, description='Output policy.')
    radv: bool | None = Field(None, description='Allow sending Router Advertisement.')

class PutNodesNodeLxcVmidFirewallOptionsRequest(ProxmoxBaseModel):
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    dhcp: bool | None = Field(None, description='Enable DHCP.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    enable: bool | None = Field(None, description='Enable/disable firewall rules.')
    ipfilter: bool | None = Field(None, description="Enable default IP filters. This is equivalent to adding an empty ipfilter-net<id> ipset for every interface. Such ipsets implicitly contain sane default restrictions such as restricting IPv6 link local addresses to the one derived from the interface's MAC address. For containers the configured IP addresses will be implicitly added.")
    log_level_in: str | None = Field(None, description='Log level for incoming traffic.')
    log_level_out: str | None = Field(None, description='Log level for outgoing traffic.')
    macfilter: bool | None = Field(None, description='Enable/disable MAC address filter.')
    ndp: bool | None = Field(None, description='Enable NDP (Neighbor Discovery Protocol).')
    policy_in: str | None = Field(None, description='Input policy.')
    policy_out: str | None = Field(None, description='Output policy.')
    radv: bool | None = Field(None, description='Allow sending Router Advertisement.')

class PutNodesNodeLxcVmidFirewallOptionsResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeLxcVmidFirewallRefsResponseItem(ProxmoxBaseModel):
    comment: str | None = Field(None)
    name: str | None = Field(None)
    ref: str | None = Field(None)
    scope: str | None = Field(None)
    type: str | None = Field(None)

class GetNodesNodeLxcVmidFirewallRefsResponse(RootModel[list[GetNodesNodeLxcVmidFirewallRefsResponseItem]]):
    root: list[GetNodesNodeLxcVmidFirewallRefsResponseItem] = Field(...)

class GetNodesNodeLxcVmidFirewallRulesResponseItem(ProxmoxBaseModel):
    action: str | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: str | None = Field(None, description='Descriptive comment')
    dest: str | None = Field(None, description='Restrict packet destination address')
    dport: str | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: str | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: str | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: str | None = Field(None, description='Log level for firewall rule')
    macro: str | None = Field(None, description='Use predefined standard macro')
    pos: int | None = Field(None, description='Rule position in the ruleset')
    proto: str | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: str | None = Field(None, description='Restrict packet source address')
    sport: str | None = Field(None, description='Restrict TCP/UDP source port')
    type: str | None = Field(None, description='Rule type')

class GetNodesNodeLxcVmidFirewallRulesResponse(RootModel[list[GetNodesNodeLxcVmidFirewallRulesResponseItem]]):
    root: list[GetNodesNodeLxcVmidFirewallRulesResponseItem] = Field(...)

class PostNodesNodeLxcVmidFirewallRulesRequest(ProxmoxBaseModel):
    action: str = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: str | None = Field(None, description='Descriptive comment.')
    dest: str | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: str | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: str | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: str | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: str | None = Field(None, description='Log level for firewall rule.')
    macro: str | None = Field(None, description='Use predefined standard macro.')
    pos: int | None = Field(None, description='Update rule at position <pos>.')
    proto: str | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: str | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: str | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: str = Field(..., description='Rule type.')

class PostNodesNodeLxcVmidFirewallRulesResponse(RootModel[None]):
    root: None = Field(...)

class DeleteNodesNodeLxcVmidFirewallRulesPosRequest(ProxmoxBaseModel):
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteNodesNodeLxcVmidFirewallRulesPosResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeLxcVmidFirewallRulesPosResponse(ProxmoxBaseModel):
    action: str = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: str | None = Field(None, description='Descriptive comment')
    dest: str | None = Field(None, description='Restrict packet destination address')
    dport: str | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: str | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: str | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: str | None = Field(None, description='Log level for firewall rule')
    macro: str | None = Field(None, description='Use predefined standard macro')
    pos: int = Field(..., description='Rule position in the ruleset')
    proto: str | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: str | None = Field(None, description='Restrict packet source address')
    sport: str | None = Field(None, description='Restrict TCP/UDP source port')
    type: str = Field(..., description='Rule type')

class PutNodesNodeLxcVmidFirewallRulesPosRequest(ProxmoxBaseModel):
    action: str | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: str | None = Field(None, description='Descriptive comment.')
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    dest: str | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: str | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: str | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: str | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: str | None = Field(None, description='Log level for firewall rule.')
    macro: str | None = Field(None, description='Use predefined standard macro.')
    moveto: int | None = Field(None, description='Move rule to new position <moveto>. Other arguments are ignored.')
    proto: str | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: str | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: str | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: str | None = Field(None, description='Rule type.')

class PutNodesNodeLxcVmidFirewallRulesPosResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeLxcVmidInterfacesResponseItem(ProxmoxBaseModel):
    hardware_address: str | None = Field(None, alias="hardware-address", description='The MAC address of the interface')
    hwaddr: str | None = Field(None, description='The MAC address of the interface')
    inet: str | None = Field(None, description='The IPv4 address of the interface')
    inet6: str | None = Field(None, description='The IPv6 address of the interface')
    ip_addresses: list[dict[str, object]] | None = Field(None, alias="ip-addresses", description='The addresses of the interface')
    name: str | None = Field(None, description='The name of the interface')

class GetNodesNodeLxcVmidInterfacesResponse(RootModel[list[GetNodesNodeLxcVmidInterfacesResponseItem]]):
    root: list[GetNodesNodeLxcVmidInterfacesResponseItem] = Field(...)

class GetNodesNodeLxcVmidMigrateResponse(ProxmoxBaseModel):
    allowed_nodes: list[str] | None = Field(None, alias="allowed-nodes", description='List of nodes allowed for migration.')
    dependent_ha_resources: list[str] | None = Field(None, alias="dependent-ha-resources", description='HA resources, which will be migrated to the same target node as the VM, because these are in positive affinity with the VM.')
    not_allowed_nodes: dict[str, object] | None = Field(None, alias="not-allowed-nodes", description='List of not allowed nodes with additional information.')
    running: bool = Field(..., description='Determines if the container is running.')

class PostNodesNodeLxcVmidMigrateRequest(ProxmoxBaseModel):
    bwlimit: float | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    online: bool | None = Field(None, description='Use online/live migration.')
    restart: bool | None = Field(None, description='Use restart migration')
    target: str = Field(..., description='Target node.')
    target_storage: str | None = Field(None, alias="target-storage", description="Mapping from source to target storages. Providing only a single storage ID maps all source storages to that storage. Providing the special value '1' will map each source storage to itself.")
    timeout: int | None = Field(None, description='Timeout in seconds for shutdown for restart migration')

class PostNodesNodeLxcVmidMigrateResponse(RootModel[str]):
    root: str = Field(..., description='the task ID.')

class PostNodesNodeLxcVmidMoveVolumeRequest(ProxmoxBaseModel):
    bwlimit: float | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    delete: bool | None = Field(None, description='Delete the original volume after successful copy. By default the original is kept as an unused volume entry.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA1 " .\n\t\t    "digest. This can be used to prevent concurrent modifications.')
    storage: str | None = Field(None, description='Target Storage.')
    target_digest: str | None = Field(None, alias="target-digest", description='Prevent changes if current configuration file of the target " .\n\t\t    "container has a different SHA1 digest. This can be used to prevent " .\n\t\t    "concurrent modifications.')
    target_vmid: int | None = Field(None, alias="target-vmid", description='The (unique) ID of the VM.')
    target_volume: str | None = Field(None, alias="target-volume", description='The config key the volume will be moved to. Default is the source volume key.')
    volume: str = Field(..., description='Volume which will be moved.')

class PostNodesNodeLxcVmidMoveVolumeResponse(RootModel[str]):
    root: str = Field(...)

class PostNodesNodeLxcVmidMtunnelRequest(ProxmoxBaseModel):
    bridges: str | None = Field(None, description='List of network bridges to check availability. Will be checked again for actually used bridges during migration.')
    storages: str | None = Field(None, description='List of storages to check permission and availability. Will be checked again for all actually used storages during migration.')

class PostNodesNodeLxcVmidMtunnelResponse(ProxmoxBaseModel):
    socket: str = Field(...)
    ticket: str = Field(...)
    upid: str = Field(...)

class GetNodesNodeLxcVmidMtunnelwebsocketResponse(ProxmoxBaseModel):
    port: str | None = Field(None)
    socket: str | None = Field(None)

class GetNodesNodeLxcVmidPendingResponseItem(ProxmoxBaseModel):
    delete: int | None = Field(None, description='Indicates a pending delete request if present and not 0.')
    key: str | None = Field(None, description='Configuration option name.')
    pending: str | None = Field(None, description='Pending value.')
    value: str | None = Field(None, description='Current value.')

class GetNodesNodeLxcVmidPendingResponse(RootModel[list[GetNodesNodeLxcVmidPendingResponseItem]]):
    root: list[GetNodesNodeLxcVmidPendingResponseItem] = Field(...)

class PostNodesNodeLxcVmidRemoteMigrateRequest(ProxmoxBaseModel):
    bwlimit: float | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    delete: bool | None = Field(None, description='Delete the original CT and related data after successful migration. By default the original CT is kept on the source cluster in a stopped state.')
    online: bool | None = Field(None, description='Use online/live migration.')
    restart: bool | None = Field(None, description='Use restart migration')
    target_bridge: str = Field(..., alias="target-bridge", description="Mapping from source to target bridges. Providing only a single bridge ID maps all source bridges to that bridge. Providing the special value '1' will map each source bridge to itself.")
    target_endpoint: str = Field(..., alias="target-endpoint", description='Remote target endpoint')
    target_storage: str = Field(..., alias="target-storage", description="Mapping from source to target storages. Providing only a single storage ID maps all source storages to that storage. Providing the special value '1' will map each source storage to itself.")
    target_vmid: int | None = Field(None, alias="target-vmid", description='The (unique) ID of the VM.')
    timeout: int | None = Field(None, description='Timeout in seconds for shutdown for restart migration')

class PostNodesNodeLxcVmidRemoteMigrateResponse(RootModel[str]):
    root: str = Field(..., description='the task ID.')

class PutNodesNodeLxcVmidResizeRequest(ProxmoxBaseModel):
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.')
    disk: str = Field(..., description='The disk you want to resize.')
    size: str = Field(..., description="The new size. With the '+' sign the value is added to the actual size of the volume and without it, the value is taken as an absolute one. Shrinking disk size is not supported.")

class PutNodesNodeLxcVmidResizeResponse(RootModel[str]):
    root: str = Field(..., description='the task ID.')

class GetNodesNodeLxcVmidRrdResponse(ProxmoxBaseModel):
    filename: str = Field(...)

class GetNodesNodeLxcVmidRrddataResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeLxcVmidSnapshotResponseItem(ProxmoxBaseModel):
    description: str | None = Field(None, description='Snapshot description.')
    name: str | None = Field(None, description="Snapshot identifier. Value 'current' identifies the current VM.")
    parent: str | None = Field(None, description='Parent snapshot identifier.')
    snaptime: int | None = Field(None, description='Snapshot creation time')

class GetNodesNodeLxcVmidSnapshotResponse(RootModel[list[GetNodesNodeLxcVmidSnapshotResponseItem]]):
    root: list[GetNodesNodeLxcVmidSnapshotResponseItem] = Field(...)

class PostNodesNodeLxcVmidSnapshotRequest(ProxmoxBaseModel):
    description: str | None = Field(None, description='A textual description or comment.')
    snapname: str = Field(..., description='The name of the snapshot.')

class PostNodesNodeLxcVmidSnapshotResponse(RootModel[str]):
    root: str = Field(..., description='the task ID.')

class DeleteNodesNodeLxcVmidSnapshotSnapnameRequest(ProxmoxBaseModel):
    force: bool | None = Field(None, description='For removal from config file, even if removing disk snapshots fails.')

class DeleteNodesNodeLxcVmidSnapshotSnapnameResponse(RootModel[str]):
    root: str = Field(..., description='the task ID.')

class GetNodesNodeLxcVmidSnapshotSnapnameResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeLxcVmidSnapshotSnapnameConfigResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PutNodesNodeLxcVmidSnapshotSnapnameConfigRequest(ProxmoxBaseModel):
    description: str | None = Field(None, description='A textual description or comment.')

class PutNodesNodeLxcVmidSnapshotSnapnameConfigResponse(RootModel[None]):
    root: None = Field(...)

class PostNodesNodeLxcVmidSnapshotSnapnameRollbackRequest(ProxmoxBaseModel):
    start: bool | None = Field(None, description='Whether the container should get started after rolling back successfully')

class PostNodesNodeLxcVmidSnapshotSnapnameRollbackResponse(RootModel[str]):
    root: str = Field(..., description='the task ID.')

class PostNodesNodeLxcVmidSpiceproxyRequest(ProxmoxBaseModel):
    proxy: str | None = Field(None, description="SPICE proxy server. This can be used by the client to specify the proxy server. All nodes in a cluster runs 'spiceproxy', so it is up to the client to choose one. By default, we return the node where the VM is currently running. As reasonable setting is to use same node you use to connect to the API (This is window.location.hostname for the JS GUI).")

class PostNodesNodeLxcVmidSpiceproxyResponse(ProxmoxBaseModel):
    host: str = Field(...)
    password: str = Field(...)
    proxy: str = Field(...)
    tls_port: int = Field(..., alias="tls-port")
    type: str = Field(...)

class GetNodesNodeLxcVmidStatusResponseItem(ProxmoxBaseModel):
    subdir: str | None = Field(None)

class GetNodesNodeLxcVmidStatusResponse(RootModel[list[GetNodesNodeLxcVmidStatusResponseItem]]):
    root: list[GetNodesNodeLxcVmidStatusResponseItem] = Field(...)

class GetNodesNodeLxcVmidStatusCurrentResponse(ProxmoxBaseModel):
    cpu: float | None = Field(None, description='Current CPU usage.')
    cpus: float | None = Field(None, description='Maximum usable CPUs.')
    disk: int | None = Field(None, description='Root disk image space-usage in bytes.')
    diskread: int | None = Field(None, description="The amount of bytes the guest read from it's block devices since the guest was started. (Note: This info is not available for all storage types.)")
    diskwrite: int | None = Field(None, description="The amount of bytes the guest wrote from it's block devices since the guest was started. (Note: This info is not available for all storage types.)")
    ha: dict[str, object] = Field(..., description='HA manager service status.')
    lock: str | None = Field(None, description='The current config lock, if any.')
    maxdisk: int | None = Field(None, description='Root disk image size in bytes.')
    maxmem: int | None = Field(None, description='Maximum memory in bytes.')
    maxswap: int | None = Field(None, description='Maximum SWAP memory in bytes.')
    mem: int | None = Field(None, description='Currently used memory in bytes.')
    name: str | None = Field(None, description='Container name.')
    netin: int | None = Field(None, description='The amount of traffic in bytes that was sent to the guest over the network since it was started.')
    netout: int | None = Field(None, description='The amount of traffic in bytes that was sent from the guest over the network since it was started.')
    pressurecpusome: float | None = Field(None, description='CPU Some pressure stall average over the last 10 seconds.')
    pressureiofull: float | None = Field(None, description='IO Full pressure stall average over the last 10 seconds.')
    pressureiosome: float | None = Field(None, description='IO Some pressure stall average over the last 10 seconds.')
    pressurememoryfull: float | None = Field(None, description='Memory Full pressure stall average over the last 10 seconds.')
    pressurememorysome: float | None = Field(None, description='Memory Some pressure stall average over the last 10 seconds.')
    status: str = Field(..., description='LXC Container status.')
    tags: str | None = Field(None, description='The current configured tags, if any.')
    template: bool | None = Field(None, description='Determines if the guest is a template.')
    uptime: int | None = Field(None, description='Uptime in seconds.')
    vmid: int = Field(..., description='The (unique) ID of the VM.')

class PostNodesNodeLxcVmidStatusRebootRequest(ProxmoxBaseModel):
    timeout: int | None = Field(None, description='Wait maximal timeout seconds for the shutdown.')

class PostNodesNodeLxcVmidStatusRebootResponse(RootModel[str]):
    root: str = Field(...)

class PostNodesNodeLxcVmidStatusResumeRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeLxcVmidStatusResumeResponse(RootModel[str]):
    root: str = Field(...)

class PostNodesNodeLxcVmidStatusShutdownRequest(ProxmoxBaseModel):
    force_stop: bool | None = Field(None, alias="forceStop", description='Make sure the Container stops.')
    timeout: int | None = Field(None, description='Wait maximal timeout seconds.')

class PostNodesNodeLxcVmidStatusShutdownResponse(RootModel[str]):
    root: str = Field(...)

class PostNodesNodeLxcVmidStatusStartRequest(ProxmoxBaseModel):
    debug: bool | None = Field(None, description='If set, enables very verbose debug log-level on start.')
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')

class PostNodesNodeLxcVmidStatusStartResponse(RootModel[str]):
    root: str = Field(...)

class PostNodesNodeLxcVmidStatusStopRequest(ProxmoxBaseModel):
    overrule_shutdown: bool | None = Field(None, alias="overrule-shutdown", description="Try to abort active 'vzshutdown' tasks before stopping.")
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')

class PostNodesNodeLxcVmidStatusStopResponse(RootModel[str]):
    root: str = Field(...)

class PostNodesNodeLxcVmidStatusSuspendRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeLxcVmidStatusSuspendResponse(RootModel[str]):
    root: str = Field(...)

class PostNodesNodeLxcVmidTemplateRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeLxcVmidTemplateResponse(RootModel[None]):
    root: None = Field(...)

class PostNodesNodeLxcVmidTermproxyRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeLxcVmidTermproxyResponse(ProxmoxBaseModel):
    port: int = Field(...)
    ticket: str = Field(...)
    upid: str = Field(...)
    user: str = Field(...)

class PostNodesNodeLxcVmidVncproxyRequest(ProxmoxBaseModel):
    height: int | None = Field(None, description='sets the height of the console in pixels.')
    websocket: bool | None = Field(None, description='use websocket instead of standard VNC.')
    width: int | None = Field(None, description='sets the width of the console in pixels.')

class PostNodesNodeLxcVmidVncproxyResponse(ProxmoxBaseModel):
    cert: str = Field(...)
    port: int = Field(...)
    ticket: str = Field(...)
    upid: str = Field(...)
    user: str = Field(...)

class GetNodesNodeLxcVmidVncwebsocketResponse(ProxmoxBaseModel):
    port: str = Field(...)

class PostNodesNodeMigrateallRequest(ProxmoxBaseModel):
    maxworkers: int | None = Field(None, description="Maximal number of parallel migration job. If not set, uses'max_workers' from datacenter.cfg. One of both must be set!")
    target: str = Field(..., description='Target node.')
    vms: str | None = Field(None, description='Only consider Guests with these IDs.')
    with_local_disks: bool | None = Field(None, alias="with-local-disks", description='Enable live storage migration for local disk')

class PostNodesNodeMigrateallResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeNetstatResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class DeleteNodesNodeNetworkRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteNodesNodeNetworkResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeNetworkResponseItem(ProxmoxBaseModel):
    active: bool | None = Field(None, description='Set to true if the interface is active.')
    address: str | None = Field(None, description='IP address.')
    address6: str | None = Field(None, description='IP address.')
    autostart: bool | None = Field(None, description='Automatically start interface on boot.')
    bond_primary: str | None = Field(None, alias="bond-primary", description='Specify the primary interface for active-backup bond.')
    bond_mode: str | None = Field(None, description='Bonding mode.')
    bond_xmit_hash_policy: str | None = Field(None, description='Selects the transmit hash policy to use for slave selection in balance-xor and 802.3ad modes.')
    bridge_access: int | None = Field(None, alias="bridge-access", description='The bridge port access VLAN.')
    bridge_arp_nd_suppress: bool | None = Field(None, alias="bridge-arp-nd-suppress", description='Bridge port ARP/ND suppress flag.')
    bridge_learning: bool | None = Field(None, alias="bridge-learning", description='Bridge port learning flag.')
    bridge_multicast_flood: bool | None = Field(None, alias="bridge-multicast-flood", description='Bridge port multicast flood flag.')
    bridge_unicast_flood: bool | None = Field(None, alias="bridge-unicast-flood", description='Bridge port unicast flood flag.')
    bridge_ports: str | None = Field(None, description='Specify the interfaces you want to add to your bridge.')
    bridge_vids: str | None = Field(None, description="Specify the allowed VLANs. For example: '2 4 100-200'. Only used if the bridge is VLAN aware.")
    bridge_vlan_aware: bool | None = Field(None, description='Enable bridge vlan support.')
    cidr: str | None = Field(None, description='IPv4 CIDR.')
    cidr6: str | None = Field(None, description='IPv6 CIDR.')
    comments: str | None = Field(None, description='Comments')
    comments6: str | None = Field(None, description='Comments')
    exists: bool | None = Field(None, description='Set to true if the interface physically exists.')
    families: list[str] | None = Field(None, description='The network families.')
    gateway: str | None = Field(None, description='Default gateway address.')
    gateway6: str | None = Field(None, description='Default ipv6 gateway address.')
    iface: str | None = Field(None, description='Network interface name.')
    link_type: str | None = Field(None, alias="link-type", description='The link type.')
    method: str | None = Field(None, description='The network configuration method for IPv4.')
    method6: str | None = Field(None, description='The network configuration method for IPv6.')
    mtu: int | None = Field(None, description='MTU.')
    netmask: str | None = Field(None, description='Network mask.')
    netmask6: int | None = Field(None, description='Network mask.')
    options: list[str] | None = Field(None, description='A list of additional interface options for IPv4.')
    options6: list[str] | None = Field(None, description='A list of additional interface options for IPv6.')
    ovs_bonds: str | None = Field(None, description='Specify the interfaces used by the bonding device.')
    ovs_bridge: str | None = Field(None, description='The OVS bridge associated with a OVS port. This is required when you create an OVS port.')
    ovs_options: str | None = Field(None, description='OVS interface options.')
    ovs_ports: str | None = Field(None, description='Specify the interfaces you want to add to your bridge.')
    ovs_tag: int | None = Field(None, description='Specify a VLan tag (used by OVSPort, OVSIntPort, OVSBond)')
    priority: int | None = Field(None, description='The order of the interface.')
    slaves: str | None = Field(None, description='Specify the interfaces used by the bonding device.')
    type: str | None = Field(None, description='Network interface type')
    uplink_id: str | None = Field(None, alias="uplink-id", description='The uplink ID.')
    vlan_id: int | None = Field(None, alias="vlan-id", description='vlan-id for a custom named vlan interface (ifupdown2 only).')
    vlan_protocol: str | None = Field(None, alias="vlan-protocol", description='The VLAN protocol.')
    vlan_raw_device: str | None = Field(None, alias="vlan-raw-device", description='Specify the raw interface for the vlan interface.')
    vxlan_id: int | None = Field(None, alias="vxlan-id", description='The VXLAN ID.')
    vxlan_local_tunnelip: str | None = Field(None, alias="vxlan-local-tunnelip", description='The VXLAN local tunnel IP.')
    vxlan_physdev: str | None = Field(None, alias="vxlan-physdev", description='The physical device for the VXLAN tunnel.')
    vxlan_svcnodeip: str | None = Field(None, alias="vxlan-svcnodeip", description='The VXLAN SVC node IP.')

class GetNodesNodeNetworkResponse(RootModel[list[GetNodesNodeNetworkResponseItem]]):
    root: list[GetNodesNodeNetworkResponseItem] = Field(...)

class PostNodesNodeNetworkRequest(ProxmoxBaseModel):
    address: str | None = Field(None, description='IP address.')
    address6: str | None = Field(None, description='IP address.')
    autostart: bool | None = Field(None, description='Automatically start interface on boot.')
    bond_primary: str | None = Field(None, alias="bond-primary", description='Specify the primary interface for active-backup bond.')
    bond_mode: str | None = Field(None, description='Bonding mode.')
    bond_xmit_hash_policy: str | None = Field(None, description='Selects the transmit hash policy to use for slave selection in balance-xor and 802.3ad modes.')
    bridge_ports: str | None = Field(None, description='Specify the interfaces you want to add to your bridge.')
    bridge_vids: str | None = Field(None, description="Specify the allowed VLANs. For example: '2 4 100-200'. Only used if the bridge is VLAN aware.")
    bridge_vlan_aware: bool | None = Field(None, description='Enable bridge vlan support.')
    cidr: str | None = Field(None, description='IPv4 CIDR.')
    cidr6: str | None = Field(None, description='IPv6 CIDR.')
    comments: str | None = Field(None, description='Comments')
    comments6: str | None = Field(None, description='Comments')
    gateway: str | None = Field(None, description='Default gateway address.')
    gateway6: str | None = Field(None, description='Default ipv6 gateway address.')
    iface: str = Field(..., description='Network interface name.')
    mtu: int | None = Field(None, description='MTU.')
    netmask: str | None = Field(None, description='Network mask.')
    netmask6: int | None = Field(None, description='Network mask.')
    ovs_bonds: str | None = Field(None, description='Specify the interfaces used by the bonding device.')
    ovs_bridge: str | None = Field(None, description='The OVS bridge associated with a OVS port. This is required when you create an OVS port.')
    ovs_options: str | None = Field(None, description='OVS interface options.')
    ovs_ports: str | None = Field(None, description='Specify the interfaces you want to add to your bridge.')
    ovs_tag: int | None = Field(None, description='Specify a VLan tag (used by OVSPort, OVSIntPort, OVSBond)')
    slaves: str | None = Field(None, description='Specify the interfaces used by the bonding device.')
    type: str = Field(..., description='Network interface type')
    vlan_id: int | None = Field(None, alias="vlan-id", description='vlan-id for a custom named vlan interface (ifupdown2 only).')
    vlan_raw_device: str | None = Field(None, alias="vlan-raw-device", description='Specify the raw interface for the vlan interface.')

class PostNodesNodeNetworkResponse(RootModel[None]):
    root: None = Field(...)

class PutNodesNodeNetworkRequest(ProxmoxBaseModel):
    regenerate_frr: bool | None = Field(None, alias="regenerate-frr", description='Whether FRR config generation should get skipped or not.')

class PutNodesNodeNetworkResponse(RootModel[str]):
    root: str = Field(...)

class DeleteNodesNodeNetworkIfaceRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteNodesNodeNetworkIfaceResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeNetworkIfaceResponse(ProxmoxBaseModel):
    method: str = Field(...)
    type: str = Field(...)

class PutNodesNodeNetworkIfaceRequest(ProxmoxBaseModel):
    address: str | None = Field(None, description='IP address.')
    address6: str | None = Field(None, description='IP address.')
    autostart: bool | None = Field(None, description='Automatically start interface on boot.')
    bond_primary: str | None = Field(None, alias="bond-primary", description='Specify the primary interface for active-backup bond.')
    bond_mode: str | None = Field(None, description='Bonding mode.')
    bond_xmit_hash_policy: str | None = Field(None, description='Selects the transmit hash policy to use for slave selection in balance-xor and 802.3ad modes.')
    bridge_ports: str | None = Field(None, description='Specify the interfaces you want to add to your bridge.')
    bridge_vids: str | None = Field(None, description="Specify the allowed VLANs. For example: '2 4 100-200'. Only used if the bridge is VLAN aware.")
    bridge_vlan_aware: bool | None = Field(None, description='Enable bridge vlan support.')
    cidr: str | None = Field(None, description='IPv4 CIDR.')
    cidr6: str | None = Field(None, description='IPv6 CIDR.')
    comments: str | None = Field(None, description='Comments')
    comments6: str | None = Field(None, description='Comments')
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    gateway: str | None = Field(None, description='Default gateway address.')
    gateway6: str | None = Field(None, description='Default ipv6 gateway address.')
    mtu: int | None = Field(None, description='MTU.')
    netmask: str | None = Field(None, description='Network mask.')
    netmask6: int | None = Field(None, description='Network mask.')
    ovs_bonds: str | None = Field(None, description='Specify the interfaces used by the bonding device.')
    ovs_bridge: str | None = Field(None, description='The OVS bridge associated with a OVS port. This is required when you create an OVS port.')
    ovs_options: str | None = Field(None, description='OVS interface options.')
    ovs_ports: str | None = Field(None, description='Specify the interfaces you want to add to your bridge.')
    ovs_tag: int | None = Field(None, description='Specify a VLan tag (used by OVSPort, OVSIntPort, OVSBond)')
    slaves: str | None = Field(None, description='Specify the interfaces used by the bonding device.')
    type: str = Field(..., description='Network interface type')
    vlan_id: int | None = Field(None, alias="vlan-id", description='vlan-id for a custom named vlan interface (ifupdown2 only).')
    vlan_raw_device: str | None = Field(None, alias="vlan-raw-device", description='Specify the raw interface for the vlan interface.')

class PutNodesNodeNetworkIfaceResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeQemuResponseItem(ProxmoxBaseModel):
    cpu: float | None = Field(None, description='Current CPU usage.')
    cpus: float | None = Field(None, description='Maximum usable CPUs.')
    diskread: int | None = Field(None, description="The amount of bytes the guest read from it's block devices since the guest was started. (Note: This info is not available for all storage types.)")
    diskwrite: int | None = Field(None, description="The amount of bytes the guest wrote from it's block devices since the guest was started. (Note: This info is not available for all storage types.)")
    lock: str | None = Field(None, description='The current config lock, if any.')
    maxdisk: int | None = Field(None, description='Root disk size in bytes.')
    maxmem: int | None = Field(None, description='Maximum memory in bytes.')
    mem: int | None = Field(None, description='Currently used memory in bytes.')
    memhost: int | None = Field(None, description='Current memory usage on the host.')
    name: str | None = Field(None, description='VM (host)name.')
    netin: int | None = Field(None, description='The amount of traffic in bytes that was sent to the guest over the network since it was started.')
    netout: int | None = Field(None, description='The amount of traffic in bytes that was sent from the guest over the network since it was started.')
    pid: int | None = Field(None, description='PID of the QEMU process, if the VM is running.')
    pressurecpufull: float | None = Field(None, description='CPU Full pressure stall average over the last 10 seconds.')
    pressurecpusome: float | None = Field(None, description='CPU Some pressure stall average over the last 10 seconds.')
    pressureiofull: float | None = Field(None, description='IO Full pressure stall average over the last 10 seconds.')
    pressureiosome: float | None = Field(None, description='IO Some pressure stall average over the last 10 seconds.')
    pressurememoryfull: float | None = Field(None, description='Memory Full pressure stall average over the last 10 seconds.')
    pressurememorysome: float | None = Field(None, description='Memory Some pressure stall average over the last 10 seconds.')
    qmpstatus: str | None = Field(None, description="VM run state from the 'query-status' QMP monitor command.")
    running_machine: str | None = Field(None, alias="running-machine", description='The currently running machine type (if running).')
    running_qemu: str | None = Field(None, alias="running-qemu", description='The QEMU version the VM is currently using (if running).')
    serial: bool | None = Field(None, description='Guest has serial device configured.')
    status: str | None = Field(None, description='QEMU process status.')
    tags: str | None = Field(None, description='The current configured tags, if any')
    template: bool | None = Field(None, description='Determines if the guest is a template.')
    uptime: int | None = Field(None, description='Uptime in seconds.')
    vmid: int | None = Field(None, description='The (unique) ID of the VM.')

class GetNodesNodeQemuResponse(RootModel[list[GetNodesNodeQemuResponseItem]]):
    root: list[GetNodesNodeQemuResponseItem] = Field(...)

class PostNodesNodeQemuRequest(ProxmoxBaseModel):
    acpi: bool | None = Field(None, description='Enable/disable ACPI.')
    affinity: str | None = Field(None, description='List of host cores used to execute guest processes, for example: 0,5,8-11')
    agent: str | None = Field(None, description='Enable/disable communication with the QEMU Guest Agent and its properties.')
    allow_ksm: bool | None = Field(None, alias="allow-ksm", description='Allow memory pages of this guest to be merged via KSM (Kernel Samepage Merging).')
    amd_sev: str | None = Field(None, alias="amd-sev", description='Secure Encrypted Virtualization (SEV) features by AMD CPUs')
    arch: str | None = Field(None, description='Virtual processor architecture. Defaults to the host.')
    archive: str | None = Field(None, description="The backup archive. Either the file system path to a .tar or .vma file (use '-' to pipe data from stdin) or a proxmox storage backup volume identifier.")
    args: str | None = Field(None, description='Arbitrary arguments passed to kvm.')
    audio0: str | None = Field(None, description='Configure a audio device, useful in combination with QXL/Spice.')
    autostart: bool | None = Field(None, description='Automatic restart after crash (currently ignored).')
    balloon: int | None = Field(None, description='Amount of target RAM for the VM in MiB. Using zero disables the ballon driver.')
    bios: str | None = Field(None, description='Select BIOS implementation.')
    boot: str | None = Field(None, description="Specify guest boot order. Use the 'order=' sub-property as usage with no key or 'legacy=' is deprecated.")
    bootdisk: str | None = Field(None, description="Enable booting from specified disk. Deprecated: Use 'boot: order=foo;bar' instead.")
    bwlimit: int | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    cdrom: str | None = Field(None, description='This is an alias for option -ide2')
    cicustom: str | None = Field(None, description='cloud-init: Specify custom files to replace the automatically generated ones at start.')
    cipassword: str | None = Field(None, description='cloud-init: Password to assign the user. Using this is generally not recommended. Use ssh keys instead. Also note that older cloud-init versions do not support hashed passwords.')
    citype: str | None = Field(None, description='Specifies the cloud-init configuration format. The default depends on the configured operating system type (`ostype`. We use the `nocloud` format for Linux, and `configdrive2` for windows.')
    ciupgrade: bool | None = Field(None, description='cloud-init: do an automatic package upgrade after the first boot.')
    ciuser: str | None = Field(None, description="cloud-init: User name to change ssh keys and password for instead of the image's configured default user.")
    cores: int | None = Field(None, description='The number of cores per socket.')
    cpu: str | None = Field(None, description='Emulated CPU type.')
    cpulimit: float | None = Field(None, description='Limit of CPU usage.')
    cpuunits: int | None = Field(None, description='CPU weight for a VM, will be clamped to [1, 10000] in cgroup v2.')
    description: str | None = Field(None, description="Description for the VM. Shown in the web-interface VM's summary. This is saved as comment inside the configuration file.")
    efidisk0: str | None = Field(None, description="Configure a disk for storing EFI vars. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and that the default EFI vars are copied to the volume instead. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    force: bool | None = Field(None, description='Allow to overwrite existing VM.')
    freeze: bool | None = Field(None, description="Freeze CPU at startup (use 'c' monitor command to start execution).")
    ha_managed: bool | None = Field(None, alias="ha-managed", description='Add the VM as a HA resource after it was created.')
    hookscript: str | None = Field(None, description='Script that will be executed during various steps in the vms lifetime.')
    hostpci_n: str | None = Field(None, alias="hostpci[n]", description='Map host PCI devices into guest.')
    hotplug: str | None = Field(None, description="Selectively enable hotplug features. This is a comma separated list of hotplug features: 'network', 'disk', 'cpu', 'memory', 'usb' and 'cloudinit'. Use '0' to disable hotplug completely. Using '1' as value is an alias for the default `network,disk,usb`. USB hotplugging is possible for guests with machine version >= 7.1 and ostype l26 or windows > 7.")
    hugepages: str | None = Field(None, description="Enables hugepages memory.\n\nSets the size of hugepages in MiB. If the value is set to 'any' then 1 GiB hugepages will be used if possible, otherwise the size will fall back to 2 MiB.")
    ide_n: str | None = Field(None, alias="ide[n]", description="Use volume as IDE hard disk or CD-ROM (n is 0 to 3). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    import_working_storage: str | None = Field(None, alias="import-working-storage", description="A file-based storage with 'images' content-type enabled, which is used as an intermediary extraction storage during import. Defaults to the source storage.")
    intel_tdx: str | None = Field(None, alias="intel-tdx", description='Trusted Domain Extension (TDX) features by Intel CPUs')
    ipconfig_n: str | None = Field(None, alias="ipconfig[n]", description="cloud-init: Specify IP addresses and gateways for the corresponding interface.\n\nIP addresses use CIDR notation, gateways are optional but need an IP of the same type specified.\n\nThe special string 'dhcp' can be used for IP addresses to use DHCP, in which case no explicit\ngateway should be provided.\nFor IPv6 the special string 'auto' can be used to use stateless autoconfiguration. This requires\ncloud-init 19.4 or newer.\n\nIf cloud-init is enabled and neither an IPv4 nor an IPv6 address is specified, it defaults to using\ndhcp on IPv4.\n")
    ivshmem: str | None = Field(None, description='Inter-VM shared memory. Useful for direct communication between VMs, or to the host.')
    keephugepages: bool | None = Field(None, description='Use together with hugepages. If enabled, hugepages will not not be deleted after VM shutdown and can be used for subsequent starts.')
    keyboard: str | None = Field(None, description='Keyboard layout for VNC server. This option is generally not required and is often better handled from within the guest OS.')
    kvm: bool | None = Field(None, description='Enable/disable KVM hardware virtualization.')
    live_restore: bool | None = Field(None, alias="live-restore", description='Start the VM immediately while importing or restoring in the background.')
    localtime: bool | None = Field(None, description='Set the real time clock (RTC) to local time. This is enabled by default if the `ostype` indicates a Microsoft Windows OS.')
    lock: str | None = Field(None, description='Lock/unlock the VM.')
    machine: str | None = Field(None, description='Specify the QEMU machine.')
    memory: str | None = Field(None, description='Memory properties.')
    migrate_downtime: float | None = Field(None, description='Set maximum tolerated downtime (in seconds) for migrations. Should the migration not be able to converge in the very end, because too much newly dirtied RAM needs to be transferred, the limit will be increased automatically step-by-step until migration can converge.')
    migrate_speed: int | None = Field(None, description='Set maximum speed (in MB/s) for migrations. Value 0 is no limit.')
    name: str | None = Field(None, description='Set a name for the VM. Only used on the configuration web interface.')
    nameserver: str | None = Field(None, description='cloud-init: Sets DNS server IP address for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.')
    net_n: str | None = Field(None, alias="net[n]", description='Specify network devices.')
    numa: bool | None = Field(None, description='Enable/disable NUMA.')
    numa_n: str | None = Field(None, alias="numa[n]", description='NUMA topology.')
    onboot: bool | None = Field(None, description='Specifies whether a VM will be started during system bootup.')
    ostype: str | None = Field(None, description='Specify guest operating system.')
    parallel_n: str | None = Field(None, alias="parallel[n]", description='Map host parallel devices (n is 0 to 2).')
    pool: str | None = Field(None, description='Add the VM to the specified pool.')
    protection: bool | None = Field(None, description='Sets the protection flag of the VM. This will disable the remove VM and remove disk operations.')
    reboot: bool | None = Field(None, description="Allow reboot. If set to '0' the VM exit on reboot.")
    rng0: str | None = Field(None, description='Configure a VirtIO-based Random Number Generator.')
    sata_n: str | None = Field(None, alias="sata[n]", description="Use volume as SATA hard disk or CD-ROM (n is 0 to 5). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    scsi_n: str | None = Field(None, alias="scsi[n]", description="Use volume as SCSI hard disk or CD-ROM (n is 0 to 30). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    scsihw: str | None = Field(None, description='SCSI controller model')
    searchdomain: str | None = Field(None, description='cloud-init: Sets DNS search domains for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.')
    serial_n: str | None = Field(None, alias="serial[n]", description='Create a serial device inside the VM (n is 0 to 3)')
    shares: int | None = Field(None, description='Amount of memory shares for auto-ballooning. The larger the number is, the more memory this VM gets. Number is relative to weights of all other running VMs. Using zero disables auto-ballooning. Auto-ballooning is done by pvestatd.')
    smbios1: str | None = Field(None, description='Specify SMBIOS type 1 fields.')
    smp: int | None = Field(None, description='The number of CPUs. Please use option -sockets instead.')
    sockets: int | None = Field(None, description='The number of CPU sockets.')
    spice_enhancements: str | None = Field(None, description='Configure additional enhancements for SPICE.')
    sshkeys: str | None = Field(None, description='cloud-init: Setup public SSH keys (one key per line, OpenSSH format).')
    start: bool | None = Field(None, description='Start VM after it was created successfully.')
    startdate: str | None = Field(None, description="Set the initial date of the real time clock. Valid format for date are:'now' or '2006-06-17T16:01:21' or '2006-06-17'.")
    startup: str | None = Field(None, description="Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the 'up' or 'down' delay in seconds, which specifies a delay to wait before the next VM is started or stopped.")
    storage: str | None = Field(None, description='Default storage.')
    tablet: bool | None = Field(None, description='Enable/disable the USB tablet device.')
    tags: str | None = Field(None, description='Tags of the VM. This is only meta information.')
    tdf: bool | None = Field(None, description='Enable/disable time drift fix.')
    template: bool | None = Field(None, description='Enable/disable Template.')
    tpmstate0: str | None = Field(None, description="Configure a Disk for storing TPM state. The format is fixed to 'raw'. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and 4 MiB will be used instead. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    unique: bool | None = Field(None, description='Assign a unique random ethernet address.')
    unused_n: str | None = Field(None, alias="unused[n]", description='Reference to unused volumes. This is used internally, and should not be modified manually.')
    usb_n: str | None = Field(None, alias="usb[n]", description='Configure an USB device (n is 0 to 4, for machine version >= 7.1 and ostype l26 or windows > 7, n can be up to 14).')
    vcpus: int | None = Field(None, description='Number of hotplugged vcpus.')
    vga: str | None = Field(None, description='Configure the VGA hardware.')
    virtio_n: str | None = Field(None, alias="virtio[n]", description="Use volume as VIRTIO hard disk (n is 0 to 15). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    virtiofs_n: str | None = Field(None, alias="virtiofs[n]", description='Configuration for sharing a directory between host and guest using Virtio-fs.')
    vmgenid: str | None = Field(None, description="Set VM Generation ID. Use '1' to autogenerate on create or update, pass '0' to disable explicitly.")
    vmid: int = Field(..., description='The (unique) ID of the VM.')
    vmstatestorage: str | None = Field(None, description='Default storage for VM state volumes/files.')
    watchdog: str | None = Field(None, description='Create a virtual hardware watchdog device.')

class PostNodesNodeQemuResponse(RootModel[str]):
    root: str = Field(...)

class DeleteNodesNodeQemuVmidRequest(ProxmoxBaseModel):
    destroy_unreferenced_disks: bool | None = Field(None, alias="destroy-unreferenced-disks", description='If set, destroy additionally all disks not referenced in the config but with a matching VMID from all enabled storages.')
    purge: bool | None = Field(None, description='Remove VMID from configurations, like backup & replication jobs and HA.')
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')

class DeleteNodesNodeQemuVmidResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeQemuVmidResponseItem(ProxmoxBaseModel):
    subdir: str | None = Field(None)

class GetNodesNodeQemuVmidResponse(RootModel[list[GetNodesNodeQemuVmidResponseItem]]):
    root: list[GetNodesNodeQemuVmidResponseItem] = Field(...)

class GetNodesNodeQemuVmidAgentResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(..., description='Returns the list of QEMU Guest Agent commands')

class PostNodesNodeQemuVmidAgentRequest(ProxmoxBaseModel):
    command: str = Field(..., description='The QGA command.')

class PostNodesNodeQemuVmidAgentResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentExecRequest(ProxmoxBaseModel):
    command: list[str] = Field(..., description='The command as a list of program + arguments.')
    input_data: str | None = Field(None, alias="input-data", description="Data to pass as 'input-data' to the guest. Usually treated as STDIN to 'command'.")

class PostNodesNodeQemuVmidAgentExecResponse(ProxmoxBaseModel):
    pid: int = Field(..., description='The PID of the process started by the guest-agent.')

class GetNodesNodeQemuVmidAgentExecStatusResponse(ProxmoxBaseModel):
    err_data: str | None = Field(None, alias="err-data", description='stderr of the process')
    err_truncated: bool | None = Field(None, alias="err-truncated", description='true if stderr was not fully captured')
    exitcode: int | None = Field(None, description='process exit code if it was normally terminated.')
    exited: bool = Field(..., description='Tells if the given command has exited yet.')
    out_data: str | None = Field(None, alias="out-data", description='stdout of the process')
    out_truncated: bool | None = Field(None, alias="out-truncated", description='true if stdout was not fully captured')
    signal: int | None = Field(None, description='signal number or exception code if the process was abnormally terminated.')

class GetNodesNodeQemuVmidAgentFileReadResponse(ProxmoxBaseModel):
    content: str = Field(..., description='The content of the file, maximum 16777216')
    truncated: bool | None = Field(None, description='If set to 1, the output is truncated and not complete')

class PostNodesNodeQemuVmidAgentFileWriteRequest(ProxmoxBaseModel):
    content: str = Field(..., description='The content to write into the file.')
    encode: bool | None = Field(None, description='If set, the content will be encoded as base64 (required by QEMU).Otherwise the content needs to be encoded beforehand - defaults to true.')
    file: str = Field(..., description='The path to the file.')

class PostNodesNodeQemuVmidAgentFileWriteResponse(RootModel[None]):
    root: None = Field(...)

class PostNodesNodeQemuVmidAgentFsfreezeFreezeRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentFsfreezeFreezeResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentFsfreezeStatusRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentFsfreezeStatusResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentFsfreezeThawRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentFsfreezeThawResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentFstrimRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentFstrimResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetFsinfoResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetHostNameResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetMemoryBlockInfoResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetMemoryBlocksResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetOsinfoResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetTimeResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetTimezoneResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetUsersResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetVcpusResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentInfoResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentNetworkGetInterfacesResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentPingRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentPingResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentSetUserPasswordRequest(ProxmoxBaseModel):
    crypted: bool | None = Field(None, description='set to 1 if the password has already been passed through crypt()')
    password: str = Field(..., description='The new password.')
    username: str = Field(..., description='The user to set the password for.')

class PostNodesNodeQemuVmidAgentSetUserPasswordResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentShutdownRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentShutdownResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentSuspendDiskRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentSuspendDiskResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentSuspendHybridRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentSuspendHybridResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentSuspendRamRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentSuspendRamResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidCloneRequest(ProxmoxBaseModel):
    bwlimit: int | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    description: str | None = Field(None, description='Description for the new VM.')
    format: str | None = Field(None, description='Target format for file storage. Only valid for full clone.')
    full: bool | None = Field(None, description='Create a full copy of all disks. This is always done when you clone a normal VM. For VM templates, we try to create a linked clone by default.')
    name: str | None = Field(None, description='Set a name for the new VM.')
    newid: int = Field(..., description='VMID for the clone.')
    pool: str | None = Field(None, description='Add the new VM to the specified pool.')
    snapname: str | None = Field(None, description='The name of the snapshot.')
    storage: str | None = Field(None, description='Target storage for full clone.')
    target: str | None = Field(None, description='Target node. Only allowed if the original VM is on shared storage.')

class PostNodesNodeQemuVmidCloneResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeQemuVmidCloudinitResponseItem(ProxmoxBaseModel):
    delete: int | None = Field(None, description='Indicates a pending delete request if present and not 0. ')
    key: str | None = Field(None, description='Configuration option name.')
    pending: str | None = Field(None, description='The new pending value.')
    value: str | None = Field(None, description='Value as it was used to generate the current cloudinit image.')

class GetNodesNodeQemuVmidCloudinitResponse(RootModel[list[GetNodesNodeQemuVmidCloudinitResponseItem]]):
    root: list[GetNodesNodeQemuVmidCloudinitResponseItem] = Field(...)

class PutNodesNodeQemuVmidCloudinitRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PutNodesNodeQemuVmidCloudinitResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeQemuVmidCloudinitDumpResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeQemuVmidConfigResponse(ProxmoxBaseModel):
    acpi: bool | None = Field(None, description='Enable/disable ACPI.')
    affinity: str | None = Field(None, description='List of host cores used to execute guest processes, for example: 0,5,8-11')
    agent: str | None = Field(None, description='Enable/disable communication with the QEMU Guest Agent and its properties.')
    allow_ksm: bool | None = Field(None, alias="allow-ksm", description='Allow memory pages of this guest to be merged via KSM (Kernel Samepage Merging).')
    amd_sev: str | None = Field(None, alias="amd-sev", description='Secure Encrypted Virtualization (SEV) features by AMD CPUs')
    arch: str | None = Field(None, description='Virtual processor architecture. Defaults to the host.')
    args: str | None = Field(None, description='Arbitrary arguments passed to kvm.')
    audio0: str | None = Field(None, description='Configure a audio device, useful in combination with QXL/Spice.')
    autostart: bool | None = Field(None, description='Automatic restart after crash (currently ignored).')
    balloon: int | None = Field(None, description='Amount of target RAM for the VM in MiB. Using zero disables the ballon driver.')
    bios: str | None = Field(None, description='Select BIOS implementation.')
    boot: str | None = Field(None, description="Specify guest boot order. Use the 'order=' sub-property as usage with no key or 'legacy=' is deprecated.")
    bootdisk: str | None = Field(None, description="Enable booting from specified disk. Deprecated: Use 'boot: order=foo;bar' instead.")
    cdrom: str | None = Field(None, description='This is an alias for option -ide2')
    cicustom: str | None = Field(None, description='cloud-init: Specify custom files to replace the automatically generated ones at start.')
    cipassword: str | None = Field(None, description='cloud-init: Password to assign the user. Using this is generally not recommended. Use ssh keys instead. Also note that older cloud-init versions do not support hashed passwords.')
    citype: str | None = Field(None, description='Specifies the cloud-init configuration format. The default depends on the configured operating system type (`ostype`. We use the `nocloud` format for Linux, and `configdrive2` for windows.')
    ciupgrade: bool | None = Field(None, description='cloud-init: do an automatic package upgrade after the first boot.')
    ciuser: str | None = Field(None, description="cloud-init: User name to change ssh keys and password for instead of the image's configured default user.")
    cores: int | None = Field(None, description='The number of cores per socket.')
    cpu: str | None = Field(None, description='Emulated CPU type.')
    cpulimit: float | None = Field(None, description='Limit of CPU usage.')
    cpuunits: int | None = Field(None, description='CPU weight for a VM, will be clamped to [1, 10000] in cgroup v2.')
    description: str | None = Field(None, description="Description for the VM. Shown in the web-interface VM's summary. This is saved as comment inside the configuration file.")
    digest: str = Field(..., description='SHA1 digest of configuration file. This can be used to prevent concurrent modifications.')
    efidisk0: str | None = Field(None, description='Configure a disk for storing EFI vars.')
    freeze: bool | None = Field(None, description="Freeze CPU at startup (use 'c' monitor command to start execution).")
    hookscript: str | None = Field(None, description='Script that will be executed during various steps in the vms lifetime.')
    hostpci_n: str | None = Field(None, alias="hostpci[n]", description='Map host PCI devices into guest.')
    hotplug: str | None = Field(None, description="Selectively enable hotplug features. This is a comma separated list of hotplug features: 'network', 'disk', 'cpu', 'memory', 'usb' and 'cloudinit'. Use '0' to disable hotplug completely. Using '1' as value is an alias for the default `network,disk,usb`. USB hotplugging is possible for guests with machine version >= 7.1 and ostype l26 or windows > 7.")
    hugepages: str | None = Field(None, description="Enables hugepages memory.\n\nSets the size of hugepages in MiB. If the value is set to 'any' then 1 GiB hugepages will be used if possible, otherwise the size will fall back to 2 MiB.")
    ide_n: str | None = Field(None, alias="ide[n]", description='Use volume as IDE hard disk or CD-ROM (n is 0 to 3).')
    intel_tdx: str | None = Field(None, alias="intel-tdx", description='Trusted Domain Extension (TDX) features by Intel CPUs')
    ipconfig_n: str | None = Field(None, alias="ipconfig[n]", description="cloud-init: Specify IP addresses and gateways for the corresponding interface.\n\nIP addresses use CIDR notation, gateways are optional but need an IP of the same type specified.\n\nThe special string 'dhcp' can be used for IP addresses to use DHCP, in which case no explicit\ngateway should be provided.\nFor IPv6 the special string 'auto' can be used to use stateless autoconfiguration. This requires\ncloud-init 19.4 or newer.\n\nIf cloud-init is enabled and neither an IPv4 nor an IPv6 address is specified, it defaults to using\ndhcp on IPv4.\n")
    ivshmem: str | None = Field(None, description='Inter-VM shared memory. Useful for direct communication between VMs, or to the host.')
    keephugepages: bool | None = Field(None, description='Use together with hugepages. If enabled, hugepages will not not be deleted after VM shutdown and can be used for subsequent starts.')
    keyboard: str | None = Field(None, description='Keyboard layout for VNC server. This option is generally not required and is often better handled from within the guest OS.')
    kvm: bool | None = Field(None, description='Enable/disable KVM hardware virtualization.')
    localtime: bool | None = Field(None, description='Set the real time clock (RTC) to local time. This is enabled by default if the `ostype` indicates a Microsoft Windows OS.')
    lock: str | None = Field(None, description='Lock/unlock the VM.')
    machine: str | None = Field(None, description='Specify the QEMU machine.')
    memory: str | None = Field(None, description='Memory properties.')
    meta: str | None = Field(None, description='Some (read-only) meta-information about this guest.')
    migrate_downtime: float | None = Field(None, description='Set maximum tolerated downtime (in seconds) for migrations. Should the migration not be able to converge in the very end, because too much newly dirtied RAM needs to be transferred, the limit will be increased automatically step-by-step until migration can converge.')
    migrate_speed: int | None = Field(None, description='Set maximum speed (in MB/s) for migrations. Value 0 is no limit.')
    name: str | None = Field(None, description='Set a name for the VM. Only used on the configuration web interface.')
    nameserver: str | None = Field(None, description='cloud-init: Sets DNS server IP address for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.')
    net_n: str | None = Field(None, alias="net[n]", description='Specify network devices.')
    numa: bool | None = Field(None, description='Enable/disable NUMA.')
    numa_n: str | None = Field(None, alias="numa[n]", description='NUMA topology.')
    onboot: bool | None = Field(None, description='Specifies whether a VM will be started during system bootup.')
    ostype: str | None = Field(None, description='Specify guest operating system.')
    parallel_n: str | None = Field(None, alias="parallel[n]", description='Map host parallel devices (n is 0 to 2).')
    parent: str | None = Field(None, description='Parent snapshot name. This is used internally, and should not be modified.')
    protection: bool | None = Field(None, description='Sets the protection flag of the VM. This will disable the remove VM and remove disk operations.')
    reboot: bool | None = Field(None, description="Allow reboot. If set to '0' the VM exit on reboot.")
    rng0: str | None = Field(None, description='Configure a VirtIO-based Random Number Generator.')
    running_nets_host_mtu: str | None = Field(None, alias="running-nets-host-mtu", description='List of VirtIO network devices and their effective host_mtu setting. A value of 0 means that the host_mtu parameter is to be avoided for the corresponding device. This is used internally for snapshots.')
    runningcpu: str | None = Field(None, description="Specifies the QEMU '-cpu' parameter of the running vm. This is used internally for snapshots.")
    runningmachine: str | None = Field(None, description='Specifies the QEMU machine type of the running vm. This is used internally for snapshots.')
    sata_n: str | None = Field(None, alias="sata[n]", description='Use volume as SATA hard disk or CD-ROM (n is 0 to 5).')
    scsi_n: str | None = Field(None, alias="scsi[n]", description='Use volume as SCSI hard disk or CD-ROM (n is 0 to 30).')
    scsihw: str | None = Field(None, description='SCSI controller model')
    searchdomain: str | None = Field(None, description='cloud-init: Sets DNS search domains for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.')
    serial_n: str | None = Field(None, alias="serial[n]", description='Create a serial device inside the VM (n is 0 to 3)')
    shares: int | None = Field(None, description='Amount of memory shares for auto-ballooning. The larger the number is, the more memory this VM gets. Number is relative to weights of all other running VMs. Using zero disables auto-ballooning. Auto-ballooning is done by pvestatd.')
    smbios1: str | None = Field(None, description='Specify SMBIOS type 1 fields.')
    smp: int | None = Field(None, description='The number of CPUs. Please use option -sockets instead.')
    snaptime: int | None = Field(None, description='Timestamp for snapshots.')
    sockets: int | None = Field(None, description='The number of CPU sockets.')
    spice_enhancements: str | None = Field(None, description='Configure additional enhancements for SPICE.')
    sshkeys: str | None = Field(None, description='cloud-init: Setup public SSH keys (one key per line, OpenSSH format).')
    startdate: str | None = Field(None, description="Set the initial date of the real time clock. Valid format for date are:'now' or '2006-06-17T16:01:21' or '2006-06-17'.")
    startup: str | None = Field(None, description="Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the 'up' or 'down' delay in seconds, which specifies a delay to wait before the next VM is started or stopped.")
    tablet: bool | None = Field(None, description='Enable/disable the USB tablet device.')
    tags: str | None = Field(None, description='Tags of the VM. This is only meta information.')
    tdf: bool | None = Field(None, description='Enable/disable time drift fix.')
    template: bool | None = Field(None, description='Enable/disable Template.')
    tpmstate0: str | None = Field(None, description="Configure a Disk for storing TPM state. The format is fixed to 'raw'.")
    unused_n: str | None = Field(None, alias="unused[n]", description='Reference to unused volumes. This is used internally, and should not be modified manually.')
    usb_n: str | None = Field(None, alias="usb[n]", description='Configure an USB device (n is 0 to 4, for machine version >= 7.1 and ostype l26 or windows > 7, n can be up to 14).')
    vcpus: int | None = Field(None, description='Number of hotplugged vcpus.')
    vga: str | None = Field(None, description='Configure the VGA hardware.')
    virtio_n: str | None = Field(None, alias="virtio[n]", description='Use volume as VIRTIO hard disk (n is 0 to 15).')
    virtiofs_n: str | None = Field(None, alias="virtiofs[n]", description='Configuration for sharing a directory between host and guest using Virtio-fs.')
    vmgenid: str | None = Field(None, description="Set VM Generation ID. Use '1' to autogenerate on create or update, pass '0' to disable explicitly.")
    vmstate: str | None = Field(None, description='Reference to a volume which stores the VM state. This is used internally for snapshots.')
    vmstatestorage: str | None = Field(None, description='Default storage for VM state volumes/files.')
    watchdog: str | None = Field(None, description='Create a virtual hardware watchdog device.')

class PostNodesNodeQemuVmidConfigRequest(ProxmoxBaseModel):
    acpi: bool | None = Field(None, description='Enable/disable ACPI.')
    affinity: str | None = Field(None, description='List of host cores used to execute guest processes, for example: 0,5,8-11')
    agent: str | None = Field(None, description='Enable/disable communication with the QEMU Guest Agent and its properties.')
    allow_ksm: bool | None = Field(None, alias="allow-ksm", description='Allow memory pages of this guest to be merged via KSM (Kernel Samepage Merging).')
    amd_sev: str | None = Field(None, alias="amd-sev", description='Secure Encrypted Virtualization (SEV) features by AMD CPUs')
    arch: str | None = Field(None, description='Virtual processor architecture. Defaults to the host.')
    args: str | None = Field(None, description='Arbitrary arguments passed to kvm.')
    audio0: str | None = Field(None, description='Configure a audio device, useful in combination with QXL/Spice.')
    autostart: bool | None = Field(None, description='Automatic restart after crash (currently ignored).')
    background_delay: int | None = Field(None, description="Time to wait for the task to finish. We return 'null' if the task finish within that time.")
    balloon: int | None = Field(None, description='Amount of target RAM for the VM in MiB. Using zero disables the ballon driver.')
    bios: str | None = Field(None, description='Select BIOS implementation.')
    boot: str | None = Field(None, description="Specify guest boot order. Use the 'order=' sub-property as usage with no key or 'legacy=' is deprecated.")
    bootdisk: str | None = Field(None, description="Enable booting from specified disk. Deprecated: Use 'boot: order=foo;bar' instead.")
    cdrom: str | None = Field(None, description='This is an alias for option -ide2')
    cicustom: str | None = Field(None, description='cloud-init: Specify custom files to replace the automatically generated ones at start.')
    cipassword: str | None = Field(None, description='cloud-init: Password to assign the user. Using this is generally not recommended. Use ssh keys instead. Also note that older cloud-init versions do not support hashed passwords.')
    citype: str | None = Field(None, description='Specifies the cloud-init configuration format. The default depends on the configured operating system type (`ostype`. We use the `nocloud` format for Linux, and `configdrive2` for windows.')
    ciupgrade: bool | None = Field(None, description='cloud-init: do an automatic package upgrade after the first boot.')
    ciuser: str | None = Field(None, description="cloud-init: User name to change ssh keys and password for instead of the image's configured default user.")
    cores: int | None = Field(None, description='The number of cores per socket.')
    cpu: str | None = Field(None, description='Emulated CPU type.')
    cpulimit: float | None = Field(None, description='Limit of CPU usage.')
    cpuunits: int | None = Field(None, description='CPU weight for a VM, will be clamped to [1, 10000] in cgroup v2.')
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    description: str | None = Field(None, description="Description for the VM. Shown in the web-interface VM's summary. This is saved as comment inside the configuration file.")
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.')
    efidisk0: str | None = Field(None, description="Configure a disk for storing EFI vars. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and that the default EFI vars are copied to the volume instead. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    force: bool | None = Field(None, description="Force physical removal. Without this, we simple remove the disk from the config file and create an additional configuration entry called 'unused[n]', which contains the volume ID. Unlink of unused[n] always cause physical removal.")
    freeze: bool | None = Field(None, description="Freeze CPU at startup (use 'c' monitor command to start execution).")
    hookscript: str | None = Field(None, description='Script that will be executed during various steps in the vms lifetime.')
    hostpci_n: str | None = Field(None, alias="hostpci[n]", description='Map host PCI devices into guest.')
    hotplug: str | None = Field(None, description="Selectively enable hotplug features. This is a comma separated list of hotplug features: 'network', 'disk', 'cpu', 'memory', 'usb' and 'cloudinit'. Use '0' to disable hotplug completely. Using '1' as value is an alias for the default `network,disk,usb`. USB hotplugging is possible for guests with machine version >= 7.1 and ostype l26 or windows > 7.")
    hugepages: str | None = Field(None, description="Enables hugepages memory.\n\nSets the size of hugepages in MiB. If the value is set to 'any' then 1 GiB hugepages will be used if possible, otherwise the size will fall back to 2 MiB.")
    ide_n: str | None = Field(None, alias="ide[n]", description="Use volume as IDE hard disk or CD-ROM (n is 0 to 3). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    import_working_storage: str | None = Field(None, alias="import-working-storage", description="A file-based storage with 'images' content-type enabled, which is used as an intermediary extraction storage during import. Defaults to the source storage.")
    intel_tdx: str | None = Field(None, alias="intel-tdx", description='Trusted Domain Extension (TDX) features by Intel CPUs')
    ipconfig_n: str | None = Field(None, alias="ipconfig[n]", description="cloud-init: Specify IP addresses and gateways for the corresponding interface.\n\nIP addresses use CIDR notation, gateways are optional but need an IP of the same type specified.\n\nThe special string 'dhcp' can be used for IP addresses to use DHCP, in which case no explicit\ngateway should be provided.\nFor IPv6 the special string 'auto' can be used to use stateless autoconfiguration. This requires\ncloud-init 19.4 or newer.\n\nIf cloud-init is enabled and neither an IPv4 nor an IPv6 address is specified, it defaults to using\ndhcp on IPv4.\n")
    ivshmem: str | None = Field(None, description='Inter-VM shared memory. Useful for direct communication between VMs, or to the host.')
    keephugepages: bool | None = Field(None, description='Use together with hugepages. If enabled, hugepages will not not be deleted after VM shutdown and can be used for subsequent starts.')
    keyboard: str | None = Field(None, description='Keyboard layout for VNC server. This option is generally not required and is often better handled from within the guest OS.')
    kvm: bool | None = Field(None, description='Enable/disable KVM hardware virtualization.')
    localtime: bool | None = Field(None, description='Set the real time clock (RTC) to local time. This is enabled by default if the `ostype` indicates a Microsoft Windows OS.')
    lock: str | None = Field(None, description='Lock/unlock the VM.')
    machine: str | None = Field(None, description='Specify the QEMU machine.')
    memory: str | None = Field(None, description='Memory properties.')
    migrate_downtime: float | None = Field(None, description='Set maximum tolerated downtime (in seconds) for migrations. Should the migration not be able to converge in the very end, because too much newly dirtied RAM needs to be transferred, the limit will be increased automatically step-by-step until migration can converge.')
    migrate_speed: int | None = Field(None, description='Set maximum speed (in MB/s) for migrations. Value 0 is no limit.')
    name: str | None = Field(None, description='Set a name for the VM. Only used on the configuration web interface.')
    nameserver: str | None = Field(None, description='cloud-init: Sets DNS server IP address for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.')
    net_n: str | None = Field(None, alias="net[n]", description='Specify network devices.')
    numa: bool | None = Field(None, description='Enable/disable NUMA.')
    numa_n: str | None = Field(None, alias="numa[n]", description='NUMA topology.')
    onboot: bool | None = Field(None, description='Specifies whether a VM will be started during system bootup.')
    ostype: str | None = Field(None, description='Specify guest operating system.')
    parallel_n: str | None = Field(None, alias="parallel[n]", description='Map host parallel devices (n is 0 to 2).')
    protection: bool | None = Field(None, description='Sets the protection flag of the VM. This will disable the remove VM and remove disk operations.')
    reboot: bool | None = Field(None, description="Allow reboot. If set to '0' the VM exit on reboot.")
    revert: str | None = Field(None, description='Revert a pending change.')
    rng0: str | None = Field(None, description='Configure a VirtIO-based Random Number Generator.')
    sata_n: str | None = Field(None, alias="sata[n]", description="Use volume as SATA hard disk or CD-ROM (n is 0 to 5). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    scsi_n: str | None = Field(None, alias="scsi[n]", description="Use volume as SCSI hard disk or CD-ROM (n is 0 to 30). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    scsihw: str | None = Field(None, description='SCSI controller model')
    searchdomain: str | None = Field(None, description='cloud-init: Sets DNS search domains for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.')
    serial_n: str | None = Field(None, alias="serial[n]", description='Create a serial device inside the VM (n is 0 to 3)')
    shares: int | None = Field(None, description='Amount of memory shares for auto-ballooning. The larger the number is, the more memory this VM gets. Number is relative to weights of all other running VMs. Using zero disables auto-ballooning. Auto-ballooning is done by pvestatd.')
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')
    smbios1: str | None = Field(None, description='Specify SMBIOS type 1 fields.')
    smp: int | None = Field(None, description='The number of CPUs. Please use option -sockets instead.')
    sockets: int | None = Field(None, description='The number of CPU sockets.')
    spice_enhancements: str | None = Field(None, description='Configure additional enhancements for SPICE.')
    sshkeys: str | None = Field(None, description='cloud-init: Setup public SSH keys (one key per line, OpenSSH format).')
    startdate: str | None = Field(None, description="Set the initial date of the real time clock. Valid format for date are:'now' or '2006-06-17T16:01:21' or '2006-06-17'.")
    startup: str | None = Field(None, description="Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the 'up' or 'down' delay in seconds, which specifies a delay to wait before the next VM is started or stopped.")
    tablet: bool | None = Field(None, description='Enable/disable the USB tablet device.')
    tags: str | None = Field(None, description='Tags of the VM. This is only meta information.')
    tdf: bool | None = Field(None, description='Enable/disable time drift fix.')
    template: bool | None = Field(None, description='Enable/disable Template.')
    tpmstate0: str | None = Field(None, description="Configure a Disk for storing TPM state. The format is fixed to 'raw'. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and 4 MiB will be used instead. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    unused_n: str | None = Field(None, alias="unused[n]", description='Reference to unused volumes. This is used internally, and should not be modified manually.')
    usb_n: str | None = Field(None, alias="usb[n]", description='Configure an USB device (n is 0 to 4, for machine version >= 7.1 and ostype l26 or windows > 7, n can be up to 14).')
    vcpus: int | None = Field(None, description='Number of hotplugged vcpus.')
    vga: str | None = Field(None, description='Configure the VGA hardware.')
    virtio_n: str | None = Field(None, alias="virtio[n]", description="Use volume as VIRTIO hard disk (n is 0 to 15). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    virtiofs_n: str | None = Field(None, alias="virtiofs[n]", description='Configuration for sharing a directory between host and guest using Virtio-fs.')
    vmgenid: str | None = Field(None, description="Set VM Generation ID. Use '1' to autogenerate on create or update, pass '0' to disable explicitly.")
    vmstatestorage: str | None = Field(None, description='Default storage for VM state volumes/files.')
    watchdog: str | None = Field(None, description='Create a virtual hardware watchdog device.')

class PostNodesNodeQemuVmidConfigResponse(RootModel[str]):
    root: str = Field(...)

class PutNodesNodeQemuVmidConfigRequest(ProxmoxBaseModel):
    acpi: bool | None = Field(None, description='Enable/disable ACPI.')
    affinity: str | None = Field(None, description='List of host cores used to execute guest processes, for example: 0,5,8-11')
    agent: str | None = Field(None, description='Enable/disable communication with the QEMU Guest Agent and its properties.')
    allow_ksm: bool | None = Field(None, alias="allow-ksm", description='Allow memory pages of this guest to be merged via KSM (Kernel Samepage Merging).')
    amd_sev: str | None = Field(None, alias="amd-sev", description='Secure Encrypted Virtualization (SEV) features by AMD CPUs')
    arch: str | None = Field(None, description='Virtual processor architecture. Defaults to the host.')
    args: str | None = Field(None, description='Arbitrary arguments passed to kvm.')
    audio0: str | None = Field(None, description='Configure a audio device, useful in combination with QXL/Spice.')
    autostart: bool | None = Field(None, description='Automatic restart after crash (currently ignored).')
    balloon: int | None = Field(None, description='Amount of target RAM for the VM in MiB. Using zero disables the ballon driver.')
    bios: str | None = Field(None, description='Select BIOS implementation.')
    boot: str | None = Field(None, description="Specify guest boot order. Use the 'order=' sub-property as usage with no key or 'legacy=' is deprecated.")
    bootdisk: str | None = Field(None, description="Enable booting from specified disk. Deprecated: Use 'boot: order=foo;bar' instead.")
    cdrom: str | None = Field(None, description='This is an alias for option -ide2')
    cicustom: str | None = Field(None, description='cloud-init: Specify custom files to replace the automatically generated ones at start.')
    cipassword: str | None = Field(None, description='cloud-init: Password to assign the user. Using this is generally not recommended. Use ssh keys instead. Also note that older cloud-init versions do not support hashed passwords.')
    citype: str | None = Field(None, description='Specifies the cloud-init configuration format. The default depends on the configured operating system type (`ostype`. We use the `nocloud` format for Linux, and `configdrive2` for windows.')
    ciupgrade: bool | None = Field(None, description='cloud-init: do an automatic package upgrade after the first boot.')
    ciuser: str | None = Field(None, description="cloud-init: User name to change ssh keys and password for instead of the image's configured default user.")
    cores: int | None = Field(None, description='The number of cores per socket.')
    cpu: str | None = Field(None, description='Emulated CPU type.')
    cpulimit: float | None = Field(None, description='Limit of CPU usage.')
    cpuunits: int | None = Field(None, description='CPU weight for a VM, will be clamped to [1, 10000] in cgroup v2.')
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    description: str | None = Field(None, description="Description for the VM. Shown in the web-interface VM's summary. This is saved as comment inside the configuration file.")
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.')
    efidisk0: str | None = Field(None, description="Configure a disk for storing EFI vars. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and that the default EFI vars are copied to the volume instead. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    force: bool | None = Field(None, description="Force physical removal. Without this, we simple remove the disk from the config file and create an additional configuration entry called 'unused[n]', which contains the volume ID. Unlink of unused[n] always cause physical removal.")
    freeze: bool | None = Field(None, description="Freeze CPU at startup (use 'c' monitor command to start execution).")
    hookscript: str | None = Field(None, description='Script that will be executed during various steps in the vms lifetime.')
    hostpci_n: str | None = Field(None, alias="hostpci[n]", description='Map host PCI devices into guest.')
    hotplug: str | None = Field(None, description="Selectively enable hotplug features. This is a comma separated list of hotplug features: 'network', 'disk', 'cpu', 'memory', 'usb' and 'cloudinit'. Use '0' to disable hotplug completely. Using '1' as value is an alias for the default `network,disk,usb`. USB hotplugging is possible for guests with machine version >= 7.1 and ostype l26 or windows > 7.")
    hugepages: str | None = Field(None, description="Enables hugepages memory.\n\nSets the size of hugepages in MiB. If the value is set to 'any' then 1 GiB hugepages will be used if possible, otherwise the size will fall back to 2 MiB.")
    ide_n: str | None = Field(None, alias="ide[n]", description="Use volume as IDE hard disk or CD-ROM (n is 0 to 3). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    intel_tdx: str | None = Field(None, alias="intel-tdx", description='Trusted Domain Extension (TDX) features by Intel CPUs')
    ipconfig_n: str | None = Field(None, alias="ipconfig[n]", description="cloud-init: Specify IP addresses and gateways for the corresponding interface.\n\nIP addresses use CIDR notation, gateways are optional but need an IP of the same type specified.\n\nThe special string 'dhcp' can be used for IP addresses to use DHCP, in which case no explicit\ngateway should be provided.\nFor IPv6 the special string 'auto' can be used to use stateless autoconfiguration. This requires\ncloud-init 19.4 or newer.\n\nIf cloud-init is enabled and neither an IPv4 nor an IPv6 address is specified, it defaults to using\ndhcp on IPv4.\n")
    ivshmem: str | None = Field(None, description='Inter-VM shared memory. Useful for direct communication between VMs, or to the host.')
    keephugepages: bool | None = Field(None, description='Use together with hugepages. If enabled, hugepages will not not be deleted after VM shutdown and can be used for subsequent starts.')
    keyboard: str | None = Field(None, description='Keyboard layout for VNC server. This option is generally not required and is often better handled from within the guest OS.')
    kvm: bool | None = Field(None, description='Enable/disable KVM hardware virtualization.')
    localtime: bool | None = Field(None, description='Set the real time clock (RTC) to local time. This is enabled by default if the `ostype` indicates a Microsoft Windows OS.')
    lock: str | None = Field(None, description='Lock/unlock the VM.')
    machine: str | None = Field(None, description='Specify the QEMU machine.')
    memory: str | None = Field(None, description='Memory properties.')
    migrate_downtime: float | None = Field(None, description='Set maximum tolerated downtime (in seconds) for migrations. Should the migration not be able to converge in the very end, because too much newly dirtied RAM needs to be transferred, the limit will be increased automatically step-by-step until migration can converge.')
    migrate_speed: int | None = Field(None, description='Set maximum speed (in MB/s) for migrations. Value 0 is no limit.')
    name: str | None = Field(None, description='Set a name for the VM. Only used on the configuration web interface.')
    nameserver: str | None = Field(None, description='cloud-init: Sets DNS server IP address for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.')
    net_n: str | None = Field(None, alias="net[n]", description='Specify network devices.')
    numa: bool | None = Field(None, description='Enable/disable NUMA.')
    numa_n: str | None = Field(None, alias="numa[n]", description='NUMA topology.')
    onboot: bool | None = Field(None, description='Specifies whether a VM will be started during system bootup.')
    ostype: str | None = Field(None, description='Specify guest operating system.')
    parallel_n: str | None = Field(None, alias="parallel[n]", description='Map host parallel devices (n is 0 to 2).')
    protection: bool | None = Field(None, description='Sets the protection flag of the VM. This will disable the remove VM and remove disk operations.')
    reboot: bool | None = Field(None, description="Allow reboot. If set to '0' the VM exit on reboot.")
    revert: str | None = Field(None, description='Revert a pending change.')
    rng0: str | None = Field(None, description='Configure a VirtIO-based Random Number Generator.')
    sata_n: str | None = Field(None, alias="sata[n]", description="Use volume as SATA hard disk or CD-ROM (n is 0 to 5). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    scsi_n: str | None = Field(None, alias="scsi[n]", description="Use volume as SCSI hard disk or CD-ROM (n is 0 to 30). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    scsihw: str | None = Field(None, description='SCSI controller model')
    searchdomain: str | None = Field(None, description='cloud-init: Sets DNS search domains for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.')
    serial_n: str | None = Field(None, alias="serial[n]", description='Create a serial device inside the VM (n is 0 to 3)')
    shares: int | None = Field(None, description='Amount of memory shares for auto-ballooning. The larger the number is, the more memory this VM gets. Number is relative to weights of all other running VMs. Using zero disables auto-ballooning. Auto-ballooning is done by pvestatd.')
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')
    smbios1: str | None = Field(None, description='Specify SMBIOS type 1 fields.')
    smp: int | None = Field(None, description='The number of CPUs. Please use option -sockets instead.')
    sockets: int | None = Field(None, description='The number of CPU sockets.')
    spice_enhancements: str | None = Field(None, description='Configure additional enhancements for SPICE.')
    sshkeys: str | None = Field(None, description='cloud-init: Setup public SSH keys (one key per line, OpenSSH format).')
    startdate: str | None = Field(None, description="Set the initial date of the real time clock. Valid format for date are:'now' or '2006-06-17T16:01:21' or '2006-06-17'.")
    startup: str | None = Field(None, description="Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the 'up' or 'down' delay in seconds, which specifies a delay to wait before the next VM is started or stopped.")
    tablet: bool | None = Field(None, description='Enable/disable the USB tablet device.')
    tags: str | None = Field(None, description='Tags of the VM. This is only meta information.')
    tdf: bool | None = Field(None, description='Enable/disable time drift fix.')
    template: bool | None = Field(None, description='Enable/disable Template.')
    tpmstate0: str | None = Field(None, description="Configure a Disk for storing TPM state. The format is fixed to 'raw'. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and 4 MiB will be used instead. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    unused_n: str | None = Field(None, alias="unused[n]", description='Reference to unused volumes. This is used internally, and should not be modified manually.')
    usb_n: str | None = Field(None, alias="usb[n]", description='Configure an USB device (n is 0 to 4, for machine version >= 7.1 and ostype l26 or windows > 7, n can be up to 14).')
    vcpus: int | None = Field(None, description='Number of hotplugged vcpus.')
    vga: str | None = Field(None, description='Configure the VGA hardware.')
    virtio_n: str | None = Field(None, alias="virtio[n]", description="Use volume as VIRTIO hard disk (n is 0 to 15). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    virtiofs_n: str | None = Field(None, alias="virtiofs[n]", description='Configuration for sharing a directory between host and guest using Virtio-fs.')
    vmgenid: str | None = Field(None, description="Set VM Generation ID. Use '1' to autogenerate on create or update, pass '0' to disable explicitly.")
    vmstatestorage: str | None = Field(None, description='Default storage for VM state volumes/files.')
    watchdog: str | None = Field(None, description='Create a virtual hardware watchdog device.')

class PutNodesNodeQemuVmidConfigResponse(RootModel[None]):
    root: None = Field(...)

class PostNodesNodeQemuVmidDbusVmstateRequest(ProxmoxBaseModel):
    action: str = Field(..., description='Action to perform on the DBus VMState helper.')

class PostNodesNodeQemuVmidDbusVmstateResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeQemuVmidFeatureResponse(ProxmoxBaseModel):
    has_feature: bool = Field(..., alias="hasFeature")
    nodes: list[str] = Field(...)

class GetNodesNodeQemuVmidFirewallResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeQemuVmidFirewallAliasesResponseItem(ProxmoxBaseModel):
    cidr: str | None = Field(None)
    comment: str | None = Field(None)
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    name: str | None = Field(None)

class GetNodesNodeQemuVmidFirewallAliasesResponse(RootModel[list[GetNodesNodeQemuVmidFirewallAliasesResponseItem]]):
    root: list[GetNodesNodeQemuVmidFirewallAliasesResponseItem] = Field(...)

class PostNodesNodeQemuVmidFirewallAliasesRequest(ProxmoxBaseModel):
    cidr: str = Field(..., description='Network/IP specification in CIDR format.')
    comment: str | None = Field(None)
    name: str = Field(..., description='Alias name.')

class PostNodesNodeQemuVmidFirewallAliasesResponse(RootModel[None]):
    root: None = Field(...)

class DeleteNodesNodeQemuVmidFirewallAliasesNameRequest(ProxmoxBaseModel):
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteNodesNodeQemuVmidFirewallAliasesNameResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeQemuVmidFirewallAliasesNameResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PutNodesNodeQemuVmidFirewallAliasesNameRequest(ProxmoxBaseModel):
    cidr: str = Field(..., description='Network/IP specification in CIDR format.')
    comment: str | None = Field(None)
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    rename: str | None = Field(None, description='Rename an existing alias.')

class PutNodesNodeQemuVmidFirewallAliasesNameResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeQemuVmidFirewallIpsetResponseItem(ProxmoxBaseModel):
    comment: str | None = Field(None)
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    name: str | None = Field(None, description='IP set name.')

class GetNodesNodeQemuVmidFirewallIpsetResponse(RootModel[list[GetNodesNodeQemuVmidFirewallIpsetResponseItem]]):
    root: list[GetNodesNodeQemuVmidFirewallIpsetResponseItem] = Field(...)

class PostNodesNodeQemuVmidFirewallIpsetRequest(ProxmoxBaseModel):
    comment: str | None = Field(None)
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    name: str = Field(..., description='IP set name.')
    rename: str | None = Field(None, description="Rename an existing IPSet. You can set 'rename' to the same value as 'name' to update the 'comment' of an existing IPSet.")

class PostNodesNodeQemuVmidFirewallIpsetResponse(RootModel[None]):
    root: None = Field(...)

class DeleteNodesNodeQemuVmidFirewallIpsetNameRequest(ProxmoxBaseModel):
    force: bool | None = Field(None, description='Delete all members of the IPSet, if there are any.')

class DeleteNodesNodeQemuVmidFirewallIpsetNameResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeQemuVmidFirewallIpsetNameResponseItem(ProxmoxBaseModel):
    cidr: str | None = Field(None)
    comment: str | None = Field(None)
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    nomatch: bool | None = Field(None)

class GetNodesNodeQemuVmidFirewallIpsetNameResponse(RootModel[list[GetNodesNodeQemuVmidFirewallIpsetNameResponseItem]]):
    root: list[GetNodesNodeQemuVmidFirewallIpsetNameResponseItem] = Field(...)

class PostNodesNodeQemuVmidFirewallIpsetNameRequest(ProxmoxBaseModel):
    cidr: str = Field(..., description='Network/IP specification in CIDR format.')
    comment: str | None = Field(None)
    nomatch: bool | None = Field(None)

class PostNodesNodeQemuVmidFirewallIpsetNameResponse(RootModel[None]):
    root: None = Field(...)

class DeleteNodesNodeQemuVmidFirewallIpsetNameCidrRequest(ProxmoxBaseModel):
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteNodesNodeQemuVmidFirewallIpsetNameCidrResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeQemuVmidFirewallIpsetNameCidrResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PutNodesNodeQemuVmidFirewallIpsetNameCidrRequest(ProxmoxBaseModel):
    comment: str | None = Field(None)
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    nomatch: bool | None = Field(None)

class PutNodesNodeQemuVmidFirewallIpsetNameCidrResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeQemuVmidFirewallLogResponseItem(ProxmoxBaseModel):
    n: int | None = Field(None, description='Line number')
    t: str | None = Field(None, description='Line text')

class GetNodesNodeQemuVmidFirewallLogResponse(RootModel[list[GetNodesNodeQemuVmidFirewallLogResponseItem]]):
    root: list[GetNodesNodeQemuVmidFirewallLogResponseItem] = Field(...)

class GetNodesNodeQemuVmidFirewallOptionsResponse(ProxmoxBaseModel):
    dhcp: bool | None = Field(None, description='Enable DHCP.')
    enable: bool | None = Field(None, description='Enable/disable firewall rules.')
    ipfilter: bool | None = Field(None, description="Enable default IP filters. This is equivalent to adding an empty ipfilter-net<id> ipset for every interface. Such ipsets implicitly contain sane default restrictions such as restricting IPv6 link local addresses to the one derived from the interface's MAC address. For containers the configured IP addresses will be implicitly added.")
    log_level_in: str | None = Field(None, description='Log level for incoming traffic.')
    log_level_out: str | None = Field(None, description='Log level for outgoing traffic.')
    macfilter: bool | None = Field(None, description='Enable/disable MAC address filter.')
    ndp: bool | None = Field(None, description='Enable NDP (Neighbor Discovery Protocol).')
    policy_in: str | None = Field(None, description='Input policy.')
    policy_out: str | None = Field(None, description='Output policy.')
    radv: bool | None = Field(None, description='Allow sending Router Advertisement.')

class PutNodesNodeQemuVmidFirewallOptionsRequest(ProxmoxBaseModel):
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    dhcp: bool | None = Field(None, description='Enable DHCP.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    enable: bool | None = Field(None, description='Enable/disable firewall rules.')
    ipfilter: bool | None = Field(None, description="Enable default IP filters. This is equivalent to adding an empty ipfilter-net<id> ipset for every interface. Such ipsets implicitly contain sane default restrictions such as restricting IPv6 link local addresses to the one derived from the interface's MAC address. For containers the configured IP addresses will be implicitly added.")
    log_level_in: str | None = Field(None, description='Log level for incoming traffic.')
    log_level_out: str | None = Field(None, description='Log level for outgoing traffic.')
    macfilter: bool | None = Field(None, description='Enable/disable MAC address filter.')
    ndp: bool | None = Field(None, description='Enable NDP (Neighbor Discovery Protocol).')
    policy_in: str | None = Field(None, description='Input policy.')
    policy_out: str | None = Field(None, description='Output policy.')
    radv: bool | None = Field(None, description='Allow sending Router Advertisement.')

class PutNodesNodeQemuVmidFirewallOptionsResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeQemuVmidFirewallRefsResponseItem(ProxmoxBaseModel):
    comment: str | None = Field(None)
    name: str | None = Field(None)
    ref: str | None = Field(None)
    scope: str | None = Field(None)
    type: str | None = Field(None)

class GetNodesNodeQemuVmidFirewallRefsResponse(RootModel[list[GetNodesNodeQemuVmidFirewallRefsResponseItem]]):
    root: list[GetNodesNodeQemuVmidFirewallRefsResponseItem] = Field(...)

class GetNodesNodeQemuVmidFirewallRulesResponseItem(ProxmoxBaseModel):
    action: str | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: str | None = Field(None, description='Descriptive comment')
    dest: str | None = Field(None, description='Restrict packet destination address')
    dport: str | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: str | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: str | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: str | None = Field(None, description='Log level for firewall rule')
    macro: str | None = Field(None, description='Use predefined standard macro')
    pos: int | None = Field(None, description='Rule position in the ruleset')
    proto: str | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: str | None = Field(None, description='Restrict packet source address')
    sport: str | None = Field(None, description='Restrict TCP/UDP source port')
    type: str | None = Field(None, description='Rule type')

class GetNodesNodeQemuVmidFirewallRulesResponse(RootModel[list[GetNodesNodeQemuVmidFirewallRulesResponseItem]]):
    root: list[GetNodesNodeQemuVmidFirewallRulesResponseItem] = Field(...)

class PostNodesNodeQemuVmidFirewallRulesRequest(ProxmoxBaseModel):
    action: str = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: str | None = Field(None, description='Descriptive comment.')
    dest: str | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: str | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: str | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: str | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: str | None = Field(None, description='Log level for firewall rule.')
    macro: str | None = Field(None, description='Use predefined standard macro.')
    pos: int | None = Field(None, description='Update rule at position <pos>.')
    proto: str | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: str | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: str | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: str = Field(..., description='Rule type.')

class PostNodesNodeQemuVmidFirewallRulesResponse(RootModel[None]):
    root: None = Field(...)

class DeleteNodesNodeQemuVmidFirewallRulesPosRequest(ProxmoxBaseModel):
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteNodesNodeQemuVmidFirewallRulesPosResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeQemuVmidFirewallRulesPosResponse(ProxmoxBaseModel):
    action: str = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: str | None = Field(None, description='Descriptive comment')
    dest: str | None = Field(None, description='Restrict packet destination address')
    dport: str | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: str | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: str | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: str | None = Field(None, description='Log level for firewall rule')
    macro: str | None = Field(None, description='Use predefined standard macro')
    pos: int = Field(..., description='Rule position in the ruleset')
    proto: str | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: str | None = Field(None, description='Restrict packet source address')
    sport: str | None = Field(None, description='Restrict TCP/UDP source port')
    type: str = Field(..., description='Rule type')

class PutNodesNodeQemuVmidFirewallRulesPosRequest(ProxmoxBaseModel):
    action: str | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: str | None = Field(None, description='Descriptive comment.')
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    dest: str | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: str | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: str | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: str | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: str | None = Field(None, description='Log level for firewall rule.')
    macro: str | None = Field(None, description='Use predefined standard macro.')
    moveto: int | None = Field(None, description='Move rule to new position <moveto>. Other arguments are ignored.')
    proto: str | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: str | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: str | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: str | None = Field(None, description='Rule type.')

class PutNodesNodeQemuVmidFirewallRulesPosResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeQemuVmidMigrateResponse(ProxmoxBaseModel):
    allowed_nodes: list[str] | None = Field(None, description='List of nodes allowed for migration.')
    dependent_ha_resources: list[str] | None = Field(None, alias="dependent-ha-resources", description='HA resources, which will be migrated to the same target node as the VM, because these are in positive affinity with the VM.')
    has_dbus_vmstate: bool = Field(..., alias="has-dbus-vmstate", description='Whether the VM host supports migrating additional VM state, such as conntrack entries.')
    local_disks: list[dict[str, object]] = Field(..., description='List local disks including CD-Rom, unused and not referenced disks')
    local_resources: list[str] = Field(..., description='List local resources (e.g. pci, usb) that block migration.')
    mapped_resource_info: dict[str, object] = Field(..., alias="mapped-resource-info", description="Object of mapped resources with additional information such if they're live migratable.")
    mapped_resources: list[str] = Field(..., alias="mapped-resources", description="List of mapped resources e.g. pci, usb. Deprecated, use 'mapped-resource-info' instead.")
    not_allowed_nodes: dict[str, object] | None = Field(None, description='List of not allowed nodes with additional information.')
    running: bool = Field(..., description='Determines if the VM is running.')

class PostNodesNodeQemuVmidMigrateRequest(ProxmoxBaseModel):
    bwlimit: int | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    force: bool | None = Field(None, description='Allow to migrate VMs which use local devices. Only root may use this option.')
    migration_network: str | None = Field(None, description='CIDR of the (sub) network that is used for migration.')
    migration_type: str | None = Field(None, description='Migration traffic is encrypted using an SSH tunnel by default. On secure, completely private networks this can be disabled to increase performance.')
    online: bool | None = Field(None, description='Use online/live migration if VM is running. Ignored if VM is stopped.')
    target: str = Field(..., description='Target node.')
    targetstorage: str | None = Field(None, description="Mapping from source to target storages. Providing only a single storage ID maps all source storages to that storage. Providing the special value '1' will map each source storage to itself.")
    with_conntrack_state: bool | None = Field(None, alias="with-conntrack-state", description='Whether to migrate conntrack entries for running VMs.')
    with_local_disks: bool | None = Field(None, alias="with-local-disks", description='Enable live storage migration for local disk')

class PostNodesNodeQemuVmidMigrateResponse(RootModel[str]):
    root: str = Field(..., description='the task ID.')

class PostNodesNodeQemuVmidMonitorRequest(ProxmoxBaseModel):
    command: str = Field(..., description='The monitor command.')

class PostNodesNodeQemuVmidMonitorResponse(RootModel[str]):
    root: str = Field(...)

class PostNodesNodeQemuVmidMoveDiskRequest(ProxmoxBaseModel):
    bwlimit: int | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    delete: bool | None = Field(None, description='Delete the original disk after successful copy. By default the original disk is kept as unused disk.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.')
    disk: str = Field(..., description='The disk you want to move.')
    format: str | None = Field(None, description='Target Format.')
    storage: str | None = Field(None, description='Target storage.')
    target_digest: str | None = Field(None, alias="target-digest", description='Prevent changes if the current config file of the target VM has a different SHA1 digest. This can be used to detect concurrent modifications.')
    target_disk: str | None = Field(None, alias="target-disk", description='The config key the disk will be moved to on the target VM (for example, ide0 or scsi1). Default is the source disk key.')
    target_vmid: int | None = Field(None, alias="target-vmid", description='The (unique) ID of the VM.')

class PostNodesNodeQemuVmidMoveDiskResponse(RootModel[str]):
    root: str = Field(..., description='the task ID.')

class PostNodesNodeQemuVmidMtunnelRequest(ProxmoxBaseModel):
    bridges: str | None = Field(None, description='List of network bridges to check availability. Will be checked again for actually used bridges during migration.')
    storages: str | None = Field(None, description='List of storages to check permission and availability. Will be checked again for all actually used storages during migration.')

class PostNodesNodeQemuVmidMtunnelResponse(ProxmoxBaseModel):
    socket: str = Field(...)
    ticket: str = Field(...)
    upid: str = Field(...)

class GetNodesNodeQemuVmidMtunnelwebsocketResponse(ProxmoxBaseModel):
    port: str | None = Field(None)
    socket: str | None = Field(None)

class GetNodesNodeQemuVmidPendingResponseItem(ProxmoxBaseModel):
    delete: int | None = Field(None, description='Indicates a pending delete request if present and not 0. The value 2 indicates a force-delete request.')
    key: str | None = Field(None, description='Configuration option name.')
    pending: str | None = Field(None, description='Pending value.')
    value: str | None = Field(None, description='Current value.')

class GetNodesNodeQemuVmidPendingResponse(RootModel[list[GetNodesNodeQemuVmidPendingResponseItem]]):
    root: list[GetNodesNodeQemuVmidPendingResponseItem] = Field(...)

class PostNodesNodeQemuVmidRemoteMigrateRequest(ProxmoxBaseModel):
    bwlimit: int | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    delete: bool | None = Field(None, description='Delete the original VM and related data after successful migration. By default the original VM is kept on the source cluster in a stopped state.')
    online: bool | None = Field(None, description='Use online/live migration if VM is running. Ignored if VM is stopped.')
    target_bridge: str = Field(..., alias="target-bridge", description="Mapping from source to target bridges. Providing only a single bridge ID maps all source bridges to that bridge. Providing the special value '1' will map each source bridge to itself.")
    target_endpoint: str = Field(..., alias="target-endpoint", description='Remote target endpoint')
    target_storage: str = Field(..., alias="target-storage", description="Mapping from source to target storages. Providing only a single storage ID maps all source storages to that storage. Providing the special value '1' will map each source storage to itself.")
    target_vmid: int | None = Field(None, alias="target-vmid", description='The (unique) ID of the VM.')

class PostNodesNodeQemuVmidRemoteMigrateResponse(RootModel[str]):
    root: str = Field(..., description='the task ID.')

class PutNodesNodeQemuVmidResizeRequest(ProxmoxBaseModel):
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.')
    disk: str = Field(..., description='The disk you want to resize.')
    size: str = Field(..., description='The new size. With the `+` sign the value is added to the actual size of the volume and without it, the value is taken as an absolute one. Shrinking disk size is not supported.')
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')

class PutNodesNodeQemuVmidResizeResponse(RootModel[str]):
    root: str = Field(..., description='the task ID.')

class GetNodesNodeQemuVmidRrdResponse(ProxmoxBaseModel):
    filename: str = Field(...)

class GetNodesNodeQemuVmidRrddataResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class PutNodesNodeQemuVmidSendkeyRequest(ProxmoxBaseModel):
    key: str = Field(..., description='The key (qemu monitor encoding).')
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')

class PutNodesNodeQemuVmidSendkeyResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeQemuVmidSnapshotResponseItem(ProxmoxBaseModel):
    description: str | None = Field(None, description='Snapshot description.')
    name: str | None = Field(None, description="Snapshot identifier. Value 'current' identifies the current VM.")
    parent: str | None = Field(None, description='Parent snapshot identifier.')
    snaptime: int | None = Field(None, description='Snapshot creation time')
    vmstate: bool | None = Field(None, description='Snapshot includes RAM.')

class GetNodesNodeQemuVmidSnapshotResponse(RootModel[list[GetNodesNodeQemuVmidSnapshotResponseItem]]):
    root: list[GetNodesNodeQemuVmidSnapshotResponseItem] = Field(...)

class PostNodesNodeQemuVmidSnapshotRequest(ProxmoxBaseModel):
    description: str | None = Field(None, description='A textual description or comment.')
    snapname: str = Field(..., description='The name of the snapshot.')
    vmstate: bool | None = Field(None, description='Save the vmstate')

class PostNodesNodeQemuVmidSnapshotResponse(RootModel[str]):
    root: str = Field(..., description='the task ID.')

class DeleteNodesNodeQemuVmidSnapshotSnapnameRequest(ProxmoxBaseModel):
    force: bool | None = Field(None, description='For removal from config file, even if removing disk snapshots fails.')

class DeleteNodesNodeQemuVmidSnapshotSnapnameResponse(RootModel[str]):
    root: str = Field(..., description='the task ID.')

class GetNodesNodeQemuVmidSnapshotSnapnameResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeQemuVmidSnapshotSnapnameConfigResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PutNodesNodeQemuVmidSnapshotSnapnameConfigRequest(ProxmoxBaseModel):
    description: str | None = Field(None, description='A textual description or comment.')

class PutNodesNodeQemuVmidSnapshotSnapnameConfigResponse(RootModel[None]):
    root: None = Field(...)

class PostNodesNodeQemuVmidSnapshotSnapnameRollbackRequest(ProxmoxBaseModel):
    start: bool | None = Field(None, description='Whether the VM should get started after rolling back successfully. (Note: VMs will be automatically started if the snapshot includes RAM.)')

class PostNodesNodeQemuVmidSnapshotSnapnameRollbackResponse(RootModel[str]):
    root: str = Field(..., description='the task ID.')

class PostNodesNodeQemuVmidSpiceproxyRequest(ProxmoxBaseModel):
    proxy: str | None = Field(None, description="SPICE proxy server. This can be used by the client to specify the proxy server. All nodes in a cluster runs 'spiceproxy', so it is up to the client to choose one. By default, we return the node where the VM is currently running. As reasonable setting is to use same node you use to connect to the API (This is window.location.hostname for the JS GUI).")

class PostNodesNodeQemuVmidSpiceproxyResponse(ProxmoxBaseModel):
    host: str = Field(...)
    password: str = Field(...)
    proxy: str = Field(...)
    tls_port: int = Field(..., alias="tls-port")
    type: str = Field(...)

class GetNodesNodeQemuVmidStatusResponseItem(ProxmoxBaseModel):
    subdir: str | None = Field(None)

class GetNodesNodeQemuVmidStatusResponse(RootModel[list[GetNodesNodeQemuVmidStatusResponseItem]]):
    root: list[GetNodesNodeQemuVmidStatusResponseItem] = Field(...)

class GetNodesNodeQemuVmidStatusCurrentResponse(ProxmoxBaseModel):
    agent: bool | None = Field(None, description='QEMU Guest Agent is enabled in config.')
    clipboard: str | None = Field(None, description='Enable a specific clipboard. If not set, depending on the display type the SPICE one will be added.')
    cpu: float | None = Field(None, description='Current CPU usage.')
    cpus: float | None = Field(None, description='Maximum usable CPUs.')
    diskread: int | None = Field(None, description="The amount of bytes the guest read from it's block devices since the guest was started. (Note: This info is not available for all storage types.)")
    diskwrite: int | None = Field(None, description="The amount of bytes the guest wrote from it's block devices since the guest was started. (Note: This info is not available for all storage types.)")
    ha: dict[str, object] = Field(..., description='HA manager service status.')
    lock: str | None = Field(None, description='The current config lock, if any.')
    maxdisk: int | None = Field(None, description='Root disk size in bytes.')
    maxmem: int | None = Field(None, description='Maximum memory in bytes.')
    mem: int | None = Field(None, description='Currently used memory in bytes.')
    memhost: int | None = Field(None, description='Current memory usage on the host.')
    name: str | None = Field(None, description='VM (host)name.')
    netin: int | None = Field(None, description='The amount of traffic in bytes that was sent to the guest over the network since it was started.')
    netout: int | None = Field(None, description='The amount of traffic in bytes that was sent from the guest over the network since it was started.')
    pid: int | None = Field(None, description='PID of the QEMU process, if the VM is running.')
    pressurecpufull: float | None = Field(None, description='CPU Full pressure stall average over the last 10 seconds.')
    pressurecpusome: float | None = Field(None, description='CPU Some pressure stall average over the last 10 seconds.')
    pressureiofull: float | None = Field(None, description='IO Full pressure stall average over the last 10 seconds.')
    pressureiosome: float | None = Field(None, description='IO Some pressure stall average over the last 10 seconds.')
    pressurememoryfull: float | None = Field(None, description='Memory Full pressure stall average over the last 10 seconds.')
    pressurememorysome: float | None = Field(None, description='Memory Some pressure stall average over the last 10 seconds.')
    qmpstatus: str | None = Field(None, description="VM run state from the 'query-status' QMP monitor command.")
    running_machine: str | None = Field(None, alias="running-machine", description='The currently running machine type (if running).')
    running_qemu: str | None = Field(None, alias="running-qemu", description='The QEMU version the VM is currently using (if running).')
    serial: bool | None = Field(None, description='Guest has serial device configured.')
    spice: bool | None = Field(None, description='QEMU VGA configuration supports spice.')
    status: str = Field(..., description='QEMU process status.')
    tags: str | None = Field(None, description='The current configured tags, if any')
    template: bool | None = Field(None, description='Determines if the guest is a template.')
    uptime: int | None = Field(None, description='Uptime in seconds.')
    vmid: int = Field(..., description='The (unique) ID of the VM.')

class PostNodesNodeQemuVmidStatusRebootRequest(ProxmoxBaseModel):
    timeout: int | None = Field(None, description='Wait maximal timeout seconds for the shutdown.')

class PostNodesNodeQemuVmidStatusRebootResponse(RootModel[str]):
    root: str = Field(...)

class PostNodesNodeQemuVmidStatusResetRequest(ProxmoxBaseModel):
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')

class PostNodesNodeQemuVmidStatusResetResponse(RootModel[str]):
    root: str = Field(...)

class PostNodesNodeQemuVmidStatusResumeRequest(ProxmoxBaseModel):
    nocheck: bool | None = Field(None)
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')

class PostNodesNodeQemuVmidStatusResumeResponse(RootModel[str]):
    root: str = Field(...)

class PostNodesNodeQemuVmidStatusShutdownRequest(ProxmoxBaseModel):
    force_stop: bool | None = Field(None, alias="forceStop", description='Make sure the VM stops.')
    keep_active: bool | None = Field(None, alias="keepActive", description='Do not deactivate storage volumes.')
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')
    timeout: int | None = Field(None, description='Wait maximal timeout seconds.')

class PostNodesNodeQemuVmidStatusShutdownResponse(RootModel[str]):
    root: str = Field(...)

class PostNodesNodeQemuVmidStatusStartRequest(ProxmoxBaseModel):
    force_cpu: str | None = Field(None, alias="force-cpu", description="Override QEMU's -cpu argument with the given string.")
    machine: str | None = Field(None, description='Specify the QEMU machine.')
    migratedfrom: str | None = Field(None, description='The cluster node name.')
    migration_network: str | None = Field(None, description='CIDR of the (sub) network that is used for migration.')
    migration_type: str | None = Field(None, description='Migration traffic is encrypted using an SSH tunnel by default. On secure, completely private networks this can be disabled to increase performance.')
    nets_host_mtu: str | None = Field(None, alias="nets-host-mtu", description='Used for migration compat. List of VirtIO network devices and their effective host_mtu setting according to the QEMU object model on the source side of the migration. A value of 0 means that the host_mtu parameter is to be avoided for the corresponding device.')
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')
    stateuri: str | None = Field(None, description='Some command save/restore state from this location.')
    targetstorage: str | None = Field(None, description="Mapping from source to target storages. Providing only a single storage ID maps all source storages to that storage. Providing the special value '1' will map each source storage to itself.")
    timeout: int | None = Field(None, description='Wait maximal timeout seconds.')
    with_conntrack_state: bool | None = Field(None, alias="with-conntrack-state", description='Whether to migrate conntrack entries for running VMs.')

class PostNodesNodeQemuVmidStatusStartResponse(RootModel[str]):
    root: str = Field(...)

class PostNodesNodeQemuVmidStatusStopRequest(ProxmoxBaseModel):
    keep_active: bool | None = Field(None, alias="keepActive", description='Do not deactivate storage volumes.')
    migratedfrom: str | None = Field(None, description='The cluster node name.')
    overrule_shutdown: bool | None = Field(None, alias="overrule-shutdown", description="Try to abort active 'qmshutdown' tasks before stopping.")
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')
    timeout: int | None = Field(None, description='Wait maximal timeout seconds.')

class PostNodesNodeQemuVmidStatusStopResponse(RootModel[str]):
    root: str = Field(...)

class PostNodesNodeQemuVmidStatusSuspendRequest(ProxmoxBaseModel):
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')
    statestorage: str | None = Field(None, description='The storage for the VM state')
    todisk: bool | None = Field(None, description='If set, suspends the VM to disk. Will be resumed on next VM start.')

class PostNodesNodeQemuVmidStatusSuspendResponse(RootModel[str]):
    root: str = Field(...)

class PostNodesNodeQemuVmidTemplateRequest(ProxmoxBaseModel):
    disk: str | None = Field(None, description='If you want to convert only 1 disk to base image.')

class PostNodesNodeQemuVmidTemplateResponse(RootModel[str]):
    root: str = Field(..., description='the task ID.')

class PostNodesNodeQemuVmidTermproxyRequest(ProxmoxBaseModel):
    serial: str | None = Field(None, description='opens a serial terminal (defaults to display)')

class PostNodesNodeQemuVmidTermproxyResponse(ProxmoxBaseModel):
    port: int = Field(...)
    ticket: str = Field(...)
    upid: str = Field(...)
    user: str = Field(...)

class PutNodesNodeQemuVmidUnlinkRequest(ProxmoxBaseModel):
    force: bool | None = Field(None, description="Force physical removal. Without this, we simple remove the disk from the config file and create an additional configuration entry called 'unused[n]', which contains the volume ID. Unlink of unused[n] always cause physical removal.")
    idlist: str = Field(..., description='A list of disk IDs you want to delete.')

class PutNodesNodeQemuVmidUnlinkResponse(RootModel[None]):
    root: None = Field(...)

class PostNodesNodeQemuVmidVncproxyRequest(ProxmoxBaseModel):
    generate_password: bool | None = Field(None, alias="generate-password", description='Generates a random password to be used as ticket instead of the API ticket.')
    websocket: bool | None = Field(None, description='Prepare for websocket upgrade (only required when using serial terminal, otherwise upgrade is always possible).')

class PostNodesNodeQemuVmidVncproxyResponse(ProxmoxBaseModel):
    cert: str = Field(...)
    password: str | None = Field(None, description="Returned if requested with 'generate-password' param. Consists of printable ASCII characters ('!' .. '~').")
    port: int = Field(...)
    ticket: str = Field(...)
    upid: str = Field(...)
    user: str = Field(...)

class GetNodesNodeQemuVmidVncwebsocketResponse(ProxmoxBaseModel):
    port: str = Field(...)

class GetNodesNodeQueryOciRepoTagsResponse(RootModel[list[str]]):
    root: list[str] = Field(...)

class GetNodesNodeQueryUrlMetadataResponse(ProxmoxBaseModel):
    filename: str | None = Field(None)
    mimetype: str | None = Field(None)
    size: int | None = Field(None)

class GetNodesNodeReplicationResponseItem(ProxmoxBaseModel):
    id: str | None = Field(None)

class GetNodesNodeReplicationResponse(RootModel[list[GetNodesNodeReplicationResponseItem]]):
    root: list[GetNodesNodeReplicationResponseItem] = Field(...)

class GetNodesNodeReplicationIdResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeReplicationIdLogResponseItem(ProxmoxBaseModel):
    n: int | None = Field(None, description='Line number')
    t: str | None = Field(None, description='Line text')

class GetNodesNodeReplicationIdLogResponse(RootModel[list[GetNodesNodeReplicationIdLogResponseItem]]):
    root: list[GetNodesNodeReplicationIdLogResponseItem] = Field(...)

class PostNodesNodeReplicationIdScheduleNowRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeReplicationIdScheduleNowResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeReplicationIdStatusResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class GetNodesNodeReportResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeRrdResponse(ProxmoxBaseModel):
    filename: str = Field(...)

class GetNodesNodeRrddataResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeScanResponseItem(ProxmoxBaseModel):
    method: str | None = Field(None)

class GetNodesNodeScanResponse(RootModel[list[GetNodesNodeScanResponseItem]]):
    root: list[GetNodesNodeScanResponseItem] = Field(...)

class GetNodesNodeScanCifsResponseItem(ProxmoxBaseModel):
    description: str | None = Field(None, description='Descriptive text from server.')
    share: str | None = Field(None, description='The cifs share name.')

class GetNodesNodeScanCifsResponse(RootModel[list[GetNodesNodeScanCifsResponseItem]]):
    root: list[GetNodesNodeScanCifsResponseItem] = Field(...)

class GetNodesNodeScanIscsiResponseItem(ProxmoxBaseModel):
    portal: str | None = Field(None, description='The iSCSI portal name.')
    target: str | None = Field(None, description='The iSCSI target name.')

class GetNodesNodeScanIscsiResponse(RootModel[list[GetNodesNodeScanIscsiResponseItem]]):
    root: list[GetNodesNodeScanIscsiResponseItem] = Field(...)

class GetNodesNodeScanLvmResponseItem(ProxmoxBaseModel):
    vg: str | None = Field(None, description='The LVM logical volume group name.')

class GetNodesNodeScanLvmResponse(RootModel[list[GetNodesNodeScanLvmResponseItem]]):
    root: list[GetNodesNodeScanLvmResponseItem] = Field(...)

class GetNodesNodeScanLvmthinResponseItem(ProxmoxBaseModel):
    lv: str | None = Field(None, description='The LVM Thin Pool name (LVM logical volume).')

class GetNodesNodeScanLvmthinResponse(RootModel[list[GetNodesNodeScanLvmthinResponseItem]]):
    root: list[GetNodesNodeScanLvmthinResponseItem] = Field(...)

class GetNodesNodeScanNfsResponseItem(ProxmoxBaseModel):
    options: str | None = Field(None, description='NFS export options.')
    path: str | None = Field(None, description='The exported path.')

class GetNodesNodeScanNfsResponse(RootModel[list[GetNodesNodeScanNfsResponseItem]]):
    root: list[GetNodesNodeScanNfsResponseItem] = Field(...)

class GetNodesNodeScanPbsResponseItem(ProxmoxBaseModel):
    comment: str | None = Field(None, description='Comment from server.')
    store: str | None = Field(None, description='The datastore name.')

class GetNodesNodeScanPbsResponse(RootModel[list[GetNodesNodeScanPbsResponseItem]]):
    root: list[GetNodesNodeScanPbsResponseItem] = Field(...)

class GetNodesNodeScanZfsResponseItem(ProxmoxBaseModel):
    pool: str | None = Field(None, description='ZFS pool name.')

class GetNodesNodeScanZfsResponse(RootModel[list[GetNodesNodeScanZfsResponseItem]]):
    root: list[GetNodesNodeScanZfsResponseItem] = Field(...)

class GetNodesNodeSdnResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeSdnFabricsFabricResponseItem(ProxmoxBaseModel):
    subdir: str | None = Field(None)

class GetNodesNodeSdnFabricsFabricResponse(RootModel[list[GetNodesNodeSdnFabricsFabricResponseItem]]):
    root: list[GetNodesNodeSdnFabricsFabricResponseItem] = Field(...)

class GetNodesNodeSdnFabricsFabricInterfacesResponseItem(ProxmoxBaseModel):
    name: str | None = Field(None, description='The name of the network interface.')
    state: str | None = Field(None, description='The current state of the interface.')
    type: str | None = Field(None, description='The type of this interface in the fabric (e.g. Point-to-Point, Broadcast, ..).')

class GetNodesNodeSdnFabricsFabricInterfacesResponse(RootModel[list[GetNodesNodeSdnFabricsFabricInterfacesResponseItem]]):
    root: list[GetNodesNodeSdnFabricsFabricInterfacesResponseItem] = Field(...)

class GetNodesNodeSdnFabricsFabricNeighborsResponseItem(ProxmoxBaseModel):
    neighbor: str | None = Field(None, description='The IP or hostname of the neighbor.')
    status: str | None = Field(None, description='The status of the neighbor, as returned by FRR.')
    uptime: str | None = Field(None, description='The uptime of this neighbor, as returned by FRR (e.g. 8h24m12s).')

class GetNodesNodeSdnFabricsFabricNeighborsResponse(RootModel[list[GetNodesNodeSdnFabricsFabricNeighborsResponseItem]]):
    root: list[GetNodesNodeSdnFabricsFabricNeighborsResponseItem] = Field(...)

class GetNodesNodeSdnFabricsFabricRoutesResponseItem(ProxmoxBaseModel):
    route: str | None = Field(None, description='The CIDR block for this routing table entry.')
    via: list[str] | None = Field(None, description='A list of nexthops for that route.')

class GetNodesNodeSdnFabricsFabricRoutesResponse(RootModel[list[GetNodesNodeSdnFabricsFabricRoutesResponseItem]]):
    root: list[GetNodesNodeSdnFabricsFabricRoutesResponseItem] = Field(...)

class GetNodesNodeSdnVnetsVnetResponseItem(ProxmoxBaseModel):
    subdir: str | None = Field(None)

class GetNodesNodeSdnVnetsVnetResponse(RootModel[list[GetNodesNodeSdnVnetsVnetResponseItem]]):
    root: list[GetNodesNodeSdnVnetsVnetResponseItem] = Field(...)

class GetNodesNodeSdnVnetsVnetMacVrfResponseItem(ProxmoxBaseModel):
    ip: str | None = Field(None, description='The IP address of the MAC VRF entry.')
    mac: str | None = Field(None, description='The MAC address of the MAC VRF entry.')
    nexthop: str | None = Field(None, description='The IP address of the nexthop.')

class GetNodesNodeSdnVnetsVnetMacVrfResponse(RootModel[list[GetNodesNodeSdnVnetsVnetMacVrfResponseItem]]):
    root: list[GetNodesNodeSdnVnetsVnetMacVrfResponseItem] = Field(..., description='All routes from the MAC VRF that this node self-originates or has learned via BGP.')

class GetNodesNodeSdnZonesResponseItem(ProxmoxBaseModel):
    status: str | None = Field(None, description='Status of zone')
    zone: str | None = Field(None, description='The SDN zone object identifier.')

class GetNodesNodeSdnZonesResponse(RootModel[list[GetNodesNodeSdnZonesResponseItem]]):
    root: list[GetNodesNodeSdnZonesResponseItem] = Field(...)

class GetNodesNodeSdnZonesZoneResponseItem(ProxmoxBaseModel):
    subdir: str | None = Field(None)

class GetNodesNodeSdnZonesZoneResponse(RootModel[list[GetNodesNodeSdnZonesZoneResponseItem]]):
    root: list[GetNodesNodeSdnZonesZoneResponseItem] = Field(...)

class GetNodesNodeSdnZonesZoneBridgesResponseItem(ProxmoxBaseModel):
    name: str | None = Field(None, description='Name of the bridge.')
    ports: list[dict[str, object]] | None = Field(None, description='All ports that are members of the bridge')
    vlan_filtering: str | None = Field(None, description='Whether VLAN filtering is enabled for this bridge (= VLAN-aware).')

class GetNodesNodeSdnZonesZoneBridgesResponse(RootModel[list[GetNodesNodeSdnZonesZoneBridgesResponseItem]]):
    root: list[GetNodesNodeSdnZonesZoneBridgesResponseItem] = Field(...)

class GetNodesNodeSdnZonesZoneContentResponseItem(ProxmoxBaseModel):
    status: str | None = Field(None, description='Status.')
    statusmsg: str | None = Field(None, description='Status details')
    vnet: str | None = Field(None, description='Vnet identifier.')

class GetNodesNodeSdnZonesZoneContentResponse(RootModel[list[GetNodesNodeSdnZonesZoneContentResponseItem]]):
    root: list[GetNodesNodeSdnZonesZoneContentResponseItem] = Field(...)

class GetNodesNodeSdnZonesZoneIpVrfResponseItem(ProxmoxBaseModel):
    ip: str | None = Field(None, description='The CIDR of the route table entry.')
    metric: int | None = Field(None, description="This route's metric.")
    nexthops: list[str] | None = Field(None, description='A list of nexthops for the route table entry.')
    protocol: str | None = Field(None, description='The protocol where this route was learned from (e.g. BGP).')

class GetNodesNodeSdnZonesZoneIpVrfResponse(RootModel[list[GetNodesNodeSdnZonesZoneIpVrfResponseItem]]):
    root: list[GetNodesNodeSdnZonesZoneIpVrfResponseItem] = Field(..., description='All entries in the VRF table of zone {zone} of the node.This does not include /32 routes for guests on this host,since they are handled via the respective vnet bridge directly.')

class GetNodesNodeServicesResponseItem(ProxmoxBaseModel):
    active_state: str | None = Field(None, alias="active-state", description='Current state of the service process (systemd ActiveState).')
    desc: str | None = Field(None, description='Description of the service.')
    name: str | None = Field(None, description='Short identifier for the service (e.g., "pveproxy").')
    service: str | None = Field(None, description='Systemd unit name (e.g., pveproxy).')
    state: str | None = Field(None, description='Execution status of the service (systemd SubState).')
    unit_state: str | None = Field(None, alias="unit-state", description='Whether the service is enabled (systemd UnitFileState).')

class GetNodesNodeServicesResponse(RootModel[list[GetNodesNodeServicesResponseItem]]):
    root: list[GetNodesNodeServicesResponseItem] = Field(...)

class GetNodesNodeServicesServiceResponseItem(ProxmoxBaseModel):
    subdir: str | None = Field(None)

class GetNodesNodeServicesServiceResponse(RootModel[list[GetNodesNodeServicesServiceResponseItem]]):
    root: list[GetNodesNodeServicesServiceResponseItem] = Field(...)

class PostNodesNodeServicesServiceReloadRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeServicesServiceReloadResponse(RootModel[str]):
    root: str = Field(...)

class PostNodesNodeServicesServiceRestartRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeServicesServiceRestartResponse(RootModel[str]):
    root: str = Field(...)

class PostNodesNodeServicesServiceStartRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeServicesServiceStartResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeServicesServiceStateResponse(ProxmoxBaseModel):
    active_state: str = Field(..., alias="active-state", description='Current state of the service process (systemd ActiveState).')
    desc: str = Field(..., description='Description of the service.')
    name: str = Field(..., description='Short identifier for the service (e.g., "pveproxy").')
    service: str = Field(..., description='Systemd unit name (e.g., pveproxy).')
    state: str = Field(..., description='Execution status of the service (systemd SubState).')
    unit_state: str = Field(..., alias="unit-state", description='Whether the service is enabled (systemd UnitFileState).')

class PostNodesNodeServicesServiceStopRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeServicesServiceStopResponse(RootModel[str]):
    root: str = Field(...)

class PostNodesNodeSpiceshellRequest(ProxmoxBaseModel):
    cmd: str | None = Field(None, description="Run specific command or default to login (requires 'root@pam')")
    cmd_opts: str | None = Field(None, alias="cmd-opts", description='Add parameters to a command. Encoded as null terminated strings.')
    proxy: str | None = Field(None, description="SPICE proxy server. This can be used by the client to specify the proxy server. All nodes in a cluster runs 'spiceproxy', so it is up to the client to choose one. By default, we return the node where the VM is currently running. As reasonable setting is to use same node you use to connect to the API (This is window.location.hostname for the JS GUI).")

class PostNodesNodeSpiceshellResponse(ProxmoxBaseModel):
    host: str = Field(...)
    password: str = Field(...)
    proxy: str = Field(...)
    tls_port: int = Field(..., alias="tls-port")
    type: str = Field(...)

class PostNodesNodeStartallRequest(ProxmoxBaseModel):
    force: bool | None = Field(None, description="Issue start command even if virtual guest have 'onboot' not set or set to off.")
    vms: str | None = Field(None, description='Only consider guests from this comma separated list of VMIDs.')

class PostNodesNodeStartallResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeStatusResponse(ProxmoxBaseModel):
    boot_info: dict[str, object] = Field(..., alias="boot-info", description='Meta-information about the boot mode.')
    cpu: float = Field(..., description='The current cpu usage.')
    cpuinfo: dict[str, object] = Field(...)
    current_kernel: dict[str, object] = Field(..., alias="current-kernel", description='Meta-information about the currently booted kernel of this node.')
    loadavg: list[str] = Field(..., description='An array of load avg for 1, 5 and 15 minutes respectively.')
    memory: dict[str, object] = Field(...)
    pveversion: str = Field(..., description='The PVE version string.')
    rootfs: dict[str, object] = Field(...)

class PostNodesNodeStatusRequest(ProxmoxBaseModel):
    command: str = Field(..., description='Specify the command.')

class PostNodesNodeStatusResponse(RootModel[None]):
    root: None = Field(...)

class PostNodesNodeStopallRequest(ProxmoxBaseModel):
    force_stop: bool | None = Field(None, alias="force-stop", description='Force a hard-stop after the timeout.')
    timeout: int | None = Field(None, description='Timeout for each guest shutdown task. Depending on `force-stop`, the shutdown gets then simply aborted or a hard-stop is forced.')
    vms: str | None = Field(None, description='Only consider Guests with these IDs.')

class PostNodesNodeStopallResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeStorageResponseItem(ProxmoxBaseModel):
    active: bool | None = Field(None, description='Set when storage is accessible.')
    avail: int | None = Field(None, description='Available storage space in bytes.')
    content: str | None = Field(None, description='Allowed storage content types.')
    enabled: bool | None = Field(None, description='Set when storage is enabled (not disabled).')
    formats: dict[str, object] | None = Field(None, description="Lists the supported and default format. Use 'formats' instead. Only included if 'format' parameter is set.")
    select_existing: bool | None = Field(None, description="Instead of creating new volumes, one must select one that is already existing. Only included if 'format' parameter is set.")
    shared: bool | None = Field(None, description='Shared flag from storage configuration.')
    storage: str | None = Field(None, description='The storage identifier.')
    total: int | None = Field(None, description='Total storage space in bytes.')
    type: str | None = Field(None, description='Storage type.')
    used: int | None = Field(None, description='Used storage space in bytes.')
    used_fraction: float | None = Field(None, description='Used fraction (used/total).')

class GetNodesNodeStorageResponse(RootModel[list[GetNodesNodeStorageResponseItem]]):
    root: list[GetNodesNodeStorageResponseItem] = Field(...)

class GetNodesNodeStorageStorageResponseItem(ProxmoxBaseModel):
    subdir: str | None = Field(None)

class GetNodesNodeStorageStorageResponse(RootModel[list[GetNodesNodeStorageStorageResponseItem]]):
    root: list[GetNodesNodeStorageStorageResponseItem] = Field(...)

class GetNodesNodeStorageStorageContentResponseItem(ProxmoxBaseModel):
    ctime: int | None = Field(None, description='Creation time (seconds since the UNIX Epoch).')
    encrypted: str | None = Field(None, description="If whole backup is encrypted, value is the fingerprint or '1'  if encrypted. Only useful for the Proxmox Backup Server storage type.")
    format: str | None = Field(None, description="Format identifier ('raw', 'qcow2', 'subvol', 'iso', 'tgz' ...)")
    notes: str | None = Field(None, description='Optional notes. If they contain multiple lines, only the first one is returned here.')
    parent: str | None = Field(None, description='Volume identifier of parent (for linked cloned).')
    protected: bool | None = Field(None, description='Protection status. Currently only supported for backups.')
    size: int | None = Field(None, description='Volume size in bytes.')
    used: int | None = Field(None, description='Used space. Please note that most storage plugins do not report anything useful here.')
    verification: dict[str, object] | None = Field(None, description='Last backup verification result, only useful for PBS storages.')
    vmid: int | None = Field(None, description='Associated Owner VMID.')
    volid: str | None = Field(None, description='Volume identifier.')

class GetNodesNodeStorageStorageContentResponse(RootModel[list[GetNodesNodeStorageStorageContentResponseItem]]):
    root: list[GetNodesNodeStorageStorageContentResponseItem] = Field(...)

class PostNodesNodeStorageStorageContentRequest(ProxmoxBaseModel):
    filename: str = Field(..., description='The name of the file to create.')
    format: str | None = Field(None, description='Format of the image.')
    size: str = Field(..., description="Size in kilobyte (1024 bytes). Optional suffixes 'M' (megabyte, 1024K) and 'G' (gigabyte, 1024M)")
    vmid: int = Field(..., description='Specify owner VM')

class PostNodesNodeStorageStorageContentResponse(RootModel[str]):
    root: str = Field(..., description='Volume identifier')

class DeleteNodesNodeStorageStorageContentVolumeRequest(ProxmoxBaseModel):
    delay: int | None = Field(None, description="Time to wait for the task to finish. We return 'null' if the task finish within that time.")

class DeleteNodesNodeStorageStorageContentVolumeResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeStorageStorageContentVolumeResponse(ProxmoxBaseModel):
    format: str = Field(..., description="Format identifier ('raw', 'qcow2', 'subvol', 'iso', 'tgz' ...)")
    notes: str | None = Field(None, description='Optional notes.')
    path: str = Field(..., description='The Path')
    protected: bool | None = Field(None, description='Protection status. Currently only supported for backups.')
    size: int = Field(..., description='Volume size in bytes.')
    used: int = Field(..., description='Used space. Please note that most storage plugins do not report anything useful here.')

class PostNodesNodeStorageStorageContentVolumeRequest(ProxmoxBaseModel):
    target: str = Field(..., description='Target volume identifier')
    target_node: str | None = Field(None, description='Target node. Default is local node.')

class PostNodesNodeStorageStorageContentVolumeResponse(RootModel[str]):
    root: str = Field(...)

class PutNodesNodeStorageStorageContentVolumeRequest(ProxmoxBaseModel):
    notes: str | None = Field(None, description='The new notes.')
    protected: bool | None = Field(None, description='Protection status. Currently only supported for backups.')

class PutNodesNodeStorageStorageContentVolumeResponse(RootModel[None]):
    root: None = Field(...)

class PostNodesNodeStorageStorageDownloadUrlRequest(ProxmoxBaseModel):
    checksum: str | None = Field(None, description='The expected checksum of the file.')
    checksum_algorithm: str | None = Field(None, alias="checksum-algorithm", description='The algorithm to calculate the checksum of the file.')
    compression: str | None = Field(None, description='Decompress the downloaded file using the specified compression algorithm.')
    content: str = Field(..., description='Content type.')
    filename: str = Field(..., description='The name of the file to create. Caution: This will be normalized!')
    url: str = Field(..., description='The URL to download the file from.')
    verify_certificates: bool | None = Field(None, alias="verify-certificates", description='If false, no SSL/TLS certificates will be verified.')

class PostNodesNodeStorageStorageDownloadUrlResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeStorageStorageFileRestoreDownloadResponse(RootModel[object]):
    root: object = Field(...)

class GetNodesNodeStorageStorageFileRestoreListResponseItem(ProxmoxBaseModel):
    filepath: str | None = Field(None, description='base64 path of the current entry')
    leaf: bool | None = Field(None, description='If this entry is a leaf in the directory graph.')
    mtime: int | None = Field(None, description='Entry last-modified time (unix timestamp).')
    size: int | None = Field(None, description='Entry file size.')
    text: str | None = Field(None, description='Entry display text.')
    type: str | None = Field(None, description='Entry type.')

class GetNodesNodeStorageStorageFileRestoreListResponse(RootModel[list[GetNodesNodeStorageStorageFileRestoreListResponseItem]]):
    root: list[GetNodesNodeStorageStorageFileRestoreListResponseItem] = Field(...)

class GetNodesNodeStorageStorageImportMetadataResponse(ProxmoxBaseModel):
    create_args: dict[str, object] = Field(..., alias="create-args", description='Parameters which can be used in a call to create a VM or container.')
    disks: dict[str, object] | None = Field(None, description='Recognised disk volumes as `$bus$id` => `$storeid:$path` map.')
    net: dict[str, object] | None = Field(None, description='Recognised network interfaces as `net$id` => { ...params } object.')
    source: str = Field(..., description='The type of the import-source of this guest volume.')
    type: str = Field(..., description='The type of guest this is going to produce.')
    warnings: list[dict[str, object]] | None = Field(None, description='List of known issues that can affect the import of a guest. Note that lack of warning does not imply that there cannot be any problems.')

class PostNodesNodeStorageStorageOciRegistryPullRequest(ProxmoxBaseModel):
    filename: str | None = Field(None, description='Custom destination file name of the OCI image. Caution: This will be normalized!')
    reference: str = Field(..., description='The reference to the OCI image to download.')

class PostNodesNodeStorageStorageOciRegistryPullResponse(RootModel[str]):
    root: str = Field(...)

class DeleteNodesNodeStorageStoragePrunebackupsRequest(ProxmoxBaseModel):
    prune_backups: str | None = Field(None, alias="prune-backups", description='Use these retention options instead of those from the storage configuration.')
    type: str | None = Field(None, description="Either 'qemu' or 'lxc'. Only consider backups for guests of this type.")
    vmid: int | None = Field(None, description='Only prune backups for this VM.')

class DeleteNodesNodeStorageStoragePrunebackupsResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeStorageStoragePrunebackupsResponseItem(ProxmoxBaseModel):
    ctime: int | None = Field(None, description='Creation time of the backup (seconds since the UNIX epoch).')
    mark: str | None = Field(None, description="Whether the backup would be kept or removed. Backups that are protected or don't use the standard naming scheme are not removed.")
    type: str | None = Field(None, description="One of 'qemu', 'lxc', 'openvz' or 'unknown'.")
    vmid: int | None = Field(None, description='The VM the backup belongs to.')
    volid: str | None = Field(None, description='Backup volume ID.')

class GetNodesNodeStorageStoragePrunebackupsResponse(RootModel[list[GetNodesNodeStorageStoragePrunebackupsResponseItem]]):
    root: list[GetNodesNodeStorageStoragePrunebackupsResponseItem] = Field(...)

class GetNodesNodeStorageStorageRrdResponse(ProxmoxBaseModel):
    filename: str = Field(...)

class GetNodesNodeStorageStorageRrddataResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeStorageStorageStatusResponse(ProxmoxBaseModel):
    active: bool | None = Field(None, description='Set when storage is accessible.')
    avail: int | None = Field(None, description='Available storage space in bytes.')
    content: str = Field(..., description='Allowed storage content types.')
    enabled: bool | None = Field(None, description='Set when storage is enabled (not disabled).')
    shared: bool | None = Field(None, description='Shared flag from storage configuration.')
    total: int | None = Field(None, description='Total storage space in bytes.')
    type: str = Field(..., description='Storage type.')
    used: int | None = Field(None, description='Used storage space in bytes.')

class PostNodesNodeStorageStorageUploadRequest(ProxmoxBaseModel):
    checksum: str | None = Field(None, description='The expected checksum of the file.')
    checksum_algorithm: str | None = Field(None, alias="checksum-algorithm", description='The algorithm to calculate the checksum of the file.')
    content: str = Field(..., description='Content type.')
    filename: str = Field(..., description='The name of the file to create. Caution: This will be normalized!')
    tmpfilename: str | None = Field(None, description='The source file name. This parameter is usually set by the REST handler. You can only overwrite it when connecting to the trusted port on localhost.')

class PostNodesNodeStorageStorageUploadResponse(RootModel[str]):
    root: str = Field(...)

class DeleteNodesNodeSubscriptionRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteNodesNodeSubscriptionResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeSubscriptionResponse(ProxmoxBaseModel):
    checktime: int | None = Field(None, description='Timestamp of the last check done.')
    key: str | None = Field(None, description='The subscription key, if set and permitted to access.')
    level: str | None = Field(None, description='A short code for the subscription level.')
    message: str | None = Field(None, description='A more human readable status message.')
    nextduedate: str | None = Field(None, description='Next due date of the set subscription.')
    productname: str | None = Field(None, description='Human readable productname of the set subscription.')
    regdate: str | None = Field(None, description='Register date of the set subscription.')
    serverid: str | None = Field(None, description='The server ID, if permitted to access.')
    signature: str | None = Field(None, description='Signature for offline keys')
    sockets: int | None = Field(None, description='The number of sockets for this host.')
    status: str = Field(..., description='The current subscription status.')
    url: str | None = Field(None, description='URL to the web shop.')

class PostNodesNodeSubscriptionRequest(ProxmoxBaseModel):
    force: bool | None = Field(None, description='Always connect to server, even if local cache is still valid.')

class PostNodesNodeSubscriptionResponse(RootModel[None]):
    root: None = Field(...)

class PutNodesNodeSubscriptionRequest(ProxmoxBaseModel):
    key: str = Field(..., description='Proxmox VE subscription key')

class PutNodesNodeSubscriptionResponse(RootModel[None]):
    root: None = Field(...)

class PostNodesNodeSuspendallRequest(ProxmoxBaseModel):
    vms: str | None = Field(None, description='Only consider Guests with these IDs.')

class PostNodesNodeSuspendallResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeSyslogResponseItem(ProxmoxBaseModel):
    n: int | None = Field(None, description='Line number')
    t: str | None = Field(None, description='Line text')

class GetNodesNodeSyslogResponse(RootModel[list[GetNodesNodeSyslogResponseItem]]):
    root: list[GetNodesNodeSyslogResponseItem] = Field(...)

class GetNodesNodeTasksResponseItem(ProxmoxBaseModel):
    endtime: int | None = Field(None)
    id: str | None = Field(None)
    node: str | None = Field(None)
    pid: int | None = Field(None)
    pstart: int | None = Field(None)
    starttime: int | None = Field(None)
    status: str | None = Field(None)
    type: str | None = Field(None)
    upid: str | None = Field(None)
    user: str | None = Field(None)

class GetNodesNodeTasksResponse(RootModel[list[GetNodesNodeTasksResponseItem]]):
    root: list[GetNodesNodeTasksResponseItem] = Field(...)

class DeleteNodesNodeTasksUpidRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteNodesNodeTasksUpidResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeTasksUpidResponse(RootModel[list[dict[str, object]]]):
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeTasksUpidLogResponseItem(ProxmoxBaseModel):
    n: int | None = Field(None, description='Line number')
    t: str | None = Field(None, description='Line text')

class GetNodesNodeTasksUpidLogResponse(RootModel[list[GetNodesNodeTasksUpidLogResponseItem]]):
    root: list[GetNodesNodeTasksUpidLogResponseItem] = Field(...)

class GetNodesNodeTasksUpidStatusResponse(ProxmoxBaseModel):
    exitstatus: str | None = Field(None)
    id: str = Field(...)
    node: str = Field(...)
    pid: int = Field(...)
    pstart: int = Field(...)
    starttime: int = Field(...)
    status: str = Field(...)
    type: str = Field(...)
    upid: str = Field(...)
    user: str = Field(...)

class PostNodesNodeTermproxyRequest(ProxmoxBaseModel):
    cmd: str | None = Field(None, description="Run specific command or default to login (requires 'root@pam')")
    cmd_opts: str | None = Field(None, alias="cmd-opts", description='Add parameters to a command. Encoded as null terminated strings.')

class PostNodesNodeTermproxyResponse(ProxmoxBaseModel):
    port: int = Field(..., description='port used to bind termproxy to.')
    ticket: str = Field(..., description='VNC ticket used to verify websocket connection.')
    upid: str = Field(..., description='UPID for termproxy worker task.')
    user: str = Field(..., description='user/token that generated the VNC ticket in `ticket`.')

class GetNodesNodeTimeResponse(ProxmoxBaseModel):
    localtime: int = Field(..., description='Seconds since 1970-01-01 00:00:00 (local time)')
    time: int = Field(..., description='Seconds since 1970-01-01 00:00:00 UTC.')
    timezone: str = Field(..., description='Time zone')

class PutNodesNodeTimeRequest(ProxmoxBaseModel):
    timezone: str = Field(..., description="Time zone. The file '/usr/share/zoneinfo/zone.tab' contains the list of valid names.")

class PutNodesNodeTimeResponse(RootModel[None]):
    root: None = Field(...)

class GetNodesNodeVersionResponse(ProxmoxBaseModel):
    release: str = Field(..., description='The current installed Proxmox VE Release')
    repoid: str = Field(..., description='The short git commit hash ID from which this version was build')
    version: str = Field(..., description='The current installed pve-manager package version')

class PostNodesNodeVncshellRequest(ProxmoxBaseModel):
    cmd: str | None = Field(None, description="Run specific command or default to login (requires 'root@pam')")
    cmd_opts: str | None = Field(None, alias="cmd-opts", description='Add parameters to a command. Encoded as null terminated strings.')
    height: int | None = Field(None, description='sets the height of the console in pixels.')
    websocket: bool | None = Field(None, description='use websocket instead of standard vnc.')
    width: int | None = Field(None, description='sets the width of the console in pixels.')

class PostNodesNodeVncshellResponse(ProxmoxBaseModel):
    cert: str = Field(...)
    port: int = Field(...)
    ticket: str = Field(...)
    upid: str = Field(...)
    user: str = Field(...)

class GetNodesNodeVncwebsocketResponse(ProxmoxBaseModel):
    port: str = Field(...)

class PostNodesNodeVzdumpRequest(ProxmoxBaseModel):
    all: bool | None = Field(None, description='Backup all known guest systems on this host.')
    bwlimit: int | None = Field(None, description='Limit I/O bandwidth (in KiB/s).')
    compress: str | None = Field(None, description='Compress dump file.')
    dumpdir: str | None = Field(None, description='Store resulting files to specified directory.')
    exclude: str | None = Field(None, description='Exclude specified guest systems (assumes --all)')
    exclude_path: list[str] | None = Field(None, alias="exclude-path", description="Exclude certain files/directories (shell globs). Paths starting with '/' are anchored to the container's root, other paths match relative to each subdirectory.")
    fleecing: str | None = Field(None, description='Options for backup fleecing (VM only).')
    ionice: int | None = Field(None, description='Set IO priority when using the BFQ scheduler. For snapshot and suspend mode backups of VMs, this only affects the compressor. A value of 8 means the idle priority is used, otherwise the best-effort priority is used with the specified value.')
    job_id: str | None = Field(None, alias="job-id", description="The ID of the backup job. If set, the 'backup-job' metadata field of the backup notification will be set to this value. Only root@pam can set this parameter.")
    lockwait: int | None = Field(None, description='Maximal time to wait for the global lock (minutes).')
    mailnotification: str | None = Field(None, description='Deprecated: use notification targets/matchers instead. Specify when to send a notification mail')
    mailto: str | None = Field(None, description='Deprecated: Use notification targets/matchers instead. Comma-separated list of email addresses or users that should receive email notifications.')
    maxfiles: int | None = Field(None, description="Deprecated: use 'prune-backups' instead. Maximal number of backup files per guest system.")
    mode: str | None = Field(None, description='Backup mode.')
    notes_template: str | None = Field(None, alias="notes-template", description="Template string for generating notes for the backup(s). It can contain variables which will be replaced by their values. Currently supported are {{cluster}}, {{guestname}}, {{node}}, and {{vmid}}, but more might be added in the future. Needs to be a single line, newline and backslash need to be escaped as '\\n' and '\\\\' respectively.")
    notification_mode: str | None = Field(None, alias="notification-mode", description="Determine which notification system to use. If set to 'legacy-sendmail', vzdump will consider the mailto/mailnotification parameters and send emails to the specified address(es) via the 'sendmail' command. If set to 'notification-system', a notification will be sent via PVE's notification system, and the mailto and mailnotification will be ignored. If set to 'auto' (default setting), an email will be sent if mailto is set, and the notification system will be used if not.")
    pbs_change_detection_mode: str | None = Field(None, alias="pbs-change-detection-mode", description='PBS mode used to detect file changes and switch encoding format for container backups.')
    performance: str | None = Field(None, description='Other performance-related settings.')
    pigz: int | None = Field(None, description='Use pigz instead of gzip when N>0. N=1 uses half of cores, N>1 uses N as thread count.')
    pool: str | None = Field(None, description='Backup all known guest systems included in the specified pool.')
    protected: bool | None = Field(None, description='If true, mark backup(s) as protected.')
    prune_backups: str | None = Field(None, alias="prune-backups", description='Use these retention options instead of those from the storage configuration.')
    quiet: bool | None = Field(None, description='Be quiet.')
    remove: bool | None = Field(None, description="Prune older backups according to 'prune-backups'.")
    script: str | None = Field(None, description='Use specified hook script.')
    stdexcludes: bool | None = Field(None, description='Exclude temporary files and logs.')
    stdout: bool | None = Field(None, description='Write tar to stdout, not to a file.')
    stop: bool | None = Field(None, description='Stop running backup jobs on this host.')
    stopwait: int | None = Field(None, description='Maximal time to wait until a guest system is stopped (minutes).')
    storage: str | None = Field(None, description='Store resulting file to this storage.')
    tmpdir: str | None = Field(None, description='Store temporary files to specified directory.')
    vmid: str | None = Field(None, description='The ID of the guest system you want to backup.')
    zstd: int | None = Field(None, description='Zstd threads. N=0 uses half of the available cores, if N is set to a value bigger than 0, N is used as thread count.')

class PostNodesNodeVzdumpResponse(RootModel[str]):
    root: str = Field(...)

class GetNodesNodeVzdumpDefaultsResponse(ProxmoxBaseModel):
    all: bool | None = Field(None, description='Backup all known guest systems on this host.')
    bwlimit: int | None = Field(None, description='Limit I/O bandwidth (in KiB/s).')
    compress: str | None = Field(None, description='Compress dump file.')
    dumpdir: str | None = Field(None, description='Store resulting files to specified directory.')
    exclude: str | None = Field(None, description='Exclude specified guest systems (assumes --all)')
    exclude_path: list[str] | None = Field(None, alias="exclude-path", description="Exclude certain files/directories (shell globs). Paths starting with '/' are anchored to the container's root, other paths match relative to each subdirectory.")
    fleecing: str | None = Field(None, description='Options for backup fleecing (VM only).')
    ionice: int | None = Field(None, description='Set IO priority when using the BFQ scheduler. For snapshot and suspend mode backups of VMs, this only affects the compressor. A value of 8 means the idle priority is used, otherwise the best-effort priority is used with the specified value.')
    lockwait: int | None = Field(None, description='Maximal time to wait for the global lock (minutes).')
    mailnotification: str | None = Field(None, description='Deprecated: use notification targets/matchers instead. Specify when to send a notification mail')
    mailto: str | None = Field(None, description='Deprecated: Use notification targets/matchers instead. Comma-separated list of email addresses or users that should receive email notifications.')
    maxfiles: int | None = Field(None, description="Deprecated: use 'prune-backups' instead. Maximal number of backup files per guest system.")
    mode: str | None = Field(None, description='Backup mode.')
    node: str | None = Field(None, description='Only run if executed on this node.')
    notes_template: str | None = Field(None, alias="notes-template", description="Template string for generating notes for the backup(s). It can contain variables which will be replaced by their values. Currently supported are {{cluster}}, {{guestname}}, {{node}}, and {{vmid}}, but more might be added in the future. Needs to be a single line, newline and backslash need to be escaped as '\\n' and '\\\\' respectively.")
    notification_mode: str | None = Field(None, alias="notification-mode", description="Determine which notification system to use. If set to 'legacy-sendmail', vzdump will consider the mailto/mailnotification parameters and send emails to the specified address(es) via the 'sendmail' command. If set to 'notification-system', a notification will be sent via PVE's notification system, and the mailto and mailnotification will be ignored. If set to 'auto' (default setting), an email will be sent if mailto is set, and the notification system will be used if not.")
    pbs_change_detection_mode: str | None = Field(None, alias="pbs-change-detection-mode", description='PBS mode used to detect file changes and switch encoding format for container backups.')
    performance: str | None = Field(None, description='Other performance-related settings.')
    pigz: int | None = Field(None, description='Use pigz instead of gzip when N>0. N=1 uses half of cores, N>1 uses N as thread count.')
    pool: str | None = Field(None, description='Backup all known guest systems included in the specified pool.')
    protected: bool | None = Field(None, description='If true, mark backup(s) as protected.')
    prune_backups: str | None = Field(None, alias="prune-backups", description='Use these retention options instead of those from the storage configuration.')
    quiet: bool | None = Field(None, description='Be quiet.')
    remove: bool | None = Field(None, description="Prune older backups according to 'prune-backups'.")
    script: str | None = Field(None, description='Use specified hook script.')
    stdexcludes: bool | None = Field(None, description='Exclude temporary files and logs.')
    stop: bool | None = Field(None, description='Stop running backup jobs on this host.')
    stopwait: int | None = Field(None, description='Maximal time to wait until a guest system is stopped (minutes).')
    storage: str | None = Field(None, description='Store resulting file to this storage.')
    tmpdir: str | None = Field(None, description='Store temporary files to specified directory.')
    vmid: str | None = Field(None, description='The ID of the guest system you want to backup.')
    zstd: int | None = Field(None, description='Zstd threads. N=0 uses half of the available cores, if N is set to a value bigger than 0, N is used as thread count.')

class GetNodesNodeVzdumpExtractconfigResponse(RootModel[str]):
    root: str = Field(...)

class PostNodesNodeWakeonlanRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PostNodesNodeWakeonlanResponse(RootModel[str]):
    root: str = Field(..., description='MAC address used to assemble the WoL magic packet.')

class DeletePoolsRequest(ProxmoxBaseModel):
    poolid: str = Field(...)

class DeletePoolsResponse(RootModel[None]):
    root: None = Field(...)

class GetPoolsResponseItem(ProxmoxBaseModel):
    comment: str | None = Field(None)
    members: list[dict[str, object]] | None = Field(None)
    poolid: str | None = Field(None)

class GetPoolsResponse(RootModel[list[GetPoolsResponseItem]]):
    root: list[GetPoolsResponseItem] = Field(...)

class PostPoolsRequest(ProxmoxBaseModel):
    comment: str | None = Field(None)
    poolid: str = Field(...)

class PostPoolsResponse(RootModel[None]):
    root: None = Field(...)

class PutPoolsRequest(ProxmoxBaseModel):
    allow_move: bool | None = Field(None, alias="allow-move", description='Allow adding a guest even if already in another pool. The guest will be removed from its current pool and added to this one.')
    comment: str | None = Field(None)
    delete: bool | None = Field(None, description='Remove the passed VMIDs and/or storage IDs instead of adding them.')
    poolid: str = Field(...)
    storage: str | None = Field(None, description='List of storage IDs to add or remove from this pool.')
    vms: str | None = Field(None, description='List of guest VMIDs to add or remove from this pool.')

class PutPoolsResponse(RootModel[None]):
    root: None = Field(...)

class DeletePoolsPoolidRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeletePoolsPoolidResponse(RootModel[None]):
    root: None = Field(...)

class GetPoolsPoolidResponse(ProxmoxBaseModel):
    comment: str | None = Field(None)
    members: list[dict[str, object]] = Field(...)

class PutPoolsPoolidRequest(ProxmoxBaseModel):
    allow_move: bool | None = Field(None, alias="allow-move", description='Allow adding a guest even if already in another pool. The guest will be removed from its current pool and added to this one.')
    comment: str | None = Field(None)
    delete: bool | None = Field(None, description='Remove the passed VMIDs and/or storage IDs instead of adding them.')
    storage: str | None = Field(None, description='List of storage IDs to add or remove from this pool.')
    vms: str | None = Field(None, description='List of guest VMIDs to add or remove from this pool.')

class PutPoolsPoolidResponse(RootModel[None]):
    root: None = Field(...)

class GetStorageResponseItem(ProxmoxBaseModel):
    storage: str | None = Field(None)

class GetStorageResponse(RootModel[list[GetStorageResponseItem]]):
    root: list[GetStorageResponseItem] = Field(...)

class PostStorageRequest(ProxmoxBaseModel):
    authsupported: str | None = Field(None, description='Authsupported.')
    base: str | None = Field(None, description='Base volume. This volume is automatically activated.')
    blocksize: str | None = Field(None, description='block size')
    bwlimit: str | None = Field(None, description='Set I/O bandwidth limit for various operations (in KiB/s).')
    comstar_hg: str | None = Field(None, description='host group for comstar views')
    comstar_tg: str | None = Field(None, description='target group for comstar views')
    content: str | None = Field(None, description="Allowed content types.\n\nNOTE: the value 'rootdir' is used for Containers, and value 'images' for VMs.\n")
    content_dirs: str | None = Field(None, alias="content-dirs", description='Overrides for default content type directories.')
    create_base_path: bool | None = Field(None, alias="create-base-path", description="Create the base directory if it doesn't exist.")
    create_subdirs: bool | None = Field(None, alias="create-subdirs", description='Populate the directory with the default structure.')
    data_pool: str | None = Field(None, alias="data-pool", description='Data Pool (for erasure coding only)')
    datastore: str | None = Field(None, description='Proxmox Backup Server datastore name.')
    disable: bool | None = Field(None, description='Flag to disable the storage.')
    domain: str | None = Field(None, description='CIFS domain.')
    encryption_key: str | None = Field(None, alias="encryption-key", description="Encryption key. Use 'autogen' to generate one automatically without passphrase.")
    export: str | None = Field(None, description='NFS export path.')
    fingerprint: str | None = Field(None, description='Certificate SHA 256 fingerprint.')
    format: str | None = Field(None, description='Default image format.')
    fs_name: str | None = Field(None, alias="fs-name", description='The Ceph filesystem name.')
    fuse: bool | None = Field(None, description='Mount CephFS through FUSE.')
    is_mountpoint: str | None = Field(None, description='Assume the given path is an externally managed mountpoint and consider the storage offline if it is not mounted. Using a boolean (yes/no) value serves as a shortcut to using the target path in this field.')
    iscsiprovider: str | None = Field(None, description='iscsi provider')
    keyring: str | None = Field(None, description='Client keyring contents (for external clusters).')
    krbd: bool | None = Field(None, description='Always access rbd through krbd kernel module.')
    lio_tpg: str | None = Field(None, description='target portal group for Linux LIO targets')
    master_pubkey: str | None = Field(None, alias="master-pubkey", description='Base64-encoded, PEM-formatted public RSA key. Used to encrypt a copy of the encryption-key which will be added to each encrypted backup.')
    max_protected_backups: int | None = Field(None, alias="max-protected-backups", description="Maximal number of protected backups per guest. Use '-1' for unlimited.")
    mkdir: bool | None = Field(None, description="Create the directory if it doesn't exist and populate it with default sub-dirs. NOTE: Deprecated, use the 'create-base-path' and 'create-subdirs' options instead.")
    monhost: str | None = Field(None, description='IP addresses of monitors (for external clusters).')
    mountpoint: str | None = Field(None, description='mount point')
    namespace: str | None = Field(None, description='Namespace.')
    nocow: bool | None = Field(None, description='Set the NOCOW flag on files. Disables data checksumming and causes data errors to be unrecoverable from while allowing direct I/O. Only use this if data does not need to be any more safe than on a single ext4 formatted disk with no underlying raid system.')
    nodes: str | None = Field(None, description='List of nodes for which the storage configuration applies.')
    nowritecache: bool | None = Field(None, description='disable write caching on the target')
    options: str | None = Field(None, description="NFS/CIFS mount options (see 'man nfs' or 'man mount.cifs')")
    password: str | None = Field(None, description='Password for accessing the share/datastore.')
    path: str | None = Field(None, description='File system path.')
    pool: str | None = Field(None, description='Pool.')
    port: int | None = Field(None, description="Use this port to connect to the storage instead of the default one (for example, with PBS or ESXi). For NFS and CIFS, use the 'options' option to configure the port via the mount options.")
    portal: str | None = Field(None, description='iSCSI portal (IP or DNS name with optional port).')
    preallocation: str | None = Field(None, description="Preallocation mode for raw and qcow2 images. Using 'metadata' on raw images results in preallocation=off.")
    prune_backups: str | None = Field(None, alias="prune-backups", description='The retention options with shorter intervals are processed first with --keep-last being the very first one. Each option covers a specific period of time. We say that backups within this period are covered by this option. The next option does not take care of already covered backups and only considers older backups.')
    saferemove: bool | None = Field(None, description='Zero-out data when removing LVs.')
    saferemove_stepsize: int | None = Field(None, alias="saferemove-stepsize", description='Wipe step size in MiB. It will be capped to the maximum supported by the storage.')
    saferemove_throughput: str | None = Field(None, description='Wipe throughput (cstream -t parameter value).')
    server: str | None = Field(None, description='Server IP or DNS name.')
    share: str | None = Field(None, description='CIFS share.')
    shared: bool | None = Field(None, description="Indicate that this is a single storage with the same contents on all nodes (or all listed in the 'nodes' option). It will not make the contents of a local storage automatically accessible to other nodes, it just marks an already shared storage as such!")
    skip_cert_verification: bool | None = Field(None, alias="skip-cert-verification", description='Disable TLS certificate verification, only enable on fully trusted networks!')
    smbversion: str | None = Field(None, description="SMB protocol version. 'default' if not set, negotiates the highest SMB2+ version supported by both the client and server.")
    snapshot_as_volume_chain: bool | None = Field(None, alias="snapshot-as-volume-chain", description='Enable support for creating storage-vendor agnostic snapshot through volume backing-chains.')
    sparse: bool | None = Field(None, description='use sparse volumes')
    storage: str = Field(..., description='The storage identifier.')
    subdir: str | None = Field(None, description='Subdir to mount.')
    tagged_only: bool | None = Field(None, description="Only use logical volumes tagged with 'pve-vm-ID'.")
    target: str | None = Field(None, description='iSCSI target.')
    thinpool: str | None = Field(None, description='LVM thin pool LV name.')
    type: str = Field(..., description='Storage type.')
    username: str | None = Field(None, description='RBD Id.')
    vgname: str | None = Field(None, description='Volume group name.')
    zfs_base_path: str | None = Field(None, alias="zfs-base-path", description="Base path where to look for the created ZFS block devices. Set automatically during creation if not specified. Usually '/dev/zvol'.")

class PostStorageResponse(ProxmoxBaseModel):
    config: dict[str, object] | None = Field(None, description='Partial, possibly server generated, configuration properties.')
    storage: str = Field(..., description='The ID of the created storage.')
    type: str = Field(..., description='The type of the created storage.')

class DeleteStorageStorageRequest(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class DeleteStorageStorageResponse(RootModel[None]):
    root: None = Field(...)

class GetStorageStorageResponse(RootModel[dict[str, object]]):
    root: dict[str, object] = Field(...)

class PutStorageStorageRequest(ProxmoxBaseModel):
    blocksize: str | None = Field(None, description='block size')
    bwlimit: str | None = Field(None, description='Set I/O bandwidth limit for various operations (in KiB/s).')
    comstar_hg: str | None = Field(None, description='host group for comstar views')
    comstar_tg: str | None = Field(None, description='target group for comstar views')
    content: str | None = Field(None, description="Allowed content types.\n\nNOTE: the value 'rootdir' is used for Containers, and value 'images' for VMs.\n")
    content_dirs: str | None = Field(None, alias="content-dirs", description='Overrides for default content type directories.')
    create_base_path: bool | None = Field(None, alias="create-base-path", description="Create the base directory if it doesn't exist.")
    create_subdirs: bool | None = Field(None, alias="create-subdirs", description='Populate the directory with the default structure.')
    data_pool: str | None = Field(None, alias="data-pool", description='Data Pool (for erasure coding only)')
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Flag to disable the storage.')
    domain: str | None = Field(None, description='CIFS domain.')
    encryption_key: str | None = Field(None, alias="encryption-key", description="Encryption key. Use 'autogen' to generate one automatically without passphrase.")
    fingerprint: str | None = Field(None, description='Certificate SHA 256 fingerprint.')
    format: str | None = Field(None, description='Default image format.')
    fs_name: str | None = Field(None, alias="fs-name", description='The Ceph filesystem name.')
    fuse: bool | None = Field(None, description='Mount CephFS through FUSE.')
    is_mountpoint: str | None = Field(None, description='Assume the given path is an externally managed mountpoint and consider the storage offline if it is not mounted. Using a boolean (yes/no) value serves as a shortcut to using the target path in this field.')
    keyring: str | None = Field(None, description='Client keyring contents (for external clusters).')
    krbd: bool | None = Field(None, description='Always access rbd through krbd kernel module.')
    lio_tpg: str | None = Field(None, description='target portal group for Linux LIO targets')
    master_pubkey: str | None = Field(None, alias="master-pubkey", description='Base64-encoded, PEM-formatted public RSA key. Used to encrypt a copy of the encryption-key which will be added to each encrypted backup.')
    max_protected_backups: int | None = Field(None, alias="max-protected-backups", description="Maximal number of protected backups per guest. Use '-1' for unlimited.")
    mkdir: bool | None = Field(None, description="Create the directory if it doesn't exist and populate it with default sub-dirs. NOTE: Deprecated, use the 'create-base-path' and 'create-subdirs' options instead.")
    monhost: str | None = Field(None, description='IP addresses of monitors (for external clusters).')
    mountpoint: str | None = Field(None, description='mount point')
    namespace: str | None = Field(None, description='Namespace.')
    nocow: bool | None = Field(None, description='Set the NOCOW flag on files. Disables data checksumming and causes data errors to be unrecoverable from while allowing direct I/O. Only use this if data does not need to be any more safe than on a single ext4 formatted disk with no underlying raid system.')
    nodes: str | None = Field(None, description='List of nodes for which the storage configuration applies.')
    nowritecache: bool | None = Field(None, description='disable write caching on the target')
    options: str | None = Field(None, description="NFS/CIFS mount options (see 'man nfs' or 'man mount.cifs')")
    password: str | None = Field(None, description='Password for accessing the share/datastore.')
    pool: str | None = Field(None, description='Pool.')
    port: int | None = Field(None, description="Use this port to connect to the storage instead of the default one (for example, with PBS or ESXi). For NFS and CIFS, use the 'options' option to configure the port via the mount options.")
    preallocation: str | None = Field(None, description="Preallocation mode for raw and qcow2 images. Using 'metadata' on raw images results in preallocation=off.")
    prune_backups: str | None = Field(None, alias="prune-backups", description='The retention options with shorter intervals are processed first with --keep-last being the very first one. Each option covers a specific period of time. We say that backups within this period are covered by this option. The next option does not take care of already covered backups and only considers older backups.')
    saferemove: bool | None = Field(None, description='Zero-out data when removing LVs.')
    saferemove_stepsize: int | None = Field(None, alias="saferemove-stepsize", description='Wipe step size in MiB. It will be capped to the maximum supported by the storage.')
    saferemove_throughput: str | None = Field(None, description='Wipe throughput (cstream -t parameter value).')
    server: str | None = Field(None, description='Server IP or DNS name.')
    shared: bool | None = Field(None, description="Indicate that this is a single storage with the same contents on all nodes (or all listed in the 'nodes' option). It will not make the contents of a local storage automatically accessible to other nodes, it just marks an already shared storage as such!")
    skip_cert_verification: bool | None = Field(None, alias="skip-cert-verification", description='Disable TLS certificate verification, only enable on fully trusted networks!')
    smbversion: str | None = Field(None, description="SMB protocol version. 'default' if not set, negotiates the highest SMB2+ version supported by both the client and server.")
    snapshot_as_volume_chain: bool | None = Field(None, alias="snapshot-as-volume-chain", description='Enable support for creating storage-vendor agnostic snapshot through volume backing-chains.')
    sparse: bool | None = Field(None, description='use sparse volumes')
    subdir: str | None = Field(None, description='Subdir to mount.')
    tagged_only: bool | None = Field(None, description="Only use logical volumes tagged with 'pve-vm-ID'.")
    username: str | None = Field(None, description='RBD Id.')
    zfs_base_path: str | None = Field(None, alias="zfs-base-path", description="Base path where to look for the created ZFS block devices. Set automatically during creation if not specified. Usually '/dev/zvol'.")

class PutStorageStorageResponse(ProxmoxBaseModel):
    config: dict[str, object] | None = Field(None, description='Partial, possibly server generated, configuration properties.')
    storage: str = Field(..., description='The ID of the created storage.')
    type: str = Field(..., description='The type of the created storage.')

class GetVersionResponse(ProxmoxBaseModel):
    console: str | None = Field(None, description='The default console viewer to use.')
    release: str = Field(..., description='The current Proxmox VE point release in `x.y` format.')
    repoid: str = Field(..., description='The short git revision from which this version was build.')
    version: str = Field(..., description='The full pve-manager package version of this node.')
