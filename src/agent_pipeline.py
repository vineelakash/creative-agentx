import os
import time
from typing import Dict, List, Any
from .utils import clean_text, safe_format

class CreativeAgent:
    def __init__(self, offline_mode: bool = False):
        self.offline_mode = offline_mode
        # Placeholder for LLM client initialization
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            self.offline_mode = True
            print("No API key found. Switching to OFFLINE mode.")

    def _mock_generate(self, prompt: str, task_type: str) -> str:
        """
        Simulates LLM generation for offline mode.
        """
        time.sleep(0.5) # Simulate latency
        if task_type == "outline":
            return """
            I. Introduction
               - Hook the reader
               - Introduce the topic
            II. Main Point 1
               - Detail and examples
            III. Main Point 2
               - Analysis and insights
            IV. Conclusion
               - Summary and call to action
            """
        elif task_type == "blog":
            return f"""
            Here is a blog post about the topic based on the outline.
            
            Introduction:
            Welcome to our deep dive into this fascinating subject.
            
            Body:
            We explore the nuances and the impact it has on our daily lives. 
            The data suggests a strong correlation between X and Y.
            
            Conclusion:
            In summary, this is a critical area for further study.
            (Generated in offline mode for prompt: {prompt[:30]}...)
            """
        elif task_type == "script":
            return """
            [SCENE START]
            INT. STUDIO - DAY
            
            HOST
            (Excitedly)
            Have you ever wondered about this topic?
            
            [CUT TO GRAPHICS]
            
            VOICEOVER
            It's changing the world as we know it.
            
            [SCENE END]
            """
        elif task_type == "prompts":
            return """
            1. A futuristic city skyline at sunset, cyberpunk style.
            2. A close-up of a robot hand holding a flower, high detail.
            3. Abstract representation of neural networks, blue and neon lights.
            """
        return "Generic fallback content."

    def generate_outline(self, topic: str) -> str:
        prompt = f"Create a 4-section outline for a blog post about: {topic}"
        if self.offline_mode:
            return self._mock_generate(prompt, "outline")
        # Real LLM call would go here
        return self._mock_generate(prompt, "outline")

    def generate_blog(self, topic: str, outline: str, audience: str, tone: str) -> str:
        prompt = f"Write a 600-750 word blog post about {topic} for {audience} in a {tone} tone, based on this outline:\n{outline}"
        if self.offline_mode:
            return self._mock_generate(prompt, "blog")
        return self._mock_generate(prompt, "blog")

    def generate_video_script(self, topic: str) -> str:
        prompt = f"Write a 30-60s short video script about {topic}."
        if self.offline_mode:
            return self._mock_generate(prompt, "script")
        return self._mock_generate(prompt, "script")

    def generate_image_prompts(self, topic: str) -> List[str]:
        prompt = f"Generate 3 image prompts for a blog about {topic}."
        if self.offline_mode:
            content = self._mock_generate(prompt, "prompts")
        else:
            content = self._mock_generate(prompt, "prompts")
        
        # Parse the list
        prompts = [p.strip() for p in content.split('\n') if p.strip() and p[0].isdigit()]
        return prompts if prompts else ["Prompt 1", "Prompt 2", "Prompt 3"]

    def run(self, topic: str, audience: str, tone: str) -> Dict[str, Any]:
        print(f"--- Starting Creative Agent Pipeline for topic: {topic} ---")
        
        print("Generating Outline...")
        outline = self.generate_outline(topic)
        
        print("Expanding into Blog Post...")
        blog_post = self.generate_blog(topic, outline, audience, tone)
        
        print("Generating Video Script...")
        video_script = self.generate_video_script(topic)
        
        print("Generating Image Prompts...")
        image_prompts = self.generate_image_prompts(topic)
        
        return {
            "topic": topic,
            "audience": audience,
            "tone": tone,
            "outline": clean_text(outline),
            "blog_post": clean_text(blog_post),
            "video_script": clean_text(video_script),
            "image_prompts": image_prompts
        }

if __name__ == "__main__":
    agent = CreativeAgent(offline_mode=True)
    result = agent.run("Artificial Intelligence in 2025", "Tech Enthusiasts", "Optimistic")
    print(result)
