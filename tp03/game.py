"""
TP4 - Hough Transform: Line and Circle Detection Game
A simple driving game where students must:
1. Detect road lines using Hough Line Transform to keep the car centered
2. Detect footballs using Hough Circle Transform to shoot them
"""

import pygame
import numpy as np
import cv2
import random
import math
from dataclasses import dataclass
from typing import List, Tuple

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
GREEN = (50, 200, 50)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (100, 150, 255)

# Game settings
ROAD_WIDTH = 250  # Road width at bottom of screen (reduced from 400)
ROAD_WIDTH_TOP = 60  # Road width at horizon (for perspective, reduced from 100)
HORIZON_Y = 150  # Y position of horizon line
CAR_SPEED = 5
BALL_SPEED = 3
BALL_SPAWN_RATE = 120  # frames between ball spawns
DART_SPEED = 10


@dataclass
class RoadLine:
    """Represents a road line marking"""
    offset: float  # horizontal offset from center
    segments: List[Tuple[float, float]]  # list of (y_start, y_end) segments


@dataclass
class Ball:
    """Represents a football on the road"""
    x: float
    y: float
    radius: float
    active: bool = True
    initial_x_offset: float = 0.0  # Offset from road center at spawn
    flattened: bool = False  # Whether the ball has been shot/run over


@dataclass
class Dart:
    """Represents a dart projectile"""
    x: float
    y: float
    active: bool = True


class RoadGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("TP4 - Hough Transform: Road & Ball Detection")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.running = True
        self.car_x = SCREEN_WIDTH // 2  # Car horizontal position
        self.road_curve = 0  # Current road curvature
        self.road_offset = 0  # Current road center offset
        self.score = 100  # Start with 100 points
        self.balls_missed = 0
        self.out_of_bounds_timer = 0  # Track frames spent out of bounds
        
        # Road animation
        self.road_y_offset = 0
        
        # Game objects
        self.balls: List[Ball] = []
        self.darts: List[Dart] = []
        self.frame_count = 0
        
        # Trees (decorative elements on roadside)
        self.trees_left = []
        self.trees_right = []
        
        # Student implementation flags
        self.auto_steer = False  # Will be enabled when students implement line detection
        self.auto_shoot = False  # Will be enabled when students implement circle detection
        
        # Road lines (left and right)
        self.left_line_offset = -ROAD_WIDTH // 2
        self.right_line_offset = ROAD_WIDTH // 2
        self.center_line_offset = 0
        
        # Load/create sprites
        self.load_sprites()
        
    def load_sprites(self):
        """Load or create game sprites"""
        # Create a simple car sprite (viewed from behind/above in first person)
        self.car_surface = pygame.Surface((80, 40), pygame.SRCALPHA)
        # Car body (wider, shorter for first-person view)
        pygame.draw.rect(self.car_surface, BLUE, (0, 0, 80, 40), border_radius=8)
        # Rear window
        pygame.draw.rect(self.car_surface, (150, 200, 255), (10, 5, 60, 15))
        # Outline
        pygame.draw.rect(self.car_surface, BLACK, (0, 0, 80, 40), width=3, border_radius=8)
        # Spoiler/bumper
        pygame.draw.rect(self.car_surface, (70, 100, 200), (5, 35, 70, 5))
        
    def generate_trees(self):
        """Generate scattered trees along the roadside"""

        if random.random() < 0.01:  # 1% chance to regenerate trees each frame
            # Generate a random tree on left side
            y = HORIZON_Y
            x_offset = random.randint(40, 500)  # Random distance from road
            self.trees_left.append((y, x_offset))

        if random.random() < 0.01:  # 1% chance to regenerate trees each frame
            # Generate a random tree on left side
            y = HORIZON_Y
            x_offset = random.randint(40, 500)  # Random distance from road
            self.trees_right.append((y, x_offset))
    
    def draw_tree(self, x, y, scale):
        """Draw a single tree with brown trunk and green leaves"""
        if scale < 0.2:  # Too small to draw
            return
            
        # Tree dimensions based on scale (perspective)
        trunk_width = int(16 * scale)
        trunk_height = int(50 * scale)
        leaf_radius = int(30 * scale)
        
        # Draw trunk (brown rectangle)
        trunk_rect = pygame.Rect(x - trunk_width // 2, y - trunk_height, trunk_width, trunk_height)
        pygame.draw.rect(self.screen, (101, 67, 33), trunk_rect)
        
        # Draw leaves (green circles) - create a bushy effect
        leaf_positions = [
            (x, y - trunk_height - leaf_radius // 2),  # Center top
            (x - leaf_radius // 2, y - trunk_height + leaf_radius // 4),  # Left
            (x + leaf_radius // 2, y - trunk_height + leaf_radius // 4),  # Right
        ]
        
        for leaf_x, leaf_y in leaf_positions:
            pygame.draw.circle(self.screen, (34, 139, 34), (int(leaf_x), int(leaf_y)), leaf_radius)
    
    def draw_trees(self):
        """Draw scattered trees on both sides of the road with perspective"""
        road_center = SCREEN_WIDTH // 2 + self.road_offset * 0.5
        
        new_trees_left = []
        # Draw left side trees
        for i, (y, x_offset) in enumerate(self.trees_left):
            # Scroll trees down with road animation
            y = (y + CAR_SPEED / 4)
                
            # Calculate perspective scale
            scale = self.get_perspective_scale(y)
            
            # Position trees based on road position and their random offset
            road_width = self.get_road_width_at_y(y)
            tree_x = road_center - road_width // 2 - x_offset * scale
            
            # Only draw if tree is on screen
            if 0 <= tree_x <= SCREEN_WIDTH:
                self.draw_tree(tree_x, y, scale)
                new_trees_left.append((y, x_offset))
        self.trees_left = new_trees_left
        
        # Draw right side trees
        new_trees_right = []
        for i, (y, x_offset) in enumerate(self.trees_right):
            # Scroll trees down with road animation
            y = (y + CAR_SPEED / 4)
                
            # Calculate perspective scale
            scale = self.get_perspective_scale(y)
            
            # Position trees based on road position and their random offset
            road_width = self.get_road_width_at_y(y)
            tree_x = road_center + road_width // 2 + x_offset * scale
            
            # Only draw if tree is on screen
            if 0 <= tree_x <= SCREEN_WIDTH:
                self.draw_tree(tree_x, y, scale)
                new_trees_right.append((y, x_offset))
        self.trees_right = new_trees_right

        
    def update_road_curve(self):
        """Update road curvature for variety"""
        # Change road curve more frequently and with larger magnitude
        if self.frame_count % 30 == 0:  # Changed from 100 to 30 for more frequent changes
            self.road_curve = random.uniform(-10, 10)  # Increased from -0.5, 0.5
        
        # Update road offset based on curve
        self.road_offset += self.road_curve
        self.road_offset = max(-150, min(150, self.road_offset))  # Increased range from -100, 100
        
    def spawn_ball(self):
        """Spawn a new ball on the road"""
        # Spawn balls near the horizon (top of screen)
        # They will appear small and grow as they move down
        road_center = SCREEN_WIDTH // 2 + self.road_offset
        # Spawn at horizon with appropriate width
        spawn_y = HORIZON_Y + 20
        x_offset = random.uniform(-ROAD_WIDTH_TOP//3, ROAD_WIDTH_TOP//3)
        x = road_center + x_offset
        ball = Ball(x=x, y=spawn_y, radius=10, initial_x_offset=x_offset)
        self.balls.append(ball)
        
    def shoot_dart(self):
        """Shoot a dart from the car"""
        dart = Dart(x=self.car_x, y=SCREEN_HEIGHT - 60)
        self.darts.append(dart)
        
    def get_perspective_scale(self, y):
        """Calculate scale factor based on Y position for perspective effect"""
        # Objects at horizon (top) are small, at bottom are normal size
        if y <= HORIZON_Y:
            return 0.3
        # Linear interpolation between horizon and bottom
        t = (y - HORIZON_Y) / (SCREEN_HEIGHT - HORIZON_Y)
        return 0.3 + t * 0.7  # Scale from 0.3 to 1.0
        
    def get_road_width_at_y(self, y):
        """Get road width at a given Y position (for perspective)"""
        if y <= HORIZON_Y:
            return ROAD_WIDTH_TOP
        # Linear interpolation between horizon and bottom
        t = (y - HORIZON_Y) / (SCREEN_HEIGHT - HORIZON_Y)
        return ROAD_WIDTH_TOP + t * (ROAD_WIDTH - ROAD_WIDTH_TOP)
    
    def update_game_objects(self):
        """Update positions of balls and darts"""
        # Update road animation
        self.road_y_offset = (self.road_y_offset + CAR_SPEED) % 40
        
        # Update balls
        for ball in self.balls[:]:
            ball.y += BALL_SPEED
            
            # Update ball size based on perspective
            scale = self.get_perspective_scale(ball.y)
            ball.radius = 20 * scale
            
            # Move ball position to account for road curve and perspective
            road_width = self.get_road_width_at_y(ball.y)
            road_center = SCREEN_WIDTH // 2 + self.road_offset * scale
            
            # Scale the offset based on perspective (objects spread out as they get closer)
            ball.x = road_center + ball.initial_x_offset * (road_width / ROAD_WIDTH_TOP)
            
            # Remove balls that went off screen
            if ball.y > SCREEN_HEIGHT + 50:
                if ball.active:
                    self.balls_missed += 1
                self.balls.remove(ball)
                
        # Update darts (they move toward horizon)
        for dart in self.darts[:]:
            dart.y -= DART_SPEED
            
            # Remove darts that reached horizon
            if dart.y < HORIZON_Y:
                self.darts.remove(dart)
                
        # Check dart-ball collisions
        for dart in self.darts:
            if not dart.active:
                continue
            for ball in self.balls:
                if not ball.active:
                    continue
                    
                dist = math.sqrt((dart.x - ball.x)**2 + (dart.y - ball.y)**2)
                if dist < ball.radius:
                    ball.active = False
                    ball.flattened = True  # Mark as flattened
                    dart.active = False
                    self.score += 10
                    
        # Check car-ball collisions
        car_y = SCREEN_HEIGHT - 50
        for ball in self.balls:
            if not ball.active:
                continue
            # Check if ball is near the car position
            if ball.y > car_y - 30 and ball.y < car_y + 20:
                dist = abs(ball.x - self.car_x)
                if dist < ball.radius + 30:  # 30 is roughly half car width
                    ball.active = False
                    ball.flattened = True
                    self.score -= 15  # Lose points for hitting a ball
                    
        # Check if car is out of bounds
        road_center = SCREEN_WIDTH // 2 + self.road_offset
        road_left = road_center - ROAD_WIDTH // 2
        road_right = road_center + ROAD_WIDTH // 2
        
        if self.car_x < road_left + 25 or self.car_x > road_right - 25:
            self.out_of_bounds_timer += 1
            if self.out_of_bounds_timer % 10 == 0:  # Lose 1 point every 10 frames out of bounds
                self.score -= 5
        else:
            self.out_of_bounds_timer = 0
                    
    def get_game_frame(self) -> np.ndarray:
        """
        Get the current game frame as a numpy array for CV processing.
        Students will use this frame to detect lines and circles.
        """
        # Get the pygame surface as a numpy array
        frame = pygame.surfarray.array3d(self.screen)
        frame = np.transpose(frame, (1, 0, 2))
        # Convert RGB to BGR for OpenCV
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return frame
        
    def detect_road_lines(self, frame: np.ndarray) -> Tuple[float | None, float | None]:
        """
        TODO: Implémentez la transformée de Hough pour détecter les lignes de la route
        Arguments:
            frame: Image du jeu (image BGR)
            
        Retourne:
            Tuple de (ligne_gauche_x, ligne_droite_x) en bas de l'écran
            Retourne (None, None) si les lignes ne sont pas détectées
            
        Indices:
        - Convertir en niveaux de gris
        - Utiliser la détection de contours (Canny)
        - Appliquer HoughLinesP ou HoughLines pour détecter les segments de ligne
        - Trouver un moyen de filtrer les lignes pour ne garder que les lignes de la route
        - retourner les positions X des lignes gauche et droite au bas de l'écran
        """
        return None, None
        
    def detect_balls(self, frame: np.ndarray) -> List[Tuple[int, int, int]]:
        """
        TODO: Implémentez la transformée de Hough pour détecter les balles (cercles)

        Arguments:
            frame: Image du jeu (image BGR)

        Retourne:
            List of detected circles as (x, y, radius) tuples

        Indices:
        - Convertir en niveaux de gris
        - Appliquer GaussianBlur pour réduire le bruit
        - Utiliser HoughCircles pour détecter les objets circulaires
        - Filtrer les cercles en fonction de la taille attendue des balles
        """
        return []
        
    def apply_auto_steering(self, left_x: float, right_x: float):
        """
        Use detected road lines to automatically steer the car
        
        Args:
            left_x: X coordinate of left road line
            right_x: X coordinate of right road line
        """
        if left_x is not None and right_x is not None:
            # Calculate road center
            road_center = (left_x + right_x) / 2
            
            # Move car towards road center
            error = road_center - self.car_x
            self.car_x += error * 0.1  # Smooth steering
            
    def apply_auto_shooting(self, circles: List[Tuple[int, int, int]]):
        """
        Automatically shoot darts at detected balls
        
        Args:
            circles: List of detected circles (x, y, radius)
        """
        if circles and self.frame_count % 15 == 0:  # Shoot every 15 frames
            # Find the closest ball
            closest = min(circles, key=lambda c: c[1])
            if closest[1] > SCREEN_HEIGHT // 2:  # Only shoot at close balls
                # Aim at the ball
                target_x = closest[0]
                self.car_x = self.car_x * 0.7 + target_x * 0.3  # Move towards target
                self.shoot_dart()
                
    def draw_road(self):
        """Draw the road with lane markings in perspective"""
        # Draw sky
        pygame.draw.rect(self.screen, (135, 206, 235), (0, 0, SCREEN_WIDTH, HORIZON_Y))
        
        # Draw grass
        pygame.draw.rect(self.screen, GREEN, (0, HORIZON_Y, SCREEN_WIDTH, SCREEN_HEIGHT - HORIZON_Y))
        
        # Calculate road position at horizon and bottom
        road_center_top = SCREEN_WIDTH // 2 + self.road_offset * 0.3
        road_center_bottom = SCREEN_WIDTH // 2 + self.road_offset
        
        # Road corners for perspective trapezoid
        top_left = road_center_top - ROAD_WIDTH_TOP // 2
        top_right = road_center_top + ROAD_WIDTH_TOP // 2
        bottom_left = road_center_bottom - ROAD_WIDTH // 2
        bottom_right = road_center_bottom + ROAD_WIDTH // 2
        
        # Draw road surface as a trapezoid
        road_points = [
            (top_left, HORIZON_Y),
            (top_right, HORIZON_Y),
            (bottom_right, SCREEN_HEIGHT),
            (bottom_left, SCREEN_HEIGHT)
        ]
        pygame.draw.polygon(self.screen, DARK_GRAY, road_points)
        
        # Draw lane markings with perspective
        # Helper function to get road edges at any Y position
        def get_road_edges(y):
            if y <= HORIZON_Y:
                left = road_center_top - ROAD_WIDTH_TOP // 2
                right = road_center_top + ROAD_WIDTH_TOP // 2
                return left, right, road_center_top
            t = (y - HORIZON_Y) / (SCREEN_HEIGHT - HORIZON_Y)
            left = top_left + t * (bottom_left - top_left)
            right = top_right + t * (bottom_right - top_right)
            center = (left + right) / 2
            return left, right, center
        
        # Draw left and right edge lines (yellow)
        pygame.draw.line(self.screen, YELLOW,
                        (top_left, HORIZON_Y), (bottom_left, SCREEN_HEIGHT), 5)
        pygame.draw.line(self.screen, YELLOW,
                        (top_right, HORIZON_Y), (bottom_right, SCREEN_HEIGHT), 5)
        
        # Draw center dashed line (white) with perspective
        dash_start_y = HORIZON_Y + 10
        y = dash_start_y - self.road_y_offset
        
        while y < SCREEN_HEIGHT:
            # Calculate dash length based on perspective (longer when closer)
            scale = self.get_perspective_scale(y)
            dash_length = 20 + 30 * scale
            gap_length = 15 + 15 * scale
            
            if y > HORIZON_Y and y + dash_length > HORIZON_Y:
                left1, right1, center1 = get_road_edges(max(y, HORIZON_Y))
                left2, right2, center2 = get_road_edges(min(y + dash_length, SCREEN_HEIGHT))
                
                line_width = max(2, int(3 * scale))
                pygame.draw.line(self.screen, WHITE,
                               (center1, max(y, HORIZON_Y)),
                               (center2, min(y + dash_length, SCREEN_HEIGHT)),
                               line_width)
            
            y += dash_length + gap_length
            
    def draw_balls(self):
        """Draw footballs on the road"""
        for ball in self.balls:
            if ball.flattened:
                # Draw flattened ball (ellipse on the ground)
                flat_width = int(ball.radius * 2)
                flat_height = int(ball.radius * 0.4)  # Very flat
                pygame.draw.ellipse(self.screen, (100, 20, 0), 
                                   (int(ball.x - flat_width/2), int(ball.y - flat_height/2),
                                    flat_width, flat_height))
                pygame.draw.ellipse(self.screen, (60, 10, 0), 
                                   (int(ball.x - flat_width/2), int(ball.y - flat_height/2),
                                    flat_width, flat_height), 2)
                continue
            
            if not ball.active:
                continue

            # Draw football (black circle with pattern)
            pygame.draw.circle(self.screen, BLACK, 
                             (int(ball.x), int(ball.y)), int(ball.radius))
            pygame.draw.circle(self.screen, WHITE, 
                             (int(ball.x), int(ball.y)), int(ball.radius), 3)
            # Add pentagon pattern
            for i in range(5):
                angle = i * 2 * math.pi / 5
                x = ball.x + ball.radius * 0.6 * math.cos(angle)
                y = ball.y + ball.radius * 0.6 * math.sin(angle)
                pygame.draw.circle(self.screen, WHITE, (int(x), int(y)), ball.radius / 5 )
                
    def draw_darts(self):
        """Draw darts with perspective (smaller as they go farther)"""
        for dart in self.darts:
            if not dart.active:
                continue
            
            # Scale dart based on distance (perspective)
            scale = self.get_perspective_scale(dart.y)
            dart_length = 15 * scale
            dart_width = 5 * scale
            
            # Draw dart (arrow pointing away from viewer)
            pygame.draw.line(self.screen, (100, 100, 100),
                           (dart.x, dart.y), (dart.x, dart.y - dart_length), max(1, int(2 * scale)))
            
            # Arrowhead
            if scale > 0.3:
                pygame.draw.polygon(self.screen, (150, 150, 150),
                                  [(dart.x, dart.y - dart_length), 
                                   (dart.x - dart_width, dart.y - dart_length + dart_width),
                                   (dart.x + dart_width, dart.y - dart_length + dart_width)])
                               
    def draw_car(self):
        """Draw the player's car at bottom of screen (first-person view)"""
        car_y = SCREEN_HEIGHT - 50
        car_rect = self.car_surface.get_rect(center=(int(self.car_x), car_y))
        self.screen.blit(self.car_surface, car_rect)
        
    def draw_game_over(self):
        """Draw game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        
        game_over_text = font_large.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        final_score_text = font_medium.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(final_score_text, score_rect)
        
        missed_text = font_medium.render(f"Balls Missed: {self.balls_missed}", True, WHITE)
        missed_rect = missed_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(missed_text, missed_rect)
    
    def draw_ui(self):
        """Draw UI elements (score, instructions)"""
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)
        
        # Score (color changes based on score)
        score_color = WHITE if self.score >= 50 else (255, 150, 0) if self.score >= 20 else RED
        score_text = font.render(f"Score: {self.score}", True, score_color)
        self.screen.blit(score_text, (10, 10))
        
        # Missed balls
        missed_text = font.render(f"Missed: {self.balls_missed}", True, RED)
        self.screen.blit(missed_text, (10, 50))
        
        # Out of bounds warning
        if self.out_of_bounds_timer > 0:
            warning_text = font.render("OUT OF BOUNDS!", True, RED)
            text_rect = warning_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
            self.screen.blit(warning_text, text_rect)
        
        # Instructions
        instructions = [
            "Arrow Keys: Steer car",
            "Space: Shoot dart",
            "A: Toggle auto-steer (Hough Lines)",
            "S: Toggle auto-shoot (Hough Circles)",
        ]
        
        for i, instruction in enumerate(instructions):
            text = small_font.render(instruction, True, WHITE)
            self.screen.blit(text, (SCREEN_WIDTH - 350, 10 + i * 25))
            
        # Mode indicators
        if self.auto_steer:
            mode_text = small_font.render("AUTO-STEER: ON", True, GREEN)
            self.screen.blit(mode_text, (10, SCREEN_HEIGHT - 60))
            
        if self.auto_shoot:
            mode_text = small_font.render("AUTO-SHOOT: ON", True, GREEN)
            self.screen.blit(mode_text, (10, SCREEN_HEIGHT - 30))
            
    def handle_input(self):
        """Handle user input"""
        keys = pygame.key.get_pressed()
        
        # Manual steering (only when auto-steer is off)
        if not self.auto_steer:
            if keys[pygame.K_LEFT]:
                self.car_x -= 5
            if keys[pygame.K_RIGHT]:
                self.car_x += 5
        
        # Keep car within screen bounds (but allow going off road)
        self.car_x = max(40, min(SCREEN_WIDTH - 40, self.car_x))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.auto_shoot:
                    self.shoot_dart()
                    
                # Toggle auto modes
                if event.key == pygame.K_a:
                    self.auto_steer = not self.auto_steer
                    print(f"Auto-steer: {'ON' if self.auto_steer else 'OFF'}")
                    
                if event.key == pygame.K_s:
                    self.auto_shoot = not self.auto_shoot
                    print(f"Auto-shoot: {'ON' if self.auto_shoot else 'OFF'}")
                    
    def run(self):
        """Main game loop"""
        while self.running:
            self.frame_count += 1
            
            # Check if game over
            if self.score <= 0:
                self.draw_game_over()
                pygame.display.flip()
                pygame.time.wait(3000)  # Wait 3 seconds
                self.running = False
                continue
            
            # Handle input
            self.handle_input()
            
            # Update game state
            self.update_road_curve()
            self.update_game_objects()

            # spawn trees
            self.generate_trees()
            
            # Spawn balls
            if self.frame_count % BALL_SPAWN_RATE == 0:
                self.spawn_ball()
                
            # Draw everything
            self.draw_road()
            self.draw_trees()  # Draw trees after road but before objects
            self.draw_balls()
            self.draw_darts()
            self.draw_car()
            self.draw_ui()
            
            # Computer vision processing (if enabled)
            if self.auto_steer or self.auto_shoot:
                frame = self.get_game_frame()
                
                if self.auto_steer:
                    left_x, right_x = self.detect_road_lines(frame)
                    if left_x is not None and right_x is not None:
                        self.apply_auto_steering(left_x, right_x)
                        
                if self.auto_shoot:
                    circles = self.detect_balls(frame)
                    if circles:
                        self.apply_auto_shooting(circles)
            
            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()


if __name__ == "__main__":
    game = RoadGame()
    game.run()
