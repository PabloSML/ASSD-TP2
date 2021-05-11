from src.Instrument import Instrument
import numpy as np
import scipy.signal as ss
from scipy.interpolate import interp1d
from scipy.fft import fft, ifft
import soundfile as sf
# import pyaudio


class SampleSynth(Instrument):

    def __init__(self):
        super(SampleSynth, self).__init__()
        self.samples = None

    def play_note(self, frequency, duration, fs, **kwargs):
        return np.array([0.005, 0.005])

    def timeScaler(self, inputVector, winSize, hopSize, timeFactor):

        alpha = timeFactor  # Time Scaling Factor
        hopOut = int(np.round(alpha * hopSize))  # output hopSize
        wn = ss.windows.hann(winSize * 2 + 1)  # Hanning Window
        wn = wn[1::2]

        x = inputVector.copy()
        x = np.append(np.zeros(hopSize * 3), x)

        [y, numberFramesInput] = self.createFrames(x, hopSize, winSize)

        output_y = np.zeros((numberFramesInput, winSize))

        phaseCumulative = 0
        previousPhase = 0

        #   Analysis
        y = y * wn / np.sqrt(((winSize / hopSize) / 2))
        y = fft(y)
        mat_mag = np.abs(y)
        mat_phase = np.angle(y)

        for index in range(numberFramesInput):
            frame_mag = mat_mag[index, :]
            frame_phase = mat_phase[index, :]

            #   Processing
            deltaPhi = frame_phase - previousPhase
            previousPhase = frame_phase

            aux_calc = 2 * np.pi * np.arange(winSize) / winSize
            deltaPhi = deltaPhi - hopSize * aux_calc
            deltaPhi = ((deltaPhi + np.pi) % (2 * np.pi)) - np.pi

            trueFreq = deltaPhi / hopSize + aux_calc
            phaseCumulative = phaseCumulative + hopOut * trueFreq

            #   Synthesis
            currentFrame = np.real(ifft(frame_mag * np.exp(1j * phaseCumulative)))
            output_y[index, :] = currentFrame * wn / np.sqrt(((winSize / hopSize) / 2))

        outputTime = self.fusionFrames(output_y, hopOut)

        return outputTime

    def pitchShift(self, inputVector, winSize, hopSize, pitchStep):

        alpha = 2**(pitchStep/12)    # Pitch Scaling Factor
        outputTimeStreched = self.timeScaler(inputVector, winSize, hopSize, alpha)

        # Resampling
        old_x = np.arange(outputTimeStreched.size)
        f = interp1d(old_x, outputTimeStreched, kind='cubic')
        new_x = np.arange(0, outputTimeStreched.size-1, alpha)
        outputTime = f(new_x)

        return outputTime

    def createFrames(self, x, hopSize, winSize):

        numberSlices = int(np.floor((x.size - winSize) / hopSize))
        x = x[0: (numberSlices*hopSize + winSize)]
        vectorFrames = np.zeros((int(np.floor(x.size / hopSize)), winSize))

        for index in range(numberSlices):

            indexTimeStart = index*hopSize
            indexTimeEnd = index*hopSize + winSize
            vectorFrames[index, :] = x[indexTimeStart: indexTimeEnd]

        return vectorFrames, numberSlices

    def fusionFrames(self, framesMatrix, hopSize):

        numberFrames = framesMatrix.shape[0]
        sizeFrames = framesMatrix.shape[1]

        vectorTime = np.zeros(numberFrames*hopSize - hopSize + sizeFrames)
        timeIndex = 0

        for index in range(numberFrames):

            vectorTime[timeIndex : timeIndex + sizeFrames] = vectorTime[timeIndex: timeIndex + sizeFrames] + framesMatrix[index, :]
            timeIndex += hopSize

        return vectorTime


#   Test Main

# synth = SampleSynth()
# x, fs = sf.read('/tests/promo_m.wav')
# # leftChannel = x[:, 0]
# # rightChannel = x[:, 1]
#
# # averageBoth = ((leftChannel + rightChannel) / 2) # Mono processing
# # y = pitchShift(x, 1024, 256, 2)
#
# # y_left = pitchShift(leftChannel, 1024, 256, -2)  # Stereo Processing
# # y_right = pitchShift(rightChannel, 1024, 256, -2)
# # y = np.column_stack((y_left, y_right))
#
# y = synth.timeScaler(x, 1024, 256, 1/2)   # Reduce el tiempo a la mitad, sin cambiar tono
# # y = synth.pitchShift(x, 1024, 256, -2)  # Disminuye un tono, sin cambiar la escala temporal
# sf.write('../../tests/promo_fast.wav', y, fs)