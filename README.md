# Linux System Configurator

Linux System Configurator is a Python script that automates the installation of packages and themes on different Linux distributions based on a JSON configuration file.

## Requirements

- Python 3.x
- Curl (to download the JSON configuration file)

## Usage

1. Clone the repository:

```shell
git clone https://github.com/joshua-cotugno/LinuxSystemConfigurator.git
cd LinuxSystemConfigurator
```

2. Run the script, providing the Git repository URL as an argument:

```shell
python3 script.py https://github.com/joshua-cotugno/LinuxSystemConfigurator
```

## Configuration

The script uses a JSON configuration file to specify the packages and themes to be installed. The `systemConfig.json` file is located in the root directory of the repository. The file is organized into two main sections:

1. **Packages**: Contains the package installation information, including the package manager, installation method, package names, and alternate installation methods (e.g., snap, flatpak).
```json
  "packages": {
    "requirements": {
      "git": {
        "installation_method": "package-manager",
        "package-name": "git",
        "alternate_installation_methods": {
          "snap": "git",
          "flatpak": "org.gnome.git"
        }
      },
      "code": {
        "installation_method": "script",
        "script": [
          "script in",
          "individual lines"
        ]
      }
    }
  },
```
2. **Themes**: Contains the theme installation information, including the Git repositories and installation scripts for different theme types.
```json
  "themes": {
    "gnome": {
      "main_theme": {
        "git_repo": "https://github.com/a-user/theme.git",
        "installation_script": [
          "cd theme-dir",
          "cp * ~/.themes"
        ]
      },
      "icon_theme": {
        "git_repo": "https://github.com/a-user/icon-theme.git",
        "installation_script": [
          "cd icon-theme-dir",
          "cp * ~/.icons"
        ]
      },
      "other_themes": {
        "Theme Type Name":{
            "git_repo": "https://github.com/a-user/theme.git",
            "installation_script": [
                "./install-theme.sh"
            ]
        }
      }
    },
    "kde":{}
  }
}
```

## Supported Package Managers

The script currently supports the following package managers for different Linux distributions:

- `apt`: Debian and Ubuntu-based systems
- `dnf`: Fedora, CentOS, and RHEL-based systems
- `pacman`: Arch Linux

If your distribution is not explicitly supported, the script will try to use `snap` and `flatpak` as alternative package managers if specified in the JSON configuration.

## Contribution

Contributions to the project are welcome! If you find a bug or have a suggestion for improvement, please open an issue or submit a pull request.

## Disclaimer

Please use this script with caution and review the JSON configuration before running it on your system. The script will install packages and themes as specified in the configuration, which may modify your system's settings. Make sure to have the necessary permissions to run package manager commands with `sudo`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
