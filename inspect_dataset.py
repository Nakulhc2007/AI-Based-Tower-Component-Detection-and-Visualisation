"""
Dataset inspection script for Tower Detection Hackathon.
Analyzes all images in the sample/ directory for:
- Count, formats, dimensions
- File sizes
- Corrupt files
- Duplicate detection (by file size + hash)
- Brightness/blur statistics
"""

import os
import hashlib
import json
from pathlib import Path
from collections import Counter

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import cv2
    import numpy as np
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

SAMPLE_DIR = Path(r"a:\projects\ksit hackathon\sample")

def file_hash(path, chunk_size=65536):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def inspect():
    files = sorted(SAMPLE_DIR.iterdir())
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    
    results = {
        'total_files': len(files),
        'extensions': Counter(),
        'sizes_bytes': [],
        'dimensions': [],
        'corrupt': [],
        'hash_groups': {},
        'size_groups': {},
        'brightness_stats': [],
        'blur_stats': [],
        'filenames': [],
    }
    
    for f in files:
        ext = f.suffix.lower()
        results['extensions'][ext] += 1
        fsize = f.stat().st_size
        results['sizes_bytes'].append((f.name, fsize))
        results['filenames'].append(f.name)
        
        # Group by file size (exact duplicates will have same size)
        results['size_groups'].setdefault(fsize, []).append(f.name)
        
        # Hash for duplicate detection
        try:
            h = file_hash(f)
            results['hash_groups'].setdefault(h, []).append(f.name)
        except Exception as e:
            pass
        
        # Read image
        if HAS_PIL and ext in image_extensions:
            try:
                img = Image.open(f)
                img.verify()  # Check not corrupt
                img = Image.open(f)  # Re-open after verify
                w, h_img = img.size
                results['dimensions'].append((f.name, w, h_img))
            except Exception as e:
                results['corrupt'].append((f.name, str(e)))
                continue
        
        # OpenCV analysis for brightness and blur
        if HAS_CV2 and ext in image_extensions:
            try:
                img_cv = cv2.imread(str(f))
                if img_cv is not None:
                    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
                    mean_brightness = float(np.mean(gray))
                    laplacian_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
                    dark_pct = float(np.sum(gray < 30) / gray.size * 100)
                    bright_pct = float(np.sum(gray > 225) / gray.size * 100)
                    results['brightness_stats'].append({
                        'name': f.name,
                        'mean_brightness': round(mean_brightness, 1),
                        'dark_pct': round(dark_pct, 2),
                        'bright_pct': round(bright_pct, 2),
                    })
                    results['blur_stats'].append({
                        'name': f.name,
                        'laplacian_var': round(laplacian_var, 2),
                    })
            except Exception:
                pass
    
    # Print report
    print("=" * 70)
    print("DATASET INSPECTION REPORT")
    print("=" * 70)
    
    print(f"\nTotal files: {results['total_files']}")
    
    print(f"\nFile extensions:")
    for ext, count in results['extensions'].most_common():
        print(f"  {ext}: {count}")
    
    # Dimensions summary
    if results['dimensions']:
        widths = [d[1] for d in results['dimensions']]
        heights = [d[2] for d in results['dimensions']]
        dim_counter = Counter([(d[1], d[2]) for d in results['dimensions']])
        print(f"\nImage dimensions:")
        print(f"  Width range: {min(widths)} - {max(widths)}")
        print(f"  Height range: {min(heights)} - {max(heights)}")
        print(f"  Unique dimensions: {len(dim_counter)}")
        print(f"  Top 10 dimensions:")
        for dim, count in dim_counter.most_common(10):
            print(f"    {dim[0]}x{dim[1]}: {count} images")
    
    # File sizes
    sizes = [s[1] for s in results['sizes_bytes']]
    print(f"\nFile sizes:")
    print(f"  Min: {min(sizes):,} bytes ({min(sizes)/1024:.1f} KB)")
    print(f"  Max: {max(sizes):,} bytes ({max(sizes)/1024/1024:.1f} MB)")
    print(f"  Mean: {sum(sizes)/len(sizes):,.0f} bytes ({sum(sizes)/len(sizes)/1024/1024:.1f} MB)")
    
    # Small files (potentially low quality or thumbnails)
    small_files = [(n, s) for n, s in results['sizes_bytes'] if s < 50000]
    if small_files:
        print(f"\n  Small files (<50KB): {len(small_files)}")
        for n, s in sorted(small_files, key=lambda x: x[1]):
            print(f"    {n}: {s:,} bytes ({s/1024:.1f} KB)")
    
    # Large files
    large_files = [(n, s) for n, s in results['sizes_bytes'] if s > 5_000_000]
    print(f"\n  Large files (>5MB): {len(large_files)}")
    
    # Corrupt
    if results['corrupt']:
        print(f"\nCorrupt images: {len(results['corrupt'])}")
        for name, err in results['corrupt']:
            print(f"  {name}: {err}")
    else:
        print(f"\nCorrupt images: 0")
    
    # Exact duplicates (same hash)
    dup_groups = {h: names for h, names in results['hash_groups'].items() if len(names) > 1}
    if dup_groups:
        print(f"\nExact duplicates (same MD5 hash): {len(dup_groups)} groups")
        for h, names in dup_groups.items():
            print(f"  Hash {h[:12]}...: {names}")
    else:
        print(f"\nExact duplicates: 0")
    
    # Same-size files (potential near-duplicates)
    same_size = {s: names for s, names in results['size_groups'].items() if len(names) > 1}
    if same_size:
        print(f"\nSame-size file groups (potential near-duplicates): {len(same_size)} groups")
        for s, names in sorted(same_size.items()):
            print(f"  Size {s:,} bytes: {names}")
    
    # Brightness stats
    if results['brightness_stats']:
        brightnesses = [b['mean_brightness'] for b in results['brightness_stats']]
        print(f"\nBrightness statistics:")
        print(f"  Mean brightness range: {min(brightnesses):.1f} - {max(brightnesses):.1f}")
        print(f"  Average mean brightness: {sum(brightnesses)/len(brightnesses):.1f}")
        
        dark_imgs = [b for b in results['brightness_stats'] if b['mean_brightness'] < 60]
        bright_imgs = [b for b in results['brightness_stats'] if b['mean_brightness'] > 200]
        
        if dark_imgs:
            print(f"\n  Very dark images (mean < 60): {len(dark_imgs)}")
            for b in sorted(dark_imgs, key=lambda x: x['mean_brightness']):
                print(f"    {b['name']}: brightness={b['mean_brightness']}, dark_pct={b['dark_pct']}%")
        
        if bright_imgs:
            print(f"\n  Very bright images (mean > 200): {len(bright_imgs)}")
            for b in sorted(bright_imgs, key=lambda x: -x['mean_brightness']):
                print(f"    {b['name']}: brightness={b['mean_brightness']}, bright_pct={b['bright_pct']}%")
    
    # Blur stats
    if results['blur_stats']:
        laps = [b['laplacian_var'] for b in results['blur_stats']]
        print(f"\nBlur (Laplacian variance) statistics:")
        print(f"  Range: {min(laps):.2f} - {max(laps):.2f}")
        print(f"  Mean: {sum(laps)/len(laps):.2f}")
        print(f"  Median: {sorted(laps)[len(laps)//2]:.2f}")
        
        blurry = [b for b in results['blur_stats'] if b['laplacian_var'] < 50]
        if blurry:
            print(f"\n  Potentially blurry images (Laplacian var < 50): {len(blurry)}")
            for b in sorted(blurry, key=lambda x: x['laplacian_var']):
                print(f"    {b['name']}: laplacian_var={b['laplacian_var']}")
    
    print("\n" + "=" * 70)
    print("END OF REPORT")
    print("=" * 70)

if __name__ == '__main__':
    inspect()
