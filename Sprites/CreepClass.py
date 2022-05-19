

class CreepClass:

    def __init__(self, gameObj):
        self.gameObj = gameObj

        self.creepsType = ["soldier"]
        self.creepClassByType = {"soldier": NewSoldier}
        self.creepsList = []

    def newCreep(self, name, img, pos, creep_type, prio, state, id, health, damage, armor, speed, team, col_box_size=None, col_box_pos=None):
        self.creepEntity = self.creepClassByType[creep_type]()
        self.creepsList.append(self.creepEntity)
        return self.creepEntity

    def update(self, gameObj):
        self.gameObj = gameObj


class NewSoldier:

    def __init__(self, creepClass, name, img, pos, type, prio, state, id, health, damage, armor, speed, team, col_box_size=None, col_box_pos=None):
        self.creepClass = creepClass
        self.gameObj = self.creepClass.gameObj
        self.entityClass = self.gameObj.world.entityClass

        self.health = health
        self.actual_health = health
        self.armor = armor
        self.speed
        self.team = team

        self.type = type
        self.entityObj = self.entityClass.newEntity(name, img, pos, self.type, prio, state, id, 0, self.speed, self.health, col_box_size, col_box_pos)
        self.spriteObj = self.entityObj.spriteObj
