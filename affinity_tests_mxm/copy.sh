export OUT_DIR=./outputs/output_20210718_105255
export CUR_DATE_STR=20210718_105255
export VARIATION_DIR=${OUT_DIR}"/logs/cham_no_affinity"
find "${OUT_DIR}/../" -maxdepth 1 -iname "*${CUR_DATE_STR}" -type d -exec cp -r -n -- ${OUT_DIR}/logs '{}' ';'