# DRM & Media Tool build exe

``` 
pip install pyinstaller
```

```
 pyinstaller --onefile --add-data "assets;assets" --name="DRM & Media Tool" --windowed --icon=assets\\logo.ico main.py --noconsole 
```
Note: if that not work use pyinstaller main.py


For more info refer: https://github.com/joeldcosta/pyinstaller

# Reference

https://stackoverflow.com/questions/9913032/how-can-i-extract-audio-from-video-with-ffmpeg

https://plainenglish.io/blog/pyinstaller-exe-false-positive-trojan-virus-resolved-b33842bd3184