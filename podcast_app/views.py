import json
import os
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from podcast_app.tts_utils import generate_podcast
import tempfile
import asyncio

@csrf_exempt
def create_podcast(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        script = json.loads(request.POST.get("script", "[]"))
        if not isinstance(script, list) or not all("speaker" in seg and "text" in seg for seg in script):
            return JsonResponse({"error": "Invalid script format"}, status=400)

        bg_music_file = request.FILES.get("background_music")
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_out:
            output_path = temp_out.name

        bg_music_path = None
        if bg_music_file:
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_music:
                for chunk in bg_music_file.chunks():
                    temp_music.write(chunk)
                bg_music_path = temp_music.name

        # Run async function in sync context
        asyncio.run(generate_podcast(script, output_path, bg_music_path))

        response = FileResponse(open(output_path, 'rb'), content_type='audio/mpeg')
        response['Content-Disposition'] = 'attachment; filename="podcast.mp3"'
        return response

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
