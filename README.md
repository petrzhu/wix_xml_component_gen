# wix_xml_component_gen
Python script for generating component &amp; reference elements for WiX Toolset.

# Purpose
This script's purpose is to generate the list of components combined in the components group and to generate components' references Fragment element.

The generated content is shown in the console output.

# Usage
```python wix_xml_component_gen.py -d {DIRECTORY_WITH_FILES} -e {YOUR_EXTENSIONS_NAME}```

It is possible to pass several values as arguments, example:

```python wix_xml_component_gen.py -d C:\dir1 C:\dir2 -e exe manifest config```

Modify **extensionIdDict** dictionary to add or change IDs of ComponentGroup dedicated for different type of files.
