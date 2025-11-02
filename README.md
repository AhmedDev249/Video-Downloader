# Video-Downloader

A Django REST API backend service for downloading videos from various platforms using yt-dlp. This application provides endpoints to retrieve video information and download videos in different formats.

## Features

- **Video Information Retrieval**: Get detailed information about videos including title, uploader, duration, and available formats
- **Multiple Format Support**: Download videos in various resolutions and formats
- **RESTful API**: Clean and simple REST API endpoints
- **Cookie Support**: Optional cookie file support for authentication-required content
- **CORS Enabled**: Cross-Origin Resource Sharing enabled for frontend integration
- **File Serving**: Direct file serving endpoint for downloaded videos

## Technology Stack

- **Django 5.2.7**: Web framework
- **Django REST Framework 3.16.1**: API framework
- **yt-dlp 2025.10.22**: Video downloading library
- **django-cors-headers 4.9.0**: CORS handling
- **SQLite**: Database (default)

## API Endpoints

### 1. Get Video Info
**POST** `/api/youtube/info/`

Retrieve video metadata and available formats.

**Request Body:**
```json
{
  "url": "https://example.com/video"
}
```

**Response:**
```json
{
  "title": "Video Title",
  "uploader": "Channel Name",
  "duration": 180,
  "formats": [
    {
      "format_id": "22",
      "height": 720,
      "ext": "mp4"
    }
  ]
}
```

### 2. Download Video
**POST** `/api/youtube/download/`

Download a video in a specific format.

**Request Body:**
```json
{
  "url": "https://example.com/video",
  "format_id": "22"
}
```

**Response:**
```json
{
  "message": "تم التحميل بنجاح ✅",
  "file_url": "http://localhost:8000/api/youtube/downloaded/Video_Title.mp4"
}
```

### 3. Serve Downloaded File
**GET** `/api/youtube/downloaded/<filename>/`

Download the previously downloaded video file.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Video-Downloader
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Navigate to the core directory:
```bash
cd core
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## Configuration

### Cookie Support
To download videos that require authentication, place a `cookies.txt` file in the `core/` directory. The application will automatically detect and use it.

### Downloads Directory
Downloaded videos are stored in the `downloads/` directory within the project root. This directory is automatically created if it doesn't exist.

## Project Structure

```
Video-Downloader/
├── core/
│   ├── core/              # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── youtube_downloader/ # Main application
│   │   ├── views.py       # API endpoints
│   │   ├── urls.py        # URL routing
│   │   └── ...
│   ├── downloads/         # Downloaded videos (ignored in git)
│   ├── cookies.txt        # Optional cookie file (ignored in git)
│   ├── db.sqlite3         # Database (ignored in git)
│   └── manage.py
├── venv/                  # Virtual environment (ignored in git)
├── requirements.txt       # Python dependencies
└── README.md
```

## Security Notes

- The application is configured for development (`DEBUG = True`)
- CORS is enabled for all origins (`CORS_ALLOW_ALL_ORIGINS = True`)
- Before deploying to production:
  - Set `DEBUG = False`
  - Configure proper `ALLOWED_HOSTS`
  - Restrict CORS to specific origins
  - Use environment variables for sensitive data
  - Use a production-grade database (PostgreSQL/MySQL)
  - Implement proper authentication and rate limiting

## License

This project is provided as-is for educational and personal use.