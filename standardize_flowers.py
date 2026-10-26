import os
import shutil
from PIL import Image

TARGET_WIDTH = 800
TARGET_HEIGHT = 1000
TARGET_RATIO = TARGET_WIDTH / TARGET_HEIGHT  # 0.8 (4:5)

FLOWERS_DIR = os.path.join(os.path.dirname(__file__), 'media', 'flowers')
BACKUP_DIR = os.path.join(os.path.dirname(__file__), 'media', 'flowers_backup')

def standardize_image(image_path):
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        w, h = img.size
        current_ratio = w / h

        if current_ratio > TARGET_RATIO:
            # Rasm kengroq (landscape) - markazdan kesiladi
            new_w = int(h * TARGET_RATIO)
            left = (w - new_w) // 2
            box = (left, 0, left + new_w, h)
        else:
            # Rasm balandroq (portrait) - tepa va pastdan mos qirqiladi
            # Gullar odatda biroz yuqoriroq yoki markazda joylashganligi uchun:
            new_h = int(w / TARGET_RATIO)
            top = max(0, int((h - new_h) * 0.4))  # 40% yuqoridan, 60% pastdan
            box = (0, top, w, top + new_h)

        cropped = img.crop(box)
        standardized = cropped.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
        standardized.save(image_path, 'JPEG', quality=92, optimize=True)
        print(f"[OK] {os.path.basename(image_path)}: {w}x{h} -> {TARGET_WIDTH}x{TARGET_HEIGHT}")

def main():
    if not os.path.exists(BACKUP_DIR):
        print(f"[BACKUP] Zaxira nusxa yaratilmoqda: {BACKUP_DIR}")
        shutil.copytree(FLOWERS_DIR, BACKUP_DIR)

    count = 0
    for root, dirs, files in os.walk(FLOWERS_DIR):
        if 'backup' in root or 'test' in root:
            continue
        for file in sorted(files):
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                p = os.path.join(root, file)
                standardize_image(p)
                count += 1

    print(f"\n[SUCCESS] Jami {count} ta gul rasmlari muvaffaqiyatli 800x1000 (4:5) o'lchamga keltirildi!")

if __name__ == '__main__':
    main()
