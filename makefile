.PHONY:

FILES :=                              \
    cs.html                      \
    cs.log                       \
    language_detecting.py                        \
    RunAnalysis.in                     \
    RunAnalysis.out                    \
    RunAnalysis.py                     \
    TestAnalysis.out                   \
    TestAnalysis.py 
#

ifeq ($(shell uname), Darwin)          # Apple	
    PYTHON   := python3
    PIP      := pip3
    PYLINT   := pylint
    COVERAGE := coverage
    PYDOC    := pydoc3
    AUTOPEP8 := autopep8
else ifeq ($(shell uname -p), unknown) # Windows
    PYTHON   := python                 # on my machine it's python
    PIP      := pip3
    PYLINT   := pylint
    COVERAGE := coverage
    PYDOC    := python -m pydoc        # on my machine it's pydoc
    AUTOPEP8 := autopep8
else                                   # UTCS
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

RunAnalysis.tmp: RunAnalysis.in RunAnalysis.out RunAnalysis.py
	$(PYTHON) RunAnalysis.py < RunAnalysis.in > RunAnalysis.tmp
	diff --strip-trailing-cr RunAnalysis.tmp RunAnalysis.out

TestAnalysis.tmp: TestAnalysis.py
	$(COVERAGE) run    --branch TestAnalysis.py >  TestAnalysis.tmp 2>&1
	$(COVERAGE) report -m                      >> TestAnalysis.tmp
	cat TestAnalysis.tmp

check:
	@not_found=0;                                 \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
    echo "success";

clean:
	rm -f  .coverage
	rm -f  *.pyc
	rm -f  RunAnalysis.tmp
	rm -f  TestAnalysis.tmp
	rm -rf __pycache__

config:
	git config -l

format:
	$(AUTOPEP8) -i language_detecting.py
	$(AUTOPEP8) -i RunAnalysis.py
	$(AUTOPEP8) -i TestAnalysis.py

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

test: cs.html cs.log RunAnalysis.tmp TestAnalysis.tmp check

