import argparse
import time
from virusshare import VirusShare

# Initialize VirusShare API
v = VirusShare('XXXX')  # Replace 'XXXX' with your VirusShare API key


def download_sample(hash_value, destination_folder, max_retries=3, rate_limit_pause=60, request_interval=15):
    """
    Attempts to download a sample for a given hash value from VirusShare.
    """
    retries = 0
    while retries < max_retries:
        try:
            result = v.download(hash_value, destination_folder)
            print(f"Downloaded: {hash_value} to {destination_folder}")
            time.sleep(request_interval)  # Control request interval
            return True
        except Exception as e:
            if "rate limit" in str(e).lower():
                print(f"Rate limit exceeded, pausing for {rate_limit_pause} seconds...")
                time.sleep(rate_limit_pause)
            else:
                print(f"Failed to download {hash_value}: {e}")
                return False
        retries += 1
    print(f"Failed to download after {max_retries} retries: {hash_value}")
    return False


def download_samples_from_file(file_path, destination_folder, max_retries=3, rate_limit_pause=60, request_interval=15):
    """
    Reads hash values from a file and downloads corresponding samples.
    """
    try:
        with open(file_path, 'r') as file:
            hash_list = [line.strip() for line in file if line.strip()]

        for hash_value in hash_list:
            success = download_sample(hash_value, destination_folder, max_retries, rate_limit_pause, request_interval)
            if not success:
                print(f"Skipping sample download due to failure: {hash_value}")
    except Exception as e:
        print(f"Error reading file: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download malware samples from VirusShare by providing a hash file.')
    parser.add_argument('hash_file', type=str, help='Path to the file containing hashes')
    parser.add_argument('destination_folder', type=str, help='Directory where samples will be downloaded')

    args = parser.parse_args()

    download_samples_from_file(args.hash_file, args.destination_folder)
