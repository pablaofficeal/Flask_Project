# Environment Variables

```.env
SECRET_KEY=my_secret_key  # Secret key for session management
DATABASE_URL=sqlite:///test.db  # Database URL for SQLAlchemy

# Server Configuration
IP=0.0.0.0 # IP address to bind the server to
PORT=5000 # Port number to bind the server to
DEBUG=True # Whether to run the server in debug mode


# Google OAuth2 Configuration
GOOGLE_CLIENT_ID=####################################################################### # Google OAuth2 client ID
GOOGLE_CLIENT_SECRET=############################################  # Google OAuth2 client secret

# Create cookie config
SESSION_COOKIE_SAMESITE=None # SameSite policy for session cookie
SESSION_COOKIE_SECURE=False # Whether to set the session cookie as secure (HTTPS only)
SESSION_COOKIE_HTTPONLY=True # Whether to set the session cookie as HTTP-only
SESSION_COOKIE_KEY=your_secret_key  # Secret key for session cookie
SESSION_COOKIE_NAME=session # Name of the session cookie

# GitHub OAuth2 URLs configuration
GITHUB_AUTHORIZE_URL=https://github.com/login/oauth/authorize # GitHub OAuth2 authorize URL
GITHUB_TOKEN_URL=https://github.com/login/oauth/access_token # GitHub OAuth2 token URL
GITHUB_USER_URL=https://api.github.com/user # GitHub OAuth2 user URL
GITHUB_EMAILS_URL=https://api.github.com/user/emails # GitHub OAuth2 emails URL
GITHUB_REDIRECT_URI=http://localhost:5000/auth/github/callback # GitHub OAuth2 redirect URI


# GitHub OAuth2 Configuration
GITHUB_CLIENT_ID=#################### # GitHub OAuth2 client ID
GITHUB_CLIENT_SECRET=######################## # GitHub OAuth2 client secret


```