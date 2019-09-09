# TODO

<big>Mark a task as "done" be replacing the space between [ ] with an x as demonstrated below</big>

- [ ] This is an uncompleted task

- [x] This is a completed task

---

## LaTeX Paper

<big>Taken from the assignment writeup, verbatim

1. [x] Title and Author name(s)

2. [ ] A brief, one paragraph abstract summarizing the results of the experiments

3. [ ] Problem statement, including hypothesis

4. [ ] Description of algorithms implemented

5. [ ] Description of your experimental approach

6. [ ] Presentation of the results of your experiments (in words, tables, and graphs)

7. [ ] A discussion of the behavior of your algorithms, combined with any conclusions you can draw

8. [ ] Summary

9. [ ] References

    - You should have at least one reference related to the algorithms implemented since you will know what it is by the time the assignment is due. You should also include a reference to the data sources, and any other references you consider to be relevant. You may not reference websites except for the data sets.

## Dana

- [x] Make a LaTeX outline

    - Site algorithms as used

## Troy

- [ ] Begin respective algorithm

## George
- [x] User input for selecting database to use
- [x] Clean Database of missing attributes
    -use bootstrapping esc method of selecting missing attributes from normal rows with no missing atributes.
- [ ] Split Database into `training` sets and `prediction check` sets.
    - Can just take a single .data file, and partition it into a `training set` and a `validation set`.

## Henry

- [ ] Step 2

- [ ] Step 3

## Anyone:
- [ ] Implement K-fold cross validation
    - [ ] determine bin size by dividing by k and rounding down. (10 arbitrarily chosen for this assignment) 
    - [ ] split data up into bins
    - [ ] Keep one bin as a testing bin, use the others for training
    - [ ] run k (10) learning experiments 
    - [ ] Average test results from k learning experiments as our algorithms accuracy
    - [ ] return learning experiments test set & training set with the best accuracy.