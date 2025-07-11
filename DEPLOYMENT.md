# Vercel Deployment Guide for TP Adhikari Chatbot

## Files Updated for Vercel Compatibility

1. **`api/chat.py`** - Serverless function for handling chat requests
2. **`vercel.json`** - Vercel configuration file
3. **`requirements.txt`** - Python dependencies
4. **`static/js/script.js`** - Updated API endpoint to `/api/chat`

## Deployment Steps

### 1. Environment Variables Setup
In your Vercel dashboard, go to your project settings and add these environment variables:
- `GOOGLE_API_KEY` = your actual Gemini API key
- OR `GEMINI_API_KEY` = your actual Gemini API key

### 2. Company Content Update
Edit `api/chat.py` and replace the placeholder company_info with your actual company services content from the PDF.

### 3. Deploy to Vercel
1. Push your code to GitHub
2. Connect your GitHub repo to Vercel
3. Vercel will automatically deploy using the `vercel.json` configuration

### 4. Test the Deployment
- Your chatbot should be accessible at `https://your-project-name.vercel.app`
- The API endpoint will be at `https://your-project-name.vercel.app/api/chat`

## Troubleshooting

### If the API still doesn't work:
1. Check Vercel function logs for errors
2. Verify environment variables are set correctly
3. Ensure the API key is valid and has proper permissions
4. Check that the frontend is making requests to `/api/chat`

### Common Issues:
- **API Key Not Found**: Set `GOOGLE_API_KEY` in Vercel environment variables
- **CORS Errors**: The serverless function includes CORS headers
- **Function Timeout**: Gemini API calls should complete within Vercel's timeout limits

## File Structure for Vercel
```
chatbot/
├── api/
│   └── chat.py          # Serverless function
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── index.html           # Frontend
├── vercel.json          # Vercel config
├── requirements.txt     # Python dependencies
└── .env.example         # Environment variables template
```

## Next Steps
1. Add your actual company services content to the `company_info` variable in `api/chat.py`
2. Deploy to Vercel
3. Test the chatbot functionality
4. Monitor Vercel function logs for any issues
