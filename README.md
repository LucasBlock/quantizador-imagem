usage: lab1.py [-h] [--method METHOD] [--grayscale GRAYSCALE] [--image IMAGE]
               [--percent PERCENT]

optional arguments:
  -h, --help            show this help message and exit
  --method METHOD, -m METHOD
                        Escolhe qual método de quantização
  --grayscale GRAYSCALE, -g GRAYSCALE
                        Quantidade de níveis de cinza
  --image IMAGE, -i IMAGE
                        Caminho da imagem escolhida
  --percent PERCENT, -p PERCENT
                        Porcentual de amostragem

Arguments:
--method ou -m, valores possíveis: media, moda, mediana
--grayscale ou -g, valores possíveis: [2,4,8,16,32,64,128,256]
--image ou -i, Caminho relativo/absoluto da imagem 
--percent ou -p, Percentual da amostragem: [0..2]
Exemplo python3 lab1.py -m media -g 4 -p 2 -i exemplo.png

Exemplo python3 lab1.py -m mediana -g 2 -p 0.5 -i exemplo.png

Exemplo python3 lab1.py -m moda -g 2 -p 1.2 -i exemplo.png

Exemplo python3 lab1.py -m media -g 32 -p 1.7 -i exemplo.png

Exemplo python3 lab1.py -m mediana -g 16 -p 0.2 -i exemplo.png

Exemplo python3 lab1.py -m moda -g 256 -p 0.1 -i exemplo.png