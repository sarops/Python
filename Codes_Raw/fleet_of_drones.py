# An update to the first drone code; this code now has a fleet/team of drones monitoring maritime traffic
# as well as objects found at sea for object collision avoidance system related taks (such as large bodies of mass: glaciers are used in this code.)

import turtle, time, random, math


# turtle screen
screen = turtle.Screen()
screen.title("Drone Monitoring Maritime Traffic")
screen.bgcolor("lightblue")
screen.setup(width=800, height=600)

# main ship
ship = turtle.Turtle()
ship.shape("square")
ship.color("blue")
ship.penup()
ship.goto(0, 0)  # ship starts at the origin

# radius and sectors for drones
radius = 300
num_drones = 3
sectors = [(i * (360 / num_drones), (i + 1) * (360 / num_drones)) for i in range(num_drones)]

# create random positions for other vessels and glaciers
def generate_random_positions(num_positions, radius):
    positions = []
    for _ in range(num_positions):
        angle = random.uniform(0, 360)
        r = random.uniform(50, radius)  # Avoid center to ensure they are within the radius
        x = r * math.cos(math.radians(angle))
        y = r * math.sin(math.radians(angle))
        positions.append((x, y))
    return positions

# create other vessels and glaciers
other_vessels = generate_random_positions(5, radius)
glaciers = generate_random_positions(3, radius)

# creating a fleet of drones
class Drone(turtle.Turtle):
    def __init__(self, color):
        super().__init__()
        self.shape("triangle")
        self.color(color)
        self.penup()
        self.goto(ship.position())  # the drone starts at the ship's position
        self.data = []

    def gather_data(self, position):
        distance = self.distance(position)
        flow, congestion = gather_maritime_traffic_data(distance)
        self.data.append((flow, congestion))
        return flow, congestion

# function to simulate maritime traffic data based on distance
def gather_maritime_traffic_data(distance):
    if distance < 50:
        flow = random.randint(200, 400)  # high flow if close
        congestion = random.randint(7, 10)  # high congestion if close
    elif distance < 100:
        flow = random.randint(100, 200)  # moderate flow if medium distance
        congestion = random.randint(4, 6)  # moderate congestion if medium distance
    else:
        flow = random.randint(20, 100)   # low flow if far away
        congestion = random.randint(1, 3)  # low congestion if far away
    
    return flow, congestion

# display traffic data from the drone
def display_traffic_data(drone):
    turtle.clear()  # clear previous messages
    turtle.penup()
    turtle.hideturtle()
    turtle.goto(-350, 250)  # position for displaying text
    
    if drone.data:
        flow, congestion = drone.data[-1]  # get the latest data
        turtle.write(f"Drone: Traffic Flow: {flow} vessels/hour", font=("Arial", 16, "normal"))
        turtle.goto(-350, 220)
        turtle.write(f"Congestion Level: {congestion}/10", font=("Arial", 16, "normal"))

    turtle.goto(-350, 190)
    turtle.write("Monitoring Maritime Traffic...", font=("Arial", 16, "normal"))

# move each drone to its assigned sector and monitor vessels and glaciers
def move_drones_to_monitor(drones):
    for drone_index, drone in enumerate(drones):
        # calculate the center angle of the sector for this drone
        start_angle, end_angle = sectors[drone_index]
        
        # monitor positions within the sector
        for angle in range(int(start_angle), int(end_angle), 45):  # Check every 45 degrees within the sector
            pos_x = radius * math.cos(math.radians(angle))
            pos_y = radius * math.sin(math.radians(angle))
            monitoring_position = (pos_x, pos_y)

            drone.goto(monitoring_position)  # move the drone to monitoring position
            time.sleep(1)  # wait for a second to visualize the monitoring
            
            # gather data from all vessels and glaciers at this position
            for vessel in other_vessels + glaciers:

                flow, congestion = drone.gather_data(vessel)
            
            # display traffic data after monitoring this position
            display_traffic_data(drone)
            time.sleep(2)  # Wait a bit longer to read the data
        
        # return the drone to the ship's position after monitoring
        drone.goto(ship.position())
        time.sleep(1)  # wait for a second before ending

# fleet of drones
drones = [Drone(color=random.choice(["red", "orange", "yellow", "purple"])) for _ in range(num_drones)]

# vessels and glaciers
for vessel in other_vessels:
    vessel_turtle = turtle.Turtle()
    vessel_turtle.shape("circle")
    vessel_turtle.color("green")
    vessel_turtle.penup()
    vessel_turtle.goto(vessel)

for glacier in glaciers:
    glacier_turtle = turtle.Turtle()
    glacier_turtle.shape("square")
    glacier_turtle.color("white")
    glacier_turtle.penup()
    glacier_turtle.goto(glacier)

# start
move_drones_to_monitor(drones)

screen.exitonclick()
