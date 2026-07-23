---
name: Imported dependency files
description: Environment-specific handling for imported Python dependency manifests.
---

Imported repositories may contain a UTF-16 `requirements.txt`, which can make the package manager install dependencies but fail when it rereads the manifest. Normalize the file to UTF-8 before relying on automated dependency setup.

**Why:** The package manager expects a standard text requirements file and does not consistently handle the imported encoding.

**How to apply:** Check the encoding of an imported Python dependency manifest before installation; preserve the declared package versions while converting only the file encoding.