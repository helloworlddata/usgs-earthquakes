WRANGLE_DIR=./wrangle
SCRIPTS_DIR=$(WRANGLE_DIR)/scripts
FETCHED_DIR=$(WRANGLE_DIR)/corral/fetched
COLLATED_DIR=$(WRANGLE_DIR)/corral/collated
DATA_DIR=./data

fetch:
	python wrangle/scripts/fetch_archives.py 1970-01 $(shell date +%Y-%m)

fetch_this_year:
	python wrangle/scripts/fetch_archives.py $(shell date +%Y-01) $(shell date +%Y-%m)


package:
	mkdir -p $(DATA_DIR)
	cp $(COLLATED_DIR)/contiguous-united-states.csv $(DATA_DIR)/usgs-earthquakes-contiguous-united-states.csv
	cp $(COLLATED_DIR)/decade-1980.csv $(DATA_DIR)/usgs-earthquakes-decade-1980.csv
	cp $(COLLATED_DIR)/decade-1990.csv $(DATA_DIR)/usgs-earthquakes-decade-1990.csv
	cp $(COLLATED_DIR)/decade-2000.csv $(DATA_DIR)/usgs-earthquakes-decade-2000.csv
	cp $(COLLATED_DIR)/decade-2010.csv $(DATA_DIR)/usgs-earthquakes-decade-2010.csv


collate_usa: $(COLLATED_DIR)/contiguous-united-states.csv

$(COLLATED_DIR)/contiguous-united-states.csv:
	python $(SCRIPTS_DIR)/collate_contiguous_us.py > $(COLLATED_DIR)/contiguous-united-states.csv

collate_decades: $(COLLATED_DIR)/decade-1970.csv\
	$(COLLATED_DIR)/decade-1980.csv\
	$(COLLATED_DIR)/decade-1990.csv\
	$(COLLATED_DIR)/decade-2000.csv\
	$(COLLATED_DIR)/decade-2010.csv


$(COLLATED_DIR)/decade-1970.csv:
	python $(SCRIPTS_DIR)/collate_decade.py 1970 > $(COLLATED_DIR)/decade-1970.csv
$(COLLATED_DIR)/decade-1980.csv:
	python $(SCRIPTS_DIR)/collate_decade.py 1980 > $(COLLATED_DIR)/decade-1980.csv
$(COLLATED_DIR)/decade-1990.csv:
	python $(SCRIPTS_DIR)/collate_decade.py 1990 > $(COLLATED_DIR)/decade-1990.csv
$(COLLATED_DIR)/decade-2000.csv:
	python $(SCRIPTS_DIR)/collate_decade.py 2000 > $(COLLATED_DIR)/decade-2000.csv
$(COLLATED_DIR)/decade-2010.csv:
	python $(SCRIPTS_DIR)/collate_decade.py 2010 > $(COLLATED_DIR)/decade-2010.csv

