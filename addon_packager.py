import json
import zipfile
import os
import shutil

addon_info = "addon_info.json"
addon_packager_path = "addon-packager/"


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def addon_info_initialization(addon_info):
    if not os.path.exists(addon_info):
        addon_info_path = os.path.join(addon_packager_path, addon_info)

        if not os.path.exists(addon_info_path):
            print(
                f"{bcolors.FAIL}Error: {addon_info} not found. Expected path is {addon_info_path}.{bcolors.ENDC}"
            )
            return

        shutil.copy(addon_info_path, addon_info)
        print(f"{addon_info} created in the addon repo.")


def update_toml_verison(addon_info):
    with open(addon_info, "r") as f:
        data = json.load(f)

    version = data.get("addon_version")

    for file in data["files"]:
        if not file.endswith(".toml"):
            continue

        if not os.path.exists(file):
            current_working_directory = os.getcwd()
            print(
                f"{bcolors.FAIL}Error: No blender-manifest.toml file found in {current_working_directory}.{bcolors.ENDC}"
            )
            print(
                f"{bcolors.FAIL}Make sure you are runing the script from the addon repo.{bcolors.ENDC}"
            )
            raise SystemExit

        with open(file, "r") as f:
            lines = f.readlines()

            for i, line in enumerate(lines):
                if not line.startswith("version = ") and not line.startswith(
                    "version="
                ):
                    continue

                version_numbers = line.split("=")[1].strip().strip('"').split(".")
                major, minor, patch = map(int, version_numbers)
                vmajor, vminor, vpatch = map(int, version.split("."))

                if major <= vmajor and minor <= vminor and patch <= vpatch:
                    lines[i] = f'version = "{version}"\n'
                    with open(file, "w") as f:
                        f.writelines(lines)
                        print(f"Version updated in {file}")
                else:
                    print(
                        f"{bcolors.WARNING}Warrning: Version in {file} is higher than the version in the {addon_info}.{bcolors.ENDC}"
                    )
                    print(
                        f"{bcolors.OKCYAN}    1. {addon_info} version: {bcolors.BOLD}{version}{bcolors.ENDC}"
                    )
                    print(
                        f"{bcolors.OKGREEN}    2. {file} version: {bcolors.BOLD}{major}.{minor}.{patch}{bcolors.ENDC}"
                    )
                    
                    while True:
                        override_value = input(
                            f"What version do you want to keep? ({bcolors.OKCYAN}{bcolors.BOLD}1{bcolors.ENDC}|{bcolors.OKGREEN}{bcolors.BOLD}2{bcolors.ENDC}): "
                        )

                        if override_value == "1":
                            lines[i] = f'version = "{version}"\n'
                            with open(file, "w") as f:
                                f.writelines(lines)
                                print(f"Version updated in {file}")
                            break
                        elif override_value == "2":
                            print(f"Version in {file} not updated.")
                            break
                        else:
                            print(f"{bcolors.FAIL}Invalid input. Please enter 1 or 2 for the version you want to keep.{bcolors.ENDC}")
                            print(
                                f"{bcolors.OKCYAN}    1. {addon_info} version: {bcolors.BOLD}{version}{bcolors.ENDC}"
                            )
                            print(
                                    f"{bcolors.OKGREEN}    2. {file} version: {bcolors.BOLD}{major}.{minor}.{patch}{bcolors.ENDC}"
                            )


def pack_files_from_jazon(addon_info):
    with open(addon_info, "r") as f:
        data = json.load(f)

    addon_name = data.get("addon_name")
    version = data.get("addon_version")
    output_zip = f"{addon_name}-{version}.zip"

    if os.path.exists(addon_name):
        print(f"Error: Folder '{addon_name}' already exists.")
        return

    os.makedirs(addon_name)

    for file in data["files"]:
        if os.path.exists(file):
            shutil.copy(file, os.path.join(addon_name, os.path.basename(file)))
        else:
            print(f"File not found: {file}")

    if os.path.exists(output_zip):
        os.remove(output_zip)
        print(f"Zip file '{output_zip}' have been override.")

    with zipfile.ZipFile(output_zip, "w") as zipf:
        for root, _, files in os.walk(addon_name):
            for file in files:
                zipf.write(
                    os.path.join(root, file),
                    os.path.relpath(os.path.join(root, file), addon_name),
                )

    shutil.rmtree(addon_name)

    print(f"Addon packed to '{output_zip}'")


addon_info_initialization(addon_info)
update_toml_verison(addon_info)
pack_files_from_jazon(addon_info)
