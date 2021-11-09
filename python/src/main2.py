import os

import numpy as np
import matplotlib as plt

import run_path_tools as rpt
import ptc_tools as ptc
from settings import Settings


SRC_LOC = r"C:\Users\vidar\OneDrive - University of Bristol\Documents\Uni_2021_2022\MAPS_experiment\code\python\src"
QTE = "Press <q> to exit program"
ETS = "Press <enter> to skip"


if __name__=="__main__":
# Set working directory to src, exit program if failed
    if os.getcwd() != SRC_LOC:
        try:
            os.chdir(SRC_LOC)
        except:
            raise ImportError("Could not find src directory at \"{}\""\
                    .format(SRC_LOC))
# Intial setup:
    prog_data = rpt.Prog_data()
    settings = Settings(SRC_LOC)
    settings.check()
    settings.src_path = SRC_LOC
    # Decide whether to load in previous offset and dark noise
    while True:
        print("Load default settings (y/n)?")
        print(QTE)
        load = input().strip()
        if load == "y":
            settings.load_default()
            break
        elif load == "n":
            break
        elif load == "":
            exit()
        else:
            print("Error: did not recognise input please try again\n")
    
# Main program:
    while True:
        print("--------------------------------------------------------")
        prog_data.print_saved_all()
        print("Press <1> to load new run")
        print("Press <2> to load PT curve")
        print("Press <3> to remove a loaded run")
        print("Press <4> to remove a loaded PT curve")
        print("Press <5> to analyse a loaded run")
        print("Press <6> to analyse loaded PT curve")
        print("Press <7> to update settings")
        print(QTE)
        func_choice = input()
        print("\n")
        if func_choice == "1":
        # Load new run
            print("Please enter one of the following:")
            print("The path to a single dataset run")
            print("The path to a run directory containing multiple datasets")
            print(ETS)
            run_path = input()
            if run_path == "":
                continue
            elif os.path.isfile(run_path) == True:
                print("Recieved path to a single dataset\n")
                run_name = prog_data.new_run_name(prog_data)
                prog_data.saved_runs[run_name] = rpt.get_single_run(\
                    name=run_name, filepath=run_path,\
                    start_frame=settings.start_frame)
                print("Run \"{}\" successfully created".format(run_name))
            elif os.path.isdir(run_path) == True:
                print("Recived path to run directory\n")
                run_name = prog_data.new_run_name()
                prog_data.saved_runs[run_name] = rpt.get_multi_run(\
                    dirpath=run_path, start_frame=settings.start_frame)
                print("Run \"{}\" successfully created".format(run_name))
            else:
                print("Error: the path \"{}\" was not recognised, aborting!\n"\
                    .format(run_path))
                print("\n")
                continue

        elif func_choice == "2":
        # Load new PT curve
            # Check that there exists and offset, and dark (read) noise
            if type(settings.offset) != np.ndarray:
                print("Error: no offset loaded,", end=" ")
                print("please update settings first, aborting!")
            if type(settings.dark_noise) != np.ndarray:
                print("Error: no dark noise loaded,", end=" ")
                print("please update setting first, aborting!")
            # Check that there exists at least one loaded run
            if len(prog_data.saved_runs) == 0:
                print("Error: 0 runs loaded.", end=" ")
                print("PT curve requires at least 1 loaded run, aborting!")
                continue
            run_name = prog_data.get_run_name()
            if run_name == None:
                continue
            ptc_name = prog_data.new_ptc_name()
            if prog_data.check_ptc_req(run_name) == False:
                continue
            while True:
                print("Sort each pixel against mean signal (y/n)?")
                sorting = input()
                if sorting.strip() == "y":
                    sorting = True
                    break
                elif sorting.strip() == "n":
                    sorting = False
                    break
                else:
                    print("Error did not understand input, please try again")
                    continue
            prog_data.saved_ptc[ptc_name] = ptc.get_ptc(\
                prog_data.saved_runs[run_name], settings.offset,\
                settings.dark_noise, settings.resolution,\
                sort=sorting)

        elif func_choice == "3":
        # Remove loaded run
            prog_data.print_saved_runs()
            print("Please choose run to delete")
            run_name = input()
            prog_data.del_run(run_name)
            continue

        elif func_choice == "4":
        # Remove loaded PT curve
            prog_data.print_saved_ptc()
            print("Please choose PT curve to delete")
            ptc_name = input()
            prog_data.del_ptc(ptc_name)
            pass
        
        elif func_choice == "5":
        # Analyse 
            print("Please choose one of the following options:")
            print("<1> determine mean signal for single dataset run")
            print("<2> determine std. dev. for single dataset run")
            print("<3> create graphs over a single dataset")
            print("<4> Peason's cumulative test against model functions")
            print(ETS)
            analyse_choice = input()
            if analyse_choice == "1":
                # mean signal from single dataset
                pass

            elif analyse_choice == "2":
                # std. dev. from single dataset
                pass

            elif analyse_choice == "3":
                # create graphs over a single dataset
                pass

            elif analyse_choice == "4":
                # Peason's test
                pass
            
            elif analyse_choice == "":
                # back to main menu
                continue
            
            else:
                print("Error: input \"{}\" not recognised, aborting!"\
                    .format(analyse_choice))

            # Choice of what actions to perform on current datasets
            # - Get mean
            # - Get offset
            # - Graph a single pixel over a single dataset
            # - Test fit of a pixel
            # - Create PTC curve
                # - Plot differnt values
                # - need to be able to delete ptc obect (save space)

        elif func_choice == "6":
        # Analysis of loaded PT curve
            ptc_name = prog_data.get_ptc_name()
            ptc.graph_ptc(prog_data.saved_ptc[ptc_name])
            # Ask user for a valid PT curve by name
            # Checks if it exists
            # if it exists pass PT curve to graph_PTC
            pass

        elif func_choice == "7":
            pass
            # Change settings
            # Pedestal and dark values

        elif func_choice == "q":
            exit()
        
        else:
            print("Error: input \"{}{}\" was not recognised, please try again\n"\
                .format(func_choice, r"\n"))
        
    # ask to load a new dataset (create new run object)
    # ask to create multiple datasets
    #     this will only load the dataset, not calc any values!!!
    # ask what to do aftewards