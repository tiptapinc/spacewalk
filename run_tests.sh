#!/bin/sh

pytest tests --cov=spacewalk --cov-report term-missing --cov-config=.coveragerc
