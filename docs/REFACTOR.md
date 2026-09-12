
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


## Step 2 - Extract login route

### Changes
- Moved Login endpoint to app/routes/auth.py.

### Why
Authentication logic should remain together in one module instead of being mixed with tweet and profile features.

### Status
✅ Import successful.

## Step 2 - Extract Login route

### Changes
- Moved Login route from routes.py to routes/auth.py.
- Updated endpoint references to Blueprint format (main.Login).

### Why
Authentication endpoints should live in one module.
Using Blueprint-qualified endpoints avoids BuildError after refactoring.

### Status
✅ Login route extracted successfully.


## Step 3 - Extract ForgetPassword route

### Changes
- Moved ForgetPassword route to app/routes/auth.py.

### Why
Password recovery belongs to the authentication module.

### Status
✅ Route extracted.


## Step 4 - Extract password recovery

### Changes
- Moved ForgetPassword and ResetPassword to app/routes/auth.py.
- Updated blueprint endpoint references.

### Why
Authentication-related routes are now grouped together, reducing the size of routes.py and improving maintainability.

### Status
✅ Auth module now contains:
- Logout
- Signup
- Login
- ForgetPassword
- ResetPassword

