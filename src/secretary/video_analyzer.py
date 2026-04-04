from typing import Optional
import re
import yt_dlp

from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

from secretary.models import VideoMetadata, VideoChapter, Material
from secretary.ai_router import ai_router
from secretary.database import db
from secretary.config import settings


class VideoAnalyzer:
    def __init__(self):
        self.ai = ai_router

    def _get_yt_dlp_info(self, url: str) -> Optional[dict]:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'socket_timeout': 30,
        }
        if settings.proxy_url:
            ydl_opts['proxy'] = settings.proxy_url
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(url, download=False)
        except Exception as e:
            print(f"yt-dlp error: {e}")
            return None

    def get_video_info(self, url: str) -> VideoMetadata:
        info = self._get_yt_dlp_info(url)
        
        if info:
            return VideoMetadata(
                channel=info.get('uploader', info.get('channel', 'unknown')),
                views=info.get('view_count', 0),
                likes=info.get('like_count', 0),
                duration=info.get('duration', 0),
            )
        
        return VideoMetadata(channel='unknown', views=0, likes=0, duration=0)

    def get_title(self, url: str) -> str:
        info = self._get_yt_dlp_info(url)
        return info.get('title', url) if info else url

    def get_transcript(self, url: str) -> Optional[str]:
        video_id = self._extract_video_id(url)
        if not video_id:
            return None
        
        try:
            ytt_api = YouTubeTranscriptApi()
            transcript_list = ytt_api.list(video_id)
            
            try:
                transcript = transcript_list.find_generated_transcript(['ru', 'en'])
            except:
                transcript = transcript_list.find_transcript(['ru', 'en'])
            
            transcript_data = transcript.fetch()
            text = " ".join([entry.text for entry in transcript_data])
            
            return text
            
        except Exception as e:
            print(f"Could not get transcript: {e}")
            return None

    def get_chapters(self, url: str) -> list[VideoChapter]:
        info = self._get_yt_dlp_info(url)
        
        chapters = []
        if info:
            try:
                chapters_data = info.get('chapters', [])
                if chapters_data:
                    for ch in chapters_data:
                        chapters.append(VideoChapter(
                            time=int(ch.get('start_time', 0)),
                            title=ch.get('title', '')
                        ))
            except Exception as e:
                print(f"Could not parse chapters: {e}")
            
            if not chapters:
                description = info.get('description', '')
                time_pattern = r'(\d{1,2}:?\d{0,2}:?\d{0,2})'
                for line in description.split('\n'):
                    match = re.match(rf'{time_pattern}\s+(.+)', line.strip())
                    if match:
                        time_str = match.group(1)
                        title = match.group(2).strip()
                        seconds = self._parse_time(time_str)
                        if seconds:
                            chapters.append(VideoChapter(time=seconds, title=title))
        
        return chapters

    def _detect_language(self, text: str) -> str:
        if not text:
            return 'en'
        ru_chars = sum(1 for c in text[:2000] if '\u0400' <= c <= '\u04FF')
        en_chars = sum(1 for c in text[:2000] if c.isalpha() and not '\u0400' <= c <= '\u04FF')
        return 'ru' if ru_chars > en_chars * 0.3 else 'en'

    def summarize_video(self, url: str) -> str:
        transcript = self.get_transcript(url)
        
        if not transcript:
            metadata = self.get_video_info(url)
            content = f"Video title: {url}\nChannel: {metadata.channel}"
        else:
            content = transcript
        
        if len(content) > 4000:
            content = content[:4000]
        
        lang = self._detect_language(content)
        
        if lang == 'ru':
            prompt = f"""╨ƒ╤Ç╨╛╨░╨╜╨░╨╗╨╕╨╖╨╕╤Ç╤â╨╣ ╤é╤Ç╨░╨╜╤ü╨║╤Ç╨╕╨┐╤é ╨╕ ╤ü╨╛╨╖╨┤╨░╨╣ ╤ü╤é╤Ç╤â╨║╤é╤â╤Ç╨╕╤Ç╨╛╨▓╨░╨╜╨╜╤â╤Ä ╨▓╤ï╨╢╨╕╨╝╨║╤â.

╨ñ╨╛╤Ç╨╝╨░╤é:
1. **╨₧ ╤ç╤æ╨╝:** (1 ╨┐╤Ç╨╡╨┤╨╗╨╛╨╢╨╡╨╜╨╕╨╡ - ╨▒╨╡╨╖ "╨▓╨╕╨┤╨╡╨╛"/"video")
2. **╨Ü╨╗╤Ä╤ç╨╡╨▓╤ï╨╡ ╨╝╤ï╤ü╨╗╨╕:** (3-5 ╨┐╤â╨╜╨║╤é╨╛╨▓ - ╨║╨╛╨╜╨║╤Ç╨╡╤é╨╜╤ï╨╡ ╨╕╨┤╨╡╨╕, ╤ä╨░╨║╤é╤ï)
3. **╨ÿ╨╜╤ü╤é╤Ç╤â╨╝╨╡╨╜╤é╤ï/╨á╨╡╤ê╨╡╨╜╨╕╤Å:** (╨╜╨░╨╖╨▓╨░╨╜╨╕╤Å + ╨║╤Ç╨░╤é╨║╨╛╨╡ ╨╛╨┐╨╕╤ü╨░╨╜╨╕╨╡ + ╨║╨╗╤Ä╤ç╨╡╨▓╨╛╨╡ ╨╛╤é╨╗╨╕╤ç╨╕╨╡ ╨╛╤é ╨┤╤Ç╤â╨│╨╕╤à)
4. **╨ÿ╤é╨╛╨│:** (╨▓╤ï╨▓╨╛╨┤)

╨æ╤â╨┤╤î ╨║╨╛╨╜╨║╤Ç╨╡╤é╨╜╤ï╨╝. ╨ò╤ü╨╗╨╕ ╤ì╤é╨╛ ╤ü╤Ç╨░╨▓╨╜╨╡╨╜╨╕╨╡ - ╨╛╨┐╨╕╤ê╨╕ ╨║╨╗╤Ä╤ç╨╡╨▓╤ï╨╡ ╨╛╤é╨╗╨╕╤ç╨╕╤Å ╤ü╤Ç╨░╨▓╨╜╨╕╨▓╨░╨╡╨╝╤ï╤à ╤ê╤é╤â╨║.

╨ó╤Ç╨░╨╜╤ü╨║╤Ç╨╕╨┐╤é:
{content}

╨Æ╤ï╨╢╨╕╨╝╨║╨░:"""
        else:
            prompt = f"""Analyze this transcript and create a structured summary.

Format:
1. **What it's about:** (1 sentence - no "video"/"video")
2. **Key points:** (3-5 bullet points - specific ideas, facts)
3. **Tools/Solutions:** (names + brief description + key difference from others)
4. **Conclusion:** (takeaway)

Be specific. If this is a comparison - describe key differences between items.

Transcript:
{content}

Summary:"""
        
        summary = self.ai.complete(prompt)
        
        return summary

    def find_relevant_parts(
        self,
        url: str,
        query: str
    ) -> list[tuple[int, str]]:
        transcript = self.get_transcript(url)
        
        if not transcript:
            return []
        
        prompt = f"""╨¥╨░╨╣╨┤╨╕ ╨▓ ╤é╤Ç╨░╨╜╤ü╨║╤Ç╨╕╨┐╤é╨╡ ╨▓╨╕╨┤╨╡╨╛ ╨╝╨╛╨╝╨╡╨╜╤é╤ï, ╤Ç╨╡╨╗╨╡╨▓╨░╨╜╤é╨╜╤ï╨╡ ╨╖╨░╨┐╤Ç╨╛╤ü╤â "{query}".
╨Æ╨╡╤Ç╨╜╨╕ ╤ü╨┐╨╕╤ü╨╛╨║ timestamps ╨╕ ╤ü╨╛╨╛╤é╨▓╨╡╤é╤ü╤é╨▓╤â╤Ä╤ë╨╕╤à ╤ä╤Ç╨░╨│╨╝╨╡╨╜╤é╨╛╨▓ ╤é╨╡╨║╤ü╤é╨░.

╨ó╤Ç╨░╨╜╤ü╨║╤Ç╨╕╨┐╤é:
{transcript[:10000]}

╨ñ╨╛╤Ç╨╝╨░╤é ╨╛╤é╨▓╨╡╤é╨░ (╨▓╨╡╤Ç╨╜╨╕ 3-5 ╤ü╨░╨╝╤ï╤à ╤Ç╨╡╨╗╨╡╨▓╨░╨╜╤é╨╜╤ï╤à):
0:00 - ╤Ç╨╡╨╗╨╡╨▓╨░╨╜╤é╨╜╤ï╨╣ ╤ä╤Ç╨░╨│╨╝╨╡╨╜╤é
2:30 - ╨┤╤Ç╤â╨│╨╛╨╣ ╤ä╤Ç╨░╨│╨╝╨╡╨╜╤é
..."""
        
        result = self.ai.complete(prompt)
        
        parts = []
        for line in result.split('\n'):
            if ' - ' in line and ':' in line:
                try:
                    time_part, text = line.split(' - ', 1)
                    time_part = time_part.strip()
                    seconds = self._parse_time(time_part)
                    if seconds is not None:
                        parts.append((seconds, text.strip()))
                except:
                    continue
        
        return parts[:5]

    def analyze_video(self, material_id: str) -> Material:
        material = db.get_material(material_id)
        if not material or not material.source_url:
            raise ValueError(f"Video material not found: {material_id}")
        
        url = material.source_url
        
        metadata = self.get_video_info(url)
        metadata.chapters = self.get_chapters(url)
        
        transcript = self.get_transcript(url)
        if transcript:
            metadata.transcript = transcript[:5000]
        
        if transcript:
            summary = self.summarize_video(url)
        else:
            summary = self.ai.summarize(f"{material.title}\n{material.source_url}")
        
        material.video_metadata = metadata
        material.summary = summary
        material.title = self.get_title(url)
        
        return material

    def _extract_video_id(self, url: str) -> Optional[str]:
        from urllib.parse import urlparse, parse_qs
        
        parsed = urlparse(url)
        
        if "youtu.be" in parsed.netloc:
            return parsed.path.lstrip('/')
        
        if "youtube.com" in parsed.netloc:
            query = parse_qs(parsed.query)
            return query.get("v", [None])[0]
        
        return None

    def _parse_time(self, time_str: str) -> Optional[int]:
        parts = time_str.split(':')
        
        try:
            if len(parts) == 3:
                h, m, s = parts
                return int(h) * 3600 + int(m) * 60 + int(s)
            elif len(parts) == 2:
                m, s = parts
                return int(m) * 60 + int(s)
            elif len(parts) == 1:
                return int(parts[0])
        except:
            return None
        
        return None


video_analyzer = VideoAnalyzer()
