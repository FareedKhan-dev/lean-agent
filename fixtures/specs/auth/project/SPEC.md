# Sign-in

`Auth` in `accounts/auth.py` signs users in.

- `Auth(clock=time.time)`: the clock is passed in so tests can control time.
- `register(username, password)` stores a user. Passwords are never stored as given: keep a salted PBKDF2-SHA256 hash. Registering a username that exists raises ValueError; so does a password shorter than 10 characters.
- `login(username, password)` returns a session token (a random, URL-safe string) that is valid for one hour. A wrong password and an unknown username both raise PermissionError, with the same message.
- After 5 failed logins for a username, logins for it are refused for 15 minutes (PermissionError), even with the right password.
- `user_for(token)` returns the username a valid token belongs to, or None if the token is unknown or has expired.
