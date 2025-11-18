import subprocess
import os
import tempfile
from pathlib import Path
import logging
from typing import Dict, Any, Callable
from ..config import settings
from ..core.presets import ANIMATION_PRESETS, LIGHTING_PRESETS

logger = logging.getLogger(__name__)

class BlenderRenderer:
    """Service for rendering 3D logo animations with Blender"""

    def __init__(self):
        self.blender_path = settings.BLENDER_PATH
        self.temp_dir = settings.TEMP_DIR
        Path(self.temp_dir).mkdir(parents=True, exist_ok=True)

    def generate_blender_script(
        self,
        logo_path: str,
        output_path: str,
        config: Dict[str, Any],
        is_preview: bool = False
    ) -> str:
        """Generate a Blender Python script for rendering"""

        preset_name = config.get("preset", "classic_spin")
        preset = ANIMATION_PRESETS.get(preset_name)
        if not preset:
            raise ValueError(f"Unknown preset: {preset_name}")

        lighting_name = config.get("lighting", "soft")
        lighting = LIGHTING_PRESETS.get(lighting_name, LIGHTING_PRESETS["soft"])

        duration = config.get("duration", 5.0)
        fps = config.get("fps", 30)
        extrusion = config.get("extrusion", 0.5)
        speed = config.get("speed", 1.0)

        # Resolution settings
        if is_preview:
            width = settings.PREVIEW_WIDTH
            height = settings.PREVIEW_HEIGHT
            samples = settings.PREVIEW_SAMPLES
        else:
            resolution = config.get("resolution", "1080p")
            if resolution == "4K":
                width = settings.RENDER_WIDTH_4K
                height = settings.RENDER_HEIGHT_4K
            else:
                width = settings.RENDER_WIDTH_1080P
                height = settings.RENDER_HEIGHT_1080P

            quality = config.get("quality", "standard")
            samples = (settings.RENDER_SAMPLES_HIGH if quality == "high"
                      else settings.RENDER_SAMPLES_STANDARD)

        # Background settings
        bg_config = config.get("background", {})
        bg_type = bg_config.get("type", "solid")
        bg_color = bg_config.get("color", "#ffffff")

        # Convert hex color to RGB
        bg_rgb = self._hex_to_rgb(bg_color)

        # Calculate total frames
        total_frames = int(duration * fps / speed)

        script = f'''
import bpy
import math
import os

# Clear existing scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Set render settings
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'GPU'
scene.cycles.samples = {samples}
scene.render.resolution_x = {width}
scene.render.resolution_y = {height}
scene.render.fps = {fps}
scene.frame_start = 1
scene.frame_end = {total_frames}
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'HIGH'
scene.render.ffmpeg.ffmpeg_preset = 'GOOD'
scene.render.filepath = "{output_path}"

# Enable transparency if needed
scene.render.film_transparent = {"true" if bg_type == "transparent" else "false"}

# Create camera
bpy.ops.object.camera_add(location=(0, -8, 2))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(75), 0, 0)
scene.camera = camera

# Import logo image as plane
bpy.ops.import_image.to_plane(
    files=[{{"name": "{os.path.basename(logo_path)}"}}],
    directory="{os.path.dirname(logo_path)}",
    shader='EMISSION'
)

logo_plane = bpy.context.active_object
logo_plane.name = "Logo"

# Add Solidify modifier for extrusion
solidify = logo_plane.modifiers.new(name="Solidify", type='SOLIDIFY')
solidify.thickness = {extrusion}
solidify.offset = 0

# Add material with emission
if logo_plane.data.materials:
    mat = logo_plane.data.materials[0]
else:
    mat = bpy.data.materials.new(name="LogoMaterial")
    logo_plane.data.materials.append(mat)

mat.use_nodes = True
nodes = mat.node_tree.nodes
nodes.clear()

# Create emission shader
output_node = nodes.new(type='ShaderNodeOutputMaterial')
emission_node = nodes.new(type='ShaderNodeEmission')
image_node = nodes.new(type='ShaderNodeTexImage')

# Load logo image
image = bpy.data.images.load("{logo_path}")
image_node.image = image

# Connect nodes
links = mat.node_tree.links
links.new(image_node.outputs['Color'], emission_node.inputs['Color'])
links.new(emission_node.outputs['Emission'], output_node.inputs['Surface'])

emission_node.inputs['Strength'].default_value = 1.0

# Add lighting
light_data_key = bpy.data.lights.new(name="KeyLight", type='AREA')
light_data_key.energy = {lighting["key_light"]["energy"]}
light_data_key.color = {lighting["key_light"]["color"]}
light_key = bpy.data.objects.new(name="KeyLight", object_data=light_data_key)
light_key.location = {lighting["key_light"]["location"]}
bpy.context.collection.objects.link(light_key)

light_data_fill = bpy.data.lights.new(name="FillLight", type='AREA')
light_data_fill.energy = {lighting["fill_light"]["energy"]}
light_data_fill.color = {lighting["fill_light"]["color"]}
light_fill = bpy.data.objects.new(name="FillLight", object_data=light_data_fill)
light_fill.location = {lighting["fill_light"]["location"]}
bpy.context.collection.objects.link(light_fill)

light_data_rim = bpy.data.lights.new(name="RimLight", type='AREA')
light_data_rim.energy = {lighting["rim_light"]["energy"]}
light_data_rim.color = {lighting["rim_light"]["color"]}
light_rim = bpy.data.objects.new(name="RimLight", object_data=light_data_rim)
light_rim.location = {lighting["rim_light"]["location"]}
bpy.context.collection.objects.link(light_rim)

# Set background
if not scene.render.film_transparent:
    world = bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs[0].default_value = ({bg_rgb[0]}, {bg_rgb[1]}, {bg_rgb[2]}, 1.0)

# Animation keyframes
'''

        # Add keyframe animation
        for kf_index, keyframe in enumerate(preset.keyframes):
            frame_num = int(keyframe["frame"] * total_frames) + 1 if keyframe["frame"] > 0 else 1

            script += f"\nscene.frame_set({frame_num})\n"

            # Object transformations
            if "object_location" in keyframe:
                loc = keyframe["object_location"]
                script += f"logo_plane.location = {loc}\nlogo_plane.keyframe_insert(data_path='location')\n"

            if "object_rotation" in keyframe:
                rot = keyframe["object_rotation"]
                script += f"logo_plane.rotation_euler = {rot}\nlogo_plane.keyframe_insert(data_path='rotation_euler')\n"

            if "object_scale" in keyframe:
                scale = keyframe["object_scale"]
                script += f"logo_plane.scale = {scale}\nlogo_plane.keyframe_insert(data_path='scale')\n"

            # Camera transformations
            if "camera_location" in keyframe:
                cam_loc = keyframe["camera_location"]
                script += f"camera.location = {cam_loc}\ncamera.keyframe_insert(data_path='location')\n"

            if "camera_rotation" in keyframe:
                cam_rot = keyframe["camera_rotation"]
                script += f"camera.rotation_euler = {cam_rot}\ncamera.keyframe_insert(data_path='rotation_euler')\n"

        script += '''
# Render animation
bpy.ops.render.render(animation=True)
'''

        return script

    def render(
        self,
        logo_path: str,
        output_path: str,
        config: Dict[str, Any],
        is_preview: bool = False,
        progress_callback: Callable[[int], None] = None
    ) -> bool:
        """Execute Blender rendering"""
        try:
            # Generate Blender script
            script = self.generate_blender_script(logo_path, output_path, config, is_preview)

            # Save script to temporary file
            script_path = os.path.join(self.temp_dir, f"render_script_{os.getpid()}.py")
            with open(script_path, 'w') as f:
                f.write(script)

            # Execute Blender in background mode
            cmd = [
                self.blender_path,
                "--background",
                "--python", script_path
            ]

            logger.info(f"Executing Blender render: {' '.join(cmd)}")

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            # Monitor progress
            for line in process.stdout:
                logger.debug(line.strip())
                # Parse Blender progress output
                if "Fra:" in line and progress_callback:
                    try:
                        # Extract frame number from Blender output
                        parts = line.split("Fra:")
                        if len(parts) > 1:
                            frame_str = parts[1].split()[0]
                            current_frame = int(frame_str)
                            total_frames = int(config.get("duration", 5.0) * config.get("fps", 30))
                            progress = int((current_frame / total_frames) * 100)
                            progress_callback(min(progress, 100))
                    except Exception as e:
                        logger.debug(f"Progress parsing error: {e}")

            process.wait()

            # Clean up script file
            try:
                os.remove(script_path)
            except Exception as e:
                logger.warning(f"Could not remove script file: {e}")

            if process.returncode == 0:
                logger.info(f"Render completed successfully: {output_path}")
                return True
            else:
                stderr = process.stderr.read()
                logger.error(f"Render failed with code {process.returncode}: {stderr}")
                return False

        except Exception as e:
            logger.error(f"Render error: {e}")
            return False

    @staticmethod
    def _hex_to_rgb(hex_color: str) -> tuple:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

blender_renderer = BlenderRenderer()
