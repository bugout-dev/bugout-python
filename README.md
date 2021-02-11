# bugout-python
Python client library for Bugout API

## Setup
- Add variables from `sample.env` in you development environment
```bash
export BUGOUT_TIMEOUT_SECONDS=5
```

```python
from bugout.app import Bugout

def main():
    bugout = Bugout(brood_api_url="http://localhost:9001", spire_api_url="http://localhost:9002")
    
    user = bugout.get_user(<user token ID>)
    print(f"User name is {user.username}")
    
    group = bugout.get_group(<user token ID>, <group ID>)
    
    journal = bugout.get_journal(<user token ID>, <journal ID>)
    entry = bugout.get_entry(<user token ID>, <journal ID>, <entry ID>)
    
    search_res = bugout.search(<user token ID>, <journal ID>, query="your query", content=False)

if __name__ == "__main__":
    main()
```
