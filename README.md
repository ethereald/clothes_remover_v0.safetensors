# Clothes Remover Lora Model Backup for ComfyUI

This repository serves as a backup for the `clothes_remover_v0.safetensors` Lora model used with [ComfyUI](https://github.com/comfyanonymous/ComfyUI), an advanced and modular stable diffusion GUI and backend.

## Purpose
The main purpose of this repo is to safely store and manage the `clothes_remover_v0.safetensors` Lora model, which can be used for image manipulation tasks in ComfyUI. It also includes tools and scripts to help with archiving and restoring model files.

## Reference
- [ComfyUI GitHub Repository](https://github.com/comfyanonymous/ComfyUI)

## Usage


### 1. Backup and Restore with `zipper.py`
The `zipper.py` script helps you archive (zip) and restore (unzip) your Lora model files using positional arguments.

#### Example: Backup Lora Model Directory
```powershell
python zipper.py zip ComfyUI/models/loras
```
This command will encode all files in the `ComfyUI/models/loras` directory into JSON archives (e.g., `archive_1.json`, `archive_2.json`, ...), and delete the original files after archiving.

#### Example: Backup to a Different Directory
```powershell
python zipper.py zip ComfyUI/models/loras backup_dir
```
This command will encode all files in `ComfyUI/models/loras` into JSON archives in `backup_dir` (source files are not deleted).

#### Example: Restore Lora Model Directory
```powershell
python zipper.py unzip ComfyUI/models/loras
```
This command will decode all JSON archives in `ComfyUI/models/loras` and restore the original files, removing the JSON archives after extraction.

### 2. Integration with ComfyUI
After restoring the model, you can use it in ComfyUI by placing it in the `ComfyUI/models/loras/` directory. Then, load the model in the ComfyUI interface as you would with any other Lora model.

## Notes
- Make sure you have Python 3.8+ installed.
- For more advanced usage, run `python zipper.py --help` to see all available commands and options.

## License

This project is licensed under the MIT License:

```
MIT License

Copyright (c) 2025 ethereald

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
