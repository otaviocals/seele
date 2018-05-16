# Splunk Enterprise Environment Lab Engine
### Written by Otavio Cals
---
## Overview

SEELE is a project for quickly building and deploying entire Splunk environments automatically.

With SEELE, one can deploy and configure Search Heads, Indexers and Forwarders throughout as many machines as necessary.

SEELE is written in Python and use SSH connections to configure remotely the Splunk servers.

---
## Requirements

- Python 3
- Paramiko library

---
## ToDos

- Clustering options.
- Compatibility with Splunk Cloud
- Add other Splunk components (Heavy Forwarders, License Masters, Master Nodes, etc...).
- Further customization options for current nodes.
- Data logging features.
- Configurations encryption.
- Add GUI using Kivy or other python GUI library.