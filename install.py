import os
import json
import subprocess
import platform
import argparse

def get_package_manager():
    try:
        distro_info = subprocess.run(['lsb_release', '-i', '-r'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        output = distro_info.stdout.strip().split('\n')
        distro_name = output[0].split(':')[1].strip().lower()
        distro_version = output[1].split(':')[1].strip()
    except Exception as e:
        print(f"\033[91mError: Failed to determine the Linux distribution. {e}\033[0m")
        return None

    if distro_name in ["ubuntu", "debian"]:
        return "apt"
    elif distro_name in ["fedora", "centos", "rhel"]:
        return "dnf"
    elif distro_name in ["arch"]:
        return "pacman"
    else:
        print(f"\033[93mWarning: Unsupported Linux distribution ({distro_name} {distro_version}). Trying snap or flatpak...\033[0m")
        return None

def install_package(package_info, package_manager):
    if "installation_method" in package_info:
        if package_info["installation_method"] == "package-manager":
            package_name = package_info["package-name"]
            print(f"\033[92mInstalling package: {package_name}\033[0m")
            if package_manager == "apt":
                subprocess.run(["sudo", package_manager, "install", package_name])
            elif package_manager == "dnf":
                subprocess.run(["sudo", package_manager, "install", package_name])
            elif package_manager == "pacman":
                subprocess.run(["sudo", package_manager, "-S", package_name])
            else:
                print("\033[93mWarning: Unsupported package manager. Trying snap or flatpak...\033[0m")
                try_alternative_installation(package_info)

        elif package_info["installation_method"] == "script":
            for script in package_info["script"]:
                print(f"\033[92mRunning script: {script}\033[0m")
                subprocess.run(["bash", "-c", script])

def try_alternative_installation(package_info):
    # Try using snap as an alternative
    if "snap" in package_info.get("alternate_installation_methods", {}):
        snap_package = package_info["alternate_installation_methods"]["snap"]
        print(f"\033[92mTrying Snap alternative: {snap_package}\033[0m")
        subprocess.run(["sudo", "snap", "install", snap_package])
        return

    # Try using flatpak as an alternative
    if "flatpak" in package_info.get("alternate_installation_methods", {}):
        flatpak_package = package_info["alternate_installation_methods"]["flatpak"]
        print(f"\033[92mTrying Flatpak alternative: {flatpak_package}\033[0m")
        subprocess.run(["flatpak", "install", flatpak_package])
        return

    print("\033[91mNo alternative package manager found. Skipping installation.\033[0m")

def install_themes(theme_info):
    desktop_env = os.environ.get("DESKTOP_SESSION", "").lower()
    if not desktop_env:
        print("\033[91mDesktop environment not detected. Skipping theme installation.\033[0m")
        return

    if desktop_env in theme_info:
        theme_data = theme_info[desktop_env]
        git_repo = theme_data["git_repo"]
        installation_script = theme_data["installation_script"]

        print(f"\033[96mCloning theme repository: {git_repo}\033[0m")
        subprocess.run(["git", "clone", git_repo])

        print(f"\033[96mInstalling {desktop_env} theme\033[0m")
        for script in installation_script:
            subprocess.run(["bash", "-c", script], cwd=os.path.basename(git_repo))
    else:
        print(f"\033[91mNo theme available for {desktop_env}. Skipping theme installation.\033[0m")

def check_and_install_curl():
    if subprocess.run(["which", "curl"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0:
        package_manager = get_package_manager()
        if package_manager:
            print("\033[93mInstalling curl...\033[0m")
            subprocess.run(["sudo", package_manager, "install", "curl"])
        else:
            print("\033[91mCannot install curl automatically. Please install curl manually and re-run the script.\033[0m")
            exit(1)

def main():
    parser = argparse.ArgumentParser(description="Install packages and themes based on a JSON configuration file.")
    parser.add_argument("git_repo", type=str, help="Git repository URL")
    args = parser.parse_args()

    # Check and install curl if not present
    check_and_install_curl()

    json_url = f"{args.git_repo.rstrip('/')}/raw/main/systemConfig.json"
    try:
        # Download the JSON file using curl
        subprocess.run(["curl", "-o", "systemConfig.json", json_url], check=True)
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
                    print(f"\033[92mInstalling package: {package_name}\033[0m")
                    if package_manager:
                        subprocess.run(["sudo", package_manager, "install", package_name])
                    else:
                        print("\033[93mWarning: Unsupported package manager. Trying snap or flatpak...\033[0m")
                        try_alternative_installation(package_info)

        # Install themes
        install_themes(config_data["packages"]["themes"]["gnome"])

    except Exception as e:
        print(f"\033[91mAn error occurred: {e}\033[0m")

if __name__ == "__main__":
    main()

