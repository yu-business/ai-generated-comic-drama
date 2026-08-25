from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .models import Shot


class ImageProvider:
    def generate(self, shot: Shot, output_path: Path, force: bool = False) -> str:
        raise NotImplementedError


class PlaceholderImageProvider(ImageProvider):
    """Creates visual comic-style placeholders when external image APIs are absent."""

    def generate(self, shot: Shot, output_path: Path, force: bool = False) -> str:
        if output_path.exists() and not force:
            return str(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        img = self._canvas(shot)
        draw = ImageDraw.Draw(img)
        if shot.shot_id in {"S01", "S04"}:
            self._draw_road(draw)
            self._draw_elena_fallen(draw, close=shot.shot_id == "S04")
            if shot.shot_id == "S01":
                self._draw_umbrella_man(draw, 780, 520, scale=0.72, blurred=True)
            self._draw_rain(draw)
        elif shot.shot_id == "S02":
            self._draw_road(draw)
            self._draw_umbrella_man(draw, 540, 610, scale=1.28)
            self._draw_rain(draw)
        elif shot.shot_id == "S03":
            self._draw_road(draw)
            self._draw_umbrella_man(draw, 450, 630, scale=1.05)
            self._draw_woman(draw, 650, 720, dress=(214, 188, 154), hair=(225, 207, 122), scale=0.98)
            self._draw_rain(draw)
        elif shot.shot_id == "S05":
            self._draw_headlights(draw)
            self._draw_rain(draw, bright=True)
        elif shot.shot_id == "S06":
            self._draw_black_transition(draw)
        elif shot.shot_id == "S07":
            self._draw_eye_rebirth(draw)
        elif shot.shot_id in {"S08", "S12", "S13"}:
            self._draw_church(draw)
            self._draw_bride(draw, 430, 1120, scale=1.08)
            self._draw_groom(draw, 650, 1120, scale=1.08)
            if shot.shot_id == "S13":
                self._draw_silence_gap(draw)
        elif shot.shot_id == "S09":
            self._draw_church(draw)
            self._draw_hands(draw)
        elif shot.shot_id == "S10":
            self._draw_church(draw)
            self._draw_woman(draw, 540, 1160, dress=(214, 188, 154), hair=(230, 211, 116), scale=1.35)
        elif shot.shot_id == "S11":
            self._draw_montage(draw)
        elif shot.shot_id == "S14":
            self._draw_church(draw)
            self._draw_woman(draw, 680, 1030, dress=(214, 188, 154), hair=(230, 211, 116), scale=0.9)
            self._draw_bride(draw, 430, 1160, scale=1.15, cold_smile=True)
            self._draw_title(draw)
        else:
            self._draw_church(draw)
        self._draw_film_frame(draw, shot)
        img.save(output_path)
        return str(output_path)

    def _canvas(self, shot: Shot) -> Image.Image:
        top, bottom = self._bg(shot)
        img = Image.new("RGB", (1080, 1920), top)
        pix = img.load()
        for y in range(1920):
            t = y / 1919
            color = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
            for x in range(1080):
                pix[x, y] = color
        return img

    def _bg(self, shot: Shot) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
        if shot.asset_type == "black":
            return (0, 0, 0), (0, 0, 0)
        if shot.shot_id in {"S01", "S02", "S03", "S04", "S05", "S11"}:
            return (7, 14, 24), (24, 35, 48)
        return (238, 223, 190), (70, 48, 56)

    def _draw_road(self, draw: ImageDraw.ImageDraw) -> None:
        draw.polygon([(0, 1920), (1080, 1920), (780, 760), (300, 760)], fill=(18, 22, 28))
        for x in range(80, 1080, 180):
            draw.line([(x, 1880), (x + 280, 850)], fill=(61, 77, 91), width=3)
        for y in range(900, 1880, 150):
            draw.ellipse((180, y, 900, y + 28), fill=(40, 57, 68))
        for x, y in [(150, 680), (930, 700), (240, 820)]:
            draw.ellipse((x - 18, y - 18, x + 18, y + 18), fill=(198, 221, 232))
            draw.line((x, y, x - 70, y + 760), fill=(111, 143, 160), width=5)

    def _draw_rain(self, draw: ImageDraw.ImageDraw, bright: bool = False) -> None:
        color = (185, 219, 239) if bright else (101, 144, 170)
        for x in range(-80, 1150, 52):
            for y in range(0, 1940, 180):
                draw.line((x, y, x + 34, y + 92), fill=color, width=3)

    def _draw_elena_fallen(self, draw: ImageDraw.ImageDraw, close: bool = False) -> None:
        if close:
            draw.ellipse((170, 360, 910, 1110), fill=(226, 206, 190))
            draw.polygon([(150, 620), (930, 610), (960, 1190), (120, 1200)], fill=(15, 14, 20))
            draw.ellipse((330, 665, 430, 730), fill=(42, 24, 28))
            draw.ellipse((650, 665, 750, 730), fill=(42, 24, 28))
            draw.ellipse((690, 682, 722, 714), fill=(255, 255, 255))
            draw.ellipse((374, 682, 406, 714), fill=(255, 255, 255))
            draw.ellipse((520, 795, 558, 825), fill=(35, 20, 24))
            draw.ellipse((356, 770, 390, 804), fill=(30, 25, 24))
            draw.line((320, 910, 760, 930), fill=(86, 36, 45), width=10)
            return
        draw.ellipse((290, 1030, 520, 1240), fill=(219, 199, 184))
        draw.polygon([(260, 1190), (820, 1360), (780, 1510), (205, 1340)], fill=(10, 10, 15))
        draw.line((390, 1240, 650, 1430), fill=(34, 24, 29), width=42)
        draw.line((500, 1240, 820, 1330), fill=(34, 24, 29), width=38)
        draw.ellipse((260, 1010, 470, 1140), fill=(20, 17, 20))
        draw.ellipse((410, 1090, 440, 1118), fill=(255, 255, 255))

    def _draw_umbrella_man(self, draw: ImageDraw.ImageDraw, x: int, y: int, scale: float = 1.0, blurred: bool = False) -> None:
        c = (38, 42, 50) if blurred else (8, 9, 13)
        w = int(280 * scale)
        h = int(95 * scale)
        draw.pieslice((x - w, y - h, x + w, y + h), 180, 360, fill=c)
        draw.line((x, y, x, y + int(520 * scale)), fill=c, width=max(6, int(10 * scale)))
        draw.ellipse((x - int(58 * scale), y + int(150 * scale), x + int(58 * scale), y + int(270 * scale)), fill=(213, 191, 174) if not blurred else c)
        draw.polygon([(x - int(105 * scale), y + int(280 * scale)), (x + int(105 * scale), y + int(280 * scale)), (x + int(160 * scale), y + int(660 * scale)), (x - int(160 * scale), y + int(660 * scale))], fill=c)

    def _draw_woman(self, draw: ImageDraw.ImageDraw, x: int, y: int, dress: tuple[int, int, int], hair: tuple[int, int, int], scale: float = 1.0) -> None:
        draw.ellipse((x - int(70 * scale), y - int(420 * scale), x + int(70 * scale), y - int(280 * scale)), fill=(232, 205, 187))
        draw.pieslice((x - int(90 * scale), y - int(450 * scale), x + int(90 * scale), y - int(250 * scale)), 180, 360, fill=hair)
        draw.polygon([(x, y - int(250 * scale)), (x - int(170 * scale), y + int(270 * scale)), (x + int(170 * scale), y + int(270 * scale))], fill=dress)
        draw.ellipse((x - int(35 * scale), y - int(360 * scale), x - int(12 * scale), y - int(340 * scale)), fill=(34, 70, 46))
        draw.ellipse((x + int(12 * scale), y - int(360 * scale), x + int(35 * scale), y - int(340 * scale)), fill=(34, 70, 46))

    def _draw_bride(self, draw: ImageDraw.ImageDraw, x: int, y: int, scale: float = 1.0, cold_smile: bool = False) -> None:
        self._draw_woman(draw, x, y, dress=(246, 244, 236), hair=(18, 17, 19), scale=scale)
        draw.ellipse((x - int(48 * scale), y - int(352 * scale), x - int(28 * scale), y - int(332 * scale)), fill=(42, 26, 24))
        draw.ellipse((x + int(28 * scale), y - int(352 * scale), x + int(48 * scale), y - int(332 * scale)), fill=(42, 26, 24))
        if cold_smile:
            draw.arc((x - int(38 * scale), y - int(300 * scale), x + int(38 * scale), y - int(260 * scale)), 10, 170, fill=(88, 36, 45), width=4)

    def _draw_groom(self, draw: ImageDraw.ImageDraw, x: int, y: int, scale: float = 1.0) -> None:
        draw.ellipse((x - int(70 * scale), y - int(420 * scale), x + int(70 * scale), y - int(280 * scale)), fill=(222, 198, 181))
        draw.pieslice((x - int(78 * scale), y - int(455 * scale), x + int(78 * scale), y - int(300 * scale)), 180, 360, fill=(51, 31, 25))
        draw.polygon([(x - int(120 * scale), y - int(260 * scale)), (x + int(120 * scale), y - int(260 * scale)), (x + int(150 * scale), y + int(260 * scale)), (x - int(150 * scale), y + int(260 * scale))], fill=(8, 9, 12))
        draw.polygon([(x - int(32 * scale), y - int(245 * scale)), (x + int(32 * scale), y - int(245 * scale)), (x, y - int(70 * scale))], fill=(245, 245, 240))

    def _draw_church(self, draw: ImageDraw.ImageDraw) -> None:
        draw.polygon([(120, 1920), (960, 1920), (740, 720), (340, 720)], fill=(92, 65, 61))
        draw.rectangle((145, 650, 935, 1920), outline=(235, 216, 180), width=10)
        for x in (210, 870):
            draw.rectangle((x - 35, 620, x + 35, 1680), fill=(226, 207, 171))
            draw.ellipse((x - 95, 520, x + 95, 710), outline=(240, 222, 184), width=8)
        draw.polygon([(540, 240), (225, 690), (855, 690)], outline=(242, 225, 190), width=12)
        for x in range(180, 930, 120):
            draw.ellipse((x, 1120, x + 85, 1205), fill=(245, 245, 235))
            draw.line((x + 42, 1200, x + 20, 1450), fill=(70, 52, 50), width=16)

    def _draw_hands(self, draw: ImageDraw.ImageDraw) -> None:
        draw.ellipse((210, 1030, 560, 1350), fill=(232, 205, 187))
        draw.ellipse((520, 1040, 870, 1360), fill=(232, 205, 187))
        draw.arc((360, 1110, 480, 1230), 0, 350, fill=(235, 232, 220), width=12)
        draw.arc((600, 1120, 720, 1240), 0, 350, fill=(235, 232, 220), width=12)

    def _draw_headlights(self, draw: ImageDraw.ImageDraw) -> None:
        draw.rectangle((0, 0, 1080, 1920), fill=(14, 18, 24))
        draw.polygon([(160, 1920), (470, 580), (590, 580), (920, 1920)], fill=(238, 244, 255))
        draw.ellipse((270, 710, 440, 860), fill=(255, 255, 245))
        draw.ellipse((640, 710, 810, 860), fill=(255, 255, 245))

    def _draw_black_transition(self, draw: ImageDraw.ImageDraw) -> None:
        draw.rectangle((0, 0, 1080, 1920), fill=(0, 0, 0))
        for r in range(70, 310, 70):
            draw.ellipse((540 - r, 960 - r, 540 + r, 960 + r), outline=(30, 30, 35), width=8)

    def _draw_eye_rebirth(self, draw: ImageDraw.ImageDraw) -> None:
        draw.rectangle((0, 0, 1080, 1920), fill=(245, 226, 190))
        draw.ellipse((150, 620, 930, 1190), fill=(232, 205, 187))
        draw.ellipse((245, 765, 835, 1050), fill=(248, 248, 242))
        draw.ellipse((420, 790, 660, 1030), fill=(55, 34, 30))
        draw.ellipse((498, 868, 582, 952), fill=(15, 10, 10))
        draw.ellipse((560, 820, 610, 870), fill=(255, 255, 255))
        draw.polygon([(120, 650), (940, 620), (900, 760), (180, 735)], fill=(21, 19, 21))

    def _draw_montage(self, draw: ImageDraw.ImageDraw) -> None:
        draw.rectangle((0, 0, 1080, 1920), fill=(8, 8, 12))
        panels = [(70, 180, 1010, 560), (70, 680, 1010, 1060), (70, 1180, 1010, 1560)]
        colors = [(40, 60, 78), (75, 35, 44), (245, 245, 235)]
        for rect, color in zip(panels, colors):
            draw.rectangle(rect, fill=color, outline=(240, 240, 230), width=6)
        draw.line((210, 360, 820, 360), fill=(10, 10, 16), width=44)
        draw.ellipse((450, 800, 630, 980), fill=(232, 205, 187))
        draw.polygon([(270, 1560), (480, 1240), (600, 1240), (830, 1560)], fill=(255, 255, 245))

    def _draw_silence_gap(self, draw: ImageDraw.ImageDraw) -> None:
        draw.rectangle((0, 0, 1080, 1920), outline=(120, 29, 42), width=20)

    def _draw_title(self, draw: ImageDraw.ImageDraw) -> None:
        title_font = self._font(86, bold=True)
        ep_font = self._font(42)
        draw.rectangle((0, 1460, 1080, 1920), fill=(0, 0, 0))
        draw.text((162, 1580), "SECOND CHANCE", fill=(238, 230, 211), font=title_font)
        draw.text((405, 1695), "EPISODE 2", fill=(180, 32, 52), font=ep_font)

    def _draw_film_frame(self, draw: ImageDraw.ImageDraw, shot: Shot) -> None:
        accent = (236, 222, 187) if shot.shot_id >= "S07" else (115, 156, 184)
        draw.rectangle((0, 0, 1080, 1920), outline=accent, width=8)

    def _font(self, size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        ]
        for path in paths:
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
        return ImageFont.load_default()


def generate_images(root: Path, shots: list[Shot], force: bool = False) -> list[Path]:
    provider = PlaceholderImageProvider()
    paths = []
    for shot in shots:
        path = root / "assets" / "images" / f"{shot.shot_id}.png"
        provider.generate(shot, path, force=force)
        paths.append(path)
        print(f"  ✓ {shot.shot_id}")
    return paths
