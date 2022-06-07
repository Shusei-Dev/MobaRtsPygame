

class CreepClass:

    def __init__(self, gameObj):
        self.gameObj = gameObj

        self.creepsType = ["soldier"]
        self.creepClassByType = {"soldier": NewSoldier}
        self.creepsList = []

    def newCreep(self, name, img, pos, creep_type, prio, state, id, health, damage, armor, speed, team, col_box_size=None, col_box_pos=None):
        self.creepEntity = self.creepClassByType[creep_type](self, name, img, pos, prio, state, id, health, damage, armor, speed, team, col_box_size=None, col_box_pos=None)
        self.creepsList.append(self.creepEntity)
        return self.creepEntity

    def update(self, gameObj):
        self.gameObj = gameObj

        for creep_entity in self.creepsList:
            creep_entity.update_Class(self)


class NewSoldier:

    def __init__(self, creepClass, name, img, pos, prio, state, id, health, damage, armor, speed, team, col_box_size=None, col_box_pos=None):
        self.creepClass = creepClass
        self.gameObj = self.creepClass.gameObj
        self.entityClass = self.gameObj.world.entityClass

        self.health = health
        self.actual_health = health
        self.armor = armor
        self.speed = speed
        self.team = team

        self.entityObj = self.entityClass.newEntity(name, img, pos, "minion", prio, state, id, 0, self.speed, self.health, col_box_size, col_box_pos)
        self.spriteObj = self.entityObj.spriteObj

    def update_Class(self, creepClass):
        self.creepClass = creepClass

    def update(self):
        self.entityObj.update()

        self.health = self.entityObj.health
        self.actual_health = self.entityObj.actual_health
        self.gameObj = self.creepClass.gameObj
        self.gameTime = self.gameObj.world.gameTime
