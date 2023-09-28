# Cleaner for Stable Diffusion WebUI
This is a WEBUI extension that provides image erasure functionality. It supports both UI and API simultaneously.


![Alt text](https://github.com/novitalabs/sd-webui-cleaner/blob/main/example/images/image1.png)

<br>

## install
Clone this project in the WEBUI extensions folder
```
git clone https://github.com/novitalabs/sd-webui-cleaner.git
```
<br>
## Get Started
### API

```
//request-----------------------------------
POST http://127.0.0.1:7860/cleanup

body:
{
    "input_image": "<image base64 string>",
    "mask": "<mask base64 string>"
}


//response-----------------------------------
{
  "code": 0,  // 0:success
  "message": "ok",
  "image": "<image base64 string>"
}
```
