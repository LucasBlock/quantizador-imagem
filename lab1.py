import argparse
import cv2
import os.path
from os import path
import numpy as np
import math
import sys

class InvalidMethod(Exception):
    pass
class InvalidGrayScale(Exception):
    pass
class InvalidImage(Exception):
    pass
class InvalidPercent(Exception):
    pass

def howToUse():
    print("----------------------------------------------")
    print("Arguments:")
    print("--method ou -m, valores possíveis: media, moda, mediana")
    print('--grayscale ou -g, valores possíveis: x => x > 0')
    print('--image ou -i, Caminho relativo/absoluto da imagem ')
    print('--percent ou -p, Percentual da amostragem: x => x > 0')
    print('Exemplo python3 lab1.py -m mediana -g 2 -p 0.5 -i exemplo.png')
    print("----------------------------------------------")


def defineArguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("--method", "-m",  help="Escolhe qual método de quantização")
    parser.add_argument("--grayscale", "-g",  help="Quantidade de níveis de cinza")
    parser.add_argument("--image", "-i",  help="Caminho da imagem escolhida")
    parser.add_argument("--percent", "-p",  help="Porcentual de amostragem")

    return parser.parse_args()

def getMethod(args):
    try:
        if args.method is None or args.method != 'media' and args.method != 'mediana' and args.method != 'moda':
            print('Invalid method')
            raise InvalidMethod()
        
        return args.method
    
    except(InvalidMethod):
        howToUse()
        quit()

def getGrayscale(args):
    try:
        if 0 >= int(args.grayscale):
            print('Invalid greyscale')
            raise InvalidGrayScale()
        
        return int(args.grayscale)
    
    except(InvalidGrayScale):
        howToUse()
        quit()

def getImage(args):
    try:
        if args.image is None or not(path.exists(args.image)):
            print('Image not found')
            raise InvalidImage()
        
        return args.image

    except(InvalidImage):
        howToUse()
        quit()

def getPercent(args):
    try:
        if 0 >= float(args.percent):
            print('Invalid percent')
            raise InvalidPercent()
        return float(args.percent)
    except(InvalidPercent):
        howToUse()
        quit()

def getArguments():
    arguments = {}
    arguments['method'] = getMethod
    arguments['grayscale'] = getGrayscale
    arguments['image'] = getImage
    arguments['percent'] = getPercent
    arguments['media'] = mediaSubMatriz
    arguments['moda'] = modaSubMatriz
    arguments['mediana'] = medianaSubMatriz
    return arguments

def getProximos(img, i, j, tam):
    proximos = list()
    for indice_i in range(tam):
        for indice_j in range(tam):
            proximos.append(img[i+indice_i][i+indice_j])
    return proximos

def mediaSubMatriz(matriz):
    linhas, colunas = matriz.shape[:2]
    media = 0
    for i in range(0, linhas):
        for j in range(0, colunas):
            media += matriz[i][j]
    return media/(linhas*colunas)

def modaSubMatriz(matriz):
    array = np.concatenate(matriz)
    counts = np.bincount(array)
    return np.argmax(counts)

def medianaSubMatriz(matriz):
    array = np.concatenate(matriz)
    return np.median(array)
    

if __name__ == "__main__":
    args = defineArguments()
    
    arguments = getArguments()
    method = arguments['method'](args)
    grayscale = arguments['grayscale'](args)
    image_path = arguments['image'](args)
    percent = arguments['percent'](args)
    function = arguments[method]

    print("O método escolhido foi:  %s" % method)
    print("Imagem escolhida:  %s" % image_path)
    print("Porcentual da amostragem:  %s" % percent)
    print("Escala de níveis de cinza:  %s" % grayscale)

    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    altura = gray.shape[0]
    largura = gray.shape[1]
    altura_recalculada = math.ceil(altura * percent)
    largura_recalculada = math.ceil(largura * percent)
    imagem_resultante = np.zeros((altura_recalculada + 1, largura_recalculada + 1,1), np.uint8)
    numero = 2**(8-math.log(grayscale, 2))
    niveis_cinza = math.ceil(256/(grayscale - 1) - 1)
    
    
    
    resize = 1/percent
    i = 0
    ii = 0
    if resize < 0:
        multiplicador = int(resize)
    else:
        multiplicador = 1
    while (i < altura):
        j = 0
        jj = 0
        while(j < largura):
            sub_matriz = gray[int(i):int(i) + multiplicador,int(j):int(j) + multiplicador]
            imagem_resultante[ii][jj] = function(sub_matriz)
            imagem_resultante[ii][jj] = niveis_cinza*(math.ceil(imagem_resultante[ii][jj] / numero) - 1)
            j += resize
            jj += 1
        i += resize
        ii += 1
    cv2.imshow('Matriz resultado', imagem_resultante)
    cv2.waitKey()