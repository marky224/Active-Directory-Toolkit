import argparse
import json
from utils import ou_audit, group_permissions, inactive_finder, group_desc_audit, audit_report, automation, time_sync_check
from utils.ad_connect import connect_to_ad

def main():
    parser = argparse.ArgumentParser(description="Active Directory Toolkit")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # OU Audit
    subparsers.add_parser("ou-audit", help="Check for mirrored OUs for users and computers")

    # Group Permissions Audit
    subparsers.add_parser("group-permissions", help="Audit direct user permissions")

    # Inactive Finder
    subparsers.add_parser("inactive-finder", help="Find inactive users, computers, and groups")

    # Group Description Audit
    subparsers.add_parser("group-desc-audit", help="List groups missing descriptions")

    # Monthly Audit Report
    subparsers.add_parser("audit-report", help="Generate monthly AD change report")

    # Automation
    subparsers.add_parser("automation", help="Run automated AD tasks")

    # Time Sync Check
    subparsers.add_parser("time-sync-check", help="Verify domain time synchronization")

    args = parser.parse_args()

    # Connect to AD
    ad_connection = connect_to_ad()

    # Execute the requested command
    if args.command == "ou-audit":
        result = ou_audit.audit_ous(ad_connection)
    elif args.command == "group-permissions":
        result = group_permissions.audit_permissions(ad_connection)
    elif args.command == "inactive-finder":
        result = inactive_finder.find_inactive(ad_connection)
    elif args.command == "group-desc-audit":
        result = group_desc_audit.audit_group_descriptions(ad_connection)
    elif args.command == "audit-report":
        result = audit_report.generate_report(ad_connection)
    elif args.command == "automation":
        result = automation.run_automation(ad_connection)
    elif args.command == "time-sync-check":
        result = time_sync_check.check_time_sync(ad_connection)
    else:
        parser.print_help()
        return

    # Output result in JSON format
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()