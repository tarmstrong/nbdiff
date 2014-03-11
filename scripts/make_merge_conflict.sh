#!/usr/bin/env bash

TESTFOLDER=$( python scripts/make_merge_conflict.py | grep merge-conflict-testfolder );
cd $TESTFOLDER
nbmerge --check
