"""
Particle Cosmos - Optimized & Smooth
- High-performance particle physics with sacred geometry
- Optimized rendering and physics
- All features preserved, enhanced, and accelerated
"""

import pygame
import random
import math

pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PARTICLE COSMOS - OPTIMIZED EDITION")
clock = pygame.time.Clock()

# Color palettes
BACKGROUND = (8, 6, 15)
GRID_COLOR = (25, 20, 40)
TEXT_COLOR = (100, 255, 200)
ACCENT_COLOR = (255, 50, 150)
GRAVITY_COLOR = (0, 200, 255)
REPULSION_COLOR = (255, 100, 0)
MAGNETIC_COLOR = (200, 0, 255)
TURBULENCE_COLOR = (0, 255, 150)

# Fonts
font_medium = pygame.font.Font(None, 32)
font_small = pygame.font.Font(None, 24)

# Physics settings
global_force_strength = 1.0
particle_size_multiplier = 1.0
turbulence_active = False
turbulence_strength = 0.3  # Reduced
turbulence_scale = 0.005    # Slower noise

# Max limits to prevent lag
MAX_PARTICLES = 400
MAX_GEOMETRY = 8  # Only 8 sacred patterns at once
MAX_FORCE_FIELDS = 60

# Particle types
PARTICLE_TYPES = {
    "NORMAL": {"mass": 1.0, "color": (100, 200, 255), "drag": 0.98},
    "HEAVY": {"mass": 2.0, "color": (255, 150, 50), "drag": 0.99},
    "LIGHT": {"mass": 0.5, "color": (150, 255, 100), "drag": 0.96},
    "ENERGY": {"mass": 0.3, "color": (255, 100, 255), "drag": 0.94}
}

current_particle_type = "NORMAL"

