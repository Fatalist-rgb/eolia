from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source-assets" / "chatgpt"
IMAGES = ROOT / "images"


def cover_crop(image: Image.Image, target_width: int, target_height: int, x_bias=0.5, y_bias=0.5) -> Image.Image:
    source_width, source_height = image.size
    target_ratio = target_width / target_height
    source_ratio = source_width / source_height

    if source_ratio > target_ratio:
        crop_height = source_height
        crop_width = int(crop_height * target_ratio)
        left = int((source_width - crop_width) * x_bias)
        top = 0
    else:
        crop_width = source_width
        crop_height = int(crop_width / target_ratio)
        left = 0
        top = int((source_height - crop_height) * y_bias)

    cropped = image.crop((left, top, left + crop_width, top + crop_height))
    return cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)


def save_cover(source_name: str, output_name: str, size: tuple[int, int], *, x_bias=0.5, y_bias=0.5) -> None:
    with Image.open(SOURCE / source_name) as source:
        exported = cover_crop(source.convert("RGB"), size[0], size[1], x_bias=x_bias, y_bias=y_bias)
        output_path = IMAGES / output_name
        if output_path.suffix.lower() == ".avif":
            exported.save(output_path, quality=82, speed=4)
        else:
            exported.save(output_path, optimize=True, quality=92)


def export_team_grid() -> None:
    with Image.open(SOURCE / "team-grid.png") as source:
        source = source.convert("RGB")
        cell_width = source.width // 4
        cell_height = source.height // 2

        # Existing markup renders team-08 first, then counts down to team-01.
        outputs = [
            "team-08.avif",
            "team-07.avif",
            "team-06.avif",
            "team-05.avif",
            "team-04.png",
            "team-03.avif",
            "team-02.avif",
            "team-01.avif",
        ]

        for index, output_name in enumerate(outputs):
            col = index % 4
            row = index // 4
            cell = source.crop(
                (
                    col * cell_width,
                    row * cell_height,
                    (col + 1) * cell_width,
                    (row + 1) * cell_height,
                )
            )
            portrait = cover_crop(cell, 458, 458, y_bias=0.28)
            output_path = IMAGES / output_name
            if output_path.suffix.lower() == ".avif":
                portrait.save(output_path, quality=84, speed=4)
            else:
                portrait.save(output_path, optimize=True, quality=92)


def main() -> None:
    save_cover("hero.png", "hero.avif", (2160, 1350), x_bias=0.55, y_bias=0.58)
    save_cover("about-solar.png", "about-01.avif", (225, 225), y_bias=0.38)
    save_cover("about-storage.png", "about-02.avif", (525, 525), y_bias=0.48)
    save_cover("about-wind.png", "about-03.avif", (225, 225), y_bias=0.38)
    save_cover("stats.png", "stats.avif", (945, 945), y_bias=0.5)
    save_cover("blog-future.png", "blog-01.png", (945, 495), y_bias=0.48)
    save_cover("blog-geothermal.png", "blog-02.png", (945, 495), y_bias=0.48)
    save_cover("contact.png", "contact.avif", (1440, 1300), y_bias=0.45)
    save_cover("hero.png", "../opengraph-image.png", (2400, 1260), x_bias=0.55, y_bias=0.58)
    export_team_grid()


if __name__ == "__main__":
    main()
