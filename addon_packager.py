import json
import zipfile
import os
import shutil

files_list = "packager_files.json"


def update_toml_verison(files_lsit):
    with open(files_lsit, "r") as f:
        data = json.load(f)

    version = data.get("addon_version")

    for file in data["files"]:
        if file.endswith(".toml"):
            with open(file, "r") as f:
                lines = f.readlines()

            for i, line in enumerate(lines):
                if line.startswith("version = ") or line.startswith("version="):
                    lines[i] = f'version = "{version}"\n'

            with open(file, "w") as f:
                f.writelines(lines)

            print(f"Version updated in '{file}'")


def pack_files_from_jazon(files_list):
    with open(files_list, "r") as f:
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


update_toml_verison(files_list)
pack_files_from_jazon(files_list)
