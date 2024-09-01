import sys
import time
import threading
import itertools
import random

class LoadingAnimation:
    def __init__(self, description="Loading", animation_type="dots"):
        self.description = description
        self.is_animating = False
        self.animation_thread = None
        self.animation_type = animation_type
        
        self.animations = {
            "dots": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
            "line": ["—", "\\", "|", "/"],
            "moon": ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"],
            "bouncing_ball": ["⠁", "⠂", "⠄", "⠂"],
            "arrow": ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"],
        }
        self.animation_type = random.choice(list(self.animations.keys()))

    def animate(self):
        for frame in itertools.cycle(self.animations.get(self.animation_type, self.animation_type)):
            if not self.is_animating:
                break
            sys.stdout.write(f'\r{self.description} {frame}')
            sys.stdout.flush()
            time.sleep(0.1)

    def start(self):
        self.is_animating = True
        self.animation_thread = threading.Thread(target=self.animate)
        self.animation_thread.start()

    def stop(self):
        self.is_animating = False
        if self.animation_thread:
            self.animation_thread.join()
        sys.stdout.write('\r' + ' ' * (len(self.description) + 2) + '\r')
        sys.stdout.flush()

# Example usage
def main():
    print("Available animations: dots, line, moon, bouncing_ball, arrow")
    animation_type = input("Choose an animation type: ").strip().lower()
    
    loading = LoadingAnimation("Generating response", animation_type)
    loading.start()
    
    # Simulate some work (replace this with your actual API call or processing)
    time.sleep(5)
    
    loading.stop()
    print("Response generated!")

if __name__ == "__main__":
    main()