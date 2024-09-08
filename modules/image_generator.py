# modules/image_generator.py
from openai import OpenAI

class ImageGenerator:
    def __init__(self):
        self.client = OpenAI()

    def create_image(self, prompt: str, size: str = "1024x1024", quality: str = "standard") -> str:
        """
        Generates an image using DALL-E 3 based on the provided prompt.

        Args:
            prompt (str): The text prompt to generate the image.
            size (str): The size of the generated image. Default is "1024x1024".
            quality (str): The quality of the generated image. Default is "standard".

        Returns:
            str: The URL of the generated image.
        """
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            n=1,  # DALL-E 3 requires n=1
        )
        return response.data[0].url

    def generate_social_media_images(self, topic: str, summary: str = "", num_images: int = 3) -> list:
        """
        Combines the prompt generation and image creation to produce multiple image URLs.

        Args:
            topic (str): The main topic for the image.
            summary (str): A brief summary for additional context (optional).
            num_images (int): The number of images to generate. Default is 3.

        Returns:
            list: A list of URLs of the generated images.
        """
        # Step 1: Generate the prompt for DALL-E 3
        prompt = f"Generate an image for {topic}. {summary}"

        # Step 2: Generate the images sequentially
        image_urls = []
        for _ in range(num_images):
            image_url = self.create_image(prompt)
            image_urls.append(image_url)

        return image_urls
