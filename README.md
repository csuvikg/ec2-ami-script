# Requirements
* Python3.9+

# Instructions for Unix

## Installation
* python3 -m venv venv
* . venv/bin/activate
* pip3 install -r requirements.txt

## Running the script
* python3 collect_amis.py

## Comments
* The project has type hinting to help with maintainability. MyPy was used to enforce typing
* The script relies on the generator functions provided by boto3 (eg. the resource API) for optimized batch requests
* There is a retry and filtering mechanism to help with nonexistent AMIs. Since the retry does not continue the iteration - in favor of batched requests -, it might perform poorly in some cases (eg. many instances, with evenly distributed nonexistent AMIs). This decision was made to favor cases where there are no nonexistent AMIs. The solution should be very performant in those cases, with optimized batch requests
* Testing proved that not all AMIs have all the necessary properties, so I made all nullable
