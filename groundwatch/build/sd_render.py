# ControlNet(Canny) + img2img: 실차 윤곽을 고정한 채 장비 장착 상태를 한 장면으로 다시 렌더
import os, sys, torch
from PIL import Image
from diffusers import StableDiffusionControlNetImg2ImgPipeline, ControlNetModel, AutoencoderKL, DPMSolverMultistepScheduler
SD = os.path.join(os.path.dirname(__file__), "..", "images", "sd")
dev = "mps"
cn = ControlNetModel.from_pretrained("lllyasviel/control_v11p_sd15_canny", variant="fp16", torch_dtype=torch.float16)
vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse", torch_dtype=torch.float16)
pipe = StableDiffusionControlNetImg2ImgPipeline.from_pretrained("SG161222/Realistic_Vision_V5.1_noVAE", controlnet=cn, vae=vae, torch_dtype=torch.float16, safety_checker=None, requires_safety_checker=False)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config, algorithm_type="dpmsolver++", use_karras_sigmas=True)
pipe = pipe.to(dev); pipe.enable_attention_slicing()
NEG = "cartoon, illustration, drawing, cgi, 3d render, painting, text, letters, watermark, logo, deformed, blurry, low quality, distorted wheels, extra wheels, people"
JOBS = {
  "front_night": ("front", "night", "professional automotive press photograph of a white electric cargo van parked on a quiet city street at blue hour before dawn, amber LED light bar glowing on the roof, small white GNSS antenna dome on roof, roof camera pod, headlights on, wet asphalt reflections, streetlights, cinematic realistic lighting, sharp focus, 35mm, high detail", 0.42),
  "front_day": ("front", "day", "professional automotive press photograph of a white electric cargo van, roof mounted amber light bar, small white GNSS antenna dome on roof, roof camera pod, overcast daylight, realistic reflections, sharp focus, high detail", 0.35),
  "rear_night": ("rear", "night", "professional automotive photograph of the rear of a white electric cargo van at blue hour dawn on a city street, vertical red tail lights glowing, amber roof light bar, dark ground penetrating radar antenna housing mounted low under the rear bumper on steel brackets, wet asphalt reflections, realistic lighting, sharp focus, high detail", 0.42),
  "rear_day": ("rear", "day", "professional automotive photograph of the rear of a white electric cargo van, dark ground penetrating radar antenna housing mounted low under the rear bumper on steel brackets, amber roof light bar, overcast daylight, realistic, sharp focus, high detail", 0.35),
}
for key in (sys.argv[1:] or JOBS):
    v, tone, prompt, strength = JOBS[key]
    init = Image.open(os.path.join(SD, f"{v}_{tone}.png")).convert("RGB").resize((1152, 768), Image.LANCZOS)
    ctrl = Image.open(os.path.join(SD, f"{v}_canny.png")).convert("RGB").resize((1152, 768), Image.NEAREST)
    for seed in [7, 21]:
        g = torch.Generator("cpu").manual_seed(seed)
        out = pipe(prompt=prompt, negative_prompt=NEG, image=init, control_image=ctrl, strength=strength, num_inference_steps=30, guidance_scale=6.0, controlnet_conditioning_scale=0.9, generator=g).images[0]
        out.save(os.path.join(SD, f"gen_{key}_{seed}.png")); print("saved", key, seed, flush=True)
