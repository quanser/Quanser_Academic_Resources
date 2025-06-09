# generate_breakout_script.awk
#
# USAGE:
#
# nawk -f generate_breakout_script.nawk data_def.csv > parse_vars.m
#
# Parse the stored data definition (data_def.csv) file and generate a matlab script for the breakout mapping.
#
BEGIN {
    FS = ",";
    ORS = "\n\n";
    VARIABLE_NAME = "input_data";
    SIGNAL_COUNTER = 1;

    # Start printing the file header
    printf "%%%% Auto-generated script file for parsing the stored variables\n";
    printf "%%\n";
    printf "function parse_vars( %s )\n", VARIABLE_NAME;
    printf "%%\n";
    printf "\n";
}
/^#/{ 
    # Current line is comment, skip and ignore
    next;
}
NF >= 3 {
    # Comment available
    printf "\t%%%% ";
    if (NF == 3) {
        printf "%s", $3;
    }
    else {
        for( i=3; i < NF; i++){
            printf "%s,", $i;
        }
        printf "%s", $NF
    }
    printf "\n";
}
{
    # Print the assignment statement
    if ($2 > 1) {
        printf "\tassignin('base','%s',%s(%s:%s,:));\n", $1, VARIABLE_NAME, SIGNAL_COUNTER, SIGNAL_COUNTER+$2-1;
#        print $1 " = " VARIABLE_NAME "(" SIGNAL_COUNTER ":" SIGNAL_COUNTER+$2-1 ",:);";
        SIGNAL_COUNTER += $2; 
    }
    else {
        printf "\tassignin('base','%s',%s(%s,:));\n", $1, VARIABLE_NAME, SIGNAL_COUNTER++;
#        print $1 " = " VARIABLE_NAME "(" SIGNAL_COUNTER++ ",:);";
    }
    printf "\n";
}
END {
    # Print file footer
    printf "\n";
    printf "end\n";
}
