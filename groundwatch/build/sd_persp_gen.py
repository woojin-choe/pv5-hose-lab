import sys, os, torch, cv2, numpy as np
from PIL import Image
from diffusers import StableDiffusionControlNetImg2ImgPipeline, ControlNetModel, AutoencoderKL, DPMSolverMultistepScheduler
base, outdir = sys.argv[1], sys.argv[2]
CROP = (1000, 470, 3400, 1820)
W_, H_ = 1216, 680
im = Image.open(base).convert("RGB").crop(CROP).resize((W_, H_), Image.LANCZOS)
im.save(f"{outdir}/init.png")
edges = cv2.Canny(np.array(im), 60, 160)
ctrl = Image.fromarray(np.stack([edges] * 3, -1)); ctrl.save(f"{outdir}/canny.png")
cn = ControlNetModel.from_pretrained("lllyasviel/control_v11p_sd15_canny", torch_dtype=torch.float16)
vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse", torch_dtype=torch.float16)
pipe = StableDiffusionControlNetImg2ImgPipeline.from_pretrained("SG161222/Realistic_Vision_V5.1_noVAE", controlnet=cn, vae=vae,
        torch_dtype=torch.float16, safety_checker=None, requires_safety_checker=False)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config, algorithm_type="dpmsolver++", use_karras_sigmas=True)
pipe = pipe.to("mps"); pipe.enable_attention_slicing()
P = ("photorealistic 3d cutaway product render of a white electric cargo van, side panel cut away revealing the cargo room interior, "
     "black 19 inch server rack with blinking LEDs, orange wheeled ground penetrating radar cart, grey metal storage cabinet, plywood walls and wooden floor, interior LED lighting, "
     "amber LED light bar on the roof, small white GNSS antenna dome, black tires with alloy wheels, dark tinted windows, "
     "radar sensor box mounted under the rear bumper, on grey concrete studio floor, soft studio lighting, realistic reflections, octane render, sharp focus, high detail")
N = ("cartoon, illustration, drawing, sketch, line art, flat colors, lowres, blurry, text, letters, logo, watermark, deformed, distorted, people, extra wheels")
for strength in [0.6, 0.72]:
    for seed in [3, 11]:
        g = torch.Generator("cpu").manual_seed(seed)
        out = pipe(prompt=P, negative_prompt=N, image=im, control_image=ctrl, strength=strength, num_inference_steps=30,
                   guidance_scale=6.5, controlnet_conditioning_scale=0.85, generator=g).images[0]
        out.save(f"{outdir}/v2_s{int(strength*100)}_{seed}.png"); print("saved", strength, seed, flush=True)
