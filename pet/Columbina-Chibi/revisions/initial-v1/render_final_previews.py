from pathlib import Path
from PIL import Image

root = Path('/tmp/columbina-pet-run')
atlas = Image.open(root / 'final/spritesheet-extended.png').convert('RGBA')
states = [('idle', 6), ('running-right', 8), ('running-left', 8),
          ('waving', 4), ('jumping', 5), ('failed', 8),
          ('waiting', 6), ('running', 6), ('review', 6)]
frames_root = root / 'qa/final-frames'
previews = root / 'final/previews'
previews.mkdir(parents=True, exist_ok=True)
all_frames = []
for row, (state, count) in enumerate(states):
    state_dir = frames_root / state
    state_dir.mkdir(parents=True, exist_ok=True)
    cells = []
    for col in range(count):
        cell = atlas.crop((col * 192, row * 208, (col + 1) * 192, (row + 1) * 208))
        cell.save(state_dir / f'{col:02d}.png')
        cells.append(cell)
    all_frames.extend(cells)

def gif(name, cells, duration):
    cells[0].save(previews / name, save_all=True, append_images=cells[1:],
                  duration=duration, loop=0, disposal=2, optimize=False)

gif('all-states.gif', all_frames, 170)
idle = [atlas.crop((c * 192, 0, (c + 1) * 192, 208)) for c in range(6)]
jump = [atlas.crop((c * 192, 4 * 208, (c + 1) * 192, 5 * 208)) for c in range(5)]
gif('idle-jump-idle.gif', idle + jump + idle, 120)
look = [atlas.crop((c * 192, r * 208, (c + 1) * 192, (r + 1) * 208))
        for r in (9, 10) for c in range(8)]
gif('look-loop.gif', look, 130)
for name, cell in [('idle.png', idle[0]), ('jump-apex.png', jump[2]),
                   ('look-up.png', look[0]), ('look-down.png', look[8])]:
    cell.save(previews / name)
print(previews)
