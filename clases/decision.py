import pygame

class DecisionTree():
    def __init__(self, root_node):
        self.root_node = root_node

    def make_decision(self, enemy):
        return self.root_node.decide(enemy)

class DecisionNode():
    def __init__(self, decision_func, true_node, false_node):
        self.decision_func = decision_func
        self.true_node = true_node
        self.false_node = false_node

    def decide(self, enemy):
        if self.decision_func(enemy):
            return self.true_node.decide(enemy)
        else:
            return self.false_node.decide(enemy)

class ActionNode():
    def __init__(self, action_func):
        self.action_func = action_func

    def decide(self, enemy):
        return self.action_func(enemy)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.decision_tree = None
        self.target = None

    def update(self):
        if self.decision_tree is not None:
            print("HERE with ", self.decision_tree)
            self.decision_tree.make_decision(self)

    def set_decision_tree(self, decision_tree):
        self.decision_tree = decision_tree

def is_close_to_target(enemy):
    if enemy.target is None:
        return False
    dx = enemy.target.rect.x - enemy.rect.x
    dy = enemy.target.rect.y - enemy.rect.y
    dist = ((dx ** 2) + (dy ** 2)) ** 0.5
    return dist < 100

def is_target_visible(enemy):
    if enemy.target is None:
        return False
    # Code for checking if target is visible goes here
    return True

def attack_target(enemy):
    # Code for attacking the target goes here
    pass

def move_to_target(enemy):
    if enemy.target is None:
        return False
    dx = enemy.target.rect.x - enemy.rect.x
    dy = enemy.target.rect.y - enemy.rect.y
    dist = ((dx ** 2) + (dy ** 2)) ** 0.5
    if dist > 5:
        speed = 5
        enemy.rect.x += int(dx / dist * speed)
        enemy.rect.y += int(dy / dist * speed)
        return True
    return False

def patrol(enemy):
    # Code for patrolling behavior goes here
    pass

def create_decision_tree():
    is_close_node = DecisionNode(is_close_to_target, ActionNode(attack_target), ActionNode(create_chase_tree()))
    return DecisionTree(is_close_node)

def create_chase_tree():
    is_visible_node = DecisionNode(is_target_visible, ActionNode(attack_target), ActionNode(ActionNode(move_to_target)))
    return DecisionTree(root_node=is_visible_node)