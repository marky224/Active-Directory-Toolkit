import json
import argparse
from datetime import datetime
from dateutil.relativedelta import relativedelta
from ldap3 import MODIFY_REPLACE, MODIFY_ADD

def disable_inactive_users(conn):
    """Disable user accounts inactive for 30+ days."""
    result = {"task": "disable_inactive_users", "disabled_users": [], "errors": [], "status": "success"}
    
    thirty_days_ago = (datetime.now() - relativedelta(days=30)).strftime('%Y%m%d%H%M%S.0Z')
    
    # Search for inactive users (enabled accounts only)
    conn.search(
        search_base=conn.server.info.other['defaultNamingContext'][0],
        search_filter=f'(&(objectClass=user)(lastLogon<={thirty_days_ago})(!userAccountControl:1.2.840.113556.1.4.803:=2))',
        attributes=['distinguishedName', 'userAccountControl']
    )

    for entry in conn.entries:
        dn = str(entry.distinguishedName)
        try:
            # Disable account (set userAccountControl bit for disabled)
            new_uac = int(entry.userAccountControl) | 2  # Add disabled flag
            conn.modify(dn, {'userAccountControl': [(MODIFY_REPLACE, [new_uac])]})
            if conn.result['result'] == 0:
                result["disabled_users"].append(dn)
            else:
                result["errors"].append(f"Failed to disable {dn}: {conn.result['description']}")
        except Exception as e:
            result["errors"].append(f"Error disabling {dn}: {str(e)}")

    if result["errors"]:
        result["status"] = "partial_success" if result["disabled_users"] else "failed"
    
    return result

def remove_empty_groups(conn):
    """Remove groups with no members."""
    result = {"task": "remove_empty_groups", "deleted_groups": [], "errors": [], "status": "success"}
    
    # Search for groups
    conn.search(
        search_base=conn.server.info.other['defaultNamingContext'][0],
        search_filter='(objectClass=group)',
        attributes=['distinguishedName', 'member']
    )

    for entry in conn.entries:
        dn = str(entry.distinguishedName)
        if not entry.member:  # Group has no members
            try:
                conn.delete(dn)
                if conn.result['result'] == 0:
                    result["deleted_groups"].append(dn)
                else:
                    result["errors"].append(f"Failed to delete {dn}: {conn.result['description']}")
            except Exception as e:
                result["errors"].append(f"Error deleting {dn}: {str(e)}")

    if result["errors"]:
        result["status"] = "partial_success" if result["deleted_groups"] else "failed"
    
    return result

def add_users_to_group(conn, user_dns, group_dn):
    """Add specified users to a group."""
    result = {"task": "add_users_to_group", "group": group_dn, "added_users": [], "errors": [], "status": "success"}
    
    for user_dn in user_dns:
        try:
            conn.modify(group_dn, {'member': [(MODIFY_ADD, [user_dn])]})
            if conn.result['result'] == 0:
                result["added_users"].append(user_dn)
            else:
                result["errors"].append(f"Failed to add {user_dn} to {group_dn}: {conn.result['description']}")
        except Exception as e:
            result["errors"].append(f"Error adding {user_dn} to {group_dn}: {str(e)}")

    if result["errors"]:
        result["status"] = "partial_success" if result["added_users"] else "failed"
    
    return result

def run_automation(conn):
    """Main automation function with subcommands."""
    parser = argparse.ArgumentParser(description="AD Automation Tasks")
    subparsers = parser.add_subparsers(dest="task", help="Automation tasks")

    # Disable inactive users
    subparsers.add_parser("disable-inactive", help="Disable users inactive for 30+ days")

    # Remove empty groups
    subparsers.add_parser("remove-empty-groups", help="Remove groups with no members")

    # Add users to group
    add_parser = subparsers.add_parser("add-users-to-group", help="Add users to a group")
    add_parser.add_argument("--users", required=True, help="Comma-separated list of user DNs")
    add_parser.add_argument("--group", required=True, help="Group DN")

    args = parser.parse_args()

    if args.task == "disable-inactive":
        return disable_inactive_users(conn)
    elif args.task == "remove-empty-groups":
        return remove_empty_groups(conn)
    elif args.task == "add-users-to-group":
        user_dns = args.users.split(",")
        return add_users_to_group(conn, user_dns, args.group)
    else:
        return {
            "task": "none",
            "status": "failed",
            "errors": ["No valid automation task specified. Use --help for options."]
        }