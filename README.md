# Active Directory Toolkit

A modular, command-line toolkit for Windows-based Active Directory (AD) Domain Controllers, designed to help administrators implement best practices, automate common tasks, and generate audit and health reports in JSON format.

## Purpose

The Active Directory Toolkit empowers AD administrators to:
- **Implement Best Practices**: Ensure Organizational Unit (OU) structure, group permissions, and account management align with security and operational standards.
- **Automate Tasks**: Streamline user, group, and cleanup operations to save time and reduce errors.
- **Generate Reports**: Produce actionable audit and health reports for compliance, troubleshooting, and monitoring.

This toolkit is modular, extensible, and safe for sharing, with no hardcoded credentials or sensitive data.

## Project Structure & Key Components

The toolkit is organized as follows:

- **`requirements.txt`**  
  Lists Python dependencies: `ldap3`, `python-dateutil`, `pywin32`, and `colorama`.

- **`config.ini`**  
  A template for storing AD domain controller and base DN settings, with support for environment variable overrides to customize connectivity.

- **`ad_toolkit.py`**  
  The main command-line interface (CLI) entry point. Uses `argparse` to provide subcommands for each toolkit function.

- **`utils/`**  
  A Python package containing modular scripts for best practices and automation tasks:
  - `ad_connect.py`: Handles credential prompts, loads `config.ini`, and returns a connected LDAP object.
  - `ou_audit.py`: Checks for mirrored OUs for users and computers.
  - `group_permissions.py`: Audits for direct permissions granted to users instead of groups.
  - `inactive_finder.py`: Identifies inactive users, computers, and groups (no activity in the last 30 days).
  - `group_desc_audit.py`: Lists AD groups missing descriptions.
  - `audit_report.py`: Generates a monthly report of AD changes, including notes on failed logins and lockouts (requires event log access).
  - `automation.py`: A skeleton for automating common AD tasks (e.g., user/group management, cleanup).
  - `time_sync_check.py`: Verifies domain time synchronization.
  - `__init__.py`: Empty file to make `utils` a Python package.

- **`README.md`**  
  This file, providing setup and usage instructions.

## Output Format

All reports and outputs are generated in **JSON format** for easy parsing, integration with other tools, and automation workflows.

## Best Practices Covered

The toolkit enforces and audits the following Active Directory best practices:
- **OU Mirroring**: Ensures separate OUs for users and computers to improve organization and policy application.
- **Security Group Permissions**: Verifies permissions are assigned to groups, not individual users, to enhance security and manageability.
- **Inactive Account Cleanup**: Identifies users, computers, and groups inactive for 30+ days for potential decommissioning.
- **Group Description Completeness**: Flags groups missing descriptions to maintain clear documentation.
- **Monthly Audit Reports**: Tracks AD changes, including failed logins and lockouts (requires event log access for full functionality).
- **Automation of Common Tasks**: Provides a foundation for automating user/group management and cleanup (extendable via `automation.py`).
- **Domain Time Synchronization**: Confirms domain time is properly synced to prevent authentication and replication issues.

## How to Use

### Prerequisites
- **Operating System**: Windows (tested on Windows Server 2019/2022, Windows 10/11).
- **Python**: Version 3.8 or higher.
- **Permissions**: Administrative access to the Active Directory domain controller or read-only access for audits.
- **Network**: Connectivity to the domain controller.

### Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/active-directory-toolkit.git
   cd active-directory-toolkit
   ```

2. **Install Dependencies**:
   Install required Python packages using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure `config.ini`**:
   - Copy the provided `config.ini` template and edit it with your domain controller and base DN settings.
   - Example `config.ini`:
     ```ini
     [AD]
     domain_controller = dc01.example.local
     base_dn = DC=example,DC=local
     ```
   - Optionally, override settings with environment variables (e.g., `AD_DOMAIN_CONTROLLER`, `AD_BASE_DN`).

### Running the Toolkit
Run the toolkit using the main script with a subcommand:
```bash
python ad_toolkit.py <command>
```

Available `<command>` options:
- `ou-audit`: Audits OU structure for user/computer mirroring.
- `group-permissions`: Checks for direct user permissions.
- `inactive-report`: Lists inactive users, computers, and groups.
- `group-desc-audit`: Identifies groups without descriptions.
- `monthly-audit`: Generates a monthly report of AD changes.
- `automation`: Runs automated AD tasks (customizable via `automation.py`).
- `time-sync-check`: Verifies domain time synchronization.

**Example**:
```bash
python ad_toolkit.py ou-audit
```

- **Credentials**: Follow on-screen prompts to enter AD credentials at runtime (no credentials are stored).
- **Output**: Results are printed in JSON format to the console, suitable for piping to files or other tools (e.g., `python ad_toolkit.py ou-audit > output.json`).

## Example Output
Running `python ad_toolkit.py group-desc-audit` might produce:
```json
[
  {
    "group_name": "SalesTeam",
    "distinguished_name": "CN=SalesTeam,OU=Groups,DC=example,DC=local",
    "description": null
  },
  {
    "group_name": "TempAccess",
    "distinguished_name": "CN=TempAccess,OU=Groups,DC=example,DC=local",
    "description": null
  }
]
```

## Extending the Toolkit
The modular design allows easy extension:
- **Add New Subcommands**: Modify `ad_toolkit.py` to include new `argparse` subcommands and corresponding scripts in `utils/`.
- **Customize Automation**: Extend `automation.py` with specific AD tasks (e.g., bulk user creation, group cleanup).
- **Integrate with Other Tools**: Use JSON outputs in scripts or monitoring systems for automated workflows.

## Security Notes
- **No Hardcoded Credentials**: Credentials are prompted at runtime or sourced securely via environment variables.
- **Safe for Sharing**: The toolkit contains no sensitive data and is designed for public repositories.
- **Permissions**: Use least-privilege accounts for audits (read-only where possible) to minimize risk.

## Troubleshooting
- **Connection Errors**: Verify `config.ini` settings and network connectivity to the domain controller.
- **Missing Dependencies**: Ensure all packages in `requirements.txt` are installed (`pip install -r requirements.txt`).
- **Event Log Access**: Some `monthly-audit` features (e.g., failed logins) require event log permissions; check AD security settings.
- **Output Issues**: If JSON output is malformed, check for script errors or contact the repository maintainer.

## Contributing
Contributions are welcome! Please submit pull requests or open issues on the GitHub repository for bug reports, feature requests, or improvements.
