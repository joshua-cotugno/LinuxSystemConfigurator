import os
import json
import subprocess
import platform
import argparse
from colorama import Fore, Style

def get_package_manager():
    distro = platform.linux_distribution(full_distribution_name=False)[0].lower()
    if distro in ["ubuntu", "debian"]:
        return "apt"
    elif distro in ["fedora", "centos", "rhel"]:
        return "dnf"
    elif distro in ["arch"]:
        return "pacman"
    else:
        return None

def install_package(package_info, package_manager):
    if "installation_method" in package_info:
        if package_info["installation_method"] == "package-manager":
            package_name = package_info["package-name"]
            print(f"{Fore.GREEN}Installing package: {package_name}{Style.RESET_ALL}")
            if package_manager == "apt":
                subprocess.run(["sudo", package_manager, "install", package_name])
            elif package_manager == "dnf":
                subprocess.run(["sudo", package_manager, "install", package_name])
            elif package_manager == "pacman":
                subprocess.run(["sudo", package_manager, "-S", package_name])
            else:
                print(f"{Fore.YELLOW}Warning: Unsupported package manager. Trying snap or flatpak...{Style.RESET_ALL}")
                try_alternative_installation(package_info)

        elif package_info["installation_method"] == "script":
            for script in package_info["script"]:
                print(f"{Fore.GREEN}Running script: {script}{Style.RESET_ALL}")
                subprocess.run(["bash", "-c", script])

def try_alternative_installation(package_info):
    # Try using snap as an alternative
    if "snap" in package_info.get("alternate_installation_methods", {}):
        snap_package = package_info["alternate_installation_methods"]["snap"]
        print(f"{Fore.GREEN}Trying Snap alternative: {snap_package}{Style.RESET_ALL}")
        subprocess.run(["sudo", "snap", "install", snap_package])
        return

    # Try using flatpak as an alternative
    if "flatpak" in package_info.get("alternate_installation_methods", {}):
        flatpak_package = package_info["alternate_installation_methods"]["flatpak"]
        print(f"{Fore.GREEN}Trying Flatpak alternative: {flatpak_package}{Style.RESET_ALL}")
        subprocess.run(["flatpak", "install", flatpak_package])
        return

    print(f"{Fore.RED}No alternative package manager found. Skipping installation.{Style.RESET_ALL}")

def install_themes(theme_info):
    for theme_type, theme_data in theme_info.items():
        git_repo = theme_data["git_repo"]
        installation_script = theme_data["installation_script"]

        print(f"{Fore.CYAN}Cloning theme repository: {git_repo}{Style.RESET_ALL}")
        subprocess.run(["git", "clone", git_repo])

        print(f"{Fore.CYAN}Installing {theme_type} theme{Style.RESET_ALL}")
        for script in installation_script:
            subprocess.run(["bash", "-c", script], cwd=os.path.basename(git_repo))

def main():
    parser = argparse.ArgumentParser(description="Install packages and themes based on a JSON configuration file.")
    parser.add_argument("git_repo", type=str, help="Git repository URL")
    args = parser.parse_args()

    json_url = f"{args.git_repo.rstrip('/')}/raw/main/systemConfig.json"
    try:
        # Download the JSON file using curl
        subprocess.run(["curl", "-o", "systemConfig.json", json_url])
        with open("systemConfig.json", "r") as file:
            config_data = json.load(file)

        package_manager = get_package_manager()

        # Install packages
        for package_type, package_data in config_data["packages"]["requirements"].items():
            if package_type == "all":
                for package_name, package_info in package_data.items():
                    if package_info["installation_method"] == "flatpak":
                        install_flatpak(package_info)
                    else:
                        install_package(package_info, package_manager)
            else:
                for package_name in package_data:
                    print(f"{Fore.GREEN}Installing package: {package_name}{Style.RESET_ALL}")
                    if package_manager:
                        subprocess.run(["sudo", package_manager, "install", package_name])
                    else:
                        print(f"{Fore.YELLOW}Warning: Unsupported package manager. Trying snap or flatpak...{Style.RESET_ALL}")
                        try_alternative_installation(package_info)

        # Install themes
        install_themes(config_data["packages"]["themes"]["gnome"])

    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