# Force Field (Optimized)
class ForceField:
    def __init__(self, x, y, strength, radius, field_type, duration=120):
        self.x = x
        self.y = y
        self.strength = strength
        self.radius_sq = radius * radius  # Compare squared distances
        self.field_type = field_type
        self.age = 0
        self.max_age = duration
        self.active_radius_sq = (radius + 20) ** 2
    
    def update(self):
        self.age += 1
        return self.age < self.max_age

    def is_near(self, x, y):
        dx = x - self.x
        dy = y - self.y
        return dx*dx + dy*dy < self.active_radius_sq

    def draw(self, surf):
        alpha = max(0, 200 - self.age * 1.2)
        pulse = 1 + 0.15 * math.sin(self.age * 0.2)
        radius = 4 + pulse * 4

        if self.field_type == "gravity":
            color = GRAVITY_COLOR
        elif self.field_type == "repulsion":
            color = REPULSION_COLOR
        else:
            color = MAGNETIC_COLOR

        pygame.draw.circle(surf, color, (int(self.x), int(self.y)), int(radius))
        pygame.draw.circle(surf, (*color, alpha // 3), (int(self.x), int(self.y)), int(8 * pulse), 1)

# Particle (Optimized Physics)
class Particle:
    __slots__ = ('x', 'y', 'vx', 'vy', 'type_data', 'mass', 'size', 'target_size', 'color',
                 'trail', 'max_trail', 'energy', 'max_energy', 'age', 'max_age', 'glow',
                 'merge_cooldown', 'charged', 'charge', 'base_size')

    def __init__(self, x, y, particle_type="NORMAL"):
        self.x = float(x)
        self.y = float(y)
        self.vx = random.uniform(-1.0, 1.0)
        self.vy = random.uniform(-1.0, 1.0)
        self.type_data = PARTICLE_TYPES[particle_type]
        self.mass = self.type_data["mass"]
        self.base_size = random.uniform(2.0, 5.0) * particle_size_multiplier
        self.size = self.base_size
        self.target_size = self.size
        self.color = list(self.type_data["color"])  # Mutable for efficiency
        self.trail = []
        self.max_trail = 6
        self.energy = 100
        self.max_energy = 100
        self.age = 0
        self.max_age = random.randint(400, 1200)  # Shorter life
        self.glow = 0
        self.merge_cooldown = 0
        self.charged = random.random() < 0.3
        self.charge = random.choice([-1, 1])

    def update(self, force_fields, particles, dt):
        self.age += 1
        if self.merge_cooldown > 0:
            self.merge_cooldown -= 1

        # Trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail:
            self.trail.pop(0)

        # Turbulence (light)
        if turbulence_active:
            nx = math.sin(self.x * turbulence_scale + self.age * 0.02) * turbulence_strength
            ny = math.cos(self.y * turbulence_scale + self.age * 0.02) * turbulence_strength
            self.vx += nx
            self.vy += ny

        # Force fields
        for field in force_fields:
            if not field.is_near(self.x, self.y):
                continue
            dx = field.x - self.x
            dy = field.y - self.y
            dist_sq = dx*dx + dy*dy
            if dist_sq < 1: dist_sq = 1
            distance = math.sqrt(dist_sq)

            if distance >= field.radius_sq ** 0.5:
                continue

            if field.field_type == "gravity":
                force = field.strength * self.mass / distance
            elif field.field_type == "repulsion":
                force = -field.strength * self.mass / distance
            else:
                force = field.strength * self.charge / distance

            ax = (dx / distance) * force * 0.8
            ay = (dy / distance) * force * 0.8
            self.vx += ax
            self.vy += ay

        # Drag
        drag = self.type_data["drag"]
        self.vx *= drag
        self.vy *= drag

        # Speed limit
        speed_sq = self.vx*self.vx + self.vy*self.vy
        if speed_sq > 225:  # 15^2
            scale = 15.0 / math.sqrt(speed_sq)
            self.vx *= scale
            self.vy *= scale

        # Move
        self.x += self.vx * 2
        self.y += self.vy * 2

        # Bounds
        if self.x < 0 or self.x > WIDTH:
            self.vx *= -0.6
            self.x = max(0, min(WIDTH, self.x))
        if self.y < 0 or self.y > HEIGHT:
            self.vy *= -0.6
            self.y = max(0, min(HEIGHT, self.y))

        # Size interp
        self.size += (self.target_size - self.size) * 0.1

        # Energy & color
        energy_ratio = self.energy / self.max_energy
        self.color[0] = min(255, int(100 + 155 * energy_ratio))
        self.color[1] = min(255, int(150 + 100 * energy_ratio))
        self.color[2] = min(255, int(100 + 155 * (1 - energy_ratio)))

        # Glow
        self.glow = self.glow + 0.5 if self.energy > 80 else max(0, self.glow - 0.3)

        # Size by energy
        if self.energy < 20:
            self.target_size = max(1, self.base_size * 0.7)
        elif self.energy > 80:
            self.target_size = min(self.base_size * 2, self.size * 1.01)
        else:
            self.target_size = self.base_size

        return self.age > self.max_age or self.energy <= 0

    def draw(self, surf):
        # Trail
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(200 * (i / len(self.trail)))
            size = max(1, int(self.size * 0.5))
            pygame.draw.circle(surf, (*self.color, alpha // 2), (int(tx), int(ty)), size)

        # Glow
        if self.glow > 0:
            radius = int(self.size + self.glow)
            s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, 40), (radius, radius), radius)
            surf.blit(s, (int(self.x) - radius, int(self.y) - radius))

        # Main
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), max(1, int(self.size)))

        # Charge
        if self.charged:
            col = (255, 255, 0) if self.charge > 0 else (0, 255, 255)
            pygame.draw.circle(surf, col, (int(self.x), int(self.y)), max(1, int(self.size * 0.3)))

