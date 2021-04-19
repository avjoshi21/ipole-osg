# ipole-osg

A simple setup for running a large number of `ipole` jobs on the Open
Science Grid (OSG) using HTCondor.

## Usage

This git repository is designed to be cloned to OSG connect as a run
directory for both submitting a large OSG job and gathering the
output.
To start,

    ssh osg
	cd /public/<user>/
    git clone git@github.com:bhpire/ipole-osg.git run-01
	cd run-01

All the scripts are placed inside `bin/`.
The empty directories `dat/`, `log/`, and `out/` will be used to stage
GRMHD data (as input to `ipole`), OSG run logs, and `ipole` output.

Before submitting a job, one needs to copy a static linked `ipole`
binary to `bin/` and populate `dat/` with GRMHD data.

    cp ~/src/ipole/ipole bin
    scp bh:sim-lib/sample/dump_*.h5 dat

Edit to `bin/pargen` may be made to generate the necessary parameter
sets.
Then, simply submit an OSG job by

    bin/submit

`bin/submit` is a standard Condor submission script starts with a
hashbang directive to use the system `condor_submit`.
It uses `bin/pargen` to generate a list of parameter sets based on all
the GRMHD input data in `dat/` and the parameter listed inside
`bin/pargen`.
These parameter sets are then passed to `bin/wrapper` on the worker
machines as command line arguments.
`bin/wrapper` will automatically generate a `ipole` parameter file
based on the arguments, and start `ipole` with it.

All Condor logs, `stdout`, and `stderr` will be sent to `log/`.
The parameter files and spectrum output will be saved to `out/`.
Their file names are transform according to the rules described in
`bin/submit`.
