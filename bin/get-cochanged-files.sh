# get-cochanged-files
# 
# Description: 
#     This uses git and a python script to parse through the commits and changed files to return 
#     an output of the most commonly changed files
# 
# Arguments:
#     (1) - arguments to pass to "git rev-list" (example: "--until=11/01/2017")
#     (2) - arguments to pass to "git diff-tree" (example: "| grep -P \"([0-9a-f]{40})|(.java)\" | grep -v Test")
#     (3) - arguments to pass to "parse_cochanged_files.py" (example: "2 3") 
#
dir_bin=$(dirname ${0})
dir_src=$(readlink -f ${dir_bin}/../src)

rev_args=${1}
diff_args=${2}
parse_args=${3}
command="git rev-list --all ${rev_args} | git diff-tree -r --name-only --stdin ${diff_args} | ${dir_src}/parse_cochanged_files.py ${parse_args}"
echo "${command}"
eval "${command}"