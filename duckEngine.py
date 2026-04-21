import numpy as np

class Entity:
    def __init__(self, pos=None, direction=0.0):
        """
        pos: position initiale [x, y], np.array
        direction: angle en degrés, 0 = x positif
        """
        self.pos = np.array(pos if pos is not None else [0.0, 0.0], dtype=np.float64)
        self.direction = direction % 360.0  # degrés

    @property
    def direction_rad(self):
        return np.radians(self.direction)

    def _normalize_dir(self):
        self.direction %= 360.0

    def set_direction(self, angle):
        self.direction = angle % 360.0

    def rotate(self, angle):
        self.direction = (self.direction + angle) % 360.0

    def forward(self, distance):
        """
        Avancer dans la direction actuelle.
        distance: distance à parcourir
        """
        delta = np.array([np.cos(self.direction_rad), np.sin(self.direction_rad)]) * distance
        self.pos += delta

    def move_arc(self, length, radius):
        """
        Déplacement suivant un arc de cercle.
        length: longueur de l'arc
        radius: rayon (+ pour gauche, - pour droite)
        """
        if radius == 0:
            self.forward(length)
            return

        turn_left = radius > 0
        angle_rad = length / abs(radius)
        if not turn_left:
            angle_rad = -angle_rad

        center_angle = self.direction_rad + (np.pi/2 if turn_left else -np.pi/2)
        center = self.pos + np.array([np.cos(center_angle), np.sin(center_angle)]) * abs(radius)

        offset = self.pos - center

        rotation_matrix = np.array([
            [np.cos(angle_rad), -np.sin(angle_rad)],
            [np.sin(angle_rad),  np.cos(angle_rad)]
        ])
        self.pos = center + rotation_matrix @ offset

        self.direction = (self.direction + np.degrees(angle_rad)) % 360.0
