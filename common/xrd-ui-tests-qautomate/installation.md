# Qautomate installation guide

Ubuntu 16.04 has Python2.7.12

1. Download and unzip Linux64-bit installer file
2. Install following SW packages from unzipped folder
    * Ubuntu 16.04
    * older Ubuntu versions

If problems installing Python modules, run "$ sudo apt-get update"

Finalize installation by logging off computer and logging in to make sure that environment variables are loaded correctly.

1. Environmental variable PYTHONPATH:
    * "/home/user/.local/lib/python2.7/site-packages/qautomate"
2. Environment variable PATH:
    * "/home/user/.local/lib/python2.7/site-packages/qautomate/webframework/resources"
