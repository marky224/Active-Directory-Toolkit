import json

def audit_group_descriptions(conn):
    result = {"groups_missing_description": []}
    
    # Search for groups
    conn.search(search_base=conn.server.info.other['defaultNamingContext'][0],
                search_filter='(objectClass=group)',
                attributes=['distinguishedName', 'description'])

    for entry in conn.entries:
        if not entry.description:
            result["groups_missing_description"].append(str(entry.distinguishedName))

    return result