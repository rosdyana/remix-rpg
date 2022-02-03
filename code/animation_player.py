from random import choices
import pygame
from particles import ParticleEffect
from utils import import_folder


class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # magic
            'flame': import_folder('../graphics/particles/flame/frames'),
            'aura': import_folder('../graphics/particles/aura'),
            'heal': import_folder('../graphics/particles/heal/frames'),

            # attacks
            'claw': import_folder('../graphics/particles/claw'),
            'slash': import_folder('../graphics/particles/slash'),
            'sparkle': import_folder('../graphics/particles/sparkle'),
            'leaf_attack': import_folder('../graphics/particles/leaf_attack'),
            'thunder': import_folder('../graphics/particles/thunder'),

            # monster deaths
            'squid': import_folder('../graphics/particles/smoke_orange'),
            'raccoon': import_folder('../graphics/particles/raccoon'),
            'spirit': import_folder('../graphics/particles/nova'),
            'bamboo': import_folder('../graphics/particles/bamboo'),

            # leafs
            'leaf': (
                import_folder('../graphics/particles/leaf1'),
                import_folder('../graphics/particles/leaf2'),
                import_folder('../graphics/particles/leaf3'),
                import_folder('../graphics/particles/leaf4'),
                import_folder('../graphics/particles/leaf5'),
                import_folder('../graphics/particles/leaf6'),
                self.reflect_images(import_folder(
                    '../graphics/particles/leaf1')),
                self.reflect_images(import_folder(
                    '../graphics/particles/leaf2')),
                self.reflect_images(import_folder(
                    '../graphics/particles/leaf3')),
                self.reflect_images(import_folder(
                    '../graphics/particles/leaf4')),
                self.reflect_images(import_folder(
                    '../graphics/particles/leaf5')),
                self.reflect_images(import_folder(
                    '../graphics/particles/leaf6'))
            )
        }

    def reflect_images(self, frames):
        new_frames = []

        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_grass_particles(self, pos, groups):
        animation_frames = choices(self.frames['leaf'])
        ParticleEffect(pos, animation_frames, groups)

    def create_particles(self, animation_type, pos, groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)
