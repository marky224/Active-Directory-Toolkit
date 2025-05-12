from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json

def find_inactive(conn):
    result = {"inactive_users": [], "inactive_computers": [], "inactive_groups": []}
    thirty_days_ago = (datetime.now() - relativedelta(days=30)).strftime('%Y%m%d%H%M%S.0Z')

    # Search for inactive users
    conn.search(search_base=conn.server.info.other['defaultNamingContext'][0],
                search_filter=f'(&(objectClass=user)(lastLogon<={thirty_days_ago}))',
                attributes=['distinguishedName'])

    for entry in conn.entries:
        result["inactive_users"].append(str(entry.distinguishedName))

    # Search for inactive computers
    conn.search(search_base=conn.server.info.other['defaultNamingContext'][0],
                search_filter=f'(&(objectClass=computer)(lastLogon<={thirty_days_ago}))',
                attributes=['distinguishedName'])

    for entry in conn.entries:
        result["inactive_computers"].append(str(entry.distinguishedName))

    # Search for inactive groups (simplified: no membership changes)
    conn.search(search_base=conn.server.info.other['defaultNamingContext'][0],
                search_filter=f'(&(objectClass=group)(whenChanged<={thirty_days_ago}))',
                attributes=['distinguishedName'])

    for entry in conn.entries:
        result["inactive_groups"].append(str(entry.distinguishedName))

    return result