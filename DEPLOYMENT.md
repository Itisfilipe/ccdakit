# Deployment Guide

## Deploy to Render (Free)

### Step 1: Sign Up & Connect GitHub

1. Go to https://render.com/
2. Click "Get Started for Free"
3. Sign up with your GitHub account
4. Authorize Render to access your repositories

### Step 2: Create New Web Service

1. Click "New +" → "Web Service"
2. Connect your `ccdakit` repository
3. Render will auto-detect the `render.yaml` configuration
4. Click "Apply" to use the blueprint
5. Click "Create Web Service"

**That's it!** Render will:
- Install dependencies using `uv`
- Start the Flask app
- Give you a URL like `https://ccdakit.onrender.com`

### Step 3: Use Your Custom Domain (Optional)

If you want to use `ccdakit.com`:

#### In Render:
1. Go to your service → Settings → Custom Domains
2. Add `ccdakit.com` and `www.ccdakit.com`
3. Render will show you DNS records (CNAME or A records)

#### In Cloudflare:
1. Log in to Cloudflare dashboard
2. Select your `ccdakit.com` domain
3. Go to DNS → Records
4. Add the records Render provided:
   - Type: `CNAME`
   - Name: `@` (or `www`)
   - Target: `ccdakit.onrender.com` (or value Render gave you)
   - Proxy status: Can enable (orange cloud) for Cloudflare CDN
5. Wait 5-10 minutes for DNS propagation

### Step 4: Auto-Deploy on Git Push

Already configured! Every time you push to `main` branch:
- Render automatically rebuilds and deploys
- Takes ~2-3 minutes
- Zero downtime

## Render Free Tier Limits

✅ What's included:
- Free SSL certificate
- Auto-deploys from GitHub
- 750 hours/month (more than enough)
- Custom domain support

⚠️ Limitations:
- App sleeps after 15 minutes of inactivity
- Wakes up in ~30 seconds on first request
- 512 MB RAM (enough for this app)

To stay always-on: Upgrade to $7/month (optional)

## Monitoring Your Deployment

1. View logs: Render Dashboard → Logs tab
2. Check status: Dashboard shows "Live" when running
3. Access metrics: Dashboard → Metrics tab

## Troubleshooting

**App won't start?**
- Check logs in Render dashboard
- Ensure `uv` installed correctly
- Verify Python version is 3.11+

**Domain not working?**
- Wait 10-15 minutes for DNS propagation
- Use `dig ccdakit.com` to check DNS records
- Ensure Cloudflare DNS records are correct

**App is slow?**
- First request after sleep takes ~30 seconds (free tier)
- Consider upgrading to paid tier for always-on

## Cost Estimate

- **Free tier**: $0/month (with sleep after inactivity)
- **Paid tier**: $7/month (always-on, no sleep)

## Need Help?

- Render Docs: https://render.com/docs
- Support: help@render.com
- Community: https://community.render.com/
