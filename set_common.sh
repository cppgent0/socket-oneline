#! /usr/bin/env bash
OVERALLRC=0
# should be overridden
tag=''

cmn_mod_name=socket_oneline

# --------------------
# push log lines to outfile
function cmn_tee() {
  tee -a "${OUTFILE}"
}

# --------------------
function cmn_check_rc() {
  RC=${PIPESTATUS[0]}
  OVERALLRC=$((OVERALLRC + RC))
  printf "%-4s %s\n" " " "$1 rc=$RC" | cmn_tee
}

# --------------------
# set the python environment and activate
function cmn_activate_env() {
  source set_env.sh
  source "${pybin}/activate"
}

# --------------------
# setup the out directory
function cmn_setup_outdir() {
  CW_DIR="$(pwd)"
  OUT_DIR="${CW_DIR}/out"
  mkdir -p "${OUT_DIR}"
}

# --------------------
# initialize the output file
function cmn_setup_outfile() {
  OUTFILE="${OUT_DIR}/${cmn_mod_name}.txt"
  echo | tee "${OUTFILE}"
}

# --------------------
# clean up the out/* directories
function cmn_clean_out() {
  rm -rf out/$1
  mkdir -p out/$1
}

# --------------------
# clean up the coverage related files
function cmn_clean_coverage() {
  cmn_clean_out coverage
  rm -f .coverage
}

# --------------------
# clean up common directories and files
function cmn_clean_out_common() {
  cmn_clean_out doc
  cmn_clean_out ver
  cmn_clean_coverage
}

# --------------------
# clean directories and files for publishing
function cmn_clean_publish() {
  rm -rf dist
  rm -rf out
  rm -rf .pytest_cache
  rm -rf ${cmd_mod_name}.egg-info/
}

# --------------------
# log the overall rc
function cmn_log_overall() {
  printf "%-4s %s\n" "" "$1 overall rc=$OVERALLRC" | cmn_tee
}

# --------------------
# log start message
function cmn_log_start() {
  printf "%-4s %s\n" "====" "${tag} $1" | cmn_tee
}

# --------------------
# run doxygen
function cmn_run_doxygen() {
  doxygen

  # generate pdf
  pushd out/doc/latex
  make
  cmn_check_rc make

  cp refman.pdf "../../${cmn_mod_name}.pdf"
  popd

  # sort the output file
  sort -o out/doxygen.txt{,}
}

# --------------------
# setup all main parts
function cmn_main_setup() {
  cmn_activate_env
  cmn_setup_outdir
  cmn_setup_outfile
}

# --------------------
# run basic setup
function cmn_run_setup() {
  export PYTHONPATH=${PYTHONPATH}:.
  cmn_clean_out_common
}

# --------------------
# set the common coverage options
function cmn_set_coverage_opts() {
  # --cov-report=  : no std out
  # --cov-branch   : gather branch data
  # --cov-config=setup.cfg   : use the given cfg file
  # --cov-append   : append to the coverage data
  COV_OPTS="--cov-report= --cov-branch --cov-config=setup.cfg --cov-append"
}

# --------------------
# run the coverage for the named includes
function cmn_run_coverage() {
  cmn_log_start 'run coverage report'
  coverage html --rcfile setup.cfg >>"${OUTFILE}"
  cmn_check_rc 'coverage'
}
