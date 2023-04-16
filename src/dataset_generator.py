import argparse
import os
import utils


def get_arguments() -> argparse.Namespace:
    """
    Parse the command line arguments.
    :return: Parsed arguments.
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(description='Audio convolution script')

    parser.add_argument('-i', '--input-dir', type=str, default='data/dataset_base',
                        help='directory path for the base dataset')
    parser.add_argument('-o', '--output-dir', type=str, default='data/dataset_processed',
                        help='directory path for the processed dataset')
    parser.add_argument('-rc', '--rir-configs-path', type=str, default='configs/rir_configs.json',
                        help='path to the json file containing the rir configurations')
    parser.add_argument('-ac', '--anec-configs-path', type=str, default='configs/anec_configs.json',
                        help='path to the json file containing the anechoic configurations')
    parser.add_argument('-ps', '--preset-size', type=str, choices=['tiny', 'small', 'medium', 'large'], default='tiny', 
                        help='Size preset of the dataset choose between (tiny, small, medium, large))')
    parser.add_argument('-p', '--processes', type=int, default=os.cpu_count(),
                        help='number of parallel processes to use')
    parser.add_argument('-s', '--sequential', action='store_true', help='use sequential processing')

    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    """
    Convolve audio files in parallel or sequentially.
    :param args: Command line arguments.
    """

    dataframe_metainfo = utils.generate_dataframe(args.input_dir)
    dataframe_preset_metainfo = utils.get_dataframe_preset(dataframe_metainfo, args.rir_configs_path, args.anec_configs_path, args.preset_size)
    # print(dataframe_preset_metainfo)
    impulse_responses, anechoic_sounds = utils.split_audio_types(dataframe_preset_metainfo)
    cartesian_products = utils.generate_cartesian_product(impulse_responses, anechoic_sounds) # type: ignore

    output_dir_preset = os.path.join(args.output_dir, args.preset_size)

    # Convolve the audio pairs.
    try:
        if args.sequential:
            utils.convolve_sequential(cartesian_products, output_dir_preset)
        else:
            utils.convolve_parallel(cartesian_products, output_dir_preset, args.processes)
    except Exception as e:
        print(f"An error occurred during audio convolution: {e}")


if __name__ == '__main__':
    args = get_arguments()
    main(args)
