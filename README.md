# bugout-python
Python client library for Bugout API

```python
from bugout.app import Bugout

def main():
    bugout = Bugout(brood_api_url="http://localhost:9001", spire_api_url="http://localhost:9002")
    user = bugout.get_user("<user token id>")
    group = bugout.get_group("<user token id>", "<group id>")

if __name__ == "__main__":
    main()
```
