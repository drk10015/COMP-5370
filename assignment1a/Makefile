# Target run when the shell command `make build` is run.
# There is nothing to build for Python so simply exit successfully.
build:
	@exit 0

# Target run when the shell command `make run FILE=XXXX` is run.
# The input file path is passed as the `XXXX` portion of the argument to make
# and is relayed to the Python script as it's first and only command line
# argument.
run:
	@python3 main.py -f $(FILE)
