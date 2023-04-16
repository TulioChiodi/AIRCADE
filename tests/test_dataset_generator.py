import src.utils as utils
import pandas as pd

def test_filter_dataframe():
    dataframe = utils.generate_dataframe('data/dataset_raw')
    
    rirs_00 = pd.Series({
        "filenames" : [
            "rir_0001.wav",
            "rir_0002.wav",
            "rir_0064.wav",
            ]
        })

    anecs_00 = pd.Series({
        "guitar": 2,
        "song": 2,
        "speech": 2
    })

    rirs_01 = pd.Series({
        "filenames" : 'all'
        })

    anecs_01 = pd.Series({
        "guitar": 'all',
        "song": 'all',
        "speech": 'all'
    })

    filtered_dataframe_00 = utils.filter_dataframe(dataframe, rirs_00, anecs_00)
    filtered_dataframe_01 = utils.filter_dataframe(dataframe, rirs_01, anecs_01)

    assert len(filtered_dataframe_00) == 9
    assert len(filtered_dataframe_01) == 4_725
