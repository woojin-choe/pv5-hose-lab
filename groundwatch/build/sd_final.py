# 최종 실사화: 실차 사진+장비 레이어(외관), Blender 렌더(실내·GPR) → ControlNet Canny + img2img
import os, sys, torch, numpy as np, cv2
from PIL import Image
from diffusers import StableDiffusionControlNetImg2ImgPipeline, ControlNetModel, AutoencoderKL, DPMSolverMultistepScheduler
R = os.path.join(os.path.dirname(__file__), "..", "images")
cn = ControlNetModel.from_pretrained("lllyasviel/control_v11p_sd15_canny", variant="fp16", torch_dtype=torch.float16)
vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse", torch_dtype=torch.float16)
pipe = StableDiffusionControlNetImg2ImgPipeline.from_pretrained("SG161222/Realistic_Vision_V5.1_noVAE", controlnet=cn, vae=vae, torch_dtype=torch.float16, safety_checker=None, requires_safety_checker=False)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config, algorithm_type="dpmsolver++", use_karras_sigmas=True)
pipe = pipe.to("mps"); pipe.enable_attention_slicing()
NEG = "cartoon, illustration, drawing, cgi, 3d render, low poly, painting, text, letters, watermark, logo, deformed, warped, blurry, low quality, extra wheels, people, exhaust pipe, tow hitch"
def canny(img, lo=60, hi=140):
    g = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2GRAY); g = cv2.bilateralFilter(g, 9, 50, 50)
    return Image.fromarray(cv2.Canny(g, lo, hi)).convert("RGB")
ROOF = "black roof rack crossbars, slim amber LED light bar on the roof, small white GNSS antenna dome, compact 360 camera on a short mast"
JOBS = {
  "x_front_day": ("sd/front_day.png", f"professional automotive press photograph of a white electric cargo van fitted as a road survey vehicle, {ROOF}, overcast daylight, realistic reflections, sharp focus, high detail, 35mm", 0.36, 0.9, (1152, 768)),
  "x_front_night": ("sd/front_night.png", f"professional automotive press photograph of a white electric cargo van fitted as a road survey vehicle at blue hour before dawn, {ROOF}, amber light bar glowing, headlights on, cinematic realistic lighting, sharp focus, high detail", 0.42, 0.9, (1152, 768)),
  "x_rear_day": ("sd/rear_day.png", "professional automotive photograph of the rear of a white electric cargo van fitted as a road survey vehicle, amber roof light bar, GNSS antenna dome, overcast daylight, realistic, sharp focus, high detail", 0.35, 0.9, (1152, 768)),
  "x_rear_night": ("sd/rear_night.png", "professional automotive photograph of the rear of a white electric cargo van at blue hour dawn on a city street, vertical red tail lights glowing, amber roof light bar glowing, realistic lighting, sharp focus, high detail", 0.4, 0.9, (1152, 768)),
  "x_interior": ("3d/interior.png", "photograph of the interior of a white cargo van fitted out as a mobile engineering survey laboratory, viewed through open rear doors, server rack with status LEDs, aluminium workbench with two monitors, ground penetrating radar cart strapped to the floor, grey storage cabinets, orange traffic cone, rubber floor, LED ceiling light, professional commercial vehicle upfit photography, realistic materials, sharp focus", 0.55, 0.85, (1152, 648)),
  "x_interior_side": ("3d/interior_side.png", "photograph of the interior of a white cargo van mobile survey laboratory seen through the open side door, server rack with status LEDs, aluminium workbench with monitor and seat, yellow ground penetrating radar cart strapped to floor, storage cabinets, equipment cases on a shelf, LED lighting, professional upfit photography, realistic materials, sharp focus", 0.55, 0.85, (1152, 648)),
  "x_gpr": ("3d/gpr.png", "close-up photograph of a dark grey multi-channel ground penetrating radar antenna array mounted low under the rear bumper of a white van with aluminium brackets, a few centimeters above asphalt road, industrial survey equipment, realistic metal and plastic, shallow depth of field", 0.5, 0.85, (1152, 648)),
}
for key in (sys.argv[1:] or JOBS):
    src, prompt, strength, ccs, size = JOBS[key]
    init = Image.open(os.path.join(R, src)).convert("RGB").resize(size, Image.LANCZOS)
    ctrl = canny(init)
    for seed in (7, 21, 33):
        g = torch.Generator("cpu").manual_seed(seed)
        out = pipe(prompt=prompt, negative_prompt=NEG, image=init, control_image=ctrl, strength=strength, num_inference_steps=32, guidance_scale=6.0, controlnet_conditioning_scale=ccs, generator=g).images[0]
        out.save(os.path.join(R, "sd", f"{key}_{seed}.png")); print("saved", key, seed, flush=True)
