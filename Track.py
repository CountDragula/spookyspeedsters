class Segment:
    def __init__(self, shape, length, start, radius):
        self.shape = shape
        self.length = length
        self.start = start
        self.radius = radius

    def __str__(self):
        return "Shape: {0:10s} Length: {1:6d} Start: {2:6d} Radius: {3:6d}"  \
            .format(self.shape, self.length, self.start, self.radius)

class Track:

    def __init__(self, shape, length):
        self.shape = shape
        self.length = length
        self.start = 0
        self.end = self.length
        # List of Segments, in order beginning with the start segment
        self.segments = []

    def __str__(self):
        return "Shape: {0:10s} Length: {1:6d} Start: {2:6d} End: {3:6d}"  \
            .format(self.shape, self.length, self.start, self.end)

    def buildTrack(self):
        match self.shape:
            # Dragstrip is a straight line, start to end in one go
            case 'Dragstrip':
                self.segments.append(Segment('Start', 0, self.start, 0))
                self.segments.append(Segment('Straight', self.length, self.start, 0))
                self.segments.append(Segment('End', 0, self.length, 0))
            # The race Oval is 2 straightaways joined by 2 half circle turns
            # The start and end are in the middle of the 'top' straighaway.
            case 'Oval':
                straightLength = int(self.length/4)
                curveLength = int(self.length/4)
                curveRadius = int(curveLength/3.14)
                halfStraight =  int(straightLength/2)
                currentPosition = self.start
                self.segments.append(Segment('Start', 0, self.start, 0))
                self.segments.append(Segment('Straight', halfStraight, currentPosition, 0))
                currentPosition = currentPosition + halfStraight
                self.segments.append(Segment('Curve', curveLength, currentPosition, curveRadius))
                currentPosition = currentPosition + curveLength
                self.segments.append(Segment('Straight', straightLength, currentPosition, 0))
                currentPosition = currentPosition + straightLength
                self.segments.append(Segment('Curve', curveLength, currentPosition, curveRadius))
                currentPosition = currentPosition + curveLength
                self.segments.append(Segment('Straight', halfStraight, currentPosition, 0))
                currentPosition = currentPosition + halfStraight
                self.segments.append(Segment('End', 0, self.length, 0))
                
                if int(currentPosition) != self.length:
                    raise Exception('Length of segments does not equal length of track')
            #case 'Fantom-1': make a wiggly track
            case _:
                raise Exception('Not a supported track shape')

