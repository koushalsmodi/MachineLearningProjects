# Variable/ function names
import numpy as np

base_pressure = 3.5
wave_length  = 15.7
wave_number = 2 * np.pi / wave_length
angular_frequency = 13.2
x = 2
t = 0.5
pressure = base_pressure  * np.cos(wave_number * x - angular_frequency * t)
print(pressure)

from IPython.display import YouTubeVideo
YouTubeVideo('kM9zcfRtOqo')

