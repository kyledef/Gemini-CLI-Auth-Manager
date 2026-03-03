# Gemini CLI Auth Manager

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-yellow.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-2.2-brightgreen.svg)

**Gemini CLI Auth Manager** is a lightweight tool designed for the Google Gemini CLI environment. It supports instant multi-account switching, **automatic rotation on quota exhaustion**, and **unified account pool management**!

> 📖 [中文版本 (Chinese Version)](./README-CN.md)

---

## ✨ Features

- **Instant Switching**: Switch between multiple accounts in seconds.
- **Auto-Backup**: Automatically saves your credentials upon switching.
- **🆕 Native OAuth Login**: One-click browser login to officially authenticate and capture accounts directly to the pool.
- **🆕 Custom Model Strategy**: Support for regex-based model rotation (e.g., `gemini-2.5.*`).
- **Quota Pre-check**: Real-time quota monitoring via Google API, auto-switches before exhaustion.
- **Pool Management**: Unified interface to view, add, and remove accounts.
- **Interactive Menu**: Visual configuration interface for easy management.
- **Slash Command**: Seamlessly integrated as `/change` in Gemini CLI.

---

## 🚀 Installation

```bash
git clone https://github.com/Besty0728/Gemini-CLI-Auth-Manager.git
cd gemini-auth-manager
python install.py
```

### Dependencies

```bash
pip install requests
```

### How to Update

If you have an older version installed:

1. Run `git pull` to get the latest code.
2. Run `python install.py` again (Recommended, updates hooks).

---

## 🛠 Usage

### Quick Commands

```bash
# List accounts
gchange

# Switch account
gchange 1                    # Switch to account #1
gchange user@gmail.com       # Switch by email
gchange next                 # Switch to next account

# Interactive Menu (Recommended)
gchange menu

# Pool Management
gchange pool                 # View pool
gchange pool login           # Login & capture account (interactive)
gchange pool login user@gmail.com  # Login specific email
gchange pool remove 2        # Remove account #2
gchange pool import ~/creds.json   # Import credentials file

# Configuration
gchange config               # View config
gchange config enabled true  # Enable auto-switch
gchange config threshold 10  # Set threshold to 10%
```

### Slash Command (Inside Gemini CLI)

```text
/change           # List accounts
/change 1         # Switch to account #1
/change next      # Switch to next account
```

### Quota Query Tool

```bash
# Query current account quota directly
python quota_api_client.py
```

Example Output:
```
📊 Gemini CLI Quota Status
======================================================================
Model                          Remaining       Resets In
----------------------------------------------------------------------
gemini-2.5-flash               🟢 93.3%        (10h 20m)
gemini-3-pro-preview           🟡 33.5%        (1h 10m)
gemini-2.5-pro                 🟡 33.5%        (1h 10m)
======================================================================
```

---

## 🎯 Interactive Menu

Run `gchange menu` to open the configuration interface:

```
  Menu:
  ----------------------------------------
  1. Switch Account
  2. Switch to Next Account
  3. Configure Auto-Switch
  4. Toggle Auto-Switch (Enable/Disable)
  5. Manage Account Pool
  0. Exit
```

---

## 🔄 Quota Pre-check (BeforeAgent Hook)

The system monitors quota status in real-time via the Google Code Assist API:

```
User sends request
    ↓
BeforeAgent Hook triggers
    ↓
Calls Google API for remaining quota %
    ↓
Detects Pro models < 10%
    ↓
Automatically calls gchange next
    ↓
Shows switch notification, User resends request
```

### Configuration

Edit `~/.gemini/auth_config.json`:

```json
{
  "auto_switch": {
    "enabled": true,
    "strategy": "custom",
    "custom_model_pattern": "gemini-2.5.*",
    "threshold": 10,
    "cache_minutes": 5
  }
}
```

| Option | Description | Default |
|--------|-------------|---------|
| `enabled` | Enable auto-switch | `true` |
| `strategy` | Switch strategy (`gemini3-first`, `conservative`, `custom`) | `gemini3-first` |
| `custom_model_pattern` | Regex pattern for custom strategy | `""` |
| `threshold` | Quota threshold (%) | `10` |
| `cache_minutes` | Cache duration (min) | `5` |

### Note

- **Restart Required**: Due to Gemini CLI limitations, you must restart the CLI after an account switch for the new credentials to take effect.
- **Notification**: You will see a prompt to resend your request after a successful switch.

---

## ❓ FAQ

### Q: Why do I need to restart CLI after switching?

Gemini CLI caches OAuth credentials in memory upon startup. Switching the `oauth_creds.json` file requires a process restart to reload the new credentials.

### 4. Auto-Restart (Optional)

Since Gemini CLI does not support hot-reloading credentials, a restart is required after switching accounts.
This tool provides an auto-restart feature, but it is **Disabled by Default**.

You can enable it via the menu:
```bash
gchange menu
# Select 7. Toggle Auto-Restart
```
When enabled, the script will automatically close the current window and spawn a new Gemini CLI window upon quota exhaustion.

---

## 🔧 Technical Details

### 1. Single-File Switching
Gemini CLI only recognizes `~/.gemini/oauth_creds.json`.
This tool maintains copies of credentials in `~/.gemini/auth_profiles/`. When switching, it performs a **"Backup -> Overwrite -> Clear Cache"** operation to trick the CLI into loading the new credentials.

### 2. Cache & Environment Variables
To prevent the CLI from reading stale Windows Keychain cache, this tool sets `GEMINI_FORCE_FILE_STORAGE=true` during installation. This forces the CLI to use file-based storage, which our script forces to reload by deleting the cache file on every switch.

### 3. Token Auto-Renewal
As long as your `oauth_creds.json` contains a `refresh_token`, Gemini CLI handles Access Token renewal automatically. Your imported credentials should work indefinitely without frequent manual logins.

### Q: How to handle 403 VALIDATION_REQUIRED?

This is a Google Account validation issue.
1. Visit the link provided in the error.
2. Login and verify your account.
3. Or delete credentials and re-login: `rm ~/.gemini/oauth_creds.json && gemini`

---

## 📁 File Structure

```
~/.gemini/
├── oauth_creds.json          # Current credentials
├── auth_config.json          # Configuration
├── gemini_cli_auth_manager.py # Core script
├── gchange.bat               # Command launcher
├── accounts/                 # Account pool
│   ├── user1@gmail.com.json
│   └── ...
├── hooks/
│   ├── quota_pre_check.py    # BeforeAgent Hook
│   └── quota_auto_switch.py  # AfterAgent Hook
└── commands/
    └── change.toml           # Slash command config
```

---

## ❤️ Contributing

Issues and PRs are welcome!
