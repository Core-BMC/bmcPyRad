# BMC-PyRad

[한국어](#kr) | [English](#en)

---

##### <a name="#kr">KR</a>

`BMC-PyRad`는 TMJ (Temporomandibular Joint) 관련 방사선 이미지를 처리하고, Pyradiomics를 통해 방사선학적 특징을 추출하는 프로젝트입니다.

## 요구 사항 
- Python 3.11
- Pyradiomics 3.10
- tqdm

## Python 3.11.9 빠른 설치

다음 명령어를 터미널에서 실행하여 Python 3.11.9을 설치할 수 있습니다.

### Step 1: ActiveState CLI 설치

```bash
curl -fsSL https://platform.activestate.com/dl/cli/_pdli02/install.sh | sh
```

### Step 2: 런타임 다운로드

```bash
state checkout bmc-lab/Python-3.11.9-Linux-Ubuntu .
```

이 명령어는 `activestate.yaml` 파일을 현재 작업 디렉토리에 추가합니다.

### Step 3: 런타임 사용 시작

```bash
state use Python-3.11.9-Linux-Ubuntu
```

이 명령어는 시스템 전역에서 사용할 수 있도록 Python 런타임을 설정합니다. 기본 설정을 제거하려면 `state use reset` 명령어를 사용합니다.

## 프로젝트 클론

```bash
git clone https://github.com/Core-BMC/bmcPyRad
cd bmcPyRad
```

## 가상환경 설정 및 활성화

```bash
python -m venv .bmcPyRad
source .bmcPyRad/bin/activate
pip install -r requirements.txt
```

## Pyradiomics v3.10 설치 (GitHub에서 설치)

```bash
git clone git://github.com/Radiomics/pyradiomics
pip install -r pyradiomics/requirements.txt
python pyradiomics/setup.py install
```

## 프로젝트 사용 방법

### Step 1: 분석할 데이터를 준비합니다.

분석할 데이터는 두 개의 폴더(`./Control`, `./TMJOA`)에 저장되어 있어야 합니다. 각각의 폴더 내에 방사선 이미지 파일과 마스크 파일이 포함되어 있어야 합니다.

### Step 2: 스크립트 실행

스크립트는 두 개의 폴더에 대해 방사선학적 특징을 추출하고 각각의 CSV 파일로 결과를 저장합니다.

```bash
#!/bin/bash

# Set the folder paths and n value
FOLDER_PATHS=("./Control" "./TMJOA")
N=34
OUTPUT_FILES=("output_features_Control.csv" "output_features_TMJOA.csv")

# Loop through each folder path and corresponding output file
for i in "${!FOLDER_PATHS[@]}"; do
    FOLDER_PATH=${FOLDER_PATHS[$i]}
    OUTPUT_FILE=${OUTPUT_FILES[$i]}
    
    echo "Processing folder: $FOLDER_PATH"

    # Run the Python script with the specified parameters
    python -c "
import os
from PyRadiomicsPrep_bmc import RadiomicsPreparation

# Initialize the class with the folder path and n value
radiomics_prep = RadiomicsPreparation('$FOLDER_PATH', $N)

# Prepare the input file
radiomics_prep.prepare_input_file()

# Run Pyradiomics
radiomics_prep.run_pyradiomics('$OUTPUT_FILE')
"
done
```

이 스크립트를 실행하면, 각 폴더에 있는 방사선 이미지와 마스크 파일을 기반으로 `output_features_Control.csv`와 `output_features_TMJOA.csv` 파일이 생성됩니다.

### Step 3: Pyradiomics를 통한 특징 추출

위 스크립트는 `pyradiomics` 명령어를 실행하여 각 폴더의 데이터를 분석한 결과를 CSV 파일로 출력합니다. 결과 파일들은 설정된 `output_features_Control.csv` 및 `output_features_TMJOA.csv`에 저장됩니다.

## 참고 사항

- `tqdm` 라이브러리는 방사선 이미지 처리의 진행 상황을 보여줍니다. 이 라이브러리가 설치되지 않았다면, `pip install tqdm` 명령어로 설치할 수 있습니다.
- Pyradiomics의 요구 사항을 충족하려면, Python 3.11 환경에서 제대로 설치되었는지 확인하세요.

---

##### <a name="#en">EN</a>

`BMC-PyRad` is a project for processing TMJ (Temporomandibular Joint) radiological images and extracting radiomic features using Pyradiomics.

## Requirements 
- Python 3.11
- Pyradiomics 3.10
- tqdm

## Quick Installation of Python 3.11.9

Run the following commands in your terminal to install Python 3.11.9.

### Step 1: Install ActiveState CLI

```bash
curl -fsSL https://platform.activestate.com/dl/cli/_pdli02/install.sh | sh
```

### Step 2: Download the runtime

```bash
state checkout bmc-lab/Python-3.11.9-Linux-Ubuntu .
```

This command adds an `activestate.yaml` file into your current working directory.

### Step 3: Start using the runtime

```bash
state use Python-3.11.9-Linux-Ubuntu
```

This command sets the Python runtime system-wide. To unset it, use the `state use reset` command.

## Clone this repository

```bash
git clone https://github.com/Core-BMC/bmcPyRad
cd bmcPyRad
```

## Create and activate virtual environment

```bash
python -m venv .bmcPyRad
source .bmcPyRad/bin/activate
pip install -r requirements.txt
```

## Install Pyradiomics v3.10 (from GitHub)

```bash
git clone git://github.com/Radiomics/pyradiomics
pip install -r pyradiomics/requirements.txt
python pyradiomics/setup.py install
```

## How to use the project

### Step 1: Prepare the data for analysis

The data to be analyzed must be stored in two folders: `./Control` and `./TMJOA`. Each folder should contain radiological image files and corresponding mask files.

### Step 2: Run the script

The script extracts radiomic features from the data in the two folders and saves the results as CSV files.

```bash
#!/bin/bash

# Set the folder paths and n value
FOLDER_PATHS=("./Control" "./TMJOA")
N=34
OUTPUT_FILES=("output_features_Control.csv" "output_features_TMJOA.csv")

# Loop through each folder path and corresponding output file
for i in "${!FOLDER_PATHS[@]}"; do
    FOLDER_PATH=${FOLDER_PATHS[$i]}
    OUTPUT_FILE=${OUTPUT_FILES[$i]}
    
    echo "Processing folder: $FOLDER_PATH"

    # Run the Python script with the specified parameters
    python -c "
import os
from PyRadiomicsPrep_bmc import RadiomicsPreparation

# Initialize the class with the folder path and n value
radiomics_prep = RadiomicsPreparation('$FOLDER_PATH', $N)

# Prepare the input file
radiomics_prep.prepare_input_file()

# Run Pyradiomics
radiomics_prep.run_pyradiomics('$OUTPUT_FILE')
"
done
```

After running this script, `output_features_Control.csv` and `output_features_TMJOA.csv` will be generated based on the image and mask files in each folder.

### Step 3: Extract radiomic features using Pyradiomics

The script uses the `pyradiomics` command to analyze the data in each folder and output the results as CSV files. The output files are stored as `output_features_Control.csv` and `output_features_TMJOA.csv`.

## Notes

- The `tqdm` library provides progress bars for the image processing. If it's not installed, run `pip install tqdm` to install it.
- Make sure Python 3.11 is properly installed to meet Pyradiomics' requirements.
