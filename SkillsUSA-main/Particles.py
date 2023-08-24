import arcade as arc
from PIL import Image

particle_color_num = 0


class WallParticle(arc.FadeParticle):
    def __init__(self, wall_color):
        global particle_color_num
        texture = arc.Texture(f"Wall_Particle{particle_color_num}", Image.new("RGBA", (32, 32), wall_color), hit_box_algorithm=None)
        particle_color_num += 1
        super().__init__(filename_or_texture=texture, change_xy=arc.rand_in_circle((0, 0), 1),
                         lifetime=.5)


class DrillEmitter(arc.Emitter):
    def __init__(self, center_xy, wall_color=(50, 50, 50)):
        super().__init__(center_xy=center_xy, emit_controller=arc.EmitBurst(1),
                         particle_factory=lambda emitter: WallParticle(wall_color))


def drill_wall_emit(center_xy, wall_color=(50, 50, 50)):
    e = DrillEmitter(center_xy, wall_color)
    return drill_wall_emit.__doc__, e
