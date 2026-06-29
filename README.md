# image hoster

a simple static image server for hosting images for other web applications


## Get Started 

### Start the server

move into the directory
```bash
cd /mnt/sdb1/Code/_MyApps/Python/image-hoster
```

get python dependancies
```bash
python -m pip install -r requirements.txt
```

run the app
```bash
python main.py
```

- You should see Flask start on http://localhost:8000

### Upload a test image from another terminal

move into the directory
```bash
cd /mnt/sdb1/Code/_MyApps/Python/image-hoster
```

upload an image to the web app
```bash
curl -F "image=@/full/path/to/your/test-image.png" http://localhost:8000/upload
```

Expected response is JSON with fields like:
```json
{
    url: "url to the location of the file",
    markdown: null,
    filename: "name of the file"
}
```

### Verify the image endpoint

Copy the url from the upload response
Open it in a browser, or run:
```bash
curl -I "PASTE_URL_HERE"
```


You should get HTTP 200 and an image content type.

### Test Markdown embedding
Use the returned markdown value directly, example format:
<img src="http://localhost:8000/images/....png" alt="test-image.png">


## Run Tests

Open terminal in `/mnt/sdb1/Code/_MyApps/Python/image-hoster`
Run:
```bash
python -m unittest discover -s tests -v
```