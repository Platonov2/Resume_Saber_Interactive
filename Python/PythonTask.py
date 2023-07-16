import json
import sys
import argparse

def createParser () -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument ('firstFilePath')
    parser.add_argument ('secondFilePath')
    parser.add_argument ('-o', '--outputFilePath')

    return parser

def mergeLogFiles (firstFilePath, secondFilePath, outputFilePath) -> None:
    firstFile = open(firstFilePath, "r")
    secondFile = open(secondFilePath, "r")
    outputFile = open(outputFilePath, "w")

    isFirstFileRowLoaded = False
    isSecondFileRowLoaded = False

    # Алгоритм заключается в том, что на каждой итерации цикла по временным меткам сравниваются 2 записи из переданных файлов.
    #   Наименьшая из них загружается в итоговый файл, наибольшая - остаётся для дальнейшего сравнения.
    #   Если один из файлов закончился раньше другого, то дальнее сравнение не имеет смысла
    #     и необходимо полностью скопировать оставшиеся строки в выходной файл.
    # Сложность алгоритма = О(n + m), где n и m - кол-во строк в исходных файлах соответственно.

    while True:
        if not isFirstFileRowLoaded:
            firstFileLine = firstFile.readline()
            if firstFileLine:
                isFirstFileRowLoaded = True
            else:
                outputFile.write(secondFileLine)
                break
        if not isSecondFileRowLoaded:
            secondFileLine = secondFile.readline()
            if secondFileLine:
                isSecondFileRowLoaded = True
            else:
                outputFile.write(firstFileLine)
                break

        if json.loads(firstFileLine)["timestamp"] < json.loads(secondFileLine)["timestamp"]:
            outputFile.write(firstFileLine)
            isFirstFileRowLoaded = False
        else:
            outputFile.write(secondFileLine)
            isSecondFileRowLoaded = False

    notEndedFile = firstFile if isFirstFileRowLoaded else secondFile
    while True:
        line = notEndedFile.readline()

        if line:
            outputFile.write(line)
        else: break
        

if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    mergeLogFiles(namespace.firstFilePath, namespace.secondFilePath, namespace.outputFilePath)