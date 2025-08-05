#!/bin/bash

echo "🚀 ZSchool Deployment Script"
echo "==========================="

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: docker-compose.yml not found. Run this script from the project root."
    exit 1
fi

# Check if git is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  Warning: You have uncommitted changes."
    read -p "Do you want to commit them now? (y/n): " commit_changes
    
    if [ "$commit_changes" = "y" ]; then
        git add .
        read -p "Enter commit message: " commit_msg
        git commit -m "$commit_msg"
    fi
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin main

echo ""
echo "✅ Code pushed to GitHub!"
echo ""
echo "🎯 Next Steps for Railway Deployment:"
echo "1. Go to https://railway.app"
echo "2. Sign up with GitHub"
echo "3. Click 'New Project' → 'Deploy from GitHub repo'"
echo "4. Select your repository"
echo "5. Railway will auto-detect all services"
echo ""
echo "📝 Don't forget to add these environment variables in Railway:"
echo ""
echo "Backend Service:"
echo "- HF_TOKEN=your_huggingface_token"
echo "- XAI_TOKEN=your_xai_token" 
echo "- CANVAS_BEARER_TOKEN=your_canvas_token"
echo "- CANVAS_USER_ID=your_canvas_user_id"
echo "- ENVIRONMENT=production"
echo ""
echo "Frontend Service:"
echo "- REACT_APP_API_URL=https://zschool-backend-production.up.railway.app"
echo "- REACT_APP_ENVIRONMENT=production"
echo ""
echo "🎉 Your app will be live at:"
echo "- Frontend: zschool.up.railway.app"
echo "- Backend: zschool-backend-production.up.railway.app" 