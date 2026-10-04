"""Render previews directly from an encoded Gemielle pet sheet."""
from pathlib import Path
import argparse
import json
import sys
from PIL import Image, ImageDraw

SPECS = [
    ("idle", 0, 6, 180), ("running-right", 1, 8, 120),
    ("running-left", 2, 8, 120), ("waving", 3, 4, 160),
    ("jumping", 4, 5, 160), ("failed", 5, 8, 160),
    ("waiting", 6, 6, 180), ("running", 7, 6, 180), ("review", 8, 6, 180),
]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("atlas", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--media-path", type=Path)
    args=parser.parse_args()
    im=Image.open(args.atlas).convert("RGBA")
    out=args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    def cell(row, col):
        return im.crop((col*192,row*208,(col+1)*192,(row+1)*208))
    def canvas(frame, label):
        bg=Image.new("RGB",(192,232),(240,240,245))
        bg.paste(frame,(0,0),frame)
        ImageDraw.Draw(bg).text((8,216),label,fill=(25,25,45))
        return bg
    all_frames, durations=[],[]
    for state,row,count,duration in SPECS:
        for col in range(count):
            label=state
            if state=="running":
                label="Thinking" if col<3 else "Writing"
            if state=="review":
                label="Finished: clipboard up"
            all_frames.append(canvas(cell(row,col),label))
            durations.append(duration)
    all_frames[0].save(out/"all-states.gif",save_all=True,
                     append_images=all_frames[1:],duration=durations,loop=0)
    transition=[cell(0,0),cell(0,2),*[cell(4,i) for i in range(5)],cell(0,3),cell(0,5)]
    transition[0].save(out/"idle-jump-idle.gif",save_all=True,
                       append_images=transition[1:],duration=180,loop=0,disposal=2)
    look=[cell(9+i//8,i%8) for i in range(16)]
    look[0].save(out/"look-loop.gif",save_all=True,
                 append_images=look[1:],duration=140,loop=0,disposal=2)
    states=[("Listening",0,0),("Thinking",7,1),("Writing",7,4),("Completed",8,2)]
    stills=Image.new("RGB",(768,232),(240,240,245))
    for i,(label,row,col) in enumerate(states):
        stills.paste(canvas(cell(row,col),label),(192*i,0))
    stills.save(out/"four-stills.png")
    for name,row,col in [("idle",0,0),("jump-apex",4,2),("look-up",9,0),("look-down",10,0)]:
        cell(row,col).save(out/(name+".png"))
    video=None
    if args.media_path:
        sys.path.insert(0,str(args.media_path))
        import imageio_ffmpeg
        video=out/"all-states.mp4"
        writer=imageio_ffmpeg.write_frames(str(video),(192,232),fps=15,
               codec="libx264",macro_block_size=1,
               output_params=["-movflags","+faststart"])
        writer.send(None)
        for frame,duration in zip(all_frames,durations):
            for _ in range(max(1,round(duration*15/1000))):
                writer.send(frame.tobytes())
        writer.close()
    (out/"preview-manifest.json").write_text(json.dumps({
        "source_atlas":str(args.atlas),"states":9,"look_directions":16,
        "all_state_frames":len(all_frames),"video":video.name if video else None,
        "rendered_from_encoded_sheet":True
    },indent=2)+"\n",encoding="utf-8")
    print("Rendered nine-state GIF, transition, sixteen directions, four stills"+
          (", and MP4." if video else "."))

if __name__=="__main__":
    main()
