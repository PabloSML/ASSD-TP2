import numpy as np
from math import ceil
class partial:
    def __init__(self,f,phase, start, At, kAo, Dt, Ao, St, So, Rt):
        '''
        Parámetros:
               f: frecuencia del parcial.
               phase: Fase del parcial.
               start: Tiempo de inicio del parcial.
               At: start + duración de Attack.
               kAo: Amplitud A-D.
               Dt: At + duración de Decay.
               Ao: Amplitud D-S.
               St: Dt + duración de Sustain.
               So: Amplitud S-R.
               Rt: Fin del parcial
               '''
        self.f = f
        self.phase = phase
        self.start = start
        self.dtA = At - start  # duración de Attack
        self.kAo = kAo
        self.dtD = Dt - At  # duración Decay
        self.Ao = Ao
        self.dtS = St - Dt  # duración Sustain
        self.So = So
        self.dtR = Rt - St  # duración Release
        self.end = Rt

    def get_amplitude_array(self, note):
        self.output_signal = self.calculateADSR(note, note.duration)

    def calculateADSR(self, note, last_time_value):

        stageA = np.arange(0, self.dtA, note.fs) * self.kAo / self.dtA
        stageD = np.arange(0, self.dtD, note.fs) * ((self.Ao - self.kAo)/self.dtD) + self.kAo
        stageS = np.arange(0, self.dtS, note.fs) * ((self.So - self.Ao)/self.dtS) + self.Ao
        stageR = np.arange(0, self.dtR, note.fs) * (-self.So/self.dtR) + self.So

        data = np.concatenate([stageA, stageD, stageS, stageR])  # Concateno las etapas

        return data