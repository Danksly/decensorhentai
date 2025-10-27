# GitHub Actions Deployment Instructions

This workflow automatically builds and pushes your model to Replicate whenever you push to GitHub.

## Step 1: Upload Files to GitHub

Upload these files to your `anime-uncensor` GitHub repository:
- `predict.py`
- `cog.yaml`
- `README.md`
- `.github/workflows/deploy.yml` (create this folder structure)

## Step 2: Add GitHub Secret

1. Go to your GitHub repo: `https://github.com/YOUR-USERNAME/anime-uncensor`
2. Click **Settings** (top menu)
3. Click **Secrets and variables** → **Actions** (left sidebar)
4. Click **New repository secret**
5. Name: `REPLICATE_CLI_TOKEN`
6. Value: `6719617e-deb5-425b-85b3-e3338b12a8e5`
7. Click **Add secret**

## Step 3: Trigger Deployment

### Option A: Push to GitHub
Just commit any change to your repo and push to trigger the workflow.

### Option B: Manual Trigger
1. Go to **Actions** tab in your repo
2. Click **Deploy to Replicate** workflow
3. Click **Run workflow** button
4. Click **Run workflow** again to confirm

## Step 4: Monitor Build

1. Go to **Actions** tab
2. Click on the running workflow
3. Watch the build logs
4. Build takes 10-15 minutes

## Step 5: Test Your Model

Once complete, your model will be live at:
`https://replicate.com/danksly/decensor`

You can test it via API or the Replicate playground.
