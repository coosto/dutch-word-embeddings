#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import getpass
import os
import shutil
import sys
import urllib.error
import urllib.request

def downloadModel(destination):
    modelUrl = "https://github.com/coosto/dutch-word-embeddings/releases/download/v1.0/model.bin"

    # Optional token to speed up the download
    username = getpass.getpass("(Optional, but increases download speed)\nGitHub username:")
    token = getpass.getpass("GitHub Token:")
    if username and token:
        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, "https://github.com/coosto/", username, token)
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)

    # Request model data
    try:
        request = urllib.request.Request(modelUrl)
        with urllib.request.urlopen(request) as response, open(destination, 'wb') as fp:
            shutil.copyfileobj(response, fp)
            sys.stderr.write("Model saved: {}\n".format(fp.name))
    except urllib.error.HTTPError as error:
        sys.stderr.write("Error fetching model from github.com - {}\n".format(error))
        sys.stderr.write("{}".format(error.read()))
        exit(1)


def demoAnalogies(model):
    sys.stdout.write("\n---------ANALOGIES---------\n\n")

    # Load some analogies from file and print the results
    with open('analogies.txt') as fp:
        for line in fp:
            line = line.strip()
            if len(line) == 0 or line[0] == '#':
                continue
            if line[0] == ":":
                sys.stdout.write("\nCategory: {}\n".format(line[2:]))
                continue
            neg, pos, q = line.split(' ', 3)
            result = model.most_similar(positive=[q, pos], negative=[neg], topn=1)[0]
            sys.stdout.write("{} - {} + {} = {} ({})\n".format(pos.ljust(12), neg.ljust(12), q.ljust(12), result[0], result[1]))
    return


def demoDistance(model):
    sys.stdout.write("\n---------DISTANCE---------\n(examples: 'banaan', 'hoppa', 'mss', '#dtv', '#wieisdemol')\n\n")
    while True:
        try:
            query = input("Enter word or sentence: ")
            terms = model.most_similar(positive=query, topn=10)
            size = max([len(x[0]) for x in terms]) + 3
            line = "Term".center(size) + "|" + "Distance".center(20)
            print(line)
            print('-' * len(line))
            for term in terms:
                line = term[0].ljust(size) + "|" + str(term[1])
                print(line)

        except KeyError as error:
            print(error)
            continue
        except KeyboardInterrupt:
            del model
            return
    return


def demoModel(inputFile):
    # Let's not presume gensim installation until needed
    import gensim
    sys.stderr.write("Loading model...\n")
    model = gensim.models.KeyedVectors.load_word2vec_format(inputFile, binary=True)
    sys.stderr.write("Model loaded\n")

    # Start demo
    demoAnalogies(model)
    demoDistance(model)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to download/test the Dutch Word2Vec model')
    subparsers = parser.add_subparsers(help='', dest='action')

    parser_download = subparsers.add_parser('download', help="Downloads the Word2Vec model to the target destination")
    parser_download.add_argument('--dest', default="model.bin", type=str, metavar="FILE", help="File path to store the model")

    parser_test = subparsers.add_parser('demo', help="Loads the downloaded model and shows some word analogies and neighbors")
    parser_test.add_argument('--model', type=str, metavar="FILE", required=True, help="File path to the stored model")
    args = parser.parse_args()

    if args.action == 'download':
        downloadModel(args.dest)
    elif args.action == 'demo':
        demoModel(args.model)
    else:
        parser.print_help()
        exit(1)
