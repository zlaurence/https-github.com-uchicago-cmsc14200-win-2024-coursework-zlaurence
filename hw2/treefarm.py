"""
CMSC 14200, Winter 2024
Homework #2

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""
import os
import sys
from typing import Optional

from trees import BaseBST, BSTEmpty, BSTNode

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pygame.gfxdraw

BUTTON_RADIUS = 24
NODE_RADIUS = 32
FONT_SIZE = 36


class TreeFarm:
    """
    Class for a GUI-based binary tree viewer and editor
    """

    width: int
    height: int
    border: int
    tree: BaseBST
    buttons: dict[str, tuple[int, int]]
    surface: pygame.surface.Surface
    clock: pygame.time.Clock
    font: pygame.font.Font
    
    def __init__(self, width: int = 600, height: int = 400,
                 border: int = 32):
        """
        Constructor

        Parameters:
            width : int : width of window
            height : int : height of window
            border : int : number of pixels to use as border around elements
        """
        self.width = width
        self.height = height
        self.border = border
        self.tree = BSTNode(0, BSTEmpty(), BSTEmpty())
        
        btn_x = width - border - BUTTON_RADIUS
        self.buttons = {"BST":       (btn_x, border + BUTTON_RADIUS),
                        "delete":    (btn_x, 3 * border +  2 * BUTTON_RADIUS),
                        "add-left":  (btn_x, 3 * border +  4 * BUTTON_RADIUS),
                        "add-right": (btn_x, 3 * border +  6 * BUTTON_RADIUS),
                        "plus-one":  (btn_x, 3 * border +  8 * BUTTON_RADIUS),
                        "sub-one":   (btn_x, 3 * border + 10 * BUTTON_RADIUS)}
        
        # Initialize Pygame
        pygame.init()
        pygame.display.set_caption("TreeFarm")
        self.font = pygame.font.Font(None, size=FONT_SIZE)
        self.surface = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        self.event_loop()
    
    def _draw_button(self, radius: int, center: tuple[int, int], label: str,
                     highlighted: bool) -> None:
        """
        Draws a button or tree node

        Parameters:
            radius : int : radius of circle representing button or node
            center : Tuple[int, int] : center coordinates of circle
            label : str : textual label for button or node
            highlighted : bool : whether the circle should have a colored
                                 highlight indicating it is selected

        Returns: nothing
        """
        if highlighted:
            pygame.gfxdraw.filled_circle(self.surface, center[0], center[1],
                                         radius, (100, 200, 255))
        else:
            pygame.gfxdraw.filled_circle(self.surface, center[0], center[1],
                                         radius, (255, 255, 255))
        pygame.gfxdraw.aacircle(self.surface, center[0], center[1], radius,
                                (0, 0, 0))
        
        label_img = self.font.render(label, True, (0, 0, 0))
        text_topleft = (center[0] - label_img.get_width() // 2,
                        center[1] - label_img.get_height() // 2)
        self.surface.blit(label_img, text_topleft)
    
    def _draw_tree(self, tree: BaseBST, left: int, right: int, y: int,
                  levelskip: int) -> None:
        """
        Draws a binary tree

        Parameters:
            tree : BaseBST : the (sub)tree to draw
            left : int : x-coordinate of left edge of region in which to draw
            right : int : x-coordinate of right edge of region in which to draw
            y : int : y-coordinate of center of circle for root of (sub)tree
            levelskip : int : gap in pixels when moving down from parent to
                              child

        Returns: nothing
        """
        if isinstance(tree, BSTNode):
            node_center = ((left + right) // 2, y)
            left_center = (left + (right - left) // 4, y + levelskip)
            right_center = (left + 3 * (right - left) // 4, y + levelskip)
            if isinstance(tree.left, BSTNode):
                pygame.draw.aaline(self.surface, (0, 0, 0), node_center,
                                   left_center)
            if isinstance(tree.right, BSTNode):
                pygame.draw.aaline(self.surface, (0, 0, 0), node_center,
                                   right_center)
                                 
            self._draw_button(NODE_RADIUS, node_center, str(tree.value), False)
                              
            self._draw_tree(tree.left, left, (left + right) // 2, y + levelskip,
                            levelskip)
            self._draw_tree(tree.right, (left + right) // 2, right,
                            y + levelskip, levelskip)

    def draw_window(self) -> None:
        """
        Draws the contents of the window

        Parameters: none beyond self

        Returns: nothing
        """
        self.node_positions = {}
        levels = self.tree.height
        figheight = self.height - 2 * self.border
        figwidth = self.width - 3 * self.border - 2 * BUTTON_RADIUS
        if levels != 1:
            levelskip = (figheight - 2 * NODE_RADIUS) // (levels - 1)
        else:
            levelskip = 0
        
        self.surface.fill((124, 252, 0))
        
        self._draw_button(BUTTON_RADIUS, self.buttons["BST"], "?", False)
        self._draw_button(BUTTON_RADIUS, self.buttons["delete"], "X", False)
        self._draw_button(BUTTON_RADIUS, self.buttons["add-left"], "+L", False)
        self._draw_button(BUTTON_RADIUS, self.buttons["add-right"], "+R", False)
        self._draw_button(BUTTON_RADIUS, self.buttons["plus-one"], "+1", False)
        self._draw_button(BUTTON_RADIUS, self.buttons["sub-one"], "-1", False)
        
        self._draw_tree(self.tree, self.border, self.border + figwidth,
                        self.border + NODE_RADIUS, levelskip)

    
    def is_bst(self, node=None, min_value=None, max_value=None) -> bool:
        """
        Checks if the binary tree is a BST

        Parameters:
            Node: BSTtreestub
            min_value: Min val that node must be greater than
            max_value: Max val that node must be less than

        Returns:
            True if the tree is a BST, False otherwise.
        """
        if node is None or isinstance(node, BSTEmpty):
            return True

        if (min_value is not None and node.value <= min_value) or \
           (max_value is not None and node.value >= max_value):
            return False

        left_is_bst = self.is_bst(node.left, min_value, node.value)
        right_is_bst = self.is_bst(node.right, node.value, max_value)

        return left_is_bst and right_is_bst
    
    def get_node_at_pos(self, mouse_pos):
        """
        Finds the node at the given mouse position.

        Parameters:
            cordinates of mouse

        Returns:
            Node or none
        """
        for node, position in self.node_positions.items():
            node_x, node_y = position
            if (mouse_pos[0] - node_x) ** 2 + \
               (mouse_pos[1] - node_y) ** 2 <= NODE_RADIUS ** 2:
                return node
        return None
        
    def event_loop(self) -> None:
        """
        Handles uses moves 

        Parameters:  self

        Returns: Nothing, but has interface outputs
        """       
        selected_node: Optional[BSTNode] = None  

        while True:
            # Events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = event.pos

                    for button_name, button_pos in self.buttons.items():
                        if (mouse_pos[0]\
                             - button_pos[0]) ** 2\
                            + (mouse_pos[1] - button_pos[1])\
                            ** 2 <= BUTTON_RADIUS ** 2:
                            if button_name == "add-left":
                                if self.tree.left is None:  
                                    self.tree.left = BSTNode(0)  
                                break
                            elif button_name == "add-right":
                                if self.tree.right is None:  
                                    self.tree.right = BSTNode(0)  
                                break
                            if button_name == "delete" and selected_node:
                                self.tree = \
                                self.tree.delete(selected_node.value)
                                selected_node = None
                            elif button_name == "plus-one" and selected_node:
                                selected_node.value += 1
                            elif button_name == "sub-one" and selected_node:
                                selected_node.value -= 1
                        
                        
                            break

                    clicked_node = self.get_node_at_pos(mouse_pos) 
                    #REALLY NEED TO FIGURE OUT CLICKER.PY!
                    if clicked_node:
                        if selected_node == clicked_node:
                        # Deselecting
                            selected_node = None
                        else:
                        # Selected 
                            selected_node = clicked_node
            bst_status = 'Y' if self.is_bst(self.tree) else 'N'
            self.buttons['BST'] = (self.buttons['BST'][0], \
                                   self.buttons['BST'][1], bst_status)
            self.draw_window() 
                        
        # Update the display
            self.draw_window()
            pygame.display.update()
            self.clock.tick(24)




if __name__ == "__main__":
    TreeFarm()
