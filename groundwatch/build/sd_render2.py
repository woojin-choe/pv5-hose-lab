# 1차: ControlNet img2img로 전체 장면 재렌더 → 2차: 후방 하부 GPR 영역만 인페인팅으로 실제 부품처럼 재생성
import os, sys, torch, numpy as np
from PIL import Image, ImageFilter, ImageDraw
from diffusers import (StableDiffusionControlNetImg2ImgPipeline, StableDiffusionControlNetInpaintPipeline,
                       ControlNetModel, AutoencoderKL, DPMSolverMultistepScheduler)
SD = os.path.join(os.path.dirname(__file__), "..", "images", "sd")
cn = ControlNetModel.from_pretrained("lllyasviel/control_v11p_sd15_canny", variant="fp16", torch_dtype=torch.float16)
vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse", torch_dtype=torch.float16)
i2i = StableDiffusionControlNetImg2ImgPipeline.from_pretrained("SG161222/Realistic_Vision_V5.1_noVAE", controlnet=cn, vae=vae, torch_dtype=torch.float16, safety_checker=None, requires_safety_checker=False)
i2i.scheduler = DPMSolverMultistepScheduler.from_config(i2i.scheduler.config, algorithm_type="dpmsolver++", use_karras_sigmas=True)
i2i = i2i.to("mps"); i2i.enable_attention_slicing()
inp = StableDiffusionControlNetInpaintPipeline(**i2i.components).to("mps")
NEG = "cartoon, illustration, drawing, cgi, render, painting, text, letters, stripes, decals, sticker, watermark, logo, deformed, blurry, low quality, extra wheels, people"
SZ = (1152, 768); K = 1152 / 1920
JOBS = {
  "front_night": ("front", "night", "professional automotive press photograph of a plain white electric cargo van parked on a quiet city street at blue hour before dawn, slim amber LED light bar glowing on the roof, small white GNSS antenna dome on the roof, headlights on, wet asphalt reflections, cinematic realistic lighting, sharp focus, high detail", 0.4, None),
  "front_day": ("front", "day", "professional automotive press photograph of a plain white electric cargo van, slim amber LED light bar on the roof, small white GNSS antenna dome on the roof, overcast daylight, realistic reflections, sharp focus, high detail", 0.33, None),
  "rear_night": ("rear", "night", "professional automotive photograph of the rear of a plain white electric cargo van at blue hour dawn on a city street, vertical red tail lights glowing, amber roof light bar, wet asphalt, realistic lighting, sharp focus, high detail", 0.4, (130, 1050, 890, 1150)),
  "rear_day": ("rear", "day", "professional automotive photograph of the rear of a plain white electric cargo van, amber roof light bar, overcast daylight, realistic, sharp focus, high detail", 0.33, (130, 1050, 890, 1150)),
}
GPR = "close-up detail, a low rectangular matte dark grey ground penetrating radar antenna housing mounted under the rear bumper of a van with short steel mounting brackets, a few centimeters above the asphalt, industrial survey equipment, bolted, realistic metal and plastic, consistent lighting, photograph"
for key in (sys.argv[1:] or JOBS):
    v, tone, prompt, strength, box = JOBS[key]
    init = Image.open(os.path.join(SD, f"{v}_{tone}.png")).convert("RGB").resize(SZ, Image.LANCZOS)
    ctrl = Image.open(os.path.join(SD, f"{v}_canny.png")).convert("RGB").resize(SZ, Image.NEAREST)
    for seed in [7, 21, 33]:
        g = torch.Generator("cpu").manual_seed(seed)
        out = i2i(prompt=prompt, negative_prompt=NEG, image=init, control_image=ctrl, strength=strength, num_inference_steps=30, guidance_scale=6.0, controlnet_conditioning_scale=0.9, generator=g).images[0]
        if box:
            m = Image.new("L", SZ, 0); x0, y0, x1, y1 = [int(c * K) for c in box]
            ImageDraw.Draw(m).rounded_rectangle([x0, y0, x1, y1], radius=12, fill=255); m = m.filter(ImageFilter.GaussianBlur(6))
            g2 = torch.Generator("cpu").manual_seed(seed + 100)
            fix = inp(prompt=GPR + (", dawn blue hour lighting" if tone == "night" else ", overcast daylight"), negative_prompt=NEG, image=out, mask_image=m, control_image=ctrl, strength=0.8, num_inference_steps=30, guidance_scale=6.5, controlnet_conditioning_scale=0.7, generator=g2).images[0]
            out = Image.composite(fix, out, m)
        out.save(os.path.join(SD, f"gen2_{key}_{seed}.png")); print("saved", key, seed, flush=True)
