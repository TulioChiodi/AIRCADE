import itertools
from multiprocessing import Pool
import os
from pathlib import Path
from typing import Union, Tuple, List

import librosa
import numpy as np
import pandas as pd
import soundfile as sf


def read_paths(dirpath: Union[str, Path]) -> pd.DataFrame:
    """Generate a pandas dataframe from the dataset dirpath.
    :param dirpath: Directory path of the dataset.
    :type dirpath: Path
    :return: Dataframe containing the dataset filepaths.
    :rtype: pd.DataFrame
    """
    # Get the list of filepaths and durations.
    filepaths = sorted(Path(dirpath).glob('**/*.wav'))

    # Generate a dataframe from the dataset.
    dataframe = pd.DataFrame({'filepaths': filepaths})
    
    return dataframe


def process_data_filepaths(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Process the dataframe filepaths.
    :param dataframe: Dataframe containing the dataset filepaths.
    :type dataframe: pd.DataFrame
    :return: Dataframe containing the processed dataset filepaths.
    :rtype: pd.DataFrame
    """

    audio_type_mapping = {
        'guitar': 'anechoic', 
        'song': 'anechoic', 
        'speech': 'anechoic', 
        'rir': 'impulse_response'
    }

    dataframe['filename'] = dataframe['filepaths'].apply(lambda x: x.name)
    dataframe['dirpath'] = dataframe['filepaths'].apply(lambda x: x.parent)
    dataframe['audio_event'] = dataframe['filepaths'].apply(lambda x: x.parent.name)
    dataframe['audio_type'] = dataframe['audio_event'].map(audio_type_mapping)

    return dataframe[['filename','dirpath', 'audio_event', 'audio_type']]


def split_audio_types(dataframe: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    """Split the dataframe in two dataframes, one for the impulse responses and one for the anechoic sounds.
    :param dataframe: Dataframe containing the dataset file informations.
    :type dataframe: pd.DataFrame
    :return: Dataframe containing the customized dataset filepaths.
    :rtype: Tuple[pd.DataFrame, pd.DataFrame]
    """
    # Get the list of filepaths and durations.

    def assemble_filepath(x):
        return x['dirpath'] / x['filename']

    impulse_responses = dataframe[dataframe['audio_type'] == 'impulse_response'][['filename', 'dirpath']].apply(assemble_filepath, axis=1).values
    anechoic_sounds = dataframe[dataframe['audio_type'] == 'anechoic'][['filename', 'dirpath']].apply(assemble_filepath, axis=1).values

    return (impulse_responses, anechoic_sounds)


def generate_cartesian_product(impulse_responses: Union[List, pd.Series], anechoic_sounds: Union[List, pd.Series]) -> List:
    """Generate the cartesian product of the impulse responses and the anechoic sounds.
    :param impulse_responses: List or pd.Series of impulse response posix paths.
    :type impulse_responses: Union[List[Path], pd.Series[Path]]
    :param anechoic_sounds: List or pd.Series of anechoic sounds posix paths.
    :type anechoic_sounds: Union[List[Path], pd.Series[Path]]
    :return: List of cartesian product of the impulse responses and the anechoic sounds.
    :rtype: List[Path]
    """
    # Generate the combinations.
    cartesian_products = list(itertools.product(impulse_responses, anechoic_sounds))

    return cartesian_products


def convolve_audio_pairs(audio_pair: Tuple) -> None:
    """Convolve the audio pair.
    :param audio_pair: Tuple containing the impulse response and the anechoic sound.
    :type audio_pair: Tuple[Path, Path]
    :return: None
    """
    # Unpack the audio pair.
    impulse_response, anechoic_sound = audio_pair

    # Generate the output path.
    output_filename = f'{anechoic_sound.stem}_{impulse_response.stem}.wav'
    output_dirpath = Path('data/dataset_processed')
    output_dirpath.mkdir(parents=True, exist_ok=True)
    output_filepath = output_dirpath / output_filename

    if not os.path.isfile(output_filepath):
        ir, sr_ir = librosa.load(impulse_response, sr=None)
        anechoic, sr_anechoic = librosa.load(anechoic_sound, sr=None)

        if sr_ir != sr_anechoic:
            print(f"Error: sample rates for {impulse_response} and {anechoic_sound} do not match.")

        ir_norm = ir / np.max(np.abs(ir))
        audio_norm = anechoic / np.max(np.abs(anechoic))        

        convolved_audio = np.convolve(audio_norm, ir_norm)
        convolved_audio_norm = convolved_audio / np.max(np.abs(convolved_audio))

        sf.write(output_filepath, convolved_audio_norm, sr_ir)


def convolve_sequential(cartesian_products: List) -> None:
    """Convolve the audio pairs sequentially.
    :param cartesian_products: List of cartesian product of the impulse responses and the anechoic sounds.
    :type cartesian_products: List[Path]
    :return: None
    """
    for audio_pair in cartesian_products:
        convolve_audio_pairs(audio_pair)


def convolve_parallel(cartesian_products: List) -> None:
    """Convolve the audio pairs in parallel.
    :param cartesian_products: List of cartesian product of the impulse responses and the anechoic sounds.
    :type cartesian_products: List[Path]
    :return: None
    """
    with Pool() as p:
        p.map(convolve_audio_pairs, cartesian_products)

def main():
    # Generate the csv file.
    df = read_paths('data/dataset_raw')
    df = process_data_filepaths(df)
    impulse_responses, anechoic_sounds = split_audio_types(df)
    cartesian_products = generate_cartesian_product(impulse_responses, anechoic_sounds)

    # Convolve the audio pairs.
    for audio_pair in cartesian_products:
        convolve_audio_pairs(audio_pair)


if __name__ == '__main__':
    main()
