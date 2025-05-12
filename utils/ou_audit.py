import json

def audit_ous(conn):
    result = {"user_ous": [], "computer_ous": [], "issues": []}
    
    # Search for OUs
    conn.search(search_base=conn.server.info.other['defaultNamingContext'][0],
                search_filter='(objectClass=organizationalUnit)',
                attributes=['distinguishedName', 'objectClass'])

    for entry in conn.entries:
        dn = entry.distinguishedName.value
        if "user" in dn.lower():
            result["user_ous"].append(dn)
        elif "computer" in dn.lower():
            result["computer_ous"].append(dn)

    # Check for mirroring
    if not result["user_ous"]:
        result["issues"].append("No user OUs found")
    if not result["computer_ous"]:
        result["issues"].append("No computer OUs found")

    return result