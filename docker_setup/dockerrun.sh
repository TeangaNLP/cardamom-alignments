#!/bin/bash
docker run -it\
	   -v $(PWD)/run_configs:/app/run_configs/\
	   -v $(PWD)/pipelines:/app/pipelines/\
	   cardamom-alignments bash
