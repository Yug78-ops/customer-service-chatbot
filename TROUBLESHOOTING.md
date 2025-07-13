# Vercel Deployment Troubleshooting

## Current Issue: 404 NOT_FOUND on API endpoints

The 404 errors on all API endpoints suggest that Vercel is not properly recognizing or deploying the Python serverless functions.

## Steps to Fix:

### 1. **Verify Environment Variables in Vercel Dashboard**
- Go to your Vercel project dashboard
- Navigate to Settings → Environment Variables
- Add: `GOOGLE_API_KEY` with value: `AIzaSyABZoKxOrz7RQM4O3Bzgzy4SOszNSQhNpI`

### 2. **Force Redeploy**
- In Vercel dashboard, go to Deployments
- Click on the latest deployment
- Click "Redeploy" button
- OR push a small change to trigger new deployment

### 3. **Check Build Logs**
- Go to Vercel dashboard → Deployments
- Click on the latest deployment
- Check the "Build Logs" tab for any Python/API related errors
- Look for any failed builds in the `/api` directory

### 4. **Test Individual Endpoints**
After deployment, test these URLs:
- `https://your-app.vercel.app/api/hello` (simplest test)
- `https://your-app.vercel.app/api/test`
- `https://your-app.vercel.app/api/debug`
- `https://your-app.vercel.app/api/chat`

### 5. **Alternative: Deploy Using Vercel CLI**
```bash
npm i -g vercel
cd chatbot
vercel
```

## Key Changes Made:

1. **Simplified vercel.json** - explicit builds and routes for each API file
2. **Fixed Python handlers** - using proper BaseHTTPRequestHandler format
3. **Removed Flask conflicts** - eliminated app.py Flask code
4. **Added test endpoints** - hello.py for basic connectivity test
5. **CORS headers** - proper cross-origin support

## If Still Getting 404s:

1. Check if Python runtime is enabled in your Vercel account
2. Verify the project is connected to the correct GitHub repository
3. Make sure all API files are committed and pushed to GitHub
4. Try deploying from a fresh clone of the repository

## Expected Working URLs:
- Main app: `https://your-app.vercel.app/`
- API test: `https://your-app.vercel.app/api/hello`
- Chat API: `https://your-app.vercel.app/api/chat`
