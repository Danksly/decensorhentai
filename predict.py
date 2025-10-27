"""
Custom NSFW Anime Inpainting Model for Replicate
No content filters - generates anatomically correct anime content
"""
from cog import BasePredictor, Input, Path
from diffusers import StableDiffusionInpaintPipeline, DPMSolverMultistepScheduler
import torch
from PIL import Image
import numpy as np
import io
import base64

class Predictor(BasePredictor):
    def setup(self):
        """Load the NSFW anime inpainting model"""
        model_id = "andite/anything-v5-inpainting"
        
        # Load model without safety checker
        self.pipe = StableDiffusionInpaintPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            safety_checker=None,  # Disable content filter
            requires_safety_checker=False
        )
        
        # Use DPM++ solver for better quality
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            self.pipe.scheduler.config
        )
        
        # Move to GPU
        self.pipe = self.pipe.to("cuda")
        
        # Enable memory optimizations
        self.pipe.enable_attention_slicing()
        self.pipe.enable_vae_slicing()

    def predict(
        self,
        image: Path = Input(description="Input image"),
        mask: Path = Input(description="Mask image (white = inpaint area)"),
        prompt: str = Input(
            description="Prompt for inpainting",
            default="uncensored genitalia, anatomically correct, detailed anatomy, high quality anime"
        ),
        negative_prompt: str = Input(
            description="Negative prompt",
            default="censored, mosaic, blur, pixelated, low quality, worst quality, bad anatomy"
        ),
        num_inference_steps: int = Input(
            description="Number of denoising steps",
            default=30,
            ge=1,
            le=100
        ),
        guidance_scale: float = Input(
            description="Guidance scale",
            default=7.5,
            ge=1.0,
            le=20.0
        ),
        strength: float = Input(
            description="Inpainting strength",
            default=0.95,
            ge=0.0,
            le=1.0
        ),
        seed: int = Input(
            description="Random seed (0 = random)",
            default=0
        ),
    ) -> Path:
        """Run inpainting prediction"""
        
        # Set seed for reproducibility
        if seed == 0:
            seed = torch.randint(0, 2**32 - 1, (1,)).item()
        generator = torch.Generator(device="cuda").manual_seed(seed)
        
        # Load images
        init_image = Image.open(image).convert("RGB")
        mask_image = Image.open(mask).convert("L")
        
        # Ensure mask is binary (0 or 255)
        mask_array = torch.from_numpy(np.array(mask_image))
        mask_array = (mask_array > 127).float() * 255
        mask_image = Image.fromarray(mask_array.numpy().astype(np.uint8))
        
        # Run inpainting
        output = self.pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            image=init_image,
            mask_image=mask_image,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            strength=strength,
            generator=generator,
        ).images[0]
        
        # Save output
        output_path = "/tmp/output.png"
        output.save(output_path, quality=95)
        
        return Path(output_path)
