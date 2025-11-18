from typing import Dict, List
import math

class AnimationPreset:
    def __init__(self, name: str, description: str, keyframes: List[Dict]):
        self.name = name
        self.description = description
        self.keyframes = keyframes

# Define all animation presets
ANIMATION_PRESETS = {
    "classic_spin": AnimationPreset(
        name="Classic Spin",
        description="360° rotation around Y axis with slight tilt",
        keyframes=[
            {
                "frame": 0,
                "object_rotation": (math.radians(15), 0, 0),
                "camera_location": (0, -8, 2),
                "camera_rotation": (math.radians(75), 0, 0)
            },
            {
                "frame": 1.0,  # End (normalized)
                "object_rotation": (math.radians(15), math.radians(360), 0),
                "camera_location": (0, -8, 2),
                "camera_rotation": (math.radians(75), 0, 0)
            }
        ]
    ),

    "orbital_reveal": AnimationPreset(
        name="Orbital Reveal",
        description="Camera orbits around the logo",
        keyframes=[
            {
                "frame": 0,
                "object_rotation": (math.radians(10), math.radians(-45), 0),
                "camera_location": (-6, -6, 3),
                "camera_rotation": (math.radians(70), 0, math.radians(45))
            },
            {
                "frame": 1.0,
                "object_rotation": (math.radians(10), math.radians(45), 0),
                "camera_location": (6, -6, 3),
                "camera_rotation": (math.radians(70), 0, math.radians(-45))
            }
        ]
    ),

    "zoom_rotate": AnimationPreset(
        name="Zoom & Rotate",
        description="Zoom in while rotating elegantly",
        keyframes=[
            {
                "frame": 0,
                "object_rotation": (0, 0, 0),
                "object_scale": (0.5, 0.5, 0.5),
                "camera_location": (0, -12, 2),
                "camera_rotation": (math.radians(80), 0, 0)
            },
            {
                "frame": 1.0,
                "object_rotation": (math.radians(20), math.radians(180), 0),
                "object_scale": (1.0, 1.0, 1.0),
                "camera_location": (0, -7, 2),
                "camera_rotation": (math.radians(75), 0, 0)
            }
        ]
    ),

    "flip_card": AnimationPreset(
        name="Flip Card",
        description="180° flip like a card turning",
        keyframes=[
            {
                "frame": 0,
                "object_rotation": (0, 0, 0),
                "camera_location": (0, -8, 1.5),
                "camera_rotation": (math.radians(80), 0, 0)
            },
            {
                "frame": 0.5,
                "object_rotation": (0, math.radians(90), 0),
                "camera_location": (0, -8, 1.5),
                "camera_rotation": (math.radians(80), 0, 0)
            },
            {
                "frame": 1.0,
                "object_rotation": (0, math.radians(180), 0),
                "camera_location": (0, -8, 1.5),
                "camera_rotation": (math.radians(80), 0, 0)
            }
        ]
    ),

    "rising_star": AnimationPreset(
        name="Rising Star",
        description="Logo rises from below with rotation",
        keyframes=[
            {
                "frame": 0,
                "object_location": (0, 0, -3),
                "object_rotation": (0, 0, math.radians(-45)),
                "object_scale": (0.7, 0.7, 0.7),
                "camera_location": (0, -8, 2),
                "camera_rotation": (math.radians(75), 0, 0)
            },
            {
                "frame": 1.0,
                "object_location": (0, 0, 0),
                "object_rotation": (0, 0, math.radians(15)),
                "object_scale": (1.0, 1.0, 1.0),
                "camera_location": (0, -8, 2),
                "camera_rotation": (math.radians(75), 0, 0)
            }
        ]
    ),

    "cinematic_pan": AnimationPreset(
        name="Cinematic Pan",
        description="Smooth camera pan with object rotation",
        keyframes=[
            {
                "frame": 0,
                "object_rotation": (math.radians(10), math.radians(-30), 0),
                "camera_location": (-4, -7, 2),
                "camera_rotation": (math.radians(75), 0, math.radians(25))
            },
            {
                "frame": 1.0,
                "object_rotation": (math.radians(10), math.radians(30), 0),
                "camera_location": (4, -7, 2),
                "camera_rotation": (math.radians(75), 0, math.radians(-25))
            }
        ]
    ),

    "bounce_in": AnimationPreset(
        name="Bounce In",
        description="Logo bounces into scene with physics",
        keyframes=[
            {
                "frame": 0,
                "object_location": (0, 0, 5),
                "object_scale": (0.8, 0.8, 0.8),
                "camera_location": (0, -8, 2),
                "camera_rotation": (math.radians(75), 0, 0)
            },
            {
                "frame": 0.6,
                "object_location": (0, 0, -0.3),
                "object_scale": (1.1, 1.1, 0.9),
            },
            {
                "frame": 0.8,
                "object_location": (0, 0, 0.2),
                "object_scale": (0.95, 0.95, 1.05),
            },
            {
                "frame": 1.0,
                "object_location": (0, 0, 0),
                "object_scale": (1.0, 1.0, 1.0),
                "camera_location": (0, -8, 2),
                "camera_rotation": (math.radians(75), 0, 0)
            }
        ]
    ),

    "elegant_reveal": AnimationPreset(
        name="Elegant Reveal",
        description="Gentle fade in with subtle movement",
        keyframes=[
            {
                "frame": 0,
                "object_location": (0, 0.5, 0),
                "object_rotation": (math.radians(5), math.radians(-10), 0),
                "object_scale": (0.95, 0.95, 0.95),
                "camera_location": (0, -8, 2),
                "camera_rotation": (math.radians(75), 0, 0)
            },
            {
                "frame": 1.0,
                "object_location": (0, 0, 0),
                "object_rotation": (math.radians(5), math.radians(10), 0),
                "object_scale": (1.0, 1.0, 1.0),
                "camera_location": (0, -8, 2),
                "camera_rotation": (math.radians(75), 0, 0)
            }
        ]
    )
}

