
## Step 1 - Extract authentication routes

Date: 2026-07-27

### Changes
- Created app/routes package.
- Added app/routes/__init__.py.
- Created app/routes/auth.py.
- Moved Logout route.
- Moved Signup route.

### Why
Authentication endpoints are independent from tweet logic.
Separating them reduces the size of routes.py and makes the project easier to maintain.

### Status
✅ Project still runs after the change.

