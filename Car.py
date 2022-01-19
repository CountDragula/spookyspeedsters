from numpy.random import default_rng
import array

class Car:
    def __init__(self,topspeed,accel,handling,brakes,model):
        self.topspeed = self.currentStat(topspeed)
        self.accel = self.currentStat(accel)
        self.handling = self.currentStat(handling)
        self.brakes = self.currentStat(brakes)
        self.model = model
        self.speed = 0
        self.trackRecord = array.array('I')
        #first record is always time zero, position zero
        self.trackRecord.append(0)
        self.position = 0
        self.finalTime = 1000000000

    def __str__(self):
        return "Model: {0:10s}\tTop Speed:{1:4d}\tAcceleration:{2:4d}\tHandling:{3:4d}\tBrakes:{4:4d}\t" \
            .format(self.model, self.topspeed, self.accel,self.handling,self.brakes)


    def currentStat(self, stat):
        rng = default_rng()
        adjustedStat = int(rng.normal(stat,5))
        if (adjustedStat >= 1):
            return adjustedStat
        return 1

    @classmethod
    def randomCar(cls, name):
        rng = default_rng()
        vals = rng.integers(low=1, high=100, size=4)
        return cls(vals[0], vals[1], vals[2], vals[3], "Test car " + name)