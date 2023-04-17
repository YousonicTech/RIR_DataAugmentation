import librosa
import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np
from scipy.interpolate import interp1d
import soundfile as sf
import os


#TODO:修改原始rir路径以及延长后需要存放的rir路径，并且修改延长系数

rir_path = "D:/YouSonic/wav_aug/500hz/0414_old_500hz/split_1_1"
rir_aug_path = "D:/YouSonic/wav_aug/500hz/0414_old_500hz_stretch/split_1_1_stretch"
expand_xishu = 1.65

def expand_audio(xishu,wavsignal):
    f1 = interp1d(np.arange(len(wavsignal[:])), wavsignal, kind='cubic')

    x_new1 = np.linspace(0, len(wavsignal[:]) - 1, int(len(wavsignal[:]) * xishu))
    y_new1 = f1(x_new1)
    return y_new1



if __name__== "__main__":
    data_list=[]#存放原始rir路径
    save_list=[]#存放增强rir路径
    for (root, dirs, files) in os.walk(rir_path):
        data_list = data_list + [os.path.join(root, filen) for filen in files]
        save_list = save_list + [os.path.join(root, filen) for filen in files]
    for i in range(len(data_list)):
        data_list[i] = data_list[i].replace('\\','/')
        save_list[i] = save_list[i].replace('\\','/')
        #TODO：这里也需要相应修改
        save_list[i] = save_list[i].replace('split_1_1','split_1_1_stretch')
        save_list[i] = save_list[i].replace('0414_old_500hz','0414_old_500hz_stretch')

    print(data_list)
    print(save_list)
    
    #dbtype存放获取的音频目录名称，例如central-hall-university-york之类的
    dbtype_list = os.listdir(rir_path)
    for dbtype in dbtype_list:
        if os.path.isfile(os.path.join(rir_path,dbtype)):
            dbtype_list.remove(dbtype)
    #在rir增强路径下创建文件夹central-hall-university-york
    for i in range(len(dbtype_list)):
        os.mkdir(rir_aug_path+'/'+dbtype_list[i])

        
    
    for i in range(len(data_list)):
        rir,sr = librosa.load(data_list[i],sr = 16000)
        print("rir length:",len(rir))
        rir_stretch = expand_audio(expand_xishu,rir)
        print("rir aug length:",len(rir_stretch))

        sf.write(save_list[i], rir_stretch, 16000)
