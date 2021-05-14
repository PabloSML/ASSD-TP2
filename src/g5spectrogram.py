import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq
from scipy.signal import windows
import seaborn as sb
import pandas as pd

def myspectrogram(x, nfft=2048, fs=1, window=windows.hamming(512), noverlap=256, doplot=1, dbdown=100):
    M = len(window)
    # Require window
    # if (M < 2):
    #     error('myspectrogram: Expect complete window, not just its length')

    # Zero-pad:
    nx = x.size
    if x.size < M:
        x = np.append(x, np.zeros(M - x.size))
    Modd = M % 2;  # 0 if M even, 1 if odd
    Mo2 = (M - Modd) / 2;
    w = window

    if noverlap < 0:            #If passed as negative, noverlap is hopping ammount
        nhop = - noverlap
        noverlap = M - nhop
    else:
        nhop = M - noverlap     #If passed as positive, noverlap is noverlap

    nframes = 1 + np.ceil(nx / nhop)
    wedx = np.zeros((int(nfft), int(nframes)), dtype=complex)   #sliding window
    X = np.zeros((int(nfft), int(nframes)), dtype=complex)  # output spectrogram
    zp = np.zeros(nfft - M)  # zero-padding for each FFT
    xframe = np.zeros(M)  # Define a frame
    xoff = 0 - Mo2  # input time offset = half a frame
    for m in range(int(nframes)):
        if xoff < 0:
            xframe = np.concatenate((x[0:int(M + xoff)], np.zeros(int(-xoff))))
        else:
            if xoff + M > nx:
                xframe = np.concatenate((x[int(xoff):int(nx)], np.zeros(int(xoff + M - nx))))
            else:
                xframe = x[int(xoff):int(xoff + len(xframe))] # input data
        xw = w * xframe # Apply window
        xwzp = xw.tolist()
        xwzp.extend(np.zeros(nfft - M))  # Create zero padded, windowed function for later fft
        X[:, m] = fft(xwzp)

        xoff = xoff + nhop  # advance input offset by hop size

    if doplot:
        nfodd = nfft % 2
        nfs = (nfft + nfodd)/2              # Half the frequencies
        t =  np.arange(0, nframes ) * nhop / fs
        f =  0.001*np.arange(0, nfs ) * fs / nfft;
        t =  np.around(t,2)
        f =  np.around(f,0)
        Xdb = 20 * np.log10(abs(X))
        Xdb = Xdb[0:int((nfft + nfodd) / 2), 0:int(nframes)]  # cut frequency spectre in half
        df = pd.DataFrame(data=Xdb, columns=t, index=f)
        fig1 = sb.heatmap(df, square=False, cmap="jet", cbar_kws={'label': 'Amplitude (dB)'})
        fig1.invert_yaxis()        #El zoom lo invierte
        plt.xlabel("Time (s)")
        plt.ylabel("Frequency (kHz)")
        plt.tight_layout()
        plt.show()
