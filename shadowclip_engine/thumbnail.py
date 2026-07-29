from PIL import Image, ImageDraw, ImageFont
import cv2
from pathlib import Path
from viral_thumbnail_brain import ViralThumbnailBrain
from viral_frame_selector import ViralFrameSelector


class ShadowThumbnailGenerator:

    def __init__(self):

        self.brain = ViralThumbnailBrain()
        self.frame_selector = ViralFrameSelector()
         # -----------------------------------------------------
         
def add_glow(self, draw, text, position, font):

    x, y = position

    for i in range(1, 6):
        draw.text((x+i, y+i), text, font=font, fill=(255, 100, 0))

    draw.text((x, y), text, font=font, fill=(255,255,255))
    # -----------------------------------------------------

    def add_gradient(self, image):

        width, height = image.size

        overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw_overlay = ImageDraw.Draw(overlay)

        for i in range(300):
            opacity = int(200 * (i / 300))
            draw_overlay.rectangle(
                [0, height - i, width, height - i],
                fill=(0, 0, 0, opacity)
            )

        image = image.convert("RGBA")
        image = Image.alpha_composite(image, overlay)
        image = image.convert("RGB")

        return image

    # -----------------------------------------------------

    def split_lines(self, hook):

        words = hook.split()

        if len(words) <= 3:
            return hook, ""

        if len(words) <= 5:
            return " ".join(words[:2]), " ".join(words[2:])

        return " ".join(words[:3]), " ".join(words[3:])

    # -----------------------------------------------------

    def draw_text_strong(self, draw, x, y, text, font, color):

        # sombra fuerte tipo viral
        for dx in range(-5, 6):
            for dy in range(-5, 6):
                draw.text((x + dx, y + dy), text, font=font, fill="black")

        draw.text((x, y), text, font=font, fill=color)

    # -----------------------------------------------------

    def generate_thumbnail(self, video_path, output_path, hook_text):

        # 🧠 FRAME INTELIGENTE
        frame = self.frame_selector.extract_best_frame(video_path)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)

        # 🔥 MÁS CONTRASTE
        image = image.point(lambda p: p * 1.2)

        # 🎯 GRADIENTE
        image = self.add_gradient(image)

        width, height = image.size

        # 🧠 DECISIÓN IA
        decision = self.brain.analyze(hook_text)

        hook = decision["hook"]
        color = decision["color"]

        line1, line2 = self.split_lines(hook)

        draw = ImageDraw.Draw(image)

        try:
            font_big = ImageFont.truetype("DejaVuSans-Bold.ttf", int(height * 0.14))
            font_small = ImageFont.truetype("DejaVuSans-Bold.ttf", int(height * 0.10))
        except:
            font_big = ImageFont.load_default()
            font_small = font_big

        # 📍 POSICIÓN
        y_base = int(height * 0.65)

        # LINE 1
        bbox1 = draw.textbbox((0, 0), line1, font=font_big)
        x1 = (width - (bbox1[2] - bbox1[0])) // 2

        self.draw_text_strong(draw, x1, y_base, line1, font_big, color)

        # LINE 2
        if line2:
            bbox2 = draw.textbbox((0, 0), line2, font=font_small)
            x2 = (width - (bbox2[2] - bbox2[0])) // 2
            y2 = y_base + (bbox1[3] - bbox1[1]) + 20

            self.draw_text_strong(draw, x2, y2, line2, font_small, (255, 255, 255))

        # SAVE
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        image.save(str(output_path), "JPEG", quality=95)

        print("🔥 THUMB SAVED:", output_path)

        return str(output_path)