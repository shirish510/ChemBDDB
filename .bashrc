# .bashrc

# User specific aliases and functions

# Source global definitions
  
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/projects/academic/hachmann/packages/Anaconda_May16:/projects/academic/hachmann/packages/rdkit-Release_2015_03_1
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/projects/academic/hachmann/shirish/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/projects/academic/hachmann/shirish/apr-util/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/projects/academic/hachmann/shirish/apr/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/projects/academic/hachmann/shirish/python/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/projects/academic/hachmann/shirish/apache/modules
export PATH="$PATH:/projects/academic/hachmann/shirish/apache/bin"
export HADOOP_HOME=$HADOOP_HOME:/projects/academic/hachmann/shirish/hadoop

if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi
alias mydir='cd ../../projects/academic/hachmann/shirish'
alias mysql='cd ../../projects/academic/hachmann/shirish/MySQL'
alias py='cd ../../projects/academic/hachmann/shirish/python'
alias ap='cd ../../projects/academic/hachmann/shirish/apache'

# added by Anaconda2 installer
export PATH="$PATH:/projects/academic/hachmann/shirish/python/bin"
export PATH="$PATH:/projects/academic/hachmann/shirish/apr/bin"
export PATH="$PATH:/projects/academic/hachmann/shirish/cmake-3.11.0/bin"
export MYSQL="/projects/academic/hachmann/shirish/MySQL/bin:$MYSQL"
export PATH="$PATH:$HADOOP_HOME/bin"

