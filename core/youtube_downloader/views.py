from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from django.conf import settings
import yt_dlp
import os

DOWNLOAD_PATH = os.path.join(settings.BASE_DIR, "downloads")
COOKIES_PATH = os.path.join(settings.BASE_DIR, "cookies.txt")

os.makedirs(DOWNLOAD_PATH, exist_ok=True)


@api_view(['POST'])
def get_video_info(request):
    url = request.data.get("url")
    if not url:
        return Response({"error": "Missing URL"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        ydl_opts = {
            'cookiefile': COOKIES_PATH if os.path.exists(COOKIES_PATH) else None,
            'quiet': True,
            'no_warnings': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        formats = [
            {"format_id": f["format_id"], "height": f.get("height"), "ext": f["ext"]}
            for f in info.get("formats", []) if f.get("height")
        ]

        return Response({
            "title": info.get("title"),
            "uploader": info.get("uploader"),
            "duration": info.get("duration"),
            "formats": formats
        })
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def download_video(request):
    url = request.data.get("url")
    fmt = request.data.get("format_id")

    if not url or not fmt:
        return Response({"error": "Missing URL or format_id"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        ydl_opts = {
            'cookiefile': COOKIES_PATH if os.path.exists(COOKIES_PATH) else None,
            'format': fmt + '+bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_PATH, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        file_name = os.path.basename(filename)
        file_url = request.build_absolute_uri(f"/api/youtube/downloaded/{file_name}")

        return Response({
            "message": "تم التحميل بنجاح ✅",
            "file_url": file_url
        })
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def serve_downloaded_file(request, filename):
    file_path = os.path.join(DOWNLOAD_PATH, filename)
    if not os.path.exists(file_path):
        return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)
    return FileResponse(open(file_path, "rb"), as_attachment=True)
