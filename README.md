# Custom NSFW Anime Inpainting Model

This is a custom uncensored anime inpainting model for Replicate that generates anatomically correct content without content filters.

## Model Details

- **Base Model**: Anything V5 Inpainting
- **Purpose**: Uncensored anime genitalia inpainting
- **Content Filter**: Disabled (no safety checker)
- **Optimization**: GPU-accelerated with memory optimizations

## Deployment Instructions

### Prerequisites

1. **Install Cog** (Replicate's packaging tool):
```bash
sudo curl -o /usr/local/bin/cog -L https://github.com/replicate/cog/releases/latest/download/cog_`uname -s`_`uname -m`
sudo chmod +x /usr/local/bin/cog
```

2. **Login to Replicate**:
```bash
cog login
```

### Deploy the Model

1. Navigate to this directory:
```bash
cd replicate-model
```

2. Build and push to Replicate:
```bash
# Replace YOUR_USERNAME with your Replicate username
cog push r8.im/YOUR_USERNAME/anime-uncensor-inpainting
```

This will:
- Build a Docker image with the model
- Download the Anything V5 inpainting weights
- Upload to your Replicate account
- Make it available via API

**Estimated time**: 10-15 minutes for first deployment

### Get Your Model URL

After deployment completes, you'll see:
```
✓ Pushed r8.im/YOUR_USERNAME/anime-uncensor-inpainting
```

Your model is now available at:
```
https://replicate.com/YOUR_USERNAME/anime-uncensor-inpainting
```

### Update Application Configuration

Once deployed, update your application's environment variable:

```bash
# In your Replit Secrets, add:
CUSTOM_INPAINT_MODEL=YOUR_USERNAME/anime-uncensor-inpainting
```

The application will automatically use your custom model instead of the default one.

## Model Parameters

- **prompt**: What to generate (default includes anatomical terms)
- **negative_prompt**: What to avoid (censorship, bad quality)
- **num_inference_steps**: Quality vs speed (default: 30)
- **guidance_scale**: How closely to follow prompt (default: 7.5)
- **strength**: How much to change masked area (default: 0.95)
- **seed**: For reproducible results (0 = random)

## Cost Estimate

- **GPU**: NVIDIA T4 or A10G
- **Cost**: ~$0.002-0.005 per image
- **Speed**: ~2-5 seconds per frame

## Troubleshooting

**Build fails:**
- Ensure you have Docker installed
- Check Cog installation: `cog --version`

**Model download slow:**
- First build downloads ~4GB of model weights
- Subsequent builds are cached

**Out of memory:**
- Model uses ~6GB GPU RAM
- Replicate automatically provides sufficient GPU

## Alternative Models

If you want to try different base models, edit `predict.py` and change:

```python
model_id = "andite/anything-v5-inpainting"
```

To one of:
- `"runwayml/stable-diffusion-inpainting"` - General purpose
- `"Lykon/dreamshaper-8-inpainting"` - Artistic style
- Any other inpainting model from HuggingFace

## Support

For issues with:
- **Cog/Deployment**: https://github.com/replicate/cog/issues
- **Model quality**: Adjust prompts and parameters
- **Application integration**: Check inpaintingService.ts
