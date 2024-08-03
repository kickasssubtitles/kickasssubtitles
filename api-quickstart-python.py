# KickAssSubtitles API Python example

import struct
import os
import requests
import time
import base64

def hash_opensubtitles(video_path):
    """Compute a hash using OpenSubtitles' algorithm.

    :param str video_path: path of the video.
    :return: the hash.
    :rtype: str

    """
    bytesize = struct.calcsize(b'<q')
    with open(video_path, 'rb') as f:
        filesize = os.path.getsize(video_path)
        filehash = filesize
        if filesize < 65536 * 2:
            return
        for _ in range(65536 // bytesize):
            filebuffer = f.read(bytesize)
            (l_value,) = struct.unpack(b'<q', filebuffer)
            filehash += l_value
            filehash &= 0xFFFFFFFFFFFFFFFF  # to remain as 64bit number
        f.seek(max(0, filesize - 65536), 0)
        for _ in range(65536 // bytesize):
            filebuffer = f.read(bytesize)
            (l_value,) = struct.unpack(b'<q', filebuffer)
            filehash += l_value
            filehash &= 0xFFFFFFFFFFFFFFFF
    returnedhash = '%016x' % filehash

    return returnedhash

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
        "hashes[opensubtitles]": hash_opensubtitles("Some.Movie.2006.1080p.BluRay.x264.mp4"),
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
        "hashes[opensubtitles]": hash_opensubtitles("Some.Movie.2006.1080p.BluRay.x264.mp4"),
        "language": "pl", # optional - defaults to "en"
        "encoding": "UTF-8", # optional - defaults to "UTF-8"
        "format": "subrip" # optional - defaults to "subrip"
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
        "encoding": "UTF-8", # optional - defaults to "UTF-8"
        "format": "webvtt", # optional - defaults to "subrip"
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
