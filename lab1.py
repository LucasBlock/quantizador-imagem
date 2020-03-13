import argparse
import cv2
import os.path
from os import path
import numpy as np
import math

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
    print('Exemplo python3 lab1.py -m mediana -g 10 -p 10 -i exemplo.png')
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
    return arguments

if __name__ == "__main__":
    args = defineArguments()

    arguments = getArguments()
    method = arguments['method'](args)
    grayscale = arguments['grayscale'](args)
    image_path = arguments['image'](args)
    percent = arguments['percent'](args)

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
    imagem_resultante = np.zeros((altura_recalculada, largura_recalculada,1), np.uint8)
    numero = 2**(8-math.log(grayscale, 2))
    for i in range(altura_recalculada):
        for j in range(largura_recalculada):
            imagem_resultante[i][j] = (256/grayscale)*(math.ceil(gray[i][j] / numero) - 1)
    cv2.imshow('Resultado', imagem_resultante)
    cv2.waitKey()