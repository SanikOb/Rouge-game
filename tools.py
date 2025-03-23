from math import acos

def objects_distance(obj1, obj2):
    return (((obj1[2] + obj1[0]) / 2 - (obj2[2] + obj2[0]) / 2) ** 2 + 
            ((obj1[3] + obj1[1]) / 2 - (obj2[3] + obj2[1]) / 2) ** 2) ** 0.5

def objects_angel(obj1, obj2):
    d = objects_distance(obj1, obj2) or 0.000000001
    cosa = ((obj2[2] + obj2[0]) - (obj1[2] + obj1[0])) / 2 / d
    b = (obj2[3] + obj2[1]) - (obj1[3] + obj1[1])
    return acos(cosa) if b >= 0 else -acos(cosa)

def check_entities_collision(canvas, shape, entities):
    obj_coords = canvas.coords(shape)
    for entity in entities:
        try:
            entity_coords = canvas.coords(entity.rect)
        except:
            entity_coords = canvas.coords(entity.oval)
        if (obj_coords[2] > entity_coords[0] and obj_coords[0] < entity_coords[2] and
            obj_coords[3] > entity_coords[1] and obj_coords[1] < entity_coords[3]):
            return entity
    return False