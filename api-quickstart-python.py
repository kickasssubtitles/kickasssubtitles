# KickAssSubtitles API Python example

import struct
import os
import requests
import time
import base64

def opensubtitles_hash(filename):
    try:
        longlongformat = '<q'  # little-endian long long
        bytesize = struct.calcsize(longlongformat)
        filesize = os.path.getsize(filename)
        hash = filesize

        if filesize < 65536 * 2:
            raise ValueError("File size is too small for this hash algorithm.")

        with open(filename, 'rb') as f:
            for _ in range(65536 // bytesize):
                buffer = f.read(bytesize)
                (l_value,) = struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF  # to remain as 64bit number

            f.seek(max(0, filesize - 65536), 0)
            for _ in range(65536 // bytesize):
                buffer = f.read(bytesize)
                (l_value,) = struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF

        return "{:016x}".format(hash)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def user_endpoint_example():
    print("[/api/user] endpoint example")
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer 1VS3lrNBp8UBB3eBBMWAWynHWh7KtiyuMKVJ4HiQ377c1d69"
    }
    response = requests.request("GET", "https://kickasssubtitles.com/api/user", headers=headers)
    print(response.text)

def upload_endpoint_example():
    print("[/api/upload] endpoint example")
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer 1VS3lrNBp8UBB3eBBMWAWynHWh7KtiyuMKVJ4HiQ377c1d69"
    }
    payload = {
        "filename": "Some.Movie.2006.1080p.BluRay.x264.mp4",
        "filesize": os.path.getsize("Some.Movie.2006.1080p.BluRay.x264.mp4"),
        "hashes[opensubtitles]": opensubtitles_hash("Some.Movie.2006.1080p.BluRay.x264.mp4"),
        "imdb_url": "https://www.imdb.com/title/tt0389557/",
        "language": "pl"
    }
    files = [
        ("subtitle",("Some.Movie.2006.1080p.BluRay.x264.srt", open("Some.Movie.2006.1080p.BluRay.x264.srt", "rb"), "application/octet-stream"))
    ]
    response = requests.request("POST", "https://kickasssubtitles.com/api/upload", headers=headers, data=payload, files=files)
    print(response.text)

def search_endpoint_example():
    print("[/api/search] endpoint example")
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer 1VS3lrNBp8UBB3eBBMWAWynHWh7KtiyuMKVJ4HiQ377c1d69"
    }
    payload = {
        "filename": "Some.Movie.2006.1080p.BluRay.x264.mp4",
        "filesize": os.path.getsize("Some.Movie.2006.1080p.BluRay.x264.mp4"),
        "hashes[opensubtitles]": opensubtitles_hash("Some.Movie.2006.1080p.BluRay.x264.mp4"),
        "language": "pl",
        "encoding": "UTF-8", # optional
        "format": "subrip" # optional
    }
    response = requests.request("POST", "https://kickasssubtitles.com/api/search", headers=headers, data=payload)
    task = response.json()
    print(task["id"])

    print("Sleeping for 10 seconds...")
    time.sleep(10)

    response = requests.request("GET", "https://kickasssubtitles.com/api/tasks/" + task["id"], headers=headers)
    task = response.json()
    if task["status"] != "completed":
        raise Exception("Something went wrong.")
    subtitle_file = "subtitle." + task["result"]["subtitles"][0]["extension"]
    with open(subtitle_file, "wb") as f:
        f.write(base64.b64decode(task["result"]["subtitles"][0]["contents_base64"]))
    print(f"Subtitle written to {subtitle_file}")

def convert_endpoint_example():
    print("[/api/convert] endpoint example")
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer 1VS3lrNBp8UBB3eBBMWAWynHWh7KtiyuMKVJ4HiQ377c1d69"
    }
    payload = {
        "language": "pl", # optional
        "input_encoding": "UTF-8", # optional
        "encoding": "UTF-8",
        "format": "webvtt",
        "fps": None # optional
    }
    files = [
        ("subtitle",("Some.Movie.2006.1080p.BluRay.x264.srt", open("Some.Movie.2006.1080p.BluRay.x264.srt", "rb"), "application/octet-stream"))
    ]
    response = requests.request("POST", "https://kickasssubtitles.com/api/convert", headers=headers, data=payload, files=files)
    task = response.json()
    print(task["id"])

    print("Sleeping for 10 seconds...")
    time.sleep(10)

    response = requests.request("GET", "https://kickasssubtitles.com/api/tasks/" + task["id"], headers=headers)
    task = response.json()
    if task["status"] != "completed":
        raise Exception("Something went wrong.")
    subtitle_file = "subtitle." + task["result"]["subtitles"][0]["extension"]
    with open(subtitle_file, "wb") as f:
        f.write(base64.b64decode(task["result"]["subtitles"][0]["contents_base64"]))
    print(f"Subtitle written to {subtitle_file}")

def main():
    print("KickAssSubtitles API Python example")

    # Uncomment choosen example
    # user_endpoint_example()
    # upload_endpoint_example()
    # search_endpoint_example()
    # convert_endpoint_example()

if __name__ == "__main__":
    main()