LIGHTING_PRESETS = {
    "dramatic": {
        "key_light": {"location": (-5, -5, 8), "energy": 1000, "color": (1.0, 0.95, 0.9)},
        "fill_light": {"location": (5, -3, 4), "energy": 300, "color": (0.9, 0.95, 1.0)},
        "rim_light": {"location": (0, 4, 6), "energy": 800, "color": (1.0, 1.0, 1.0)},
    },
    "soft": {
        "key_light": {"location": (-3, -5, 6), "energy": 500, "color": (1.0, 1.0, 1.0)},
        "fill_light": {"location": (3, -5, 6), "energy": 400, "color": (1.0, 1.0, 1.0)},
        "rim_light": {"location": (0, 3, 5), "energy": 300, "color": (1.0, 1.0, 1.0)},
    },
    "corporate": {
        "key_light": {"location": (-4, -6, 7), "energy": 700, "color": (1.0, 1.0, 1.0)},
        "fill_light": {"location": (4, -4, 5), "energy": 400, "color": (0.95, 0.98, 1.0)},
        "rim_light": {"location": (0, 5, 6), "energy": 500, "color": (1.0, 1.0, 1.0)},
    },
    "neon": {
        "key_light": {"location": (-5, -5, 8), "energy": 600, "color": (0.3, 0.7, 1.0)},
        "fill_light": {"location": (5, -3, 4), "energy": 400, "color": (1.0, 0.2, 0.8)},
        "rim_light": {"location": (0, 4, 6), "energy": 700, "color": (0.5, 1.0, 0.5)},
    },
    "golden_hour": {
        "key_light": {"location": (-6, -4, 7), "energy": 800, "color": (1.0, 0.8, 0.5)},
        "fill_light": {"location": (4, -5, 5), "energy": 300, "color": (0.9, 0.7, 0.6)},
        "rim_light": {"location": (0, 4, 6), "energy": 600, "color": (1.0, 0.9, 0.7)},
    }
}
