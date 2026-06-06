from http.server import BaseHTTPRequestHandler
from youtube_transcript_api import YouTubeTranscriptApi
import json
import re

class handler(BaseHTTPRequestHandler):

    def do_POST(self):

        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        data = json.loads(body)

        url = data["url"]

        match = re.search(
            r"(?:v=|youtu\.be/)([^&?/]+)",
            url
        )

        if not match:
            self.send_response(400)
            self.end_headers()
            return

        video_id = match.group(1)

        try:

            transcript = YouTubeTranscriptApi.get_transcript(
                video_id
            )

            text = " ".join(
                item["text"]
                for item in transcript
            )

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "application/json"
            )

            self.send_header(
                "Access-Control-Allow-Origin",
                "*"
            )

            self.end_headers()

            self.wfile.write(
                json.dumps({
                    "transcript": text
                }).encode()
            )

        except Exception as e:

            self.send_response(500)
            self.end_headers()

            self.wfile.write(
                json.dumps({
                    "error": str(e)
                }).encode()
            )
