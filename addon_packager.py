import json
import zipfile
import os
import shutil

addon_info = "addon_info.json"
addon_packager_path = "addon-packager/"


def addon_info_initialization(addon_info):
    if not os.path.exists(addon_info):
        addon_info_path = os.path.join(addon_packager_path, addon_info)

        if not os.path.exists(addon_info_path):
            print(
                f"Error: {addon_info} not found. Expected path is '{addon_info_path}'."
            )
            return

        shutil.copy(addon_info_path, addon_info)
        print(f"{addon_info} created in the addon repo.")

def update_toml_verison(addon_info):
    with open(addon_info, "r") as f:
        data = json.load(f)

    version = data.get("addon_version")

    for file in data["files"]:
        if file.endswith(".toml"):
            if not os.path.exists(file):
                current_working_directory = os.getcwd()
                print(f"Error: No blender-manifest.toml file found in {current_working_directory}. ")
                print("Check if you are runing the script from the addon repo.")
                raise SystemExit
            
            with open(file, "r") as f:
                lines = f.readlines()

            for i, line in enumerate(lines):
                if line.startswith("version = ") or line.startswith("version="):
                    lines[i] = f'version = "{version}"\n'

            with open(file, "w") as f:
                f.writelines(lines)

            print(f"Version updated in {file}")
            

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
