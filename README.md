# AIRCADE
Anechoic and IR Convolution-based Auralization Data Compilation Ensemble

[AIRCADE](https://zenodo.org/record/7818761#.ZDrig3bMJPZ) is a data-compilation ensemble of anechoic [speech and song samples](https://zenodo.org/record/1188976#.ZDrm6HbMJPY), together with [acoustic guitar sounds](https://zenodo.org/record/3371780#.YcCtvmjMJPY), with original annotations pertinent to emotion recognition and Music Information Retrieval (MIR). Moreover, it includes a selection of [impulse response (IR) samples](https://www.openair.hosted.york.ac.uk/) with varying RT values, providing a wide range of reverberation conditions for evaluation. It is primarily intended to serve as a resource for researchers in the field of dereverberation, particularly for data-driven approaches.

This data-compilation can be used together with [Python scripts](https://github.com/TulioChiodi/AIRCADE/tree/main/src), for generating auralized data ensembles in different sizes: *tiny*, *small*, *medium* and *large*.  **NOTICE**: the *large* version will require **200 GB** of free space, approximately.

Additionally, the provided metadata also allows for further analysis and investigation of the performance of dereverberation algorithms under different conditions. All data is licensed under [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

## Usage

### Configuring the environment
---
Create conda environment by running the following command:
```shell
conda create --name AIRCADE python=3.9
```
Activate the new environment by running the following command:
```shell
conda activate AIRCADE
```
Clone this repo by running the following command:
```shell
git clone git@github.com:TulioChiodi/AIRCADE.git
```
*obs.: use https clone if your SSH key is not configured.*


cd into the project by running the following command:
```shell
cd AIRCADE
```
Install the requirements from the requirements.txt file by running the following command:
```shell
pip install -r requirements.txt
```
---
### Preparing base dataset:
Run the script using the following command in the terminal:
```shell
python src/prepare_base_dataset.py
```
---
### Running the script:
Run the script using the following structure:
```shell
python src/dataset_generator.py [-i <input-dir>] [-o <output-dir>] [-rc <rir-configs-path>] [-ac <anec-configs-path>] [-ps <preset-size>] [-p <processes>] [-s]
```

### The following arguments are optional:

- **`-i`**, **`--input-dir`**: Directory path for the base dataset. Default is **``data/dataset_base``**.
- **`-o`**, **`--output-dir`**: Directory path for the processed dataset. Default is **``data/dataset_processed``**.
- **`-rc`**, **`--rir-configs-path`**: Path to the json file containing the RIR configurations. Default is **``configs/rir_configs.json``**.
- **`-ac`**, **`--anec-configs-path`**: Path to the json file containing the anechoic configurations. Default is **``configs/anec_configs.json``**.
- **`-ps`**, **`--preset-size`**: Size of the dataset. Default is **``tiny``**. Choose between (tiny, small, medium, large).
- **`-p`**, **`--processes`**: Number of parallel processes to use. Default is the number of CPUs available on the system.
- **`-s`**, **`--sequential`**: Use sequential processing. Default is using multiprocessing.

### Example usage:


```shell
python src/dataset_generator.py -i /path/to/input/directory -o /path/to/output/directory -ps small -p 4

```

---
## Acknowledgement:
This work was partially supported by the [São Paulo Research Foundation (FAPESP)](https://fapesp.br/), grants #2017/08120-6 and #2019/22795-1.
