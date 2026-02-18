# Assignment_4_Mashup_PsRana
# Music Mashup Generator

**Name:** Gaurika Dua
**Roll Number:** 102303271  
**Batch:** 3C18

---

# 1. Methodology

Video Collection → Audio Conversion → Audio Trimming → Audio Merging

The system downloads YouTube videos based on a singer's name, converts them to audio format, trims each audio to the specified duration, and merges all trimmed clips into a single mashup file.

# 2. Description

- **Input:** YouTube video search query (Singer name)
- **N:** Number of videos to process (minimum 10)
- **Y:** Duration of each audio clip in seconds (minimum 20)
- **Output:** mashup.mp3 (merged audio file)

# 3. Objective

- Automatically download songs from YouTube for a specified singer
- Extract and convert video files to MP3 audio format
- Trim each audio file to the specified duration
- Merge all trimmed audio clips into a single mashup file
- Compress the mashup into a ZIP file
- Send the final mashup to the user via email

# 4. Web Application

The web application provides a simple interface for users to create custom music mashups:

### Features:

- **User-friendly form** for entering singer name, number of videos, duration, and email
- **Real-time processing** with status updates
- **Email delivery** of the final mashup ZIP file
- **Responsive design** using Tailwind CSS

### Technology Stack:

- **Backend:** Flask (Python web framework)
- **Frontend:** HTML, CSS (Tailwind), JavaScript
- **Video Processing:** yt-dlp for YouTube downloads
- **Audio Processing:** FFmpeg for conversion and merging
- **Email Service:** SMTP (Gmail)

### How to Run:

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set up environment variables:
   Create a `.env` file with:

```
SENDER_EMAIL=your_email@gmail.com
APP_PASSWORD=your_app_password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
```

3. **Important: Export YouTube Cookies**

   Due to YouTube's bot detection, you need to export your browser cookies.
   See [COOKIES_SETUP.md](COOKIES_SETUP.md) for detailed instructions.

4. Run the application:

```bash
python app.py
```

5. Access the web interface at `http://localhost:5000`

# 5. Result

Upon successful execution of the mashup generator, you will receive the following:

### Output Delivered via Email:

1. **Mashup Audio File**: A single merged MP3 file containing clips from your selected artist's songs
   - Each clip is trimmed to your specified duration (minimum 20 seconds)
   - All clips are seamlessly merged into one continuous audio file

2. **ZIP Archive**: The mashup file is compressed and packaged in a ZIP format for easy download

3. **Email Delivery**: The ZIP file is automatically sent to your provided email address with the subject "Your Mashup Song Files"

### What the Mashup Contains:

- **Artist**: Songs from the singer you specified
- **Duration**: Each song clip trimmed to your chosen length
- **Quality**: High-quality audio extracted from YouTube videos
- **Format**: MP3 file format for universal compatibility
- **File Naming**: `<ArtistName>_mashup.zip` (e.g., `Ed_Sheeran_mashup.zip`)

### Example Workflow:

```
Input:
- Singer Name: Ed Sheeran
- Number of Videos: 15
- Duration: 25 seconds
- Email: your@email.com

Process:
→ Downloads 15 Ed Sheeran songs from YouTube
→ Extracts audio and converts to MP3
→ Trims each to 25 seconds
→ Merges into single mashup.mp3 (~6 minutes long)
→ Creates ZIP archive
→ Sends to your@email.com

Result:
You receive "Ed_Sheeran_mashup.zip" via email
Extract and enjoy your custom mashup!
```

### Technical Details:

- **Audio Codec**: MP3 (192 kbps)
- **Total Duration**: (Number of Videos × Duration per clip)
- **File Size**: Approximately 1-3 MB per minute of audio
- **Processing Time**: Varies based on number of videos and internet speed (typically 2-5 minutes)

---

**Note**: Make sure to check your spam/junk folder if you don't receive the email within a few minutes. The mashup generation process runs in the background, and you'll be notified via email once complete.

## Author

**Gaurika Dua**

Roll No: 102303271

Thapar Institute of Engineering and Technology

---

## License

This project is intended for **academic and educational use** as part of a university assignment. Redistribution or reuse should acknowledge the author.
