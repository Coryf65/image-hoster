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

*example*
```json
{
    "filename":"b2964707c6c541aeaec85ea2c4089ddd.webp",
    "markdown":"![How-to-make-Chicken-and-Dumplings-1.webp](http://localhost:8000/images/b2964707c6c541aeaec85ea2c4089ddd.webp)","original_filename":"How-to-make-Chicken-and-Dumplings-1.webp",
    "url":"http://localhost:8000/images/b2964707c6c541aeaec85ea2c4089ddd.webp"
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


## Run with Docker (Alpine)

This project includes a Docker image based on Alpine Linux via `python:3.12-alpine`.

### Option 1: Docker Compose (recommended)

Build and run:
```bash
docker compose up -d --build
```

The container will:
- expose the app on `http://localhost:8000`
- map container port `8000` to host port `8000`
- persist uploaded images in a named Docker volume `image_hoster_images`

Stop it:
```bash
docker compose down
```

Stop and remove the volume too:
```bash
docker compose down -v
```

### Option 2: Plain Docker CLI

Build image:
```bash
docker build -t image-hoster:alpine .
```

Run container on the same port and mount a named volume:
```bash
docker run -d \
    --name image-hoster \
    -p 8000:8000 \
    -e HOST=0.0.0.0 \
    -e PORT=8000 \
    -e IMAGE_HOSTER_DIR=/app/images \
    -v image_hoster_images:/app/images \
    image-hoster:alpine
```

Check logs:
```bash
docker logs -f image-hoster
```

Stop and remove container:
```bash
docker rm -f image-hoster
```

Remove volume (optional):
```bash
docker volume rm image_hoster_images
```