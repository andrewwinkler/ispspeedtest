# ISP Speed Test

### **Requirements**

- Python 3
- `speedtest-cli`

### **Installation**

```
git clone https://github.com/andrewwinkler/ispspeedtest.git && cd ispspeedtest
virtualenv -p python3 venv/
source venv/bin/activate
pip install google-api-python-client
pip install google-auth-oauthlib
```

Save the OAuth 2.0 `credentials.json` file from [Google APIs Credentials](https://console.developers.google.com/apis/credentials) into `ispseedtest`

### **Use**

Run `./test_isp_speed.py`

_Note:_

On the first run the credentials need to be authorized against a Google Drive account.
This will save a `token.pickle` file for all subsequent script executions.