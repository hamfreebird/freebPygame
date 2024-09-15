import freemap
import freeobject
from freestate import *

player = freeobject.Player(200, 100, 200, 100, 10, None)
object1 = freeobject.Object(600, 800, 10, None)
object2 = freeobject.Object(1200, 900, 10, None)
object3 = freeobject.Object(1550, 400, 10, None)
objects = [object1, object2, object3]
gamemap = freemap.Map(player, objects, 720, 480, 1920, 1080, 20)
