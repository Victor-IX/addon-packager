# Addon Packager

This Python script automates the process of packaging Blender addons by updating version information in TOML files and creating a zip package with only the addon files

## Prerequisites

Ensure you have Python installed on your system.

## Usage

1. Place the `addon-packager` directory containing the `addon_info.json` file and other addon files in the root directory.
2. Execute the script in the root directory where the `addon-packager` folder resides.

```bash
python addon_packager.py
```

## Functionality

- Initializes `addon_info.json` if not found.
- Updates version information in TOML files.
- Packs addon files into a zip archive.


## Important Notes

- Ensure that the `addon_info.json` file is correctly formatted and contains necessary addon information.
