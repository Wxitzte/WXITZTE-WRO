"""
Program's Entry Point for WRO2026 Senior
"""

from pybricks.parameters import Port, Color, Direction
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.hubs import PrimeHub

from huskylens import Huskylens, Block, ALGORITHM_COLOR_RECOGNITION
from drivebase import DriveBaseAPI, MissionMotor, PIVOT_LEFT, PIVOT_RIGHT
from math import ceil, floor

prime_hub = PrimeHub()
#husky = Huskylens(Port.E)
m1 = MissionMotor(Motor(Port.C))
m2 = MissionMotor(Motor(Port.D))
w = DriveBaseAPI(
    Motor(Port.A, Direction.COUNTERCLOCKWISE), 
    Motor(Port.B, Direction.CLOCKWISE), 
    ColorSensor(Port.F),
    hub = prime_hub,
    straight_params = {
        30:  (3.0, 2.5, 0.05), -30:  (2.0, 2.5, 0.05),
        50:  (3.0, 6.0, 0.075), -50:  (2.4, 6.0, 0.065),
        75:  (3.0, 10.0, 0.1), -75:  (3.0, 10.0, 0.1),
        100: (4.0, 16.0, 0.2), -100: (4.0, 16.0, 0.2),
    },
    tagline_params = {
        30:  (0.65, 0.0, 0.065), -30:  (0.65, 0.0, 0.065),
        50:  (1.0, 0.0, 0.075), -50:  (1.0, 0.0, 0.075),
        75:  (1.0, 0.0, 0.08), -75:  (1.0, 0.0, 0.08),
        100: (1.0, 0.0, 0.1), -100: (1.0, 0.0, 0.1),
    },
    turn_params = {
        90:  (2.075, 3.5, 0.05),
    },
)

# (0,0)#1, (0,1)#2, (0,2), (0,3)
# (1,0)#5, (1,1)#6, (1,2), (1,3)
# (2,0)#3, (2,1)#4, (2,2), (2,3)
def getMosaicData(tiles: list[Block], ratio_tolerance: int, area_tolerance: int) -> list[list[int]] | None:
    filtered = [tile for tile in tiles if abs(tile.ratio() - ratio_tolerance) <= 1.0 and tile.area() <= area_tolerance]
    if len(filtered) < 12: return None
    sort_by_row = sorted(filtered, key = lambda tile: tile.y)
    return [[v.id for v in sorted(sort_by_row[i:i+4], key = lambda tile: tile.x)] for i in range(0, 12, 4)]

YELLOW = 0
BLUE = 1
GREEN = 2
WHITE = 3

M2_PICK = 67
M1_DOWN = 290
BRAKE_TIME = 20

def FirstMission():
    w.run(
        [w.ms(500) , w.movetank(-75 ,-75)],
        w.resetEncoder(),
        w.resetImu(),
        [w.degree(250), w.straight(-50)],
        [w.heading(90), w.turn()],
        w.resetEncoder()
    )

    w.runConcerent(
        [w.ms(550)],
        [w.ms(300),m1.move(75)],	#set 0
        
    )

    w.runConcerent(
        [w.ms(550)],
        [w.ms(300),m2.move(75)],	#set 0
        
    )

    w.run(
        [ w.blackReflection(20), w.straight(75) ],
            [ w.all(w.blackReflection(20), w.straight(75) )],	#half
    )
    w.runConcerent(
        [m1.degree(290),m1.move(75)],
        m1.brake(),				#down
        m1.resetEncoder()
        
    )

    w.run(
        [w.ms(50), w.brake()],
        [w.heading(0), w.turn() ],
        [m1.degree(180),m1.move(-100)], 		#backdown
        [m1.degree(380),m1.move(75)],m1,hold(),
        m1.resetEncoder(),
        [w.heading(70), w.turn() ],		#turnblock
        [w.ms(20), w.brake()],
        [w.degree(100), w.straight(-50)],	
        [w.degree(300), w.straight(-75)],
        [w.degree(400), w.straight(-50)],
        w.resetEncoder(),
    )
    w.run(
        [ w.blackReflection(20), w.straight(50)],
        [w.heading(90), w.turn()],		#returntoline
        [w.degree(100), w.straight(50)],	
        [w.degree(600), w.straight(75)],
        [w.degree(700), w.straight(50)],
        w.resetEncoder(),
    )
    w.run(
        [w.ms(20),w.brake()],
        [heading(0),w.turn()],
        [w.degree(300),w.striaght(50)],
        w.resetEncoder()
    )

    w.runConcurrent(
        [w.ms(800)]
        [m1.degree(100),m1.move(-75)],m1.hold(),
        m1.resetEncoder()
    )

    w.run(
        [ w.blackReflection(20), w.straight(50) ],
        [ w.degree(100) , w.striaght(50)],
        [ w.degree(500) , w.striaght(75)],
        [ w.degree(600) , w.striaght(50)],
        [ w.heading(-90) , w.turn()],
        w.resetEncoder()
    )

    w.run(
        [w.deegree(100),w.straight(-50)],
        [w.deegree(200),w.straight(-75)],
        [w.deegree(350),w.straight(-50)],
        [m1.degree(100), m1.move(100)],		#keep yellow
        w.resetEncoder(),
        m1.resetEncoder()
    )

    w.run(
        [ w.blackReflection(20), w.straight(50) ],
        [ w.heading(-180), w.turn()],
    )

    w.run(	
        [ w.degree(100),w.striaght(50) ],
        [ w.degree(1400),w.striaght(50) ],
        [ w.degree(1500),w.striaght(50) ],
        w.resetEncoder()
    )

    w.run(
        [ w.blackReflection(20), w.straight(75) ],
        [ w.all(w.blackReflection(20), w.straight(75)) ], #back to half
    )
    
    w.run(
        [w.ms(80),w.brake()],
        [w.heding(-270), w.turn()],
        
    )
    w.run(
        [w.ms(80),w.brake()],
        [w.degree(100) , w.striaght(-50)],
        [w.degree(200) , w.striaght(-50)],
        [w.degree(300) , w.striaght(-75)],
        w.resetencoder()
        
    )
    w.runConcurrent(
        [w.ms(600)],
        [m1.degree(100), m1.move(75)],
        m1.resetEncoder()	
    )

    w.run(
        [w.blackReflection(20), w.straight(50)]	,
        [w.heading(-180),w.turn()],
        [w.degree(100),w.stright(50)],
        [w.degree(1400),w.stright(75)],
        [w.degree(1500),w.stright(50)],
        w.resetEncoder()
        [w.heading(0), w.turn()],
        [w.degree(150),w.straight(-50)]	 #SET ZERO FOR MOSAIC
        w.resetEncoder()
    )