# Sacred Geometry (Optimized)
class SacredGeometry:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.age = 0
        self.max_age = 7000
        self.shape = random.choice(['flower', 'spiral', 'mandala'])
        self.color_hue = random.random()
        self.pulse = random.uniform(0, math.pi)

    def draw(self, surf):
        self.age += 16.6  # ~60 FPS
        if self.age > self.max_age:
            return False

        t = self.age * 0.001
        progress = self.age / self.max_age

        # Collapse effect
        collapse = 1.0
        cycle = (t * 1.5) % 2.0
        if cycle > 1.2:
            collapse = 1.0 - ((cycle - 1.2) / 0.8)**2
        elif cycle > 0.8:
            collapse = 1.0 - (cycle - 0.8) * 1.25

        radius = int(100 * collapse * (1.0 - progress * 0.2))
        if radius < 5:
            return True

        hue = (self.color_hue + t * 0.1) % 1.0
        r, g, b = hsv_to_rgb(hue, 0.8, 1.0)
        color = (int(r*255), int(g*255), int(b*255))
        alpha = int(150 * (1 - progress))

        if alpha < 10:
            return True

        geom_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        if self.shape == 'flower':
            self.draw_flower(geom_surf, color, alpha, radius)
        elif self.shape == 'spiral':
            self.draw_spiral(geom_surf, color, alpha, radius, t)
        elif self.shape == 'mandala':
            self.draw_mandala(geom_surf, color, alpha, radius, t)

        # Only blit if not transparent
        if alpha > 20:
            screen.blit(geom_surf, (0, 0))

        return True

    def draw_flower(self, surf, color, alpha, r):
        step = r * 0.6
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                x = self.x + i * step
                y = self.y + j * step
                pygame.draw.circle(surf, (*color, alpha // 3), (x, y), r // 2, 1)

    def draw_spiral(self, surf, color, alpha, r, t):
        points = []
        for i in range(60):
            a = i / 20 + t
            d = r * i / 60
            x = self.x + math.cos(a) * d
            y = self.y + math.sin(a) * d
            points.append((x, y))
        if len(points) > 2:
            pygame.draw.lines(surf, (*color, alpha), False, points, 1)

    def draw_mandala(self, surf, color, alpha, r, t):
        for i in range(12):
            a = t + i * math.pi / 6
            x1 = self.x + math.cos(a) * 10
            y1 = self.y + math.sin(a) * 10
            x2 = self.x + math.cos(a) * r
            y2 = self.y + math.sin(a) * r
            pygame.draw.line(surf, (*color, alpha), (x1, y1), (x2, y2), 1)

def hsv_to_rgb(h, s, v):
    i = int(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    i %= 6
    if i == 0: return v, t, p
    if i == 1: return q, v, p
    if i == 2: return p, v, t
    if i == 3: return p, q, v
    if i == 4: return t, p, v
    return v, p, q

# Explosion shards (reusable)
def create_explosion_at(x, y, color, count=15):  # Reduced count
    global particles
    for _ in range(count):
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(2.0, 6.0)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        p = Particle(x, y, "LIGHT")
        p.vx = vx
        p.vy = vy
        p.size = random.uniform(1.0, 2.0)
        p.target_size = p.size
        p.color = [
            min(255, color[0] + random.randint(-30, 30)),
            min(255, color[1] + random.randint(-30, 30)),
            min(255, color[2] + random.randint(-30, 30))
        ]
        p.max_age = random.randint(40, 80)
        p.energy = 50
        p.drag = 0.90
        particles.append(p)

# HUD
def draw_hud(surf, count, strength, turbulence):
    text = font_medium.render(f"PARTICLES: {count}", True, TEXT_COLOR)
    surf.blit(text, (WIDTH - 200, 20))
    
    stats = [
        f"FORCE: {strength:.1f}x",
        f"TURB: {'ON' if turbulence else 'OFF'}",
        f"MODE: {current_particle_type[:4]}",
    ]
    for i, s in enumerate(stats):
        text = font_small.render(s, True, TEXT_COLOR)
        surf.blit(text, (20, 20 + i * 25))

# Background grid (lightweight)
def draw_grid(surf):
    time_offset = pygame.time.get_ticks() * 0.0003
    for x in range(0, WIDTH, 60):
        a = 10 + 10 * math.sin(time_offset + x * 0.01)
        pygame.draw.line(surf, (*GRID_COLOR, int(a)), (x, 0), (x, HEIGHT), 1)

# Main
particles = []
force_fields = []
sacred_geometry = []
particle_count = 0

# Initial particles
for _ in range(120):
    particles.append(Particle(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
particle_count = len(particles)

key_timers = {}
mouse_pressed = {"left": False, "right": False, "middle": False}
mouse_pos = (0, 0)

running = True
last_time = pygame.time.get_ticks()

while running:
    current_time = pygame.time.get_ticks()
    dt = (current_time - last_time) / 1000.0
    last_time = current_time

    # Handle keys
    keys = pygame.key.get_pressed()
    ctrl_held = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]

    # UP/DOWN with repeat
    for key, delta in [(pygame.K_UP, 0.1), (pygame.K_DOWN, -0.1)]:
        if keys[key]:
            if key not in key_timers:
                key_timers[key] = current_time + 200
                adjust_force_strength(delta)
            elif current_time >= key_timers[key]:
                adjust_force_strength(delta)
                key_timers[key] = current_time + 50
        elif key in key_timers:
            del key_timers[key]

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q):
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                particles.clear()
                sacred_geometry.clear()
                force_fields.clear()
            elif event.key == pygame.K_r:
                global_force_strength = 1.0
                particle_size_multiplier = 1.0
                turbulence_active = False
            elif event.key == pygame.K_SPACE:
                spawn_particle_burst(mouse_pos[0], mouse_pos[1], 15)
            elif event.key == pygame.K_TAB:
                turbulence_active = not turbulence_active
            elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                current_particle_type = ["NORMAL", "HEAVY", "LIGHT", "ENERGY"][event.key - pygame.K_1]
            elif event.key == pygame.K_LEFTBRACKET:
                particle_size_multiplier = max(0.2, particle_size_multiplier - 0.1)
            elif event.key == pygame.K_RIGHTBRACKET:
                particle_size_multiplier = min(3.0, particle_size_multiplier + 0.1)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            mouse_pos = (mx, my)

            if event.button == 1 and ctrl_held:
                # Explode nearest particle
                closest = None
                best_dist = 60
                for p in particles:
                    d = (p.x - mx)**2 + (p.y - my)**2
                    if d < best_dist * best_dist and d < (p.size + 10)**2:
                        closest = p
                        best_dist = d ** 0.5
                if closest:
                    create_explosion_at(closest.x, closest.y, closest.color)
                    particles.remove(closest)

            elif event.button == 1:
                mouse_pressed["left"] = True
                if len(force_fields) < MAX_FORCE_FIELDS:
                    force_fields.append(ForceField(mx, my, 2.0 * global_force_strength, 120, "gravity"))
            elif event.button == 3:
                mouse_pressed["right"] = True
                if len(force_fields) < MAX_FORCE_FIELDS:
                    force_fields.append(ForceField(mx, my, 3.0 * global_force_strength, 100, "repulsion"))
            elif event.button == 2:
                mouse_pressed["middle"] = True
                if len(force_fields) < MAX_FORCE_FIELDS:
                    force_fields.append(ForceField(mx, my, 4.0 * global_force_strength, 90, "magnetic"))
                if len(sacred_geometry) < MAX_GEOMETRY:
                    sacred_geometry.append(SacredGeometry(mx, my))

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed[event.button == 1 and "left" or event.button == 3 and "right" or "middle"] = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos

    # Continuous fields
    if mouse_pressed["left"] and len(force_fields) < MAX_FORCE_FIELDS:
        force_fields.append(ForceField(mouse_pos[0], mouse_pos[1], 1.2 * global_force_strength, 80, "gravity", 10))
    if mouse_pressed["right"] and len(force_fields) < MAX_FORCE_FIELDS:
        force_fields.append(ForceField(mouse_pos[0], mouse_pos[1], 1.8 * global_force_strength, 70, "repulsion", 10))
    if mouse_pressed["middle"] and len(force_fields) < MAX_FORCE_FIELDS:
        force_fields.append(ForceField(mouse_pos[0], mouse_pos[1], 2.2 * global_force_strength, 80, "magnetic", 10))

    # Spawn particles (limited)
    if len(particles) < MAX_PARTICLES and random.random() < 0.2:
        particles.append(Particle(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50), current_particle_type))

    # Update
    screen.fill(BACKGROUND)

    # Sacred geometry
    sacred_geometry = [g for g in sacred_geometry if g.draw(screen)]

    # Grid
    draw_grid(screen)

    # Force fields
    force_fields = [f for f in force_fields if f.update()]
    for f in force_fields:
        f.draw(screen)

    # Particles
    particles = [p for p in particles if not p.update(force_fields, particles, dt)]
    for p in particles:
        p.draw(screen)

    particle_count = len(particles)

    # HUD
    draw_hud(screen, particle_count, global_force_strength, turbulence_active)

    pygame.display.flip()
    clock.tick(60)  # Cap at 60 FPS

pygame.quit()