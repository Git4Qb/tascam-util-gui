## Future idea: generate UI icon sizes automatically

Keep only the source/master icon in the repository:

`tuxam/ui/assets/icons/source/tuxam_icon.png`

During install/build, automatically generate required runtime icon sizes:

- 16x16
- 32x32
- 48x48
- 128x128
- 256x256

Generated files should go to:

`tuxam/ui/assets/icons/`

Possible script name:

`tools/generate_icons.sh`

Possible command:

```bash
for s in 16 32 48 128 256; do
  ffmpeg -y -i tuxam/ui/assets/icons/source/tuxam_icon.png \
    -vf scale=${s}:${s} \
    tuxam/ui/assets/icons/tuxam_icon_${s}.png
done
