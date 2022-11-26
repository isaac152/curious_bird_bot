import random
from typing import List, Optional

import requests

from constants import MEDIA_URL


class Bird:
    def __init__(
        self,
        code: str,
        scientific_name: str,
        common_name: str,
        description: str,
        image: str,
        audio: str,
        url: str,
    ) -> None:
        self.code_name = code
        self.scientific_name = scientific_name
        self.common_name = common_name
        self.description = description
        self.image = image
        self.audio_id = audio
        self.url = url

    def get_audio(self) -> bytes:
        return self._get_media(f"{MEDIA_URL}/{self.audio_id}")

    def get_image(self) -> bytes:
        return self._get_media(self.image)

    def _get_media(self, url) -> bytes:
        response = requests.get(url)
        return response.content

    def __str__(self):
        return self.code


class BirdContainer:
    def __init__(self, bird_json: dict):
        self._options_size = 4
        self._bird_list = [Bird(**bird_dict) for bird_dict in bird_json]

    def get_random_bird(self, birds: Optional[List[Bird]] = None) -> Bird:
        birds = self._bird_list if not birds else birds
        return random.choice(birds)

    def get_random_bird_list(self) -> List[Bird]:
        return random.sample(self._bird_list, self._options_size)

    def get_random_bird_audios(self) -> List[Bird]:
        birds = []
        while len(birds) < self._options_size:
            selected_birds = random.sample(self._bird_list, self._options_size)
            birds += [bird for bird in selected_birds if bird.audio_id]
        return birds
