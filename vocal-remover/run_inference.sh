#!/bin/bash

# 引数の解析
while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        --input)
        INPUT_PATH="$2"
        shift
        shift
        ;;
        *)
        echo "Unknown option: $1"
        exit 1
        ;;
    esac
done

# INPUT_PATHが指定されているか確認
if [ -z "$INPUT_PATH" ]; then
    echo "Usage: $0 --input path"
    exit 1
fi

# 除外ファイルのリスト
EXCLUDE_FILES=("audio.mp3 Chessboard.mp3 SOULSOUP.mp3")

# INPUT_PATH内のファイルのループ
for file in "$INPUT_PATH"/*.mp3; do
    filename=$(basename -- "$file")
    if [[ ! " ${EXCLUDE_FILES[@]} " =~ " ${filename} " ]]; then
        # 除外ファイルでなければPythonスクリプトを実行
        python interference.py --input "$file"
    fi
done
