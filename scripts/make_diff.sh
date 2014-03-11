#!/usr/bin/env bash

TESTFOLDER=$( python scripts/make_diff.py | grep merge-diff-testfolder );
cd $TESTFOLDER
nbdiff --check
