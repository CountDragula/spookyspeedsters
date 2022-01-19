from Car import Car
from Track import Track


car = Car(50, 100,60,30,"Dragula")
print(car)
stats = car.getRaceStats()
print(stats)
track = Track('Oval', 1000)
print(track)
track.buildTrack()

track = Track('Dragstrip', 5000)
print(track)
track.buildTrack