#!/bin/bash

date >> logs/docker.elasnocongresso.log
python elasnocongresso.py 1>> logs/elasnocongresso.log 2>> logs/elasnocongresso.err.log;
python enviar_tweets.py 1>>logs/enviar_tweets.log 2>>logs/enviar_tweets.err.log;
sleep 10800;
date >> logs/docker.elasnocongresso.log
python elasnocongresso.py 1>> logs/elasnocongresso.log 2>> logs/elasnocongresso.err.log;
python enviar_tweets.py 1>>logs/enviar_tweets.log 2>>logs/enviar_tweets.err.log;
sleep 18000;
date >> logs/docker.elasnocongresso.log
python elasnocongresso.py 1>> logs/elasnocongresso.log 2>> logs/elasnocongresso.err.log;
python enviar_tweets.py 1>>logs/enviar_tweets.log 2>>logs/enviar_tweets.err.log;


