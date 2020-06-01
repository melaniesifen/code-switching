.PHONY:

FILES :=			\
    cs.html			\
    cs.log			\
    language_detecting.py	\
    text_class.py		\
    RunAnalysis.py  		\
    results.py

#

ifeq ($(shell uname), Darwin)          # Apple	
    PYTHON   := python3
    PIP      := pip3
    PYLINT   := pylint
    COVERAGE := coverage
    PYDOC    := pydoc3
    AUTOPEP8 := autopep8
else ifeq ($(shell uname -p), unknown) # Windows
    PYTHON   := python                 
    PIP      := pip3
    PYLINT   := pylint
    COVERAGE := coverage
    PYDOC    := python -m pydoc        
    AUTOPEP8 := autopep8
else                                   
    PYTHON   := python3
    PIP      := pip3
    PYLINT   := pylint3
    COVERAGE := coverage
    PYDOC    := pydoc3
    AUTOPEP8 := autopep8
endif



cs.html: language_detecting.py
	$(PYDOC) -w language_detecting

cs.log:
	git log > cs.log

clean:
	rm -f  .coverage
	rm -f  *.pyc
	rm -rf __pycache__
	rm -f results.txt

config:
	git config -l

format:
	$(AUTOPEP8) -i language_detecting.py
	$(AUTOPEP8) -i RunAnalysis.py

scrub:
	make clean
	rm -f  cs.html
	rm -f  cs.log

status:
	make clean
	@echo
	git branch
	git remote -v
	git status

versions:
	which       $(AUTOPEP8)
	$(AUTOPEP8) --version
	@echo
	which       $(COVERAGE)
	$(COVERAGE) --version
	@echo
	which       git
	git         --version
	@echo
	which       make
	make        --version
	@echo
	which       $(PIP)
	$(PIP)      --version
	@echo
	which       $(PYLINT)
	$(PYLINT)   --version
	@echo
	which        $(PYTHON)
	$(PYTHON)    --version

test: cs.html cs.log



