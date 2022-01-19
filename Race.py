from Car import Car
from Track import Track

cars = []
for i in range(10):
    cars.append(Car.randomCar(str(i)))
    print(i, '  ', cars[i])
cars[9] = Car(27,38,1,1,"bugmobile")

#returns time the segment finsihed, overrun distance, and True for 
# race end, False for continue 
def traverseSegment(car,currentSegment,nextSegment,currentTime,track):

    if track.segments[currentSegment].shape == 'Start':
        if track.segments[nextSegment].shape == 'Straight':
            return (currentTime, 0, False)

    if track.segments[currentSegment].shape == 'Straight':
        if track.segments[nextSegment].shape == 'End':
            remainingLength = track.segments[currentSegment].length
            while remainingLength > 0:
                car.speed = min(car.topspeed, car.speed + car.accel)
                remainingLength = remainingLength - car.speed
                currentTime = currentTime + 1
                car.position = car.position + car.speed
                car.trackRecord.append(car.position)
                print('Location:', car.position, 'Speed:', car.speed)
                #print(currentTime)
                #print(car.position)
            car.finalTime = currentTime
            print('Final time', car.finalTime)
            return 0

    # If there is a curve up ahead, we need to anticipate the slowdown
    # and brake. So, we work backwards from the curve max speed,
    # to find where we would have to start braking if we were going top speed.
    # Then we work forwards, acceleratin to that point, then braking after
    # we pass it. 
    if track.segments[currentSegment].shape == 'Straight':
        if track.segments[nextSegment].shape == 'Curve':
            print('Straight length:',  track.segments[currentSegment].length )
            curveTopspeed = min(car.topspeed, car.handling)
            print('Curve top speed:', curveTopspeed)
            loc = 1000000

            #First, find out how fast the car would be going into the corner
            # if there were no limit on corner speed
            remainingLength = track.segments[currentSegment].length
            maxSpeedIntoCurve = car.speed
            while remainingLength > 0:
                maxSpeedIntoCurve = min(car.topspeed, maxSpeedIntoCurve + car.accel)
                remainingLength = remainingLength - maxSpeedIntoCurve

            speedLimits = {}
            if curveTopspeed < maxSpeedIntoCurve:
               # print("Need to slow down")
                speed = curveTopspeed
                steps = 0
                loc = car.position + track.segments[currentSegment].length
                while ((loc > car.position) and (speed < maxSpeedIntoCurve) ):
                   # print(loc, speed, steps)
                    for i in range(loc-speed, loc):
                        speedLimits[i] = speed
                    
                    loc = loc - speed
                    speed = speed + car.brakes
                    steps = steps + 1
               # print (speedLimits)

            if (loc < 0):
                loc = 0
            #print('Loc:',loc)
            # remainingLength = track.segments[currentSegment].length
            # while ((car.position < loc) and (remainingLength > 0)):
            #     car.speed = min(car.topspeed, car.speed + car.accel)
            #     remainingLength = remainingLength - car.speed
            #     currentTime = currentTime + 1
            #     car.position = car.position + car.speed
            #     car.trackRecord.append(car.position)
            #     print('Location:', car.position, 'Speed:', car.speed)
            remainingLength = track.segments[currentSegment].length
            while remainingLength > 0:
                if car.position in speedLimits and speedLimits[car.position] < car.speed and \
                     (speedLimits[car.position] + car.position) in speedLimits:
                    car.speed = max(car.speed - car.brakes, speedLimits[speedLimits[car.position] + car.position])
                # if the handling is better than topspeed, you still can't exceed topspeed
                else:
                    car.speed = min(car.speed + car.accel, car.topspeed)
                    if car.position in speedLimits and speedLimits[car.position] < car.speed and \
                     (speedLimits[car.position] + car.position) in speedLimits:
                        car.speed = speedLimits[speedLimits[car.position] + car.position]

                
                remainingLength = remainingLength - car.speed
                currentTime = currentTime + 1
                car.position = car.position + car.speed
                car.trackRecord.append(car.position)
                print('Location:', car.position, 'Speed:', car.speed)

            car.finalTime = currentTime
            return (currentTime, remainingLength * -1, True)
            
    if track.segments[currentSegment].shape == 'Curve':
        if track.segments[nextSegment].shape == 'Straight' :
            remainingLength = track.segments[currentSegment].length
            while remainingLength > 0:
                car.speed = min(car.handling, car.speed + car.accel)
                remainingLength = remainingLength - car.speed
                currentTime = currentTime + 1
                car.position = car.position + car.speed
                car.trackRecord.append(car.position)
                print('Location:', car.position, 'Speed:', car.speed)
                #print(currentTime)
                #print(car.position)
            car.finalTime = currentTime
            return (currentTime, remainingLength * -1, True)
                
    #else        
    return (0,0,False)

track = Track('Oval', 1000)
track.buildTrack()
print(track)

for car in cars:
    print("Start!!!", car)
    results = (0,0,1)
    i = 0
    while results != 0:
        results = traverseSegment(car, i, i+1, results[0], track)
        i = i + 1
    print("The results!!", results)

minTime = 1000000000
for car in cars:
    if car.finalTime < minTime:
        minTime = car.finalTime
        winner = car

print("The winner, ", winner, " won in ", winner.finalTime, "seonds!")


