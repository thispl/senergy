# You'll need to install PyJWT via pip 'pip install PyJWT' or your project packages file

import jwt
import time

METABASE_SITE_URL = "http://206.189.140.171:3000"
METABASE_SECRET_KEY = "574c106f7db072a5e12e0349f541f02aab275d533be6b549371b5c027137c241"

payload = {
  "resource": {"dashboard": 1},
  "params": {
    
  },
  "exp": round(time.time()) + (60 * 10) # 10 minute expiration
}
token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + token.decode("utf8") + "#bordered=true&titled=true"
