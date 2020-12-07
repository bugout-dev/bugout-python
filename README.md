# bugout-python
Python client library for Bugout

```python
from bugout.user import User
from bugout.group import Group
from bugout.app import Bugout

bugout = Bugout(url="http://localhost", port="433")
bugout_user = User(bugout)
bugout_group = Group(bugout)

def main():
    print(bugout_user.get_user(token="<user token>"))
    print(bugout_group.get_group(group_id="<group id>",token="<user token>"))

if __name__ == "__main__":
    main()

```