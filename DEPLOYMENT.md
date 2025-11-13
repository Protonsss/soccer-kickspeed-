# 🚀 KickSpeed Pro - Deployment Guide

**PROPRIETARY SOFTWARE** - All deployment configurations are confidential.

## Architecture

- **Frontend**: Next.js → Deploy to Vercel
- **Backend**: FastAPI + ML → Deploy to Railway/Render/Fly.io

## Option 1: Vercel + Railway (Recommended) ⭐

### Step 1: Deploy Backend to Railway

1. **Create Railway Account**: https://railway.app
2. **Install Railway CLI**:
   ```bash
   npm i -g @railway/cli
   ```

3. **Login and Deploy**:
   ```bash
   cd backend
   railway login
   railway init
   railway up
   ```

4. **Configure Environment**:
   - Railway will auto-detect the Dockerfile
   - Set environment variables in Railway dashboard:
     ```
     PORT=8000
     UPLOAD_DIR=/app/uploads
     ```

5. **Get Backend URL**:
   - Railway generates a URL like: `https://your-app.railway.app`
   - Copy this URL for frontend configuration

### Step 2: Deploy Frontend to Vercel

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Deploy**:
   ```bash
   cd frontend
   vercel
   ```

3. **Configure Environment Variables** in Vercel Dashboard:
   - Go to: Project Settings → Environment Variables
   - Add:
     ```
     NEXT_PUBLIC_API_URL=https://your-backend.railway.app
     ```

4. **Redeploy** to apply environment variables:
   ```bash
   vercel --prod
   ```

5. **Access Your App**:
   - Vercel provides URL: `https://your-app.vercel.app`

---

## Option 2: Vercel + Render

### Step 1: Deploy Backend to Render

1. **Create Render Account**: https://render.com
2. **Create New Web Service**:
   - Connect your GitHub repository
   - Select `backend` folder
   - Render auto-detects `render.yaml`

3. **Configure**:
   - Build Command: Docker (auto-detected)
   - Start Command: (auto from Dockerfile)
   - Plan: Standard ($7/month) - Free tier won't work for ML workloads

4. **Get Backend URL**:
   - Render provides: `https://your-app.onrender.com`

### Step 2: Deploy Frontend to Vercel

Same as Option 1, but use Render URL for `NEXT_PUBLIC_API_URL`

---

## Option 3: All-in-One with Fly.io

Fly.io can host both frontend and backend:

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Deploy Backend
cd backend
fly launch
fly deploy

# Deploy Frontend
cd ../frontend
fly launch
fly deploy
```

---

## Quick Deploy Commands

### If you just want it live NOW:

**Backend (Railway)**:
```bash
cd backend
railway login
railway up
railway open  # Get your URL
```

**Frontend (Vercel)**:
```bash
cd frontend
vercel --prod
```

Then set `NEXT_PUBLIC_API_URL` in Vercel dashboard to your Railway URL.

---

## Environment Variables Reference

### Backend
```env
PORT=8000
UPLOAD_DIR=/app/uploads
CONFIDENCE_THRESHOLD=0.5
MAX_FILE_SIZE=100000000
```

### Frontend
```env
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

---

## Cost Estimates

| Service | Plan | Cost | Notes |
|---------|------|------|-------|
| **Railway** | Hobby | $5/month | 500 hours + $0.000463/GB-hr |
| **Render** | Standard | $7/month | Better for ML workloads |
| **Fly.io** | Pay-as-you-go | ~$5-10/month | Scales automatically |
| **Vercel** | Hobby | FREE | Perfect for frontend |

**Total Cost**: $5-10/month for full deployment

---

## Testing Your Deployment

1. Visit your Vercel URL: `https://your-app.vercel.app`
2. Upload a test soccer kick video
3. Watch the analysis complete
4. Check backend logs in Railway/Render dashboard

---

## Troubleshooting

### Backend Issues

**Problem**: Backend crashes on Railway/Render
- **Solution**: Upgrade to paid plan (Free tier has memory limits)

**Problem**: Video upload fails
- **Solution**: Check CORS settings in `backend/app/main.py`
  ```python
  allow_origins=["https://your-app.vercel.app"]
  ```

**Problem**: Analysis timeout
- **Solution**: Increase timeout in Railway/Render (default: 60s, need 120s)

### Frontend Issues

**Problem**: "Failed to fetch" error
- **Solution**: Check `NEXT_PUBLIC_API_URL` is set correctly in Vercel

**Problem**: CORS error
- **Solution**: Add Vercel URL to backend CORS whitelist

---

## Production Optimizations

### Backend
1. **Enable GPU**: Railway/Render don't have GPU, use AWS/GCP for GPU acceleration
2. **Redis Cache**: Add Redis for caching results
3. **S3 Storage**: Store videos in S3 instead of local filesystem
4. **Load Balancing**: Multiple backend instances behind load balancer

### Frontend
1. **CDN**: Vercel includes global CDN automatically
2. **Image Optimization**: Next.js handles this
3. **Analytics**: Add Vercel Analytics

---

## Security Notes

- Backend runs with proprietary algorithms protected
- No public access to source code
- Environment variables keep sensitive config secret
- HTTPS enforced on all deployments

---

## Need Help?

Check deployment logs:
- **Railway**: `railway logs`
- **Render**: View in dashboard
- **Vercel**: `vercel logs`

---

**CONFIDENTIAL** - This deployment guide contains proprietary information.
