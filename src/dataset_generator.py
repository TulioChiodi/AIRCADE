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

    parser.add_argument('dirpath', type=str, help='directory path of the dataset')
    parser.add_argument('-o', '--output-dir', type=str, default='data/dataset_processed',
                        help='directory path for the processed dataset')
    parser.add_argument('-p', '--processes', type=int, default=os.cpu_count(),
                        help='number of parallel processes to use')
    parser.add_argument('-s', '--sequential', action='store_true', help='use sequential processing')

    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    """
    Convolve audio files in parallel or sequentially.
    :param args: Command line arguments.
    """

    audio_df_metainfo = utils.generate_dataframe(args.dirpath)
    impulse_responses, anechoic_sounds = utils.split_audio_types(audio_df_metainfo)
    cartesian_products = utils.generate_cartesian_product(impulse_responses, anechoic_sounds) # type: ignore

    # Convolve the audio pairs.
    try:
        if args.sequential:
            utils.convolve_sequential(cartesian_products, args.output_dir)
        else:
            utils.convolve_parallel(cartesian_products, args.output_dir, args.processes)
    except Exception as e:
        print(f"An error occurred during audio convolution: {e}")


if __name__ == '__main__':
    args = get_arguments()
    main(args)
