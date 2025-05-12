import json

def audit_permissions(conn):
    result = {"direct_user_permissions": []}
    
    # Search for objects with direct user permissions
    conn.search(search_base=conn.server.info.other['defaultNamingContext'][0],
                search_filter='(objectClass=*)',
                attributes=['nTSecurityDescriptor'])

    for entry in conn.entries:
        if entry.nTSecurityDescriptor and "user" in str(entry.entry_dn).lower():
            result["direct_user_permissions"].append(str(entry.entry_dn))

    return result