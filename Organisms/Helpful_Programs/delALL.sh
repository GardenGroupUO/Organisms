#!/usr/bin/env bash
#
# Geoffrey Weal, delALL.sh, 10/02/2021
#
# This program is designed to remove all Organisms files that were made during the running of the program.
#
rm -rf GA_Run_Details.txt epoch_data epoch_data.backup ga_running.lock
rm -rf Population Recorded_Data Initial_Population Saved_Points_In_GA_Run Memory_Operator_Data Diversity_Information
rm -rf __pycache__
