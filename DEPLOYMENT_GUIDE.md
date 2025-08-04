# ZSchool Deployment Guide 🚀

## Quick Start: Railway.app (Recommended)

**Why Railway?** Free tier, automatic HTTPS, GitHub integration, zero configuration.

### 1. **Deploy to Railway** ⚡ (5 minutes)

```bash
# Run the deployment script
./scripts/deploy.sh
```

1. Go to [railway.app](https://railway.app) and sign up with GitHub
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your `zschool` repository
4. Railway will auto-detect all services (frontend, backend, database)

### 2. **Add Environment Variables**

In Railway dashboard, add these to each service:

**Backend Service:**
```
HF_TOKEN=your_huggingface_token
XAI_TOKEN=your_xai_token
CANVAS_BEARER_TOKEN=your_canvas_token
CANVAS_USER_ID=your_canvas_user_id
ENVIRONMENT=production
```

**Frontend Service:**
```
REACT_APP_API_URL=https://your-backend-url.railway.app
REACT_APP_ENVIRONMENT=production
```

### 3. **Your App is Live!** 🎉
- Frontend: `https://zschool-frontend.railway.app`
- Backend: `https://zschool-backend.railway.app`

---

## Alternative Deployments

### Option 2: DigitalOcean App Platform 🌊

**Cost:** $12/month, includes $200 free credit

1. **Push the DigitalOcean config:**
   ```bash
   git add .do/app.yaml
   git commit -m "Add DigitalOcean config"
   git push origin main
   ```

2. **Deploy:**
   - Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
   - Create App from GitHub
   - Select repository
   - It will detect the `.do/app.yaml` configuration

3. **Add Secret Environment Variables** in DO dashboard

### Option 3: VPS Deployment 🔧

**Cost:** $5-20/month, full control

#### Prerequisites:
- Ubuntu/Debian VPS with Docker installed
- Domain name pointing to your VPS

#### Deploy:

1. **Copy files to server:**
   ```bash
   scp -r . user@your-server:/opt/zschool/
   ```

2. **Set up environment:**
   ```bash
   ssh user@your-server
   cd /opt/zschool
   cp .env.production.template .env.production
   nano .env.production  # Fill in your values
   ```

3. **Deploy with Docker:**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

4. **Set up SSL** (Let's Encrypt):
   ```bash
   sudo apt install certbot
   sudo certbot --nginx -d yourdomain.com
   ```

---

## Environment Variables Needed

### 🔑 **Required Tokens**

| Variable | Where to Get It | Purpose |
|----------|----------------|---------|
| `XAI_TOKEN` | [X.AI Console](https://console.x.ai/) | AI lesson conversion |
| `HF_TOKEN` | [Hugging Face](https://huggingface.co/settings/tokens) | AI models |
| `CANVAS_BEARER_TOKEN` | Canvas LMS Settings | Canvas API access |
| `CANVAS_USER_ID` | Canvas Profile | User identification |

### 📊 **Getting Canvas Tokens**

1. **Canvas Bearer Token:**
   - Log into Canvas LMS
   - Go to Account → Settings
   - Scroll to "Approved Integrations"
   - Click "+ New Access Token"
   - Copy the generated token

2. **Canvas User ID:**
   - In Canvas, go to your profile
   - Look at the URL: `canvas.instructure.com/users/12345`
   - The number `12345` is your User ID

---

## Database Setup

### Railway/DigitalOcean
- ✅ **Automatic** - PostgreSQL database is provisioned automatically

### VPS Deployment
- ✅ **Docker Compose** - PostgreSQL runs in container
- 📁 **Backups stored** in `./backups/` directory

---

## Health Monitoring

All deployments include health check endpoints:

**Backend Health:** `https://your-backend-url/health`

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "database": "healthy", 
    "ai_service": "healthy",
    "canvas_client": "healthy"
  },
  "version": "1.0.0"
}
```

---

## SSL/HTTPS

### Railway/DigitalOcean
- ✅ **Automatic HTTPS** - Handled by platform

### VPS Deployment  
- 🔧 **Manual setup** with Let's Encrypt (instructions included)

---

## Scaling & Performance

### Free Tier Limits
- **Railway:** 500 hours/month, 1GB RAM
- **DigitalOcean:** $200 credit (~4 months free)

### Production Scaling
- **Database:** Can handle 1000+ concurrent users
- **AI Processing:** Limited by X.AI API quotas
- **Caching:** Persistent storage prevents re-processing

---

## Troubleshooting

### Common Issues

**1. AI Conversion Fails**
```bash
# Check logs
docker logs zschool_backend_prod

# Verify tokens
curl https://your-backend-url/health
```

**2. Database Connection Issues**
```bash
# Check database status
docker logs zschool_db_prod

# Verify connection string
echo $DATABASE_URL
```

**3. Frontend Can't Connect to Backend**
```bash
# Check API URL environment variable
echo $REACT_APP_API_URL

# Test backend directly
curl https://your-backend-url/health
```

### Support

- **Railway:** [docs.railway.app](https://docs.railway.app)
- **DigitalOcean:** [docs.digitalocean.com](https://docs.digitalocean.com)
- **Health Check:** `GET /health` endpoint

---

## Cost Comparison

| Platform | Free Tier | Paid | Best For |
|----------|-----------|------|----------|
| **Railway** | 500 hrs/month | $5/month | Development & small projects |
| **DigitalOcean** | $200 credit | $12/month | Production apps |
| **VPS** | None | $5-20/month | Full control & customization |

## 🏆 **Recommendation**

**Start with Railway.app** - it's free, automatic, and perfect for testing your deployment. You can always migrate to DigitalOcean or VPS later for production scaling.

**Deploy now:**
```bash
./scripts/deploy.sh
``` 