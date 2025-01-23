# Planning task

This is my solution for BI-ZUM planning task. :star:

## Running

Run in the needed directory executing this:

`../fast-downward.py domain.pddl task.pddl --search "astar(lmcut())"`

if you have Fast-Downward installed in the directory right above the task one.

## Directories

Every directory contains the output plan for the given task. Here is the list of them:

 - *original*

Contains an original solution for the task.

 - *additional_1*

Contains the domain and the instance files for the modified task, where there isn't any path between the city and the academy.

 - *additional_2*

Contains the domain and the instance files for the modified task, where the wizard won't give us the map.

 - *additional_3*

Contains the domain and the instance files for the modified task, where we won't be able to find any pearl in the sea.

 - *additional_4*

Contains the domain and the instance files for the modified task, where there won't be any boat at the river to steal.

 - *test*

Contains the domain and the instance files for the testing purposes, where the marriage and the admiral endings cannot be achieved (this is just a combination of *additional_1* and *additional_3* tasks).
